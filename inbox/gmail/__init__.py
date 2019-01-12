#!/usr/bin/env python
import os, sys
## hack for credentials directory
if __name__ == '__main__' and __package__ is None: # pragma: no cover
    path_base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.append(path_base)
## hack for credentials directory
credential_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'credentials')

import httplib2
from apiclient import discovery, errors
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import base64, email, email.header, datetime
from email.mime.text import MIMEText

# detect presense of proxy and use env varibles if they exist
pi = httplib2.proxy_info_from_environment()
if pi:
    import socks
    socks.setdefaultproxy(pi.proxy_type, pi.proxy_host, pi.proxy_port)
    socks.wrapmodule(httplib2)

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
CLIENT_SECRET_FILE = os.path.join(credential_dir,'google-api.json')
APPLICATION_NAME = 'Gmail API - Python'

class Mailbox():
    def __init__(self, cred=credential_dir, flags=None):
        self.cred = credential_dir
        self.flags = flags

    def get_credentials(self): # pragma: no cover
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        if not os.path.exists(self.cred):
            os.makedirs(self.cred)
        cred_file = os.path.join(self.cred, 'gmail-token.json')

        store = Storage(cred_file)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if self.flags:
                credentials = tools.run_flow(flow, store, self.flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run_flow(flow, store)
            print('Storing credentials to ' + cred_file)
        return credentials

    def test(self):
        """Shows basic usage of the Gmail API.

        Creates a Gmail API service object and outputs a list of label names
        of the user's Gmail account.
        """
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)

        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
        else:
            print('Labels:')
        for label in labels:
            print('\t{}'.format(label))

    def archive_message(self, message):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)
        # get message's threadId   
        # remove the "INBOX" label from the whole thread
        payload = {'removeLabelIds': ['INBOX'], 'addLabelIds': []}
        r = service.users().threads().modify(userId='me', id=message['threadId'], body=payload).execute()

    def create_message(self, sender, to, subject, message_text):
        """Create a message for an email.

        Args:
            sender: Email address of the sender.
            to: Email address of the receiver.
            subject: The subject of the email message.
            message_text: The text of the email message.

        Returns:
            An object containing a base64url encoded email object.
        """
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        return {'raw': raw}

    def send_message(self, message):
        """Send an email message.

        Args:
            service: Authorized Gmail API service instance.
            user_id: User's email address. The special value "me"
            can be used to indicate the authenticated user.
            message: Message to be sent.

        Returns:
            Sent Message.
        """
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)
        try:
            message = (service.users().messages().send(userId='me', body=message).execute())
            print('Message Id: {}'.format(message['id']))
            return message
        except errors.HttpError as error:
            print('An error occurred: {}'.format(error))
        
    def process_action_support(self):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)

        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        for label in labels:
            if label['name'] == 'Action Support':
                action_support = label['id']
                break

        results = service.users().messages().list(userId='me', labelIds=[action_support]).execute()
        messages = results.get('messages', [])

        if not messages:
            print('No messages found.')
        else:
            for message in messages:
                m = service.users().messages().get(userId='me', id=message['id'], format='raw').execute()
                msg_str = base64.urlsafe_b64decode(m['raw'].encode('ASCII'))
                msg = email.message_from_bytes(msg_str)
                hdr = email.header.make_header(email.header.decode_header(msg['Subject']))
                subject = str(hdr).strip()
                # print('Subject: {}'.format(subject))
                # print('Snippet: {}'.format(m['snippet']))
                snippet = m['snippet']
                # Now convert to local date-time
                date_tuple = email.utils.parsedate_tz(msg['Date'])
                local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
                # print ("Date:", local_date.strftime("%a %d %b %Y %H:%M:%S"))
                date = local_date.strftime("%a %d %b %Y %H:%M:%S")
                msg_id = str(email.header.make_header(email.header.decode_header(msg['Message-ID'])))
                perma_link = "https://inbox.google.com/u/0/search/rfc822msgid:{}".format(msg_id)
                # msg = (subject, snippet, date, perma_link, item)
                yield (subject, snippet, date, perma_link, message)
                

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

    m = Mailbox(flags=flags)
    m.test()
