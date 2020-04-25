from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from httplib2 import Http
from oauth2client import file, client, tools
from libdw import pyrebase
import time

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store, flags) \
            if flags else tools.run(flow, store)

CAL = build('calendar', 'v3', http=creds.authorize(Http()))

################################################################################################

url = 'https://test-firebase-95e43.firebaseio.com/'
apikey = 'AIzaSyDDzT4FSVfdXLocVNLyio0vwFlWRkhmnTQ'

config = {
    "apiKey": apikey,
    "databaseURL": url,
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


def main():
    while True:
        check = db.child('DW').get().val()
        if check is None:
            time.sleep(1)
            print('yes')
            continue
        else:
            print('no')
            calendar_add()


def calendar_add():
    info = db.child('DW').get().val()

    GMT_OFF = '+08:00' # SG Timezone
    event = {
        'summary': f'{info["event_name"]}',
        'start': {'dateTime': f'{info["start_date"]}{GMT_OFF}'},
        'end': {'dateTime': f'{info["end_date"]}{GMT_OFF}'},
        'colorId': f'{info["colour"]}'
    }

    e = CAL.events().insert(calendarId='primary',
                            body=event).execute()

    print(f'''*** {event['summary']} event added:
        Start: {event['start']}
        End: {event['end']}''')

    db.child('DW').remove()

    main()

main()