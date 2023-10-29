''' Provides functionality for the "Pumpkin Pi" board from PiShop.us. '''

from time import sleep
from random import choice
from RPi import GPIO    # pylint: disable=import-error

GPIO.setmode(GPIO.BCM)

class PumpkinPi:    # pylint: disable=too-many-instance-attributes
    ''' Controls the LEDs on the "Pumpkin Pi" board and turns them on and off in different
        sequences.
    '''
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
        ''' Turns on all LEDS in PWM mode. '''
        for pin in self.left_eye, self.right_eye:
            pin.start(0.0)

        for pin in self.rim:
            pin.start(0.0)

    def off (self):
        ''' Disables all LEDs on the "Pumpkin Pi" board (i.e. turns off PWM mode). '''
        for pin in self.left_eye, self.right_eye:
            pin.stop()

        for pin in self.rim:
            pin.stop()

    def flash_eyes (self):
        ''' Toggles/Flashes the eyes of the "Pumpkin Pi" on and off with a delay between each
            toggle.
        '''
        for pin in self.left_eye, self.right_eye:
            pin.ChangeDutyCycle(self.green_duty_cycle)
        self.sleep()

        for pin in self.left_eye, self.right_eye:
            pin.ChangeDutyCycle(0.0)
        self.sleep()

    def seq (self):
        ''' Turns on each LED around the edge of the "Pumpkin Pi" in circular sequence from bottom
            left to bottom right. The eyes flash 3 times after the entire rim is lit. The board then
            resets all LEDs.
        '''
        self.start()
        for pin in self.rim:
            pin.ChangeDutyCycle(self.red_duty_cycle)
            self.sleep()

        for _ in range(3):
            self.flash_eyes()

        self.off()

    def alt (self):
        ''' Turns on every other LED (i.e. alternating LEDs) around the rim, then flashes the eyes
            on and off. Then, all rim LEDs toggle on or off, and the eyes flash on and off one more
            time. The board then resets all LEDs.
        '''
        self.start()
        rim_halves = [self.rim[::2], self.rim[1::2]]
        for pin in self.left_eye, self.right_eye:
            pin.ChangeDutyCycle(self.green_duty_cycle)
        for _ in range(5):
            for _ in range(2):
                for pin in rim_halves[0]:
                    pin.ChangeDutyCycle(self.red_duty_cycle)
                for pin in rim_halves[1]:
                    pin.ChangeDutyCycle(0.0)
                self.sleep()
                rim_halves.reverse()
        self.off()

    def rand (self):
        ''' Turns on a random LED around the rim of the "Pumpkin Pi" until all LEDs are on. The eyes
            then flash on and off 3 times, and the cycle. The board then resets all LEDs.
        '''
        self.start()
        rim_pins_left = [pin for pin in self.rim_pins]  # pylint: disable=unnecessary-comprehension
        while rim_pins_left != []:
            pin = choice(rim_pins_left)
            self.rim[self.rim_pins.index(pin)].ChangeDutyCycle(self.red_duty_cycle)
            rim_pins_left.remove(pin)
            self.sleep()

        for _ in range(3):
            self.flash_eyes()
        self.off()

    def half_and_half (self, starting_positions: str = 'top'):
        ''' Flashes complementary rim LEDs on the left and right side in a sequence determined by
            starting_positions. Once the entire rim is lit up, the eyes flash 3 times. The board
            then resets all LEDs.
        '''
        self.start()
        half = int(len(self.rim) / 2)
        left = self.rim[:half]
        right = self.rim[half:]
        if starting_positions == 'top':
            left.reverse()
        elif starting_positions == 'bottom':
            right.reverse()
        elif starting_positions == 'topleft-bottomright':
            left.reverse()
            right.reverse()

        for pin_left, pin_right in zip(left, right):
            pin_left.ChangeDutyCycle(self.red_duty_cycle)
            pin_right.ChangeDutyCycle(self.red_duty_cycle)
            self.sleep()

        for _ in range(3):
            self.flash_eyes()
        self.off()

    def cycle (self):
        ''' Randomly cycles through each of the different display options. Each option is gauranteed
            to run once. The board resets all LEDs after each display option finishes.
        '''
        half_and_half_options_left = ['top', 'bottom', 'topleft-bottomright', 'topright-bottomleft']
        fns_left = [self.seq, self.alt, self.rand] + \
                    [self.half_and_half]*len(half_and_half_options_left)
        while fns_left and half_and_half_options_left:
            fn = choice(fns_left)
            if fn == self.half_and_half:    # pylint: disable=comparison-with-callable
                option = choice(half_and_half_options_left)
                fn(option)
                half_and_half_options_left.remove(option)
            else:
                fn()
            fns_left.remove(fn)
            self.sleep()

    def sleep (self, sec: float = 1.0):
        ''' Class wrapper function for time.sleep. Default is to sleep for 1 second. '''
        sleep(sec)

    def __del__ (self):
        self.off()
        GPIO.cleanup()
