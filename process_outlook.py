#!/usr/bin/env python
import os

from inbox import outlook
from tasks import todotxt
from notes import dropbox

todotxt_path = os.path.join(dropbox.get_dropbox_path(), '@Todo', 'todo.txt')

r = input('Have you moved all interesting mails to "Action Support"? [y] ')

if not r.strip().lower() or r.strip().lower()[0] == 'y':
    print('Processing Outlook emails...')
    m = outlook.Mailbox()
    with todotxt.TodoTxt(todotxt_path) as t:
        for msg in m.process_action_support():
            # msg = (subject, snippet, date, perma_link, item)
            # check if ref is present in any existing tasks
            referenced_task = t.check_for_ref_in_tasks(msg[3])
            # if task is not present in list, prompt
            if not isinstance(referenced_task,int):
                print()
                print('Date: {}'.format(msg[2]))
                print('Subject: {}'.format(msg[0]))
                print('Snippet: {}...'.format(msg[1]))
                # if NOT, process it
                r = input('Do you want to add a task for this email? [y] ')
                if not r.strip().lower() or r.strip().lower()[0] == 'y':
                    t.add_task_with_unique_ref(msg[3])
                elif r.strip().lower()[0] == 'q':
                    break
                else:
                    r = input('Should we move this email to the archive then? [n] ')
                    if r.strip().lower()[0] == 'y':
                        m.archive_message(msg[4])
            else:
                # if it is present, echo as such and return
                print('Email is already referenced in {}'.format(t.tasks[referenced_task]))
        print()
        print(t)

    print('Reviewing Outlook links to check if resolved...')
else:
    print('Processing aborted.')
