from gpiozero import LED, Button
import RPi.GPIO as GPIO
import threading
import time
from signal import pause

# --------------------------------------------------
# GPIOZERO DEVICES
# --------------------------------------------------

# Status LED
led1 = LED(7)

# Push Button (changed to GPIO6)
push_button = Button(6)

# IR Sensor
ir_sensor = Button(19, pull_up=True)

# --------------------------------------------------
# MOTOR DRIVER SETUP (MDD10-Hat Sign-Magnitude Mode)
# --------------------------------------------------

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

AN1 = 12
AN2 = 13
DIG1 = 26
DIG2 = 24

GPIO.setup(AN1, GPIO.OUT)
GPIO.setup(AN2, GPIO.OUT)
GPIO.setup(DIG1, GPIO.OUT)
GPIO.setup(DIG2, GPIO.OUT)

p1 = GPIO.PWM(AN1, 100)
p2 = GPIO.PWM(AN2, 100)

p1.start(0)
p2.start(0)

MOTOR_SPEED = 10

# --------------------------------------------------
# LED1 BLINKING THREAD (10 Hz)
# --------------------------------------------------

def blink_led():
    while True:
        led1.toggle()
        time.sleep(0.05)   # 10 Hz

threading.Thread(target=blink_led, daemon=True).start()

# --------------------------------------------------
# MOTOR 1 CONTROL (PUSH BUTTON)
# --------------------------------------------------

def motor1_forward():
    GPIO.output(DIG1, GPIO.LOW)
    p1.ChangeDutyCycle(MOTOR_SPEED)
    print("Push Button Pressed -> Motor 1 Forward")

def motor1_stop():
    p1.ChangeDutyCycle(0)
    print("Push Button Released -> Motor 1 Stop")

push_button.when_pressed = motor1_forward
push_button.when_released = motor1_stop

# --------------------------------------------------
# MOTOR 2 CONTROL (IR SENSOR)
# --------------------------------------------------

def motor2_forward():
    GPIO.output(DIG2, GPIO.LOW)
    p2.ChangeDutyCycle(MOTOR_SPEED)
    print("IR Sensor Triggered -> Motor 2 Forward")

def motor2_stop():
    p2.ChangeDutyCycle(0)
    print("IR Sensor Normal -> Motor 2 Stop")

ir_sensor.when_pressed = motor2_forward
ir_sensor.when_released = motor2_stop

# --------------------------------------------------
# MAIN
# --------------------------------------------------

print("System Ready")
print("LED1 blinking at 10 Hz")
print("Push Button (GPIO6) -> Motor 1 Forward")
print("IR Sensor (GPIO19) -> Motor 2 Forward")

try:
    pause()

except KeyboardInterrupt:
    pass

finally:
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)
    p1.stop()
    p2.stop()
    GPIO.cleanup()
