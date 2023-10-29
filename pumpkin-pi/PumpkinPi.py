import RPi.GPIO as GPIO
from time import sleep
from random import choice

GPIO.setmode(GPIO.BCM)

# TODO: Add docstrings
class PumpkinPi:
    def __init__ (self):
        self.freq = (60, 'Hz')
        self.green_duty_cycle = 50.0
        self.red_duty_cycle = 0.5
        self.left_eye_pin = 12
        self.right_eye_pin = 6
        self.rim_pins = [18, 17, 16, 13, 24, 23, 22, 21, 20, 19]
        self.rim = []

        for pin in self.left_eye_pin, self.right_eye_pin:
            GPIO.setup(pin, GPIO.OUT)
        self.left_eye = GPIO.PWM(self.left_eye_pin, self.freq[0])
        self.right_eye = GPIO.PWM(self.right_eye_pin, self.freq[0])

        for pin in self.rim_pins:
            GPIO.setup(pin, GPIO.OUT)
            self.rim.append(GPIO.PWM(pin, self.freq[0]))

    def start (self):
        for pin in self.left_eye, self.right_eye:
            pin.start(0.0)

        for pin in self.rim:
            pin.start(0.0)

    def off (self):
        for pin in self.left_eye, self.right_eye:
            pin.stop()

        for pin in self.rim:
            pin.stop()

    def flash_eyes (self):
        for pin in self.left_eye, self.right_eye:
            pin.ChangeDutyCycle(self.green_duty_cycle)
        self.sleep()

        for pin in self.left_eye, self.right_eye:
            pin.ChangeDutyCycle(0.0)
        self.sleep()

    def seq (self):
        self.start()
        for pin in self.rim:
            pin.ChangeDutyCycle(self.red_duty_cycle)
            self.sleep()

        for _ in range(3):
            self.flash_eyes()

        self.off()

    def alt (self):
        self.start()
        rim_halves = [self.rim[::2], self.rim[1::2]]
        for _ in range(2):
            for pin in rim_halves[0]:
                pin.ChangeDutyCycle(self.red_duty_cycle)
            for pin in rim_halves[1]:
                pin.ChangeDutyCycle(0.0)
            self.flash_eyes()
            self.sleep()
            rim_halves.reverse()
        self.off()

    def rand (self):
        self.start()
        rim_pins_left = [pin for pin in self.rim_pins]
        while rim_pins_left != []:
            pin = choice(rim_pins_left)
            self.rim[self.rim_pins.index(pin)].ChangeDutyCycle(self.red_duty_cycle)
            rim_pins_left.remove(pin)
            self.sleep()

        for _ in range(3):
            self.flash_eyes()
        self.off()

    # TODO: Light up LEDs on alternating halves
    def half_and_half (self):
        self.start()
        self.off()

    # TODO: Cycle through all available modes
    def cycle (self):
        pass

    def sleep (self, sec: int = 1.0):
        sleep(sec)

    def __del__ (self):
        self.off()
        GPIO.cleanup()
