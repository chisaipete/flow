#!/usr/bin/env python
from projects import trello
from notes import google_sheets

trello_connection = trello.Trello()
sheets_connection = google_sheets.Sheets()
# entries = sheets_connection.get_values_from_spreadsheet('longsheetidstringfromsheeturl', 'Stream', 'A:A')
entries = sheets_connection.get_values_from_spreadsheet('longsheetidstringfromsheeturl', 'Ideas', 'A:A')
trello_connection.set_active_board('Social')
trello_connection.set_active_list('Backlog')
for entry in entries:
    card_string = trello_connection.create_card(entry[0], '')
    print(f"{entry} --> {card_string}")
