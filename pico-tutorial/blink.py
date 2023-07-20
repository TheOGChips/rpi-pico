from machine import Pin
from utime import sleep

led = Pin(25, Pin.OUT)

def loop():
	try:
		while True:
			led.toggle()
			sleep(1)
	except KeyboardInterrupt:
		led.low()

if __name__ == '__main__':
    loop()

