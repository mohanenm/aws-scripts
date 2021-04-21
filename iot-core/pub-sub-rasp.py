import RPi.GPIO as GPIO
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
from datetime import date, datetime
import time
import json

SENSOR_PIN = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

# initialize GPIO
 
# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("123afhlss456")
myMQTTClient.configureEndpoint("******-ats.iot.us-east-1.amazonaws.com",$
myMQTTClient.configureCredentials("/home/pi/certs/AmazonRootCA1.pem", "/home/pi/certs/*****-private.pem.key", "/home/pi/certs/****-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish qu$
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
                                  
myMQTTClient.connect()
myMQTTClient.publish("motion-sense/info", "connected", 0)
 
#loop and publish sensor reading

def my_callback(channel):
    now = datetime.utcnow()
    now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ')
    movement = bool("movement-detected")

                                  
    if movement == True:
        result = {'time': now_string, 'motion': 'movement detected'}
        result = json.dumps(result)
        payload = json.loads(result)
        myMQTTClient.publish("motion-sense/data", payload, 0)
        sleep(4)
    else:
        result = {'time': now_string, 'motion': 'no movement'}
        result = json.dumps(result)
        payload = json.loads(result)
        myMQTTClient.publish("motion-sense/data", payload, 0)
        sleep(4)

try:
    GPIO.add_event_detect(SENSOR_PIN , GPIO.RISING, callback=my_callback)
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    print("Finish...")

GPIO.cleanup()



