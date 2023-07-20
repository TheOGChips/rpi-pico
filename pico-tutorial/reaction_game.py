from machine import Pin
from utime import sleep
from urandom import uniform

buzzer = Pin(11, Pin.OUT)
led_blue = Pin(12, Pin.OUT)
led_red = Pin(13, Pin.OUT)
led_yellow = Pin(14, Pin.OUT)
led_green = Pin(15, Pin.OUT)
button_red = Pin(16, Pin.IN, Pin.PULL_DOWN)
button_yellow = Pin(17, Pin.IN, Pin.PULL_DOWN)
reset = False

def button_handler (button):
    global reset
    
    try:
        if not reset:
            button_red.irq(handler=None)
            button_yellow.irq(handler=None)
            led_blue.low()
            led_red.high() if button is button_red else led_yellow.high()
            sleep(3)
        
            led_red.low()
            led_yellow.low()
            reset = True
    except KeyboardInterrupt:
        led_red.low() if led_red.value() else None
        led_yellow.low() if led_yellow.value() else None
        buzzer.low() if buzzer.value() else None
        reset = True

def loop():
    global reset
    try:
        while True:
            button_red.irq(handler=None)
            button_yellow.irq(handler=None)
            led_green.high()
            sleep(3)
            
            led_green.low()
            sleep(uniform(3, 5))
            
            while not reset:
                button_red.irq(trigger=Pin.IRQ_RISING, handler=button_handler)
                button_yellow.irq(trigger=Pin.IRQ_RISING, handler=button_handler)
                led_blue.high()
            
            button_red.irq(handler=None)
            button_yellow.irq(handler=None)
            led_blue.low()
            sleep(3)
            reset = False
    except KeyboardInterrupt:
        led_green.low() if led_green.value() else None
        led_blue.low() if led_blue.value() else None
        button_red.irq(trigger=0, handler=None)
        button_yellow.irq(trigger=0, handler=None)

if __name__ == '__main__':
    loop()
