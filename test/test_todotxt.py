#!/usr/bin/env python

from tasks import todotxt
import unittest, datetime

class TestTasks(unittest.TestCase):
    def test_date(self):
        t = todotxt.Task()
        t.set_date('2017-01-30')
        self.assertEqual(str(t), '2017-01-30')

    def test_completion(self):
        t = todotxt.Task()
        t.mark_complete(set_date=True)
        self.assertEqual(str(t), 'x {}'.format(datetime.datetime.now().date()))

    def test_completion_with_date(self):
        t = todotxt.Task()
        t.set_date('2017-02-02')
        t.mark_complete(set_date=True)
        self.assertEqual(str(t), 'x {} {}'.format(datetime.datetime.now().date(), '2017-02-02'))
        t.mark_complete(unmark=True)
        self.assertEqual(str(t), '2017-02-02')

    def test_priority(self):
        t = todotxt.Task()
        t.set_priority()
        self.assertEqual(str(t), '(A)')
        t.increase_priority()
        self.assertEqual(str(t), '(A)')
        t.decrease_priority()
        t.decrease_priority()
        self.assertEqual(str(t), '(C)')
        t.increase_priority()
        self.assertEqual(str(t), '(B)')
        t.set_priority('Z')
        self.assertEqual(str(t), '(Z)')
        t.decrease_priority()
        self.assertEqual(str(t), '(Z)')

# Incomplete Tasks: 3 Format Rules
# Rule 1: If priority exists, it ALWAYS appears first.
    def test_priority_parsing(self):
        priority = '(A) Call Mom'
        no_priorities = [
            'Really gotta call Mom (A) @phone @someday',
            '(b) Get back to the boss',
            '(B)->Submit TPS report',
            ]
        t = todotxt.Task(priority)
        self.assertEqual(t.priority, 'A')
        for e in no_priorities:
            t = todotxt.Task(e)
            self.assertEqual(t.priority, None)

# Rule 2: A task's creation date may optionally appear directly after priority and a space.
    def test_creation_date_parsing(self):
        creation_dates = [
            '2011-03-02 Document +TodoTxt task format',
            '(A) 2011-03-02 Call Mom',
            ]
        no_creation_date = '(A) Call Mom 2011-03-02'
        t = todotxt.Task(no_creation_date)
        self.assertEqual(t.creation_date, None)
        for e in creation_dates:
            t = todotxt.Task(e)
            self.assertEqual(str(t.creation_date), '2011-03-02')

# Rule 3: Contexts and Projects may appear anywhere in the line after priority/prepended date.
# A context is preceded by a single space and an at-sign (@).
# A project is preceded by a single space and a plus-sign (+).
# A project or context contains any non-whitespace character.
# A task may have zero, one, or more than one projects and contexts included in it.
    def test_context_and_project_parse(self):
        family_plah_projects_and_iphone_phone_contexts = '(A) Call Mom +Family +PeaceLoveAndHappiness @iphone @phone'
        no_contexts = 'Email SoAndSo at soandso@example.com'
        no_projects = 'Learn how to add 2+2'
        t = todotxt.Task(family_plah_projects_and_iphone_phone_contexts)
        self.assertListEqual(t.context_tags, ['iphone','phone'])
        self.assertListEqual(t.project_tags, ['Family','PeaceLoveAndHappiness'])
        t = todotxt.Task(no_contexts)
        self.assertEqual(t.context_tags, [])
        t = todotxt.Task(no_projects)
        self.assertEqual(t.project_tags, [])

# Complete Tasks: 2 Format Rules
# Rule 1: A completed task starts with an lowercase x character (x).
    def test_completed_task_parse(self):
        complete_task = 'x 2011-03-03 Call Mom'
        incomplete_tasks = [
            'xylophone lesson',
            'X 2012-01-01 Make resolutions',
            '(A) x Find ticket prices',
            ]
        t = todotxt.Task(complete_task)
        self.assertEqual(t.completion, True)
        for e in incomplete_tasks:
            t = todotxt.Task(e)
            self.assertEqual(t.completion, False)

# Rule 2: The date of completion appears directly after the x, separated by a space.
    def test_completed_date_parse(self):
        completed_date_after_created_date = "x 2011-03-02 2011-03-01 Review Tim's pull request +TodoTxtTouch @github"
        t = todotxt.Task(completed_date_after_created_date)
        self.assertEqual(t.completion, True)
        self.assertEqual(str(t)[0:2], 'x ')

#TODO: key value pair for keeping priority after completion, because discarded (pri:A)

# key value pair for settitng due date (due:2010-01-02)
    def test_due_date_special_parse(self):
        all_possibilities = "x (A) 2016-05-20 2016-04-30 measure space for +chapelShelving @chapel due:2016-05-30"
        t = todotxt.Task(all_possibilities)
        self.assertEqual(t.special_tags, [('due','2016-05-30')])