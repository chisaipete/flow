#!/usr/bin/env python
from inbox import pocket
import unittest

class TestPocket(unittest.TestCase):
    def test_credential_import(self):
        p = pocket.Pocket()
        