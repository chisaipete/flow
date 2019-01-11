#!/usr/bin/env python
import os, sys
## hack for credentials directory
if __name__ == '__main__' and __package__ is None: # pragma: no cover
    path_base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.append(path_base)
## hack for credentials directory
credential_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'credentials')

import pocket
from credentials import read_credentials

class Pocket():
    def __init__(self):
        self.main()

    def main(self):
        cred = read_credentials('pocket')
        self.p = pocket.Pocket(
            consumer_key=cred['pocket']['consumer_key'],
            access_token=cred['pocket']['access_token'],
        )
        
    def get_archive(self):
        self.archive = self.p.get(state="archive", favorite=0)

    def get_favorites(self):
        self.archive_favorites = self.p.get(state="archive", favorite=1)
        self.list_favorites = self.p.get(state="unread", favorite=1)

    def get_list(self):
        self.archive = self.p.get(state="unread", favorite=0)

        # https://getpocket.com/developer/docs/v3/retrieve

        # Fetch a list of articles
        # try:
        #     print(p.retrieve(offset=0, count=10))
        # except PocketException as e:
        #     print(e.message)

        # # Add an article
        # p.add('https://pymotw.com/3/asyncio/')

        # # Start a bulk operation and commit
        # p.archive(1186408060).favorite(1188103217).tags_add(
        #     1168820736, 'Python'
        # ).tags_add(
        #     1168820736, 'Web Development'
        # ).commit()