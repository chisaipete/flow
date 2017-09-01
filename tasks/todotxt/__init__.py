#!/usr/bin/env python
import os, sys, datetime

class Task():
    def __init__(self, taskline=None):
        self.completion = False
        self.priority = None
        self.completion_date = None
        self.creation_date = None
        self.description = None
        self.project_tags = [] # +
        self.context_tags = [] # @
        self.special_tags = [] # ('key':'value')
        if taskline:
            self.parse_line(taskline)

    def set_date(self, date, complete=False):
        if isinstance(date, str):
            target_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        elif isinstance(date, datetime.date):
            target_date = date
        
        if complete:
            self.completion_date = target_date
        else:
            self.creation_date = target_date

    def set_description(self, description=None):
        if isinstance(description, str):
            self.description = description

    def set_priority(self, priority='A'):
        if priority.istitle():
            self.priority = priority

    def increase_priority(self):
        self.priority = chr(ord(self.priority) - 1)
        if ord(self.priority) < ord('A'):
            self.priority = 'A'

    def decrease_priority(self):
        self.priority = chr(ord(self.priority) + 1)
        if ord(self.priority) > ord('Z'):
            self.priority = 'Z'

    def decode_description(self):
        pass

    def mark_complete(self, unmark=False):
        if unmark:
            self.completion = False
            self.completion_date = None
        else:
            self.completion = True
            self.set_date(datetime.datetime.now().date(), complete=True)

    def __str__(self):
        out_list = []

        if self.completion: 
            out_list.append('x')
        if self.priority:           
            out_list.append('('+self.priority+')')
        if self.completion_date:    
            out_list.append(str(self.completion_date))
        if self.creation_date:      
            out_list.append(str(self.creation_date))
        if self.description:        
            out_list.append(self.description)

        return ' '.join(out_list)


class TodoTxt():
    def __init__(self, path=None):
        self.path = path
        if path:
            self.parse()

    def parse(self):
        if os.path.exists(self.path):
            with open(self.path,'r') as todotxt_fh:
                contents = todotxt_fh.read()

        print(contents)

