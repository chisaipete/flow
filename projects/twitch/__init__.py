#!/usr/bin/env python
import os, sys
## hack for credentials directory
if __name__ == '__main__' and __package__ is None: # pragma: no cover
    path_base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.append(path_base)
## hack for credentials directory
credential_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'credentials')

import twitch
from credentials import read_credentials


class Twitch():
    def __init__(self):
        cred = read_credentials('twitch')
        self.client = twitch.Helix(cred['twitch']['client_id'])

    def test(self, *userlist):
        for user in self.client.users(*userlist):
            print(f"Twitch user: {user.display_name} has a view count of: {user.view_count}")


if __name__ == '__main__':
    pass