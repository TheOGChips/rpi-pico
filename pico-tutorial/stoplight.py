from machine import Pin
from utime import sleep

led_red = Pin(13, Pin.OUT)
led_yellow = Pin(14, Pin.OUT)
led_green = Pin(15, Pin.OUT)

def loop():
    try:
        while True:
            led_green.high()
            sleep(1)
            led_green.low()
            led_yellow.high()
            sleep(1)
            led_yellow.low()
            led_red.high()
            sleep(1)
            led_red.low()
    except KeyboardInterrupt:
        led_red.low() if led_red.value() else None
        led_yellow.low() if led_yellow.value() else None
        led_green.low() if led_green.value() else None

if __name__ == '__main__':
    loop()

