from usocket import socket, AF_INET, SOCK_STREAM
from network import WLAN, AP_IF
from random import randint
from machine import Pin
from re import search

SSID = 'RPI PICO W'
PASSWORD = '12345678'
led = Pin(15, Pin.OUT)

ap = WLAN(AP_IF)
# NOTE: txpower can be configured for a maximum, this may be useful
ap.config(ssid=SSID, password=PASSWORD)
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

def web_page(lucky: bool = True):
    num = randint(1, 10) if lucky else '?'
    with open("index.html", "r") as infile:
        html = infile.read()
    
    return str(html %str(num))

sock = socket(AF_INET, SOCK_STREAM)
sock.bind(('', 80))
sock.listen(5)
led.off()
while True:
    conn, rx = sock.accept()
    #print('Incoming connection from %s' %str(rx))
    request = conn.recv(2**10).decode('utf-8')
    #print(request)
    cmd = url = request.split()[1]  # TODO: Might need a try-except here
    if (search("toggle-LED", cmd)):
        led.toggle()
    elif (search("favicon", cmd)):
        pass
    elif (search("lucky-number", cmd)):
        response = web_page()
    else:
        response = web_page(lucky=False)
    conn.send(response)
    conn.close()
