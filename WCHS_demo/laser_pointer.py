from machine import Pin, ADC, PWM
from utime import sleep, sleep_ms

laser = PWM(Pin(26, Pin.OUT))
button = Pin(16, Pin.IN, Pin.PULL_DOWN)

ON = 1
PULSING = 0.5
OFF = 0
laser_state = OFF

def button_handler (button):
    global laser_state

    button.irq(trigger=0, handler=None)
    sleep_ms(250)
    freq = 8
    try:
        if laser_state == OFF:
            laser_state = ON
        elif laser_state == ON:
            laser_state = PULSING
        else:
            laser_state = OFF
        pulse(freq, laser_state)
        button.irq(trigger=Pin.IRQ_RISING, handler=button_handler)
    except KeyboardInterrupt:
        laser_state = OFF
        pulse(freq, laser_state)
        button.irq(trigger=0, handler=None)

def pulse (f: int, duty_cycle: float):
    if duty_cycle >= 1.0:
        duty_cycle = 2**16 - 1
    elif duty_cycle <= 0.0:
        duty_cycle = 0
    else:
        duty_cycle = int(2**16 * duty_cycle) - 1
    try:
        laser.freq(f)
        laser.duty_u16(duty_cycle) # range 0-65535
    except(KeyboardInterrupt):
        laser.duty_u16(0)

def start ():
    button.irq(trigger=Pin.IRQ_RISING, handler=button_handler)
    try:
        while True:
            pass
    except (KeyboardInterrupt):
        button.irq(trigger=0, handler=None)

if __name__ == '__main__':
    start()
