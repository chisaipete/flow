#!/usr/bin/env python
import os, sys, re, datetime, hashlib

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


# class LinkMap():
#     def __init__(self, path=None):
#         self.path = path
#         self.links = {}
#         if path:
#             if os.path.exists(self.path):
#                 with open(self.path,'r') as linkmap_fh:
#                     self.contents = list(filter(None, linkmap_fh.read().split('\n')))
#         if self.contents:
#             self.parse()

#     def parse(self):
#         for line in self.contents:
#             link_hash, link_full = line.split(' ',1)
#             self.links[link_hash] = link_full

#     def generate_link_hash(self, link_string):
#         link_hash = None
#         # generate hash
#         while not link_hash:
#             md5 = hashlib.md5()
#             md5.update(link_string.encode('utf-8'))
#             link_hash = str(md5.hexdigest())[0:6]
#             # check that it doesn't collide with existing hashes
#             if link_hash in self.links:
#                 # if it does, mangle the string and try again
#                 link_string = link_string + 'MANGLED'
#                 link_hash = None       
#         return link_hash

#     def add_link(self, link_full):
#         self.links[self.generate_link_hash(link_full)] = link_full

#     def check_for_link(self, link_full):
#         try:
#             link_hash_index = list(self.links.values()).index(link_full)
#         except ValueError:
#             link_hash_index = None

#         if isinstance(link_hash_index, int):
#             return list(self.links.keys())[link_hash_index]
#         else:
#             return None

#     def __enter__(self):
#         return self

#     def __exit__(self, exc_type, exc_value, traceback):
#         if os.path.exists(self.path):
#             with open(self.path,'w') as fh:
#                 fh.write(self.__str__())

#     def __str__(self):
#         out_string = ''
#         for link in self.links:
#             out_string += ' '.join([link, self.links[link]]) + '\n'
#         return out_string



class TodoTxt():
    def __init__(self, path=None, string=None):
        self.path = path
#       self.link_map = None
        self.tasks = []
        if string:
            self.contents = list(filter(None, string.split('\n')))
        elif path:
            if os.path.exists(self.path):
                with open(self.path,'r') as todotxt_fh:
                    self.contents = list(filter(None, todotxt_fh.read().split('\n')))
        if self.contents:
            self.parse()

    def parse(self):
        for line in self.contents:
            self.add_task(line)

    def check_for_ref_in_tasks(self, ref):
        for task in tasks:
            if ref in str(task):
                return tasks.index(task)
        return None

    def add_task_with_unique_ref(self, ref, date=None):
        task_line = input('Task to add with reference: ')
        task_line = ' '.join([task_line,ref])
        t = Task(task_line)
        if not date:
            t.set_date(datetime.datetime.now().date())
        else:
            t.set_date(date)
        self.add_task(task_obj=t)

#   def add_linked_task(self, link, force=False):
#       if not self.link_map:
#           # check if link.map exists next to todo.txt
#           link_map_path = os.path.join(os.path.dirname(self.path),'link.map')
#           # if not, create it
#           if not os.path.exists(link_map_path):
#               open(link_map_path,'a').close()
#           # open link map file
#           self.link_map = LinkMap(link_map_path)
#       # check if link is already associated with a task, if so, prompt to continue
#       existing_link = self.link_map.check_for_link(link)
#       if existing_link:
#           print('You are hosed')
#       # prompt for task text      
#       task_line = input('Task to add with link: ')
#       # if not, add a new task, with current date, that has the link:hash tag
#       self.link_map.add_link(link)
#       link_hash = self.link_map.check_for_link(link)
#       task_line = ' '.join([task_line,':'.join(['link',link_hash])])
#       t = Task(task_line)
#       t.set_date(datetime.datetime.now().date())
#       self.add_task(task_obj=t)

    def add_task(self, task_text=None, task_obj=None):
        if task_text:
            self.tasks.append(Task(task_text))
        if task_obj:
            self.tasks.append(task_obj)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
#       if self.link_map:
#           self.link_map.__exit__(None,None,None)
        if os.path.exists(self.path):
            with open(self.path,'w') as fh:
                fh.write(self.__str__())

    def __str__(self):
        out_string = ''
        for task in self.tasks:
            out_string += str(task) + '\n'
        return out_string


#TODO: add link support for photos, outlook items, etc.
# import webbrowser
# webbrowser.open(link)

#link:8_character_hash  -> 8_character_hash in link file which resolves to actual link
