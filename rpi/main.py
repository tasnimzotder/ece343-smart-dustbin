"""
Project Name: Smart Dustbin
"""

import json

# import RPi.GPIO as GPIO
import time
import aws_config
import utils


# constant variables
DEVICE_ID = "dustbin_1"


TOPIC_PUB = aws_config.TOPIC_PUB
TOPIC_SUB = aws_config.TOPIC_SUB


# aws iot
def topic_callback(self, params, packet):
    print("received message: " + str(packet.payload))
    data = json.loads(packet.payload)

    global is_device_active
    is_device_active = data.get("is_device_active")


def handleDataPublish(cap_remaining: float, lid_status: str) -> bool:
    data = {
        "capacity_remaining": cap_remaining,
        "dustbin_lid_status": lid_status,
        "device_id": DEVICE_ID,
    }

    # publish data to AWS IoT
    response = aws_config.client.publish(TOPIC_PUB, json.dumps(data), 1)

    if response == True:
        print("data published to AWS IoT")
    else:
        print("failed to publish data to AWS IoT")

    return response


opened_time = time.time()
prev_time = time.time()
prev_publish_time = time.time()
status = "close"

OPEN_TIME_DELTA = 5  # seconds


def main():
    global prev_time
    global prev_publish_time
    global opened_time
    global status

    ir = utils.getIRValue()

    print("ir: " + str(ir))

    curr_time = time.time()

    capacity_remaining = utils.getDustbinCapacityRemaining()
    print("capacity_remaining: " + str(capacity_remaining))

    # if ir == 1:
    #     print("opened")
    #     status = "open"
    #     utils.ctrlMotor("open")
    #     opened_time = time.time()

    #     # publish data to AWS IoT
    #     capacity_remaining = utils.getDustbinCapacityRemaining()
    #     handleDataPublish(capacity_remaining, status)

    # else:
    #     if curr_time - opened_time > OPEN_TIME_DELTA and status == "open":
    #         print("closed")
    #         status = "close"
    #         utils.ctrlMotor("close")

    #         # publish data to AWS IoT
    #         capacity_remaining = utils.getDustbinCapacityRemaining()
    #         handleDataPublish(capacity_remaining, status)


if __name__ == "__main__":

    try:
        # utils.setupGPIO()
        aws_config.connectToAWSIoT()
        aws_config.client.subscribe(TOPIC_SUB, 1, topic_callback)

        while True:
            main()
            # print("looping")
            time.sleep(0.1 * 10)

    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        aws_config.client.disconnect()
        utils.servo.stop()
        utils.GPIO.cleanup()
