from machine import ADC
from utime import sleep

sensor_temp = ADC(4)
conversion_factor = 3.3 / (2**16 - 1)

def C2F (C: float):
    return (C * 9/5) + 32

while True:
    reading = sensor_temp.read_u16() * conversion_factor
    #temperature = 27 - (reading - 0.59)/0.001721
    # NOTE: This is the value I get after calibrating for the ambient temperature in my apartment at ~72 deg F (~22.22 deg C)
    temperature = 27 - (reading - 0.734)/0.001721
    #temperature = C2F(temperature)
    #print(reading)
    print('%s C -> %s F' %(temperature, C2F(temperature)))
    sleep(2)
