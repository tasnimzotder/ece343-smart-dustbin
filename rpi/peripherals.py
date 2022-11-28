import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

LED_RED_PIN = 1
LED_GREEN_PIN = 7
IR_PIN = 4

TRIGGER_PIN = 19
ECHO_PIN = 26
SERVO_PIN = 18

GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(IR_PIN, GPIO.IN)

GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

GPIO.setup(LED_RED_PIN, GPIO.OUT)
GPIO.setup(LED_GREEN_PIN, GPIO.OUT)

servo = GPIO.PWM(SERVO_PIN, 50)
servo.start(0)


# constants
DUSTBIN_HEIGHT = 12  # cm


def setMotorAngle(angle: int):
    duty = angle / 18 + 2

    servo.start(duty)
    time.sleep(0.5)

    servo.ChangeDutyCycle(0)


def ctrlMotor(command):
    if command == "open":
        setMotorAngle(90)
    elif command == "close":
        setMotorAngle(0)


def getIRValue():
    sum = 0

    for i in range(10):
        sum += GPIO.input(IR_PIN)
        time.sleep(0.01)

    if sum / 10 >= 0.8:
        return 1
    else:
        return 0


def getDustbinCapacityRemaining():
    GPIO.output(TRIGGER_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIGGER_PIN, False)

    start = time.time()
    stop = time.time()

    while GPIO.input(ECHO_PIN) == 0:
        start = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        stop = time.time()

    elapsed = stop - start
    distance = (elapsed * 34300) / 2

    # return distance

    if distance > DUSTBIN_HEIGHT:
        distance = DUSTBIN_HEIGHT
    elif distance < 0:
        distance = 0

    capacity = (DUSTBIN_HEIGHT - distance) / DUSTBIN_HEIGHT * 100

    return 100 - capacity


def set_led(color):
    if color == "red":
        GPIO.output(LED_RED_PIN, GPIO.HIGH)
        GPIO.output(LED_GREEN_PIN, GPIO.LOW)
    elif color == "green":
        GPIO.output(LED_RED_PIN, GPIO.LOW)
        GPIO.output(LED_GREEN_PIN, GPIO.HIGH)
    elif color == "off":
        GPIO.output(LED_RED_PIN, GPIO.LOW)
        GPIO.output(LED_GREEN_PIN, GPIO.LOW)
