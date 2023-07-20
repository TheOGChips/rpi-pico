from machine import Pin
from utime import sleep_ms, sleep

sensor_pir = Pin(28, Pin.IN, Pin.PULL_DOWN)
led = Pin(15, Pin.OUT)
buzzer = Pin(14, Pin.OUT)

def pir_handler (pin):
    sleep_ms(100)
    if pin.value():
        print("ALARM! Motion detected!")
        for i in range(50):
            led.toggle()
            for j in range(25):
                buzzer.toggle()
                sleep_ms(3)
        sleep_ms(100)
        
sensor_pir.irq(trigger=Pin.IRQ_RISING, handler=pir_handler)

#def loop():
while True:
    led.toggle()
    sleep(5)

#if __name__ == '__main__':
#    loop()
