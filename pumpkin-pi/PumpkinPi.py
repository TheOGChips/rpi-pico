import RPi.GPIO as GPIO
from time import sleep

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

    # TODO: Light up every other rim LED as the eyes blink
    def alt (self):
        self.start()
        self.off()

    # TODO: Randomly light up the rim
    def rand (self):
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
