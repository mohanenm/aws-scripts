import RPi.GPIO as GPIO
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
from datetime import date, datetime
import time
 
SENSOR_PIN = 23
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

# initialize GPIO
GPIO.cleanup()
 
# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("123afhlss456")
myMQTTClient.configureEndpoint("aioy8hqv8f6f5-ats.iot.us-east-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/pi/certs/AmazonRootCA1.pem", "/home/pi/certs/638c284605-private.pem.key", "/home/pi/certs/638c284605-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
 
#connect and publish
myMQTTClient.connect()
myMQTTClient.publish("motion-sense/info", "connected", 0)
 
#loop and publish sensor reading

def my_callback(channel):
    now = datetime.utcnow()
    now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ')
    movement = bool("movement-detected")
    if movement == True:
     payload = '{ "timestamp": "' + now_str + '","motion": ' + "Movement Detected' }'
        print payload
        myMQTTClient.publish("motion-sense/data", payload, 0)
        sleep(4)
    else:
        print (".")
        sleep(1)
     
try:
    GPIO.add_event_detect(SENSOR_PIN , GPIO.RISING, callback=my_callback)
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    print "Finish..."
