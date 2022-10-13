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
OPEN_TIME = 5  # seconds

# # global variables
# capacity_remaining = 0
# lid_status = "close"
# prev_time = time.time()
# prev_publish_time = time.time()
# is_device_active = True


TOPIC_PUB = "smart_dustbin/data"
TOPIC_SUB = "smart_dustbin/ctrl"


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

    return response


opened_time = time.time()
prev_time = time.time()
prev_publish_time = time.time()
status = "close"


def main():
    global prev_time
    # global capacity_remaining
    # global lid_status

    # # check if device is active
    # if not is_device_active:
    #     return

    capacity_remaining = utils.getDustbinCapacityRemaining()
    # ir_value = utils.getIRValue()

    # curr_time = time.time()

    # if ir_value == 1:
    #     lid_status = "open"
    #     utils.ctrlMotor("open")
    #     prev_time = time.time()
    # else:
    #     if curr_time - prev_time > OPEN_TIME and lid_status == "open":
    #         lid_status = "close"
    #         utils.ctrlMotor("close")

    # # publish data to AWS IoT
    # if curr_time - prev_publish_time > 5:
    #     prev_publish_time = time.time()
    #     handleDataPublish(capacity_remaining, lid_status)
    global opened_time
    global status
    ir = utils.getIRValue()

    curr_time = time.time()

    if ir == 1:
        print("opened")
        status = "open"
        utils.ctrlMotor("open")
        opened_time = time.time()

    else:
        if curr_time - opened_time > 5 and status == "open":
            print("closed")
            status = "close"
            utils.ctrlMotor("close")

    if curr_time - prev_publish_time > 5:
        prev_publish_time = time.time()
        handleDataPublish(capacity_remaining, status)


if __name__ == "__main__":

    try:
        utils.setupGPIO()
        aws_config.connectToAWSIoT()
        aws_config.client.subscribe(TOPIC_SUB, 1, topic_callback)

        while True:
            main()
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        aws_config.client.disconnect()
        utils.GPIO.cleanup()
