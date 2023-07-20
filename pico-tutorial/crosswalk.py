from machine import Pin
from utime import sleep

buzzer = Pin(11, Pin.OUT)
led_blue = Pin(12, Pin.OUT)
led_red = Pin(13, Pin.OUT)
led_yellow = Pin(14, Pin.OUT)
led_green = Pin(15, Pin.OUT)
button = Pin(16, Pin.IN, Pin.PULL_DOWN)

def loop():
    try:
        while True:
            if (button.value()):
                sleep(1)
                led_green.low()
                led_yellow.high()
                sleep(2)
                led_yellow.low()
                led_red.high()
                sleep(2)
                
                led_blue.high()
                for i in range(5):
                    buzzer.high()
                    sleep(0.2)
                    buzzer.low()
                    sleep(0.8)
                led_blue.low()
                sleep(2)
                led_red.low()
            else:
                led_green.high()
    except KeyboardInterrupt:
        led_red.low() if led_red.value() else None
        led_yellow.low() if led_yellow.value() else None
        led_green.low() if led_green.value() else None
        buzzer.low() if buzzer.value() else None

if __name__ == '__main__':
    loop()
