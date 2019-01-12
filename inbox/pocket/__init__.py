#!/usr/bin/env python
import os, sys
## hack for credentials directory
if __name__ == '__main__' and __package__ is None: # pragma: no cover
    path_base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.append(path_base)
## hack for credentials directory
credential_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'credentials')

import pocket as p
from credentials import read_credentials

# detect presense of proxy and use env varibles if they exist
pi = httplib2.proxy_info_from_environment()
if pi:
    import socks
    socks.setdefaultproxy(pi.proxy_type, pi.proxy_host, pi.proxy_port)
    socks.wrapmodule(requests)

class Pocket():
    def __init__(self):
        self.main()

    def main(self):
        cred = read_credentials('pocket')
        self.instance = p.Pocket(
            consumer_key=cred['pocket']['consumer_key'],
            access_token=cred['pocket']['access_token'],
        )

    def add(self, url="https://w.wol.ph/2013/09/18/batch-adding-data-to-pocket/"):
        self.instance.add(url=url)

    def get_archive(self):
        self.archive = self.instance.get(state="archive", favorite=0)

    def get_favorites(self):
        self.archive_favorites = self.instance.get(state="archive", favorite=1)
        self.list_favorites = self.instance.get(state="unread", favorite=1)

    def get_list(self):
        self.archive = self.instance.get(state="unread", favorite=0)

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