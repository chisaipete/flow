import win32com.client
import datetime

CALENDAR = 9
INBOX = 6
# "6" refers to the index of a folder - in this case,
# the inbox. You can change that number to reference any other folder

class Outlook():
    def __init__(self):
        self.outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        self.inbox = None
        self.calendar = None

    def test(self):
        pass

    def locate_folders(self):
        self.inbox = self.outlook.GetDefaultFolder(INBOX) 
        self.calendar = self.outlook.GetDefaultFolder(CALENDAR)
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

    def get_events(self, days=7):
        if not self.calendar:
            self.locate_folders()

        events = self.calendar.Items
        events.Sort("[Start]") # sort by start date
        events.IncludeRecurrences = "True"

        begin = datetime.date.today()
        end = begin + datetime.timedelta(days=days)
        events = events.Restrict("[Start] >= '" + begin.strftime("%m/%d/%Y") + "' AND [End] <= '" + end.strftime("%m/%d/%Y") + "'")

        fevents = []
        for event in events:
            if 'Non-Work' not in event.categories and 'Family' not in event.categories:
                b = (event.start + datetime.timedelta(hours=7)).astimezone().isoformat()
                n = (event.end + datetime.timedelta(hours=7)).astimezone().isoformat()
                fevents.append((event.subject, b, n, event.location, event.entryid))

        return fevents

# messages = inbox.Items
# message = messages.GetLast()
# body_content = message.body
# print(body_content)
# message.Display(True) #show selected item in outlook
