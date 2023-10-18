from machine import Pin
from utime import sleep
from urandom import uniform

buzzer = Pin(10, Pin.OUT)
led_blue = Pin(11, Pin.OUT)
button_red = Pin(12, Pin.IN, Pin.PULL_DOWN)
led_red1 = Pin(13, Pin.OUT)
led_red2 = Pin(14, Pin.OUT)
led_red3 = Pin(15, Pin.OUT)
leds_red = [led_red1, led_red2, led_red3]
button_yellow = Pin(19, Pin.IN, Pin.PULL_DOWN)
led_yellow1 = Pin(18, Pin.OUT)
led_yellow2 = Pin(17, Pin.OUT)
led_yellow3 = Pin(16, Pin.OUT)
leds_yellow = [led_yellow1, led_yellow2, led_yellow3]
reset = False
red_count = 0
yellow_count = 0

def flash_winner (winner_leds):
    while True:
        for led in winner_leds:
            led.toggle()
        sleep(0.5)

def button_handler (button):
    global reset, red_count, yellow_count
    
    try:
        if not reset:
            button_red.irq(handler=None)
            button_yellow.irq(handler=None)
            buzzer.low()
            if button is button_red:
                leds_red[red_count].high()
                red_count += 1
            else:
                leds_yellow[yellow_count].high()
                yellow_count += 1
            sleep(3)
        
            if red_count == len(leds_red):
                flash_winner(leds_red)
            elif yellow_count == len(leds_yellow):
                flash_winner(leds_yellow)
            reset = True
    except KeyboardInterrupt:
        for led in leds_red: led.low()
        for led in leds_yellow: led.low()
        buzzer.low() if buzzer.value() else None
        reset = True

def loop():
    global reset
    try:
        while True:
            button_red.irq(handler=None)
            button_yellow.irq(handler=None)
            led_blue.high()
            sleep(3)
            
            led_blue.low()
            sleep(uniform(3, 5))
            
            while not reset:
                button_red.irq(trigger=Pin.IRQ_RISING, handler=button_handler)
                button_yellow.irq(trigger=Pin.IRQ_RISING, handler=button_handler)
                buzzer.high()
            
            button_red.irq(handler=None)
            button_yellow.irq(handler=None)
            buzzer.low()
            sleep(3)
            reset = False
    except KeyboardInterrupt:
        buzzer.low() if buzzer.value() else None
        led_blue.low() if led_blue.value() else None
        led_red1.low() if led_red1.value() else None
        led_red2.low() if led_red2.value() else None
        led_red3.low() if led_red3.value() else None
        led_yellow1.low() if led_yellow1.value() else None
        led_yellow1.low() if led_yellow2.value() else None
        led_yellow1.low() if led_yellow3.value() else None
        button_red.irq(trigger=0, handler=None)
        button_yellow.irq(trigger=0, handler=None)

if __name__ == '__main__':
    loop()
