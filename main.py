# smart dustbin using raspberry pi

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# set ultrasonic sensor Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 23

# set led Pins
led_red = 12
led_green = 16

# set servo motor Pins
motor = 24
servo = GPIO.PWM(motor, 50)

# set IR sensor Pins
ir_sensor = 25

# set pin directions
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(led_red, GPIO.OUT)
GPIO.setup(led_green, GPIO.OUT)
GPIO.setup(motor, GPIO.OUT)
GPIO.setup(ir_sensor, GPIO.IN)

# constant variables
MAX_CAPACITY = 100  # dustbin height is cm


def getIRSensorStatus():
    return GPIO.input(ir_sensor)


def getDustbinCapacity():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime

    # multiply with the sonic speed (0.0343 cm/us)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 0.0343) / 2

    capacity_remaining = distance / MAX_CAPACITY * 100


def setAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(motor, True)
    servo.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(motor, False)
    servo.ChangeDutyCycle(0)

def controlMotor(status):
    if status == "open":
        # open the dustbin by rotating the servo motor 90 degrees
        setAngle(90)
    else:
        # close the dustbin by rotating the servo motor 0 degrees
        setAngle(0)

def controlLed(status):
    if status == "full":
        GPIO.output(led_red, GPIO.HIGH)
        GPIO.output(led_green, GPIO.LOW)
    else:
        GPIO.output(led_red, GPIO.LOW)
        GPIO.output(led_green, GPIO.HIGH)


while True:
    capacity = getDustbinCapacity()
    ir_status = getIRSensorStatus()

    if capacity > 80:
        controlLed("full")
    else:
        controlLed("empty")

    if ir_status == 1:
        controlMotor("open")
    else:
        controlMotor("close")

    time.sleep(0.25)
