# Project Working Docs

## Project Images

## Steps

1. When the dustbin is not full, the green LED is turned on and the red LED is turned on when the dustbin is full.
2. The distance between the dustbin and the ground is measured using the ultrasonic sensor and the system calculates the remaining capacity of the dustbin.
3. The IR sensor detects the presence of a person. If a person is detected, the servo motor opens the dustbin lid.
4. The remaining capacity of the dustbin and the status of the lid is sent to the AWS IoT Core using MQTT. The topic `dustbin/data` is used to send the data.
5. The data is stored in the AWS Timestream database.
6. AWS Lambda is used as a backend for the web application. It fetches the data from the AWS Timestream database and sends it to the web application.
7. The web application is built using React. It fetches the data from the AWS Lambda backend and displays it in the web application.
8. The web application also has a control panel to control the dustbin. The control panel is used to activate or deactivate the dustbin.
9. The user control data is sent to the AWS Lambda. The Lambda uses the topic `dustbin/ctrl` to send the data to the Raspberry Pi through the AWS IoT Core.

## Details of the Components

### Raspberry Pi

### Ultrasonic Sensor

### LEDs

### Servo Motor

### IR Sensor

### MQ
