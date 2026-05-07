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
from flask import Flask, render_template, Response
from threading import Thread
from time import sleep

from firebase_controller import get_devices
from gpio_controller import (
    control_light,
    control_fan,
    control_ac
)

from camera import VideoCamera

app = Flask(__name__)

camera = VideoCamera()

# -----------------------------
# FIREBASE DEVICE MONITOR
# -----------------------------
def firebase_loop():
    while True:
        try:
            devices = get_devices()

            if devices:
                control_light(devices.get("Light", 0))
                control_fan(devices.get("Fan", 0))
                control_ac(devices.get("AC", 0))

                print("Light:", devices.get("Light"))
                print("Fan:", devices.get("Fan"))
                print("AC:", devices.get("AC"))

        except Exception as e:
            print("Firebase Error:", e)

        sleep(1)

# Start background thread
Thread(target=firebase_loop, daemon=True).start()

# -----------------------------
# WEB ROUTES
# -----------------------------
@app.route('/')
def index():
    return render_template('index.html')

# -----------------------------
# CAMERA STREAM
# -----------------------------
def gen(camera):
    while True:
        frame = camera.get_frame()

        if frame is None:
            continue

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +
               frame +
               b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(
        gen(camera),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

# -----------------------------
# MAIN
# -----------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
