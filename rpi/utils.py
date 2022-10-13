import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

SERVO_PIN = 17
IR_PIN = 27
LED_PIN = 3

TRIGGER_PIN = 16
ECHO_PIN = 18

GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(LED_PIN, GPIO.OUT)
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

    start = time.time()
    stop = time.time()

    while GPIO.input(ECHO_PIN) == 0:
        start = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        stop = time.time()

    elapsed = stop - start
    distance = (elapsed * 34300) / 2

    return distance


opened_time = time.time()
status = "close"


# def main():
#     global opened_time
#     global status
#     ir = getIRValue()

#     if ir == 1:
#         print("opened")
#         status = "open"
#         ctrlMotor("open")
#         opened_time = time.time()
#     else:
#         curr_time = time.time()

#         if curr_time - opened_time > 5 and status == "open":
#             print("closed")
#             status = "close"
#             ctrlMotor("close")
