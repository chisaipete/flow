#!/usr/bin/env python
from inbox import gmail
import unittest

class TestGmail(unittest.TestCase):
    def test_credential_import(self):
        m = gmail.Mailbox()
