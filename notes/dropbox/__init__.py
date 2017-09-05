#!/usr/bin/env python
import os, sys
## hack for credentials directory
if __name__ == '__main__' and __package__ is None: # pragma: no cover
    path_base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.append(path_base)
## hack for credentials directory
credential_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'credentials')

import dropbox
from credentials import read_credentials

class Dropbox():
    def __init__(self):
        self.main()

    def main(self):
        cred = read_credentials('dropbox')
        dbx = dropbox.Dropbox(cred['dropbox']['access_token'])
        
        dbx.users_get_current_account()

        # for entry in dbx.files_list_folder('').entries:
        #     print(entry.name)

