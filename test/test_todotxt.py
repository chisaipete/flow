#!/usr/bin/env python

from tasks import todotxt
import unittest, datetime

class TestTasks(unittest.TestCase):
    def test_date(self):
        t = todotxt.Task()
        t.add_date('2017-01-30')
        self.assertEqual(str(t), '2017-01-30')

    def test_completion(self):
        t = todotxt.Task()
        t.mark_complete()
        self.assertEqual(str(t), 'x {}'.format(datetime.datetime.now().date()))

    def test_completion_with_date(self):
        t = todotxt.Task()
        t.add_date('2017-02-02')
        t.mark_complete()
        self.assertEqual(str(t), 'x {} {}'.format(datetime.datetime.now().date(), '2017-02-02'))
        t.mark_complete(unmark=True)
        self.assertEqual(str(t), '2017-02-02')

    
