#!/usr/bin/env python
import os

from inbox import gmail
from tasks import todotxt
from notes import dropbox

todotxt_path = os.path.join(dropbox.get_dropbox_path(), '@Todo', 'todo.txt')

r = input('Have you moved all interesting mails to "Action Support"? [y] ')

if not r.strip().lower() or r.strip().lower()[0] == 'y':
    print('Processing emails...')
    m = gmail.Mailbox()
    with todotxt.TodoTxt(todotxt_path) as t:
        for permalink in m.process_action_support():
            print()
            r = input('Do you want to add a task for this email? [y] ')
            if not r.strip().lower() or r.strip().lower()[0] == 'y':
                t.add_linked_task(permalink)
            else:
                r = input('Should we mark this email as done then? [n] ')
                if not r.strip().lower() or r.strip().lower()[0] == 'y':
                    pass
            print()
        print(t)
    print('Reviewing Gmail links to check if resolved...')
else:
    print('Processing aborted.')
