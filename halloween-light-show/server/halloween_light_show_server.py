''' A Bluetooth server that controls the laser output color synchronization between it and a client.
    This node also operates a web server and a Wi-Fi access point. The web server is accessed via a web
    browser using a smartphone or laptop connected to the Wi-Fi access point. The web page shown in the
    web browser is used to control the laser output.
'''
from usocket import socket, AF_INET, SOCK_STREAM
from network import WLAN, AP_IF, hostname
from machine import Pin, PWM, reset
from re import search
from bluetooth import BLE
from ble_simple_central import BLESimpleCentral
from ble_advertising import advertising_payload
from utime import sleep

def on_scan (addr_type, addr, name):
    ''' Detects whether a Bluetooth peripheral device is present and connects to it. '''
    if addr_type is not None:
        print("Found peripheral:", addr_type, addr, name)
        print(bt_server.connect())

def web_page():
    ''' Reads in an HTML file and returns it as a string. '''
    with open("index.html", "r") as infile:
        html = infile.read()

    return str(html)

# NOTE: Establish a Bluetooth connection with a peripheral device first. If a connection is not
#       established within 5 seconds, this board will hard reset. This will continue until a Bluetooth
#       peripheral device is discovered and connected to. This is (at least currently) sufficient
#       enough to circumvent the issue of a peripheral device needing to be turned on and present
#       first. Otherwise, if a peripheral device is turned on after the central device (the server) has
#       started searching, it could result in a deadlock between the devices.
led = Pin('LED', Pin.OUT)
led.off()
bt_server = BLESimpleCentral(BLE())
bt_server.scan(callback=on_scan)
for _ in range(50): # NOTE: Search for peripheral devices for 5 seconds.
    if not bt_server.is_connected():
        print('Awaiting BT peripheral connection...')
        sleep(0.1)
if not bt_server.is_connected():    # NOTE: Blink a warning that the Pico W is about to hard reset by
    for _ in range(3):              #       blinking the onboard LED in a certain pattern (roughly 3x
        for _ in range(6):          #       per second for 3 seconds).
            led.toggle()
            sleep(0.1)
        sleep(0.5)
    led.off()
    reset()
print("Connected to BT peripheral...")

# NOTE: Establish a Wi-Fi access point for external devices to connect to. The way this is currently
#       set up, if some kind of error occurs, the only way to ensure the IP address is freed is to
#       perform a hard reset of the Pico W. The password should be replaced with something more
#       security-conscious if that is a concern.
SSID = 'Halloween Light Show'
PASSWORD = 'Ha!!0w33n'
ap = WLAN(AP_IF)
ap.config(ssid=SSID, password=PASSWORD)
hostname("light-show")
#print(ap.config())
ap.active(True)

while not ap.active():
    print('Awaiting activation...')
print('Access point activated')

sock = socket(AF_INET, SOCK_STREAM)
sock.bind(('192.168.4.1', 80))
sock.listen(2)
response = web_page()
first_cmd = True
curr = None

red = PWM(Pin(15, Pin.OUT))
green = PWM(Pin(16, Pin.OUT))
# NOTE: Since I'm using PNP transistors, the on and off functions work in reverse

red.freq(60)
red.duty_u16(2**16 - 1)
green.freq(60)
green.duty_u16(2**16 - 1)

while bt_server.is_connected():
        conn, rx = sock.accept()
        #print('Incoming connection from %s' %str(rx))
        request = conn.recv(2**10).decode('utf-8')
        #print(request)
        try:
            cmd = url = request.split()[1]
            if (search("red-on", cmd)) and curr != red:
                bt_server.write('red')
                if not first_cmd:
                    for i in range(2**16):
                        green.duty_u16(i)
                for i in range(2**16, 0, -1):
                    red.duty_u16(i-1)
                first_cmd = False
                curr = red
            elif (search("green-on", cmd)) and curr != green:
                bt_server.write('green')
                if not first_cmd:
                    for i in range(2**16):
                        red.duty_u16(i)
                for i in range(2**16, 0, -1):
                    green.duty_u16(i-1)
                first_cmd = False
                curr = green
            elif (search("favicon", cmd)):
                pass
            elif (search("lasers-off", cmd)):
                bt_server.write('off')
                for i in range(2**16):
                    if curr:
                        curr.duty_u16(i)
                first_cmd = True
                curr = None
            conn.send(response)
        except:
            pass
        finally:
            conn.close()
