#!/usr/bin/env python
import os, sys, re, datetime

start_completion = re.compile(r'^(x )\w')
start_priority = re.compile(r'^(\([A-Z]\) )\w')
creation_date_after_prio = re.compile(r'^\([A-Z]\) (\d{4}-\d{2}-\d{2}) \D')
creation_date_no_prio = re.compile(r'^(\d{4}-\d{2}-\d{2}) \D')

prefix_match = re.compile(r'^(x )?(\([A-Z]\) )?(\d{4}-\d{2}-\d{2} )?(\d{4}-\d{2}-\d{2} )?(.+)$')
CHECK = 0
PRIOR = 1
DATE1 = 2
DATE2 = 3
DESCR = 4

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

    def decode_description(self, description):
        self.set_description(description)
        split_desc = description.split()
        for token in split_desc:
            if token.startswith('@'):
                self.context_tags.append(token.split('@')[1])
            elif token.startswith('+'):
                self.project_tags.append(token.split('+')[1])
            elif ':' in token and token.count(':') == 1:
                self.special_tags.append(tuple(token.split(':')))

    def mark_complete(self, unmark=False, set_date=False, force_date=None):
        if unmark:
            self.completion = False
            self.completion_date = None
        else:
            self.completion = True
            if set_date:
                self.set_date(datetime.datetime.now().date(), complete=True)
            elif force_date:
                self.set_date(force_date, complete=True)

    def parse_line(self, taskline):
        current_line = taskline
        # print('\n{}'.format(current_line))
        task_found = prefix_match.search(current_line).groups()
        # print(task_found)
        if task_found[CHECK]:
            self.mark_complete()
        if task_found[PRIOR]:
            self.set_priority(priority=task_found[PRIOR][1])
        if task_found[DATE1] and not task_found[DATE2]: # single date
            if task_found[CHECK]: # completed, therefore it must be the completion date
                self.mark_complete(force_date=task_found[DATE1].strip())
            else:
                self.set_date(task_found[DATE1].strip())
        elif task_found[DATE1] and task_found[DATE2]:
            self.mark_complete(force_date=task_found[DATE1].strip())
            self.set_date(task_found[DATE2].strip())
        if task_found[DESCR]:
            self.decode_description(task_found[DESCR])

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


# class TodoTxt():
#     def __init__(self, path=None):
#         self.path = path
#         if path:
#             self.parse()

#     def parse(self):
#         if os.path.exists(self.path):
#             with open(self.path,'r') as todotxt_fh:
#                 contents = todotxt_fh.read()

#         print(contents)

