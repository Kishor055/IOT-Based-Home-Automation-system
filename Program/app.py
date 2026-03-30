from firebase import firebase
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)

firebase = firebase.FirebaseApplication('https://iotproject-f5403.firebaseio.com/', None)

while True:
    sleep(1)
    result = firebase.get('Status', None)
    if result == 1:
        GPIO.output(40, 1)
        print("ON")
    if result == 0:
        GPIO.output(40, 0)
        print("OFF")
