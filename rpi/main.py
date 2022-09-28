# smart dustbin using raspberry pi

import json
import RPi.GPIO as GPIO
import time
import aws_config

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

# global variables
global is_device_active
global capacity_remaining
global dustbin_lid_status
global prev_time
global topic_pub
global topic_sub

is_device_active = True
capacity_remaining = 0
dustbin_lid_status = "close"
prev_time = time.time()

topic_pub = "rpi/dustbin/data"
topic_sub = "rpi/dustbin/ctrl"


# Raspberry Pi functions
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

    return capacity_remaining


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
    elif status == "empty":
        GPIO.output(led_red, GPIO.LOW)
        GPIO.output(led_green, GPIO.HIGH)
    elif status == "deactivated":
        GPIO.output(led_red, GPIO.HIGH)
        GPIO.output(led_green, GPIO.HIGH)


# aws iot
def topic_callback(self, params, packet):
    print("received message: " + str(packet.payload))
    data = json.loads(packet.payload)

    is_device_active = data.get("is_device_active")


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic_sub, 1, topic_callback)


aws_config.client.on_connect = on_connect


def connectToAWSIoT():
    print("connecting to AWS IoT...")
    aws_config.client.connect()
    print("connected to AWS IoT")


connectToAWSIoT()


def main():
    capacity_remaining = getDustbinCapacity()
    is_people_nearby = getIRSensorStatus()

    if is_device_active:
        if capacity_remaining > 80:
            dustbin_lid_status = "close"
            controlMotor(dustbin_lid_status)
            controlLed("full")
        else:
            if is_people_nearby:
                dustbin_lid_status = "open"
                controlMotor(dustbin_lid_status)
                controlLed("empty")
            else:
                dustbin_lid_status = "close"
                controlMotor(dustbin_lid_status)
                controlLed("empty")
    else:
        dustbin_lid_status = "close"
        controlMotor(dustbin_lid_status)
        controlLed("deactivated")

    curr_time = time.time()

    if curr_time - prev_time > 5:
        prev_time = curr_time

        data = {
            "capacity_remaining": capacity_remaining,
            "dustbin_lid_status": dustbin_lid_status,
            "device_id": "rpi_1",
        }

        # publish data to AWS IoT
        aws_config.client.publish(topic_pub, json.dumps(data), 1)


if __name__ == "__main__":
    # main loop
    while True:
        main()
