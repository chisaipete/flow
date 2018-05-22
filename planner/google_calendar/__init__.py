#!/usr/bin/env python
import os, sys
## hack for credentials directory
if __name__ == '__main__' and __package__ is None: # pragma: no cover
    path_base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.append(path_base)
## hack for credentials directory
credential_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'credentials')

import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

# detect presense of proxy and use env varibles if they exist
pi = httplib2.proxy_info_from_environment()
if pi:
    import socks
    socks.setdefaultproxy(pi.proxy_type, pi.proxy_host, pi.proxy_port)
    socks.wrapmodule(httplib2)

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = os.path.join(credential_dir,'google-api.json')
APPLICATION_NAME = 'Google Calendar API - Python'

class Calendar():
    def __init__(self, cred=credential_dir, flags=None):
        self.cred = credential_dir
        self.flags = flags

    def setup_service(self):
        self.credentials = self.get_credentials()
        self.http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3', http=self.http)

    def get_credentials(self): # pragma: no cover
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        if not os.path.exists(self.cred):
            os.makedirs(self.cred)
        cred_file = os.path.join(self.cred, 'calendar-token.json')

        store = Storage(cred_file)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if self.flags:
                credentials = tools.run_flow(flow, store, self.flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + cred_file)
        return credentials

    def test(self):
        """Shows basic usage of the Google Calendar API.

        Creates a Google Calendar API service object and outputs a list of the next
        10 events on the user's calendar.
        """
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        # print('Getting the upcoming 10 events')
        eventsResult = service.events().list(
            calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])

        if not events:
            print('No upcoming events found.')
        else:
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, event['summary'])

    def get_events(self, days=7):
        now = datetime.datetime.utcnow() - datetime.timedelta(hours=7)
        end = datetime.datetime.utcnow() - datetime.timedelta(hours=7) + datetime.timedelta(days=days)
        now = datetime.datetime.combine(now.date(), datetime.datetime.min.time()).isoformat() + 'Z' # 'Z' indicates UTC time
        end = datetime.datetime.combine(end.date(), datetime.datetime.min.time()).isoformat() + 'Z'
        eventsResult = self.service.events().list(calendarId='primary', timeMin=now, timeMax=end).execute()
        events = eventsResult.get('items', [])

        fevents = []
        for event in events:
            fevents.append((event['summary'], event['start'].get('dateTime', event['start'].get('date')), event['end'].get('dateTime', event['end'].get('date')), event['id']))

        return fevents

    def check_for_event(self, evt):
        pass

    def create_event(self, evt):
        e = {
          'summary': evt['summary'],
          # 'description': 'A chance to hear more about Google\'s developer products.',
          'start': {
            # 'dateTime': '2015-05-28T09:00:00-07:00',
            'dateTime': evt['start'],
          },
          'end': {
            'dateTime': evt['end'],
          },
        }
        event = self.service.events().insert(calendarId='primary', body=e).execute()
        print('Event created: {}'.format(event.get('htmlLink')))

    def update_event(self, evt):
        e = {
          'summary': evt['summary'],
          # 'description': 'A chance to hear more about Google\'s developer products.',
          'start': {
            # 'dateTime': '2015-05-28T09:00:00-07:00',
            'dateTime': evt['start'],
          },
          'end': {
            'dateTime': evt['end'],
          },
        }
        event = self.service.events().update(calendarId='primary', eventId=evt['id'], body=e).execute()
        print('Event updated: {}'.format(event.get('htmlLink')))


if __name__ == '__main__':
    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None

    # detect presense of proxy and use env varibles if they exist
    pi = httplib2.proxy_info_from_environment()
    if pi:
        import socks
        socks.setdefaultproxy(pi.proxy_type, pi.proxy_host, pi.proxy_port)
        socks.wrapmodule(httplib2)

    c = Calendar(flags=flags)
    c.test()
