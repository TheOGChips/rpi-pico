from machine import ADC, PWM, Pin
from utime import sleep

potentiometer = ADC(26)
conversion_factor = 3.3 / (2**16 - 1)

led = PWM(Pin(15))
led.freq(1000)

while True:
    led.duty_u16(potentiometer.read_u16())
