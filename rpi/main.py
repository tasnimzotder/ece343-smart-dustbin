"""
Project Name: Smart Dustbin
"""

import json
import RPi.GPIO as GPIO
import time
import aws_config


# constant variables
MAX_CAPACITY = 100  # dustbin height is cm

# global variables
is_device_active = True
capacity_remaining = 0
dustbin_lid_status = "close"
prev_time = time.time()

TOPIC_PUB = "smart_dustbin/data"
TOPIC_SUB = "smart_dustbin/ctrl"

GPIO.setmode(GPIO.BCM)

# set ultrasonic sensor Pins
GPIO_TRIGGER = 14
GPIO_ECHO = 15

# set led Pins
led_red = 23
led_green = 24

# set servo motor Pins (pwm)
motor = 18
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
    # and divide by 2, because the distance is the half of the round trip
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


def handlePeopleNearby(is_people_nearby):
    if is_people_nearby:
        dustbin_lid_status = "open"
        controlMotor(dustbin_lid_status)
        controlLed("empty")
    else:
        dustbin_lid_status = "close"
        controlMotor(dustbin_lid_status)
        controlLed("empty")


# aws iot
def topic_callback(self, params, packet):
    print("received message: " + str(packet.payload))
    data = json.loads(packet.payload)

    global is_device_active
    is_device_active = data.get("is_device_active")


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(TOPIC_SUB, 1, topic_callback)


def on_publish(client, userdata, mid):
    print("message published: " + str(mid))


def on_disconnect(client, userdata, rc):
    print("disconnected from AWS IoT")


aws_config.client.on_connect = on_connect
aws_config.client.on_publish = on_publish
aws_config.client.on_disconnect = on_disconnect


def handleDataPublish():
    curr_time = time.time()

    if curr_time - prev_time > 5:
        prev_time = curr_time

        data = {
            "capacity_remaining": capacity_remaining,
            "dustbin_lid_status": dustbin_lid_status,
            "device_id": "rpi_1",
        }

        # publish data to AWS IoT
        aws_config.client.publish(TOPIC_PUB, json.dumps(data), 1)


def connectToAWSIoT():
    print("connecting to AWS IoT...")
    aws_config.client.connect()
    print("connected to AWS IoT")


connectToAWSIoT()


def main():
    global is_device_active
    global capacity_remaining

    capacity_remaining = getDustbinCapacity()
    is_people_nearby = getIRSensorStatus()

    if is_device_active:
        if capacity_remaining > 80:
            dustbin_lid_status = "close"
            controlMotor(dustbin_lid_status)
            controlLed("full")
        else:
            handlePeopleNearby(is_people_nearby)
    else:
        dustbin_lid_status = "close"
        controlMotor(dustbin_lid_status)
        controlLed("deactivated")

    handleDataPublish()


if __name__ == "__main__":
    # main loop
    while True:
        main()
