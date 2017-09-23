from __future__ import print_function
import httplib2
import os
import json
import pprint

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from googleapiclient import sample_tools


import datetime

from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify , json,url_for
import requests

app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/calendar',
            'https://www.googleapis.com/auth/drive.metadata.readonly']
CLIENT_ID = "35011833406-oibd1d11lsl8fsltv0g4ce8lfpr9l2aj.apps.googleusercontent.com"
CLIENT_SECRET = "Gl4vGNRDyuhbEpuVO_JSr2AG"
APPLICATION_NAME = 'new2'
app.config['SECRET_KEY'] = '\xf6,\xb7\x9e\x16#\x96\xf6>=\xa0*\xa2\xb5d1"\xd5\x1b\xf3\xc7\x19\xa2\x0e'

@app.route('/oauth2callback')
def oauth2callback():
    flow = client.OAuth2WebServerFlow( CLIENT_ID, CLIENT_SECRET,
    SCOPES, redirect_uri=url_for('oauth2callback', _external=True))
    flow.params['include_granted_scopes'] = "true"   # incremental auth
    print(request.url)
    print(request.args)
    if 'code' not in request.args:
        print("code not in request.args")
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)
    else:
        print("code in request.args")
        auth_code = request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        session['credentials'] = credentials.to_json()
        return redirect(url_for('index'))

@app.route('/')
def index():
    if 'credentials' not in session:
        print("credentials not in session")
        return redirect(url_for('oauth2callback'))
    print("Reaching here")
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    print(client.Credentials.to_json(credentials))
    if credentials.access_token_expired:
        return redirect(url_for('oauth2callback'))
    else:
        http_auth = credentials.authorize(httplib2.Http())
        print(type(client.Credentials.to_json(credentials)))
        cred_String = client.Credentials.to_json(credentials)
        cred_json = json.loads(cred_String)
        token = cred_json["access_token"]
        # service = discovery.build('drive', 'v3', http=http_auth)
        # results = service.files().list(
        # pageSize=10,fields="nextPageToken, files(id, name)").execute()
        # items = results.get('files', [])
        # if not items:
        #     print('No files found.')
        # else:
        #     print('Files:')
        #     for item in items:
        #         print('{0} ({1})'.format(item['name'], item['id']))

        service = discovery.build('calendar', 'v3', http=http_auth)
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
        events = eventsResult.get('items', [])
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
    return "CALENDAR STUFF"

    """Shows basic usage of the Google Calendar API.
    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """

@app.route('/index')
def indexhtml():
    return app.send_static_file('index.html')

if __name__ == "__main__":
	#port = int(os.environ.get("PORT", 5000))
	port = 8080
	app.run(debug=True,port=port)
