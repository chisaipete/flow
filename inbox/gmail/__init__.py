#!/usr/bin/env python
## hack for credentials directory
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
## hack for credentials directory

from credentials import read_credentials
import imaplib, email, email.header, datetime, re
pattern_uid = re.compile(b'\d+ \(UID (?P<uid>\d+)\)')

class Mailbox():
    def __init__(self):
        self.cred = read_credentials('gmail')
        self.mailbox = imaplib.IMAP4_SSL(self.cred['gmail']['imap_server'])
        self.authenticate()

    def authenticate(self):        
        rv, data = self.mailbox.login(self.cred['gmail']['from_email'],self.cred['gmail']['from_pwd'])
        # print(rv, data) # could check to see that rv == 'OK'
        # rv, data = self.mailbox.list()
        # pprint.pprint(data)
        # rv, data = mail.select('INBOX')
        rv, data = self.mailbox.select('"Action Support"')
        self.process_mail()

    def parse_uid(self, data):
        match = pattern_uid.match(data)
        return match.group('uid')

    def process_mail(self):
        rv, data = self.mailbox.search(None, "ALL")
        if rv != 'OK':
            print("No messages found!")
            return

        for num in data[0].split():
            rv, data = self.mailbox.fetch(num, '(RFC822)')
            if rv != 'OK':
                print("ERROR getting message", num)
                return

            msg = email.message_from_bytes(data[0][1])
            hdr = email.header.make_header(email.header.decode_header(msg['Subject']))
            subject = str(hdr).strip()
            print('Message %s: %s' % (num, subject))
            print('Raw Date:', msg['Date'])
            # Now convert to local date-time
            date_tuple = email.utils.parsedate_tz(msg['Date'])
            if date_tuple:
                local_date = datetime.datetime.fromtimestamp(
                    email.utils.mktime_tz(date_tuple))
                print ("Local Date:", \
                    local_date.strftime("%a, %d %b %Y %H:%M:%S"))
            msg_id = str(email.header.make_header(email.header.decode_header(msg['Message-ID'])))
            print("https://inbox.google.com/u/0/search/rfc822msgid:{}".format(msg_id))

            rv, data = self.mailbox.fetch(num, '(UID)')
            if rv != 'OK':
                print("ERROR getting UID", num)
                return
            msg_uid = self.parse_uid(data[0]).decode()
            print(msg_uid)

            if msg_uid == '1':
                self.archive_mail(msg_uid)

    def archive_mail(self, uid): #Move to "[Gmail]/All Mail"
        result = self.mailbox.move(uid, '"[Gmail]/All Mail"')
