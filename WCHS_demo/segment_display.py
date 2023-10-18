from machine import Pin

a = Pin(16, Pin.OUT)
b = Pin(17, Pin.OUT)
c = Pin(14, Pin.OUT)
d = Pin(13, Pin.OUT)
e = Pin(12, Pin.OUT)
f = Pin(18, Pin.OUT)
g = Pin(19, Pin.OUT)
segments = [a, b, c, d, e, f, g]

# NOTE: This works the opposite of the way you expect for the 7-segment display I have. It's common
#       anode 7-segment display, I think?
def print_number(x: int):
    if x > 9:
        for segment in segments:
            segment.on()

    # NOTE: Segments are f -> a from left to right
    else:
        if x == 0:
            x = 0x3f
            #x = 0b0111111
        elif x == 1:
            x = 0x6
            #x = 0b0000110
        elif x == 2:
            x = 0x5b
            #x = 0b1011011
        elif x == 3:
            x = 0x4f
            #x = 0b1001111
        elif x == 4:
            x = 0x66
            #x = 0b1100110
        elif x == 5:
            x = 0x6d
            #x = 0b1101101
        elif x == 6:
            x = 0x7d
            #x = 0b1111101
        elif x == 7:
            x = 0x7
            #x = 0b0000111
        elif x == 8:
            x = 0x7f
            #x = 0b1111111
        elif x == 9:
            x = 0x6f
            #x = 0b1101111

        for segment in segments:
            segment.off() if x & 1 else segment.on()
            x >>= 1
