from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import pytz
import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = "https://www.googleapis.com/auth/calendar"
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'new2'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        #print('Storing credentials to ' + credential_path)
    return credentials

user_suggest = {
      'summary': 'RoshanRishav Dinner',
      'location': 'MC',
      'description': '',
      'start': {
        'dateTime': '2018-03-28T09:00:00-07:00',
        'timeZone': 'America/New_York',
      },
      'end': {
        'dateTime': '2018-03-28T10:00:00-07:00',
        'timeZone': 'America/New_York',
      }
     }

def listOfEvents(event_dict):
    credentials = get_credentials()
    # print(credentials)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    new_event = service.events().insert(calendarId='primary', body=event_dict).execute()
    if not events:
        # print('No upcoming events found.')
        for event in events:

        # print (event)
            start = event['start'].get('dateTime', event['start'].get('date'))
        # print(start, event['summary'], event['id'])


def create_event(event_dict):
    credentials = get_credentials()
    # print(credentials)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    start_time = event_dict["start"]["dateTime"]
    end_time = event_dict["end"]["dateTime"]
    eventsResult = service.events().list(
        calendarId='primary', timeMax=end_time, timeMin=start_time, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    event_list = eventsResult.get('items', [])
    # print(event_dict)
    # print(event_list)
    if not event_list:
        new_event = service.events().insert(calendarId='primary', body=event_dict).execute()
        # print('Event created: %s' % (new_event.get('htmlLink')))
        # print("ID : " + new_event["id"])
        return [new_event["id"] , "added"]
    else:
        # print("Busy")
        return "Busy"

def fourteen_day_schedule():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    eventsResult = service.events().list(
    calendarId='primary', timeMin=now,maxResults=100).execute()
    events = eventsResult.get('items', [])
    event_dict = {}
    for i in events:
        event_dict['summary'] = {
                                    "start_time" : i['start'],
                                    "end_time"   : i['end']
                                }
    print(event_dict)
    return event_dict
    #convert_time_to_block(event_dict)

def convert_time_to_block(events):
    dictOfTimes={}
    utc_datetime = datetime.datetime.utcnow()
    currentTime = utc_datetime.strftime("%Y-%m-%d %H:%M:%S")
    start_day=currentTime[6:7]
    #date=date[15:]
    start_time=currentTime[currentTime.index(" ")+1:]
    #date= user_suggest['start']['dateTime']
    for key,value in events.iteritems():
        dateStart=value["start_time"]["dateTime"]
        dateEnd=value["end_time"]["dateTime"]
        timeStart=dateStart[dateStart.index("T")+1:dateStart.index("T")+9]
        timeEnd=dateEnd[dateEnd.index("T")+1:dateEnd.index("T")+9]
        hours=int(timeEnd[0:timeEnd.index(":")])-int(timeStart[0:timeStart.index(":")])
        minutes=int(timeEnd[timeEnd.index(":")+1 : timeEnd.index(":")+3]) - int(timeStart[timeStart.index(":")+1 : timeStart.index(":")+3])
        duration=hours+minutes/60.0
        day_Block_Index=int(dateStart[8:10])-int(start_day)
        time_Block_Index=int(timeStart[0:timeStart.index(":")])+int(timeStart[timeStart.index(":")+1 : timeStart.index(":")+3])/60.0
        print(day_Block_Index)
        print (time_Block_Index/0.5)
        print(duration)
        dayIndex=[("blockDay",day_Block_Index)]
        timeIndex=[("blockTime",time_Block_Index)]
        duration=[("duration",duration)]
        dictOfTimes.update(dayIndex)
        dictOfTimes.update(timeIndex)
        dictOfTimes.update(duration)

def convert_input_time_to_block(time):
    hours=int(time[time.index(":")-2:time.index(":")])
    minutes=int(time[time.index(":")+1 : time.index(":")+3])
    time_Block_Index=hours+minutes/60.0
    touple=(0,time_Block_Index/0.5)
    return(touple)

def cancel_event(event_id):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    service.events().delete(calendarId='primary', eventId=event_id).execute()
    print("Cancelled")
    return "Cancelled"

#if __name__ == "__main__":
    #create_event(user_suggest);
    #id = "dpntfuuh6ejnrktil3bb8ljmmg"
    #listOfEvents(user_suggest)
    #cancel_event(id)
