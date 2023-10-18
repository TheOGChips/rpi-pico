from machine import ADC, PWM, Pin
from utime import sleep

potentiometer = ADC(26)
conversion_factor = 3.3 / (2**16 - 1)

led = PWM(Pin("LED"))
led.freq(1000)

def loop():
    try:
        while True:
            val = potentiometer.read_u16()
            val = val if val > 1500 else 0
            led.duty_u16(val)
            print(val)
    except KeyboardInterrupt:
        led.duty_u16(0)

