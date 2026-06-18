from gpiozero import LED, Button
from signal import pause
import threading
import time

# --------------------------------------------------
# GPIO Pin Configuration
# --------------------------------------------------

# LEDs
led1 = LED(7)       # LED1 connected to GPIO12
led2 = LED(16)       # LED2 connected to GPIO16

# Relays (Active HIGH)
relay1 = LED(20)     # Relay1 connected to GPIO20
relay2 = LED(21)     # Relay2 connected to GPIO21

# Inputs
push_button = Button(6)                 # Push Button on GPIO26
ir_sensor = Button(19, pull_up=True)     # IR Sensor on GPIO19 (pull-up)

# --------------------------------------------------
# Initial State
# --------------------------------------------------

# Requirement 1:
# LED1 remains ON when program starts
led1.on()

# Make sure relays start OFF
relay1.off()
relay2.off()

# --------------------------------------------------
# LED2 Blinking Thread
# --------------------------------------------------

def blink_led2():
    """
    Continuously blink LED2 every 0.5 seconds.
    """
    while True:
        led2.toggle()
        time.sleep(0.5)

# Start blinking LED2 in a background thread
threading.Thread(target=blink_led2, daemon=True).start()

# --------------------------------------------------
# Push Button Control for Relay1
# --------------------------------------------------

def relay1_on():
    relay1.on()
    print("Push Button Pressed -> Relay1 ON")

def relay1_off():
    relay1.off()
    print("Push Button Released -> Relay1 OFF")

push_button.when_pressed = relay1_on
push_button.when_released = relay1_off

# --------------------------------------------------
# IR Sensor Control for Relay2
# --------------------------------------------------
# Assuming:
# - IR sensor output is HIGH normally (pull-up)
# - IR sensor pulls LOW when triggered

def relay2_on():
    relay2.on()
    print("IR Sensor Triggered -> Relay2 ON")

def relay2_off():
    relay2.off()
    print("IR Sensor Normal -> Relay2 OFF")

ir_sensor.when_pressed = relay2_on     # GPIO goes LOW
ir_sensor.when_released = relay2_off   # GPIO returns HIGH

# --------------------------------------------------
# Keep Program Running
# --------------------------------------------------

print("Program started.")
print("LED1 = ON")
print("LED2 = Blinking every 0.5 seconds")

pause()
