import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

class PumpkinPi:
    def __init__ (self):
        self.left_eye = 12
        self.right_eye = 6
        self.rim = [18, 17, 16, 13, 24, 23, 22, 21, 20, 19]

        for pin in self.left_eye, self.right_eye:
            GPIO.setup(pin, GPIO.OUT)

        for pin in self.rim:
            GPIO.setup(pin, GPIO.OUT)

    def flash_eyes (self):
        for pin in self.left_eye, self.right_eye:
            GPIO.output(pin, True)
        sleep(1)

        for pin in self.left_eye, self.right_eye:
            GPIO.output(pin, False)
        sleep(1)

    def __del__ (self):
        for pin in self.left_eye, self.right_eye:
            GPIO.output(pin, False)

        for pin in self.rim:
            GPIO.output(pin, False)

        GPIO.cleanup()
