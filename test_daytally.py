import unittest

from analyze import Node
from analyze import TTally
from analyze import DayTally
from analyze import DAY_BEGIN

from datetime import date
from datetime import datetime
from datetime import time

class TestDayTally(unittest.TestCase):
    a_date = date(2010, 4, 10)
    tt_day_begin = TTally(DAY_BEGIN)
    first_begin = datetime.combine(a_date, time(12, 15))
    first_end = datetime.combine(a_date, time(13, 30))

    @classmethod
    def _ttally_of(cls, dt, tally=0):
        return TTally(dt.time(), tally)

    def assertSameTallies(self, actual, expected):
        output = "Different tally lists\n"
        all_same = True

        while actual or expected:
            a_item = None
            e_item = None

            if actual:
                a_item = actual.get()
            if expected:
                e_item = expected.get()

            if a_item and e_item:
                have_both = True
                same = a_item == e_item
                all_same = all_same and same
            else:
                all_same = False

            output += "{:3}{:15}{:15}\n".format(
                    "!!" if have_both and not same else "",
                    a_item if a_item else "",
                    e_item if e_item else "")

            if actual:
                actual = actual.next()

            if expected:
                expected = expected.next()

        self.assertTrue(all_same, output)
                
    def test_new(self):
        a = DayTally(self.a_date)
        self.assertEqual(a.date(), self.a_date)

        expected = Node.list_of(self.tt_day_begin)

        self.assertSameTallies(a.get_tallies(), expected)


    def test_add_first(self):
        a = DayTally(self.a_date)

        a.add(self.first_begin, self.first_end)

        expected = Node.list_of(self.tt_day_begin,
                self._ttally_of(self.first_begin, 1),
                self._ttally_of(self.first_end))

        self.assertSameTallies(a.get_tallies(), expected)

    def test_add_left(self):
        a = DayTally(self.a_date)

        second_begin = datetime.combine(self.a_date, time(10, 0))
        second_end = datetime.combine(self.a_date, time(11, 45))

        a.add(self.first_begin, self.first_end)
        a.add(second_begin, second_end)

        expected = Node.list_of(self.tt_day_begin,
                self._ttally_of(second_begin, 1),
                self._ttally_of(second_end),
                self._ttally_of(self.first_begin, 1),
                self._ttally_of(self.first_end))

        self.assertSameTallies(a.get_tallies(), expected)

    def test_add_right(self):
        a = DayTally(self.a_date)

        second_begin = datetime.combine(self.a_date, time(14, 0))
        second_end = datetime.combine(self.a_date, time(15, 45))

        a.add(self.first_begin, self.first_end)
        a.add(second_begin, second_end)

        expected = Node.list_of(self.tt_day_begin,
                self._ttally_of(self.first_begin, 1),
                self._ttally_of(self.first_end),
                self._ttally_of(second_begin, 1),
                self._ttally_of(second_end))

        self.assertSameTallies(a.get_tallies(), expected)

    def test_add_left_overlap(self):
        a = DayTally(self.a_date)

        second_begin = datetime.combine(self.a_date, time(10, 0))
        second_end = datetime.combine(self.a_date, time(12, 45))

        a.add(self.first_begin, self.first_end)
        a.add(second_begin, second_end)

        expected = Node.list_of(self.tt_day_begin,
                self._ttally_of(second_begin, 1),
                self._ttally_of(self.first_begin, 2),
                self._ttally_of(second_end, 1),
                self._ttally_of(self.first_end))

        self.assertSameTallies(a.get_tallies(), expected)

    def test_add_right_overlap(self):
        a = DayTally(self.a_date)

        second_begin = datetime.combine(self.a_date, time(12, 45))
        second_end = datetime.combine(self.a_date, time(14, 0))

        a.add(self.first_begin, self.first_end)
        a.add(second_begin, second_end)

        expected = Node.list_of(self.tt_day_begin,
                self._ttally_of(self.first_begin, 1),
                self._ttally_of(second_begin, 2),
                self._ttally_of(self.first_end, 1),
                self._ttally_of(second_end))

        self.assertSameTallies(a.get_tallies(), expected)

    def test_add_both_overlap(self):
        a = DayTally(self.a_date)

        second_begin = datetime.combine(self.a_date, time(10, 00))
        second_end = datetime.combine(self.a_date, time(14, 0))

        a.add(self.first_begin, self.first_end)
        a.add(second_begin, second_end)

        expected = Node.list_of(self.tt_day_begin,
                self._ttally_of(second_begin, 1),
                self._ttally_of(self.first_begin, 2),
                self._ttally_of(self.first_end, 1),
                self._ttally_of(second_end))

        self.assertSameTallies(a.get_tallies(), expected)

    def test_add_left_same(self):
        a = DayTally(self.a_date)

        second_end = datetime.combine(self.a_date, time(14, 0))

        a.add(self.first_begin, self.first_end)
        a.add(self.first_begin, second_end)

        expected = Node.list_of(self.tt_day_begin,
                self._ttally_of(self.first_begin, 2),
                self._ttally_of(self.first_end, 1),
                self._ttally_of(second_end))

        self.assertSameTallies(a.get_tallies(), expected)

    def test_add_right_same(self):
        a = DayTally(self.a_date)

        second_begin = datetime.combine(self.a_date, time(12, 30))

        a.add(self.first_begin, self.first_end)
        a.add(second_begin, self.first_end)

        expected = Node.list_of(self.tt_day_begin,
                self._ttally_of(self.first_begin, 1),
                self._ttally_of(second_begin, 2),
                self._ttally_of(self.first_end, 0))

        self.assertSameTallies(a.get_tallies(), expected)

    def test_add_both_same(self):
        a = DayTally(self.a_date)

        a.add(self.first_begin, self.first_end)
        a.add(self.first_begin, self.first_end)

        expected = Node.list_of(self.tt_day_begin,
            self._ttally_of(self.first_begin, 2),
            self._ttally_of(self.first_end))

        self.assertSameTallies(a.get_tallies(), expected)

    def test_add_several(self):
        a = DayTally(self.a_date)

        second_begin = datetime.combine(self.a_date, time(10, 0))
        second_end = datetime.combine(self.a_date, time(11, 45))

        third_begin = datetime.combine(self.a_date, time(12, 45))
        third_end = datetime.combine(self.a_date, time(14, 0))

        fourth_begin = datetime.combine(self.a_date, time(10, 00))
        fourth_end = datetime.combine(self.a_date, time(14, 0))

        a.add(self.first_begin, self.first_end)
        a.add(second_begin, second_end)
        a.add(third_begin, third_end)
        a.add(fourth_begin, fourth_end)

        expected = Node.list_of(self.tt_day_begin,
            self._ttally_of(second_begin, 2),
            self._ttally_of(second_end, 1),
            self._ttally_of(self.first_begin, 2),
            self._ttally_of(third_begin, 3),
            self._ttally_of(self.first_end, 2),
            self._ttally_of(third_end, 0))

        self.assertSameTallies(a.get_tallies(), expected)




