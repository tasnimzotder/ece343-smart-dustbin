import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

SERVO_PIN = 13
IR_PIN = 22

LED_1_PIN = 25
LED_2_PIN = 8
LED_3_PIN = 7

TRIGGER_PIN = 17
ECHO_PIN = 27


DUSTBIN_HEIGHT = 100  # cm


GPIO.setup(SERVO_PIN, GPIO.OUT)

GPIO.setup(LED_1_PIN, GPIO.OUT)
GPIO.setup(LED_2_PIN, GPIO.OUT)
GPIO.setup(LED_3_PIN, GPIO.OUT)

GPIO.setup(IR_PIN, GPIO.IN)

GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

GPIO.output(TRIGGER_PIN, False)
time.sleep(2)

servo = GPIO.PWM(SERVO_PIN, 50)
servo.start(0)


def setMotorAngle(angle: int):
    duty = angle / 18 + 2
    # GPIO.output(SERVO_PIN, True)
    servo.ChangeDutyCycle(duty)
    time.sleep(1)
    # GPIO.output(SERVO_PIN, False)f
    servo.ChangeDutyCycle(0)


def ctrlMotor(command):
    if command == "open":
        setMotorAngle(90)
    elif command == "close":
        setMotorAngle(0)


def getIRValue():
    return GPIO.input(IR_PIN)


def getDustbinCapacityRemaining():
    return 50
    GPIO.output(TRIGGER_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIGGER_PIN, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(ECHO_PIN) == 0:
        start_time = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        stop_time = time.time()

    time_elapsed = stop_time - start_time

    distance = (time_elapsed * 34300) / 2
    
    # return distance

    if distance >= DUSTBIN_HEIGHT:
        return 100
    elif distance <= 0:
        return 0
    
    cap_remaining = (distance / DUSTBIN_HEIGHT) * 100

    return round(cap_remaining, 2)
