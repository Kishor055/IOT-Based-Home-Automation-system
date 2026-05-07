import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

LIGHT = 40
FAN = 38
AC = 36

GPIO.setup(LIGHT, GPIO.OUT)
GPIO.setup(FAN, GPIO.OUT)
GPIO.setup(AC, GPIO.OUT)

def control_light(state):
    GPIO.output(LIGHT, state)

def control_fan(state):
    GPIO.output(FAN, state)

def control_ac(state):
    GPIO.output(AC, state)

def cleanup():
    GPIO.cleanup()
