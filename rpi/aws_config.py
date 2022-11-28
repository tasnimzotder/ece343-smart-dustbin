"""
Configuration for AWS IoT
"""

import json

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

client = AWSIoTMQTTClient("rpi")


aws_endpoint = json.load(open("config.json")).get("aws_endpoint")

# config.json contains the AWS IoT endpoint
# {
#     "aws_endpoint": "xxxxxxxxxxxxxx-ats.iot.ap-southeast-1.amazonaws.com"
# }

client.configureEndpoint(aws_endpoint, 8883)
client.configureCredentials(
    "./certs/AmazonRootCA1.pem",
    "./certs/private.pem.key",
    "./certs/certificate.pem.crt",
)

# AmazonRootCA1.pem is the Root CA certificate
# private.pem.key is the private key
# certificate.pem.crt is the device certificate file

client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
client.configureDrainingFrequency(2)  # Draining: 2 Hz
client.configureConnectDisconnectTimeout(10)  # 10 sec
client.configureMQTTOperationTimeout(5)  # 5 sec


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # client.subscribe(TOPIC_SUB, 1, topic_callback)


def on_publish(client, userdata, mid):
    print("message published: " + str(mid))


def on_disconnect(client, userdata, rc):
    print("disconnected from AWS IoT")


client.on_connect = on_connect
client.on_publish = on_publish
client.on_disconnect = on_disconnect


def connectToAWSIoT():
    print("connecting to AWS IoT...")
    client.connect()
    print("connected to AWS IoT")
