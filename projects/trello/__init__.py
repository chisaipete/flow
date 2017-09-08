#!/usr/bin/env python
import os, sys
## hack for credentials directory
if __name__ == '__main__' and __package__ is None: # pragma: no cover
    path_base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.append(path_base)
## hack for credentials directory
credential_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'credentials')

from trello import TrelloClient
from credentials import read_credentials

class Trello():
    def __init__(self):
        self.main()

    def get_comment_text(self, card):
        return [c['data']['text'] for c in card.get_comments()]

    def main(self):
        cred = read_credentials('trello')
        client = TrelloClient(
            api_key=cred['trello']['api_key'], 
            api_secret=cred['trello']['api_secret'], 
            token=cred['trello']['api_token']
            )
        
        boards = client.list_boards()
        eq_board = client.get_board([b for b in boards if b.name == 'Elders Quorum'][0].id)
        
        # all lists
        lists = eq_board.all_lists()
        news_list = [l for l in lists if 'Announcements' in l.name][0]
        callings_list = [l for l in lists if 'Callings' in l.name][0]
        delegated_list = [l for l in lists if 'Delegated' in l.name][0]
        wip_list = [l for l in lists if 'Work in Progress' in l.name][0]
        task_list = [l for l in lists if 'Tasks' in l.name][0]

        # announcements
        announcements = news_list.list_cards()

        for card in announcements:
            print(card.name, card.description, self.get_comment_text(card))

if __name__ == '__main__':
    