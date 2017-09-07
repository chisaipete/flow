import win32com.client
import datetime

INBOX = 6
# "6" refers to the index of a folder - in this case,
# the inbox. You can change that number to reference any other folder

class Mailbox():
    def __init__(self):
        self.outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        self.inbox = None

    def test(self):
        pass

    def locate_folders(self):
        self.inbox = self.outlook.GetDefaultFolder(INBOX) 
        self.action_support = None
        self.archive = None
        # Find Action Support and Archive Folders
        for folder in self.inbox.Folders:
            if folder.name == 'Action Support':
                self.action_support = folder
            elif folder.name == 'Archive':
                self.archive = folder

    def archive_message(self, message):
        message.move(self.archive)

    def process_action_support(self):
        if not self.inbox:
            self.locate_folders()

        for message in self.action_support.Items:
            # print('Subject: {}'.format(message.subject))
            subject = message.subject
            # print('Snippet: {}'.format(message.body[:100]))
            snippet = message.body[:100]
            # print('Date: {}'.format(message.receivedtime.strftime("%a %d %b %Y %H:%M:%S")))
            date = message.receivedtime.strftime("%a %d %b %Y %H:%M:%S")
            # NOTE: https://superuser.com/questions/71786/can-i-create-a-link-to-a-specific-email-message-in-outlook/829959#829959
            perma_link = 'https://api.fnkr.net/goto/jsclient/raw/?closeAfter=500#outlook:{}'.format(message.entryid)
            yield (subject, snippet, date, perma_link, message)

# messages = inbox.Items
# message = messages.GetLast()
# body_content = message.body
# print(body_content)
# message.Display(True) #show selected item in outlook
