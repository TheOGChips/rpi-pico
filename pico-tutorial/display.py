from machine import Pin, I2C
# NOTE: Uses the external repo RPI-PICO-I2C-LCD for the drivers
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

#I2C_ADDR     = 0x27
#I2C_NUM_ROWS = 2
#I2C_NUM_COLS = 16

DISPLAY = 39
NUM_ROWS = 2
NUM_COLS = 16

SDA = Pin(0)
SCL = Pin(1)
i2c = I2C(0, sda=SDA, scl=SCL, freq=400000)
#print(i2c.scan())
#i2c.writeto(display_addr, '0x01')   # clear display
#i2c.writeto(display_addr, '\x1d')
#i2c.writeto(display_addr, "hello world")

LCD = I2cLcd(i2c, DISPLAY, NUM_ROWS, NUM_COLS)

# NOTE: I've modified lcd_api.py to include an alias for putstr that
#       makes more sense to me as a name (see display member func)
def display (text: str):
    LCD.clear()
    LCD.display(text)
