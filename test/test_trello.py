#!python3
from projects import trello
import unittest

class TestTrello(unittest.TestCase):
    def test_credential_import(self):
        t = trello.Trello()
        