import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# pins
SERVO_PIN = 17
IR_PIN = 27

LED_RED_PIN = 2
LED_GREEN_PIN = 3

TRIGGER_PIN = 10
ECHO_PIN = 9

# global variables
DUSTBIN_HEIGHT = 100  # cm

opened_time = time.time()
status = "close"

GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(LED_RED_PIN, GPIO.OUT)
GPIO.setup(LED_GREEN_PIN, GPIO.OUT)
GPIO.setup(IR_PIN, GPIO.IN)

GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

servo = GPIO.PWM(SERVO_PIN, 50)
servo.start(0)


def setMotorAngle(angle: int):
    duty = angle / 18 + 2

    servo.start(duty)
    time.sleep(1)

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

    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance / DUSTBIN_HEIGHT * 100


def main():
    global opened_time
    global status

    ir = getIRValue()

    if ir == 1:
        print("opened")
        status = "open"
        ctrlMotor("open")
        opened_time = time.time()
    else:
        curr_time = time.time()

        if curr_time - opened_time > OPEN_TIME and status == "open":
            print("closed")
            status = "close"
            ctrlMotor("close")
