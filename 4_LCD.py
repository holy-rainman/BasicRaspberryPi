import smbus2
import time

# I2C address (most common is 0x27 or 0x3F)
LCD_ADDR = 0x27

# I2C bus (GPIO2 = SDA, GPIO3 = SCL → I2C-1)
bus = smbus2.SMBus(1)

# LCD commands
LCD_CHR = 1
LCD_CMD = 0

LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0

LCD_BACKLIGHT = 0x08
ENABLE = 0b00000100


def lcd_init():
    lcd_write(0x33, LCD_CMD)
    lcd_write(0x32, LCD_CMD)
    lcd_write(0x06, LCD_CMD)
    lcd_write(0x0C, LCD_CMD)
    lcd_write(0x28, LCD_CMD)
    lcd_write(0x01, LCD_CMD)
    time.sleep(0.005)


def lcd_write(bits, mode):
    high = mode | (bits & 0xF0) | LCD_BACKLIGHT
    low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT

    bus.write_byte(LCD_ADDR, high)
    lcd_toggle(high)

    bus.write_byte(LCD_ADDR, low)
    lcd_toggle(low)


def lcd_toggle(bits):
    time.sleep(0.0005)
    bus.write_byte(LCD_ADDR, (bits | ENABLE))
    time.sleep(0.0005)
    bus.write_byte(LCD_ADDR, (bits & ~ENABLE))


def lcd_text(message, line):
    message = message.ljust(16, " ")
    lcd_write(line, LCD_CMD)

    for char in message:
        lcd_write(ord(char), LCD_CHR)


# ---------------- MAIN PROGRAM ----------------

lcd_init()

# Step 1: Hello World
lcd_text("Hello World", LCD_LINE_1)
time.sleep(2)

# Step 2: Clear screen
lcd_write(0x01, LCD_CMD)
time.sleep(0.5)

# Step 3: UTHM
lcd_text("UTHM", LCD_LINE_1)

print("Done")
