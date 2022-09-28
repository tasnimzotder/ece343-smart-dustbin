from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json

client = AWSIoTMQTTClient("rpi")


aws_endpoint = json.load(open("aws_endpoint.json")).get("aws_endpoint")

client.configureEndpoint(aws_endpoint, 8883)
client.configureCredentials(
    "./certs/AmazonRootCA1.pem",
    "./certs/private.pem.key",
    "./certs/certificate.pem.crt",
)

client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
client.configureDrainingFrequency(2)  # Draining: 2 Hz
client.configureConnectDisconnectTimeout(10)  # 10 sec
client.configureMQTTOperationTimeout(5)  # 5 sec
