from machine import Pin
from utime import sleep

button = Pin(12, Pin.IN, Pin.PULL_DOWN)

def loop():
	try:
		while True:
			if (button.value()):
				print("You pressed the button")
				sleep(2)
	except KeyboardInterrupt:
		pass

if __name__ == '__main__':
    loop()

