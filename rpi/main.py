"""
Project Name: Smart Dustbin
"""

import json

# import RPi.GPIO as GPIO
import time
import aws_config
import peripherals as peripherals


# constant variables
DEVICE_ID = "dustbin_13"
OPEN_TIME = 5  # seconds

# global variables
capacity_remaining = 0
lid_status = "close"
prev_time = time.time()
prev_publish_time = time.time()
is_device_active = True


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
    global opened_time
    global status
    global prev_publish_time

    ir = peripherals.getIRValue()
    capacity_remaining = peripherals.getDustbinCapacityRemaining()

    # print("IR: ", ir)
    # print("Capacity Remaining: ", capacity_remaining)

    curr_time = time.time()

    if capacity_remaining < 50:  # for testing purposes
        peripherals.set_led("red")
    else:
        peripherals.set_led("green")

    if ir == 1:
        opened_time = time.time()

        if status == "close":
            status = "open"
            print("opened")
            peripherals.ctrlMotor("open")
            
        # print("opened")
        # status = "open"
        # peripherals.ctrlMotor("open")
        # opened_time = time.time()

    else:
        if curr_time - opened_time > 5 and status == "open":
            print("closed")
            status = "close"
            peripherals.ctrlMotor("close")

    if curr_time - prev_publish_time > 5:
        prev_publish_time = time.time()
        response = handleDataPublish(capacity_remaining, status)
        print("publish response: ", response)


if __name__ == "__main__":
    try:
        aws_config.connectToAWSIoT()
        aws_config.client.subscribe(TOPIC_SUB, 1, topic_callback)

        while True:
            main()
            time.sleep(0.1)
            # time.sleep(1)

    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        aws_config.client.disconnect()
        peripherals.GPIO.cleanup()
