import unittest

from datetime import time
from analyze import TTally

class TestTTally(unittest.TestCase):
    def test_str(self):
        self.assertEqual("10:16:00 ->  1", str(TTally(time(10, 16), 1)))

    def test_eq(self):
        a = TTally(time(10, 16), 0)
        eq = TTally(time(10, 16))
        count = TTally(time(10, 16), 1)
        tm = TTally(time(22, 19))

        self.assertEqual(a, eq)
        self.assertEqual(a, eq)
        self.assertNotEqual(a, count)
        self.assertNotEqual(a, tm)
    
    def test_bump(self):
        a = TTally(time(22, 19))
        self.assertEqual(a.tally(), 0)
        a.bump()
        self.assertEqual(a.tally(), 1)
