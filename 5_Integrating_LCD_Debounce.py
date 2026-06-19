from gpiozero import LED, Button
from signal import pause
import smbus2
import time

# --------------------------------------------------
# GPIO CONFIGURATION
# --------------------------------------------------

# LED1
led1 = LED(7)

# Relay1
relay1 = LED(20)

# Push Button with debounce
push_button = Button(6, bounce_time=0.1)

# --------------------------------------------------
# LCD I2C CONFIGURATION
# --------------------------------------------------

LCD_ADDR = 0x27
bus = smbus2.SMBus(1)

LCD_CHR = 1
LCD_CMD = 0

LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0

LCD_BACKLIGHT = 0x08
ENABLE = 0b00000100

# --------------------------------------------------
# LCD FUNCTIONS
# --------------------------------------------------

def lcd_toggle(bits):
    time.sleep(0.0005)
    bus.write_byte(LCD_ADDR, bits | ENABLE)
    time.sleep(0.0005)
    bus.write_byte(LCD_ADDR, bits & ~ENABLE)

def lcd_write(bits, mode):
    high = mode | (bits & 0xF0) | LCD_BACKLIGHT
    low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT

    bus.write_byte(LCD_ADDR, high)
    lcd_toggle(high)

    bus.write_byte(LCD_ADDR, low)
    lcd_toggle(low)

def lcd_init():
    lcd_write(0x33, LCD_CMD)
    lcd_write(0x32, LCD_CMD)
    lcd_write(0x06, LCD_CMD)
    lcd_write(0x0C, LCD_CMD)
    lcd_write(0x28, LCD_CMD)
    lcd_write(0x01, LCD_CMD)
    time.sleep(0.005)

def lcd_text(message, line):
    message = message.ljust(16, " ")
    lcd_write(line, LCD_CMD)

    for char in message:
        lcd_write(ord(char), LCD_CHR)

# --------------------------------------------------
# COUNTER SYSTEM
# --------------------------------------------------

counter = 0

def update_outputs():
    global counter

    # LCD always displays current counter value
    lcd_text(f"Counter = {counter}", LCD_LINE_1)

    # Requirement 4 & 5:
    # LED1 ON only when counter = 0
    if counter == 0:
        led1.on()
    else:
        led1.off()

    # Requirement 2:
    # Relay1 ON when counter reaches 5
    if counter >= 5:
        relay1.on()
    else:
        relay1.off()

def button_pressed():
    global counter

    counter += 1

    print(f"Counter = {counter}")

    # Requirement 3:
    # When counter reaches 10:
    # Relay1 OFF and counter reset to 0
    if counter >= 10:
        relay1.off()
        counter = 0
        print("Counter reached 10 -> Reset to 0")

    update_outputs()

# --------------------------------------------------
# INITIALIZATION
# --------------------------------------------------

lcd_init()

relay1.off()

update_outputs()

push_button.when_pressed = button_pressed

print("System Ready")
print("Press Push Button to increment counter")

# --------------------------------------------------
# MAIN LOOP
# --------------------------------------------------

pause()
