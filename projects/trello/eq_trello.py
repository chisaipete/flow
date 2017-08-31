#!python3

import os, argparse
from trello import TrelloClient

def read_credentials():
    basedir = os.path.abspath(os.path.dirname(__file__))
    credentials = {'trello':{}}
    with open(os.path.join(basedir,'trello.cred')) as fh:
        for line in fh.read().strip().split('\n'):
            if line:
                protocol, key, value = line.split()
                credentials[protocol][key] = value
    return credentials

def get_comment_text(card):
    return [c['data']['text'] for c in card.get_comments()]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Utility to access EQ Trello board and write an agenda")
    # parser.add_argument('-i', action="store", dest="input_json_path", required=True)
    args = parser.parse_args()
    cred = read_credentials()
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
        print(card.name, card.description, get_comment_text(card))
