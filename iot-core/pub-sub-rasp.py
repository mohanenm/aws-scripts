import RPi.GPIO as GPIO 
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient #aws iot sdk --> run with python3
from time import sleep # for board
from datetime import date, datetime # to get data and time from pi
# import time 
import json # for jsondumps

# initialize constant pin for in 
SENSOR_PIN = 23
# set up the pins on the raspberry pi correctly
# read on pin 23 
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

# AWS IoT certificate based connection
# start a client named motion detector
# set endpoint to my iot thing located on IOT core
# Check the certificates on my machine(these can be located on iot core)
# queueSize - Size of the queue for offline publish requests queueing.
# If set to 0, the queue is disabled. If set to -1, the queue size is set to be infinite(our case is infinite)
# configure the draining speed of queued requests while thing was offline(draining frequency)
# connectdisconnect timeout -Used to configure the time in seconds to wait for a CONNACK or a disconnect to complete. Should be called before connect.
# Mqtt operation timeout --> Used to configure the timeout in seconds for MQTT QoS 1 publish, subscribe and unsubscribe. Should be called before connect.
myMQTTClient = AWSIoTMQTTClient("motion-detector")
myMQTTClient.configureEndpoint("aioy8hqv8f6f5-ats.iot.us-east-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/pi/certs/AmazonRootCA1.pem", "/home/pi/certs/638c284605-private.pem.key", "/home/pi/certs/638c284605-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  
myMQTTClient.configureDrainingFrequency(2)  
myMQTTClient.configureConnectDisconnectTimeout(10)  
myMQTTClient.configureMQTTOperationTimeout(5)  

# connect to the client
myMQTTClient.connect()
# publish information about this connection to the topic motion-sense/info
myMQTTClient.publish("motion-sense/info", "motion-sensor connected", 0)

def my_callback(channel):
# get the current date and time from the device that the script is running on, all of which will be part of the payload
    now = datetime.now()
    time_now = now.strftime("%I:%M:%S %p")
    date_now = now.strftime("%m/%d/%Y")
    motion_message = "motion detected @ sensor 1"
      # format payload
    in_dict = {"date":date_now, "time":time_now, "motion":motion_message}
      # use dumps to make payload nice...will get an error message on topic and not be able to work with SNS if payload is not correct data type
    payload = json.dumps(in_dict)
      # Finally, publish the message to IOT core topic motion-sense/data
    myMQTTClient.publish("motion-sense/data", payload, 0)
       # also print the payload to the screen(if applicable)
    print(payload)
    sleep(4)
    
    # IGNORE, MY OWN TEST STUFF
    # do not copy
    #  else:
    #    print("No Motion Detected")
    #   sleep(1)

# look for events on board
try:
    GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, callback=my_callback)
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    print("Finish...")


