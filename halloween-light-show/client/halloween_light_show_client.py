from machine import Pin, PWM
from bluetooth import BLE
from ble_simple_peripheral import BLESimplePeripheral
from ble_advertising import advertising_payload

bt_client = BLESimplePeripheral(BLE())
red = PWM(Pin(15, Pin.OUT))
green = PWM(Pin(16, Pin.OUT))

red.freq(60)
red.duty_u16(2**16 - 1)
green.freq(60)
green.duty_u16(2**16 - 1)

curr = None
first_cmd = True

def on_rx(v):
    global curr
    global first_cmd
    print(str(v))
    if v.decode() == 'red' and curr != red:
        if not first_cmd:
            for i in range(2**16):
                green.duty_u16(i)
        for i in range(2**16, 0, -1):
            red.duty_u16(i-1)
        first_cmd = False
        curr = red
    elif v.decode() == 'green' and curr != green:
        if not first_cmd:
            for i in range(2**16):
                red.duty_u16(i)
        for i in range(2**16, 0, -1):
            green.duty_u16(i-1)
        first_cmd = False
        curr = green
    elif v.decode() == 'off' and curr != None:
        for i in range(2**16):
            curr.duty_u16(i)
        first_cmd = True
        curr = None

bt_client.on_write(on_rx)
