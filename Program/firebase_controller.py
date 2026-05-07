from firebase import firebase

firebase_app = firebase.FirebaseApplication(
    'https://iotproject-f5403.firebaseio.com/',
    None
)

def get_devices():
    data = firebase_app.get('/Devices', None)
    return data
