from usocket import socket, AF_INET, SOCK_STREAM
from network import WLAN, AP_IF, hostname
from machine import Pin, PWM
from re import search
from bluetooth import BLE
from ble_simple_central import BLESimpleCentral
from ble_advertising import advertising_payload
from utime import sleep

SSID = 'Halloween Light Show'
PASSWORD = 'Ha!!0w33n'
red = PWM(Pin(15, Pin.OUT))
green = PWM(Pin(16, Pin.OUT))
# NOTE: Since I'm using PNP transistors, the on and off functions work in reverse

red.freq(60)
red.duty_u16(2**16 - 1)
green.freq(60)
green.duty_u16(2**16 - 1)

ap = WLAN(AP_IF)
# NOTE: txpower can be configured for a maximum, this may be useful
ap.config(ssid=SSID, password=PASSWORD)
hostname("light-show")
#print(ap.config())
ap.active(True)

while not ap.active():
    print('Awaiting activation...')

print('Access point activated')
# NOTE: The same IP address is also used for the gateway
# TODO: For some reason, an IP address different from the default doesn't connect if it's different enough. For example, 192.168.4.2 works, but 10.10.200.0 doesn't, even when the netmask is all zeroes.'
#IP_ADDR='192.168.4.2'
#NETMASK='255.255.255.0'
#GATEWAY=IP_ADDR
#DNS='0.0.0.0'
#ap.ifconfig((IP_ADDR, NETMASK, GATEWAY, DNS))
#print(ap.ifconfig())

# TODO: Have the onboard LED blink consistently in a separate thread

def web_page():
    with open("index.html", "r") as infile:
        html = infile.read()
    
    return str(html)

sock = socket(AF_INET, SOCK_STREAM)
sock.bind(('192.168.4.1', 80))
sock.listen(2)
response = web_page()
first_cmd = True
curr = None

bt_server = BLESimpleCentral(BLE())
def on_scan (addr_type, addr, name):
    if addr_type is not None:
        print("Found peripheral:", addr_type, addr, name)
        print(bt_server.connect())

bt_server.scan(callback=on_scan)
while not bt_server.is_connected():
    print('Awaiting BT peripheral connection...')
    sleep(0.1)
print("Connected to BT peripheral...")

#while True:
#    if bt_server.is_connected():
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
