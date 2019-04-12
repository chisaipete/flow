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

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = os.path.join(credential_dir,'google-api.json')
APPLICATION_NAME = 'Sheets API - Python'

class Sheets():
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
        cred_file = os.path.join(self.cred, 'sheets-token.json')

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

    def create_service(self):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        self.service = discovery.build('sheets', 'v4', http=http)

    def get_values_from_spreadsheet(self, spreadsheet_id, sheet_name, range):
        self.create_service()
        sheet = self.service.spreadsheets()
        range_formula = f"{sheet_name}!{range}"
        result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                    range=range_formula).execute()
        return result.get('values', [])

    def append_list_to_table(self, spreadsheet_id, sheet_name, range, row_data):
        self.create_service()
        sheet = self.service.spreadsheets()
        range_formula = f"{sheet_name}!{range}"
        body = {
            'majorDimension': 'ROWS',
            'values': [row_data]
        }
        result = sheet.values().append(spreadsheetId=spreadsheet_id,
                                       range=range_formula,
                                       body=body,
                                       valueInputOption='USER_ENTERED').execute()
        print(f"{result.get('updates').get('updatedCells')} cells appended!")

    def main(self):
        """Shows basic usage of the Google Sheets API.
        """
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('sheets', 'v4', http=http)

        # The ID and range of a sample spreadsheet.
        SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
        SAMPLE_RANGE_NAME = 'Class Data!A2:E'

        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found')
        else:
            for row in values:
                print(f"{row[0]}, {row[4]}")


if __name__ == '__main__':
    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None
    d = Drive(flags=flags)
