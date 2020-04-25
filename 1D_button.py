import RPi.GPIO as GPIO
from time import sleep
from libdw import pyrebase


url = 'https://test-firebase-95e43.firebaseio.com/'  # URL to Firebase database
apikey = 'AIzaSyDDzT4FSVfdXLocVNLyio0vwFlWRkhmnTQ'  # unique token used for authentication

config = {
    "apiKey": apikey,
    "databaseURL": url,
}

# Create a firebase object by specifying the URL of the database and its secret token.
# The firebase object has functions put and get, that allows user to put data onto 
# the database and also retrieve data from the database.
firebase = pyrebase.initialize_app(config)
db = firebase.database()
#def button1_callback(channel):
#    subj_list.append('Digital World')
#def button2_callback(channel):
#    subj_list.append('Systems World')
#def button3_callback(channel):
#    subj_list.append('Bio/Chem')
#def button4_callback(channel):
#    subj_list.append('Physics')
#def button5_callback(channel):
#    break
    #end the process and send to firebase
# Use the BCM GPIO numbers as the numbering scheme.
GPIO.setmode(GPIO.BCM)
GPIO.setup(25,GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(12,GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(16,GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(20,GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(21,GPIO.IN, GPIO.PUD_DOWN)
# Use GPIO12, 16, 20 and 21 for the buttons.
subj_list=[]
done = False
print('yey')
while not done:
    if GPIO.input(25) == GPIO.HIGH:
        sleep(0.3)
        print('DW')
        subj_list.append('Digital World')
    elif GPIO.input(12) == GPIO.HIGH:
        sleep(0.3)
        print('SW')
        subj_list.append('Systems World')
    elif GPIO.input(16) == GPIO.HIGH:
        sleep(0.3)
        subj_list.append('Bio/Chem')
    elif GPIO.input(20)==GPIO.HIGH:
        sleep(0.3)
        subj_list.append('Physics')
    elif GPIO.input(21) == GPIO.HIGH:
        sleep(0.3)
        print('ok')
        break
    
#    GPIO.add_event_detect(25, GPIO.RISING,callback= button1_callback)
#    GPIO.add_event_detect(12, GPIO.RISING,callback= button2_callback)
#    GPIO.add_event_detect(16, GPIO.RISING,callback= button3_callback)
#    GPIO.add_event_detect(20, GPIO.RISING,callback= button4_callback)
#    GPIO.add_event_detect(21, GPIO.RISING,callback= button5_callback)

print(subj_list)
print('DONE')
db.child('Subject').set(subj_list)
GPIO.cleanup()