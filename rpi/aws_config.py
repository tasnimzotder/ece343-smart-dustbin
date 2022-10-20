"""
Configuration for AWS IoT
"""

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json

client = AWSIoTMQTTClient("rpi")


TOPIC_PUB = "smart_dustbin/data"
TOPIC_SUB = "smart_dustbin/ctrl"

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


def connectToAWSIoT():
    print("connecting to AWS IoT...")
    connect = client.connect()

    if connect == True:
        print("connected to AWS IoT")
    else:
        print("failed to connect to AWS IoT")
