#!/usr/bin/env python
from notes import dropbox
import unittest

class TestDropbox(unittest.TestCase):
    def test_credential_import(self):
        d = dropbox.Dropbox()