from machine import Pin
from utime import sleep

buzzer = Pin(11, Pin.OUT)
led_blue = Pin(12, Pin.OUT)
led_red = Pin(13, Pin.OUT)
led_yellow = Pin(14, Pin.OUT)
led_green = Pin(15, Pin.OUT)
button = Pin(16, Pin.IN, Pin.PULL_DOWN)

def crosswalk_handler (pin):
    # NOTE: The keyboard interrupt in this function is here because two keyboard interrupts are needed
    #       to exit this program from within this interrupt handler. The first interrupts the button
    #       interrupt, the second interrupts the main loop.
    try:
        button.irq(handler=None)
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
    except KeyboardInterrupt:
        led_red.low() if led_red.value() else None
        led_yellow.low() if led_yellow.value() else None
        led_blue.low() if led_blue.value() else None
        buzzer.low() if buzzer.value() else None

def loop():
    try:
        while True:
            button.irq(trigger=Pin.IRQ_RISING, handler=crosswalk_handler)
            led_green.high()
    except KeyboardInterrupt:
        led_green.low() if led_green.value() else None
        button.irq(handler=None)

if __name__ == '__main__':
    loop()
