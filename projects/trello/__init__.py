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
        # self.process_eq_board()
        cred = read_credentials('trello')
        self.client = TrelloClient(
            api_key=cred['trello']['api_key'],
            api_secret=cred['trello']['api_secret'],
            token=cred['trello']['api_token']
        )

    def set_active_board(self, board):
        self.active_board = self.client.get_board([b for b in self.client.list_boards() if b.name == board][0].id)

    def set_active_list(self, _list):
        # try:
        self.active_list = [l for l in self.active_board.all_lists() if _list in l.name][0]
        # except:
        #     print('Active Board is not set')

    def create_card(self, title, description, board=None, _list=None):
        if board and _list:
            self.set_active_board(board)
            self.set_active_list(_list)

        # create a new card with title and description
        new_card = self.active_list.add_card(title, description)
        return str(new_card)

    def get_comment_text(self, card):
        return [c['data']['text'] for c in card.get_comments()]

    def process_eq_board(self):

        boards = self.client.list_boards()
        eq_board = self.client.get_board([b for b in boards if b.name == 'Elders Quorum'][0].id)

        # all lists
        lists = eq_board.all_lists()
        news_list = [l for l in lists if 'Announcements' in l.name][0]
        # callings_list = [l for l in lists if 'Callings' in l.name][0]
        # delegated_list = [l for l in lists if 'Delegated' in l.name][0]
        # wip_list = [l for l in lists if 'Work in Progress' in l.name][0]
        # task_list = [l for l in lists if 'Tasks' in l.name][0]

        # announcements
        announcements = news_list.list_cards()

        for card in announcements:
            print(card.name, card.description, self.get_comment_text(card))


if __name__ == '__main__':
    pass
