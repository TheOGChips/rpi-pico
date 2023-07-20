from machine import Pin
from utime import sleep

button = Pin(12, Pin.IN, Pin.PULL_DOWN)
led = Pin(15, Pin.OUT)

def loop():
	try:
		while True:
			if (button.value()):
				for i in range(3):
					led.high()
					sleep(1)
					led.low()
					sleep(1)
	except KeyboardInterrupt:
		led.low() if led.value() else None

if __name__ == '__main__':
    loop()

