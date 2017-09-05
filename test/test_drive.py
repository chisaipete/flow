#!/usr/bin/env python
from notes import google_drive
import unittest

class TestDrive(unittest.TestCase):
    def test_credential_import(self):
        d = google_drive.Drive()
