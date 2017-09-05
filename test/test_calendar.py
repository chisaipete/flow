#!/usr/bin/env python
from planner import google_calendar
import unittest

class TestCalendar(unittest.TestCase):
    def test_credential_import(self):
        c = google_calendar.Calendar()
