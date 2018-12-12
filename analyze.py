#!/usr/bin/python

import csv
import sys

from datetime import date
from datetime import datetime
from datetime import time

from json import dumps

DAY_BEGIN = time(00, 00, 00)
DAY_END = time(23, 59, 00)

class TTally:
    def __init__(self, tm, tally=0):
        assert isinstance(tm, time)
        self._time = tm
        self._tally = tally 

    @classmethod
    def tally_up(cls, dt, previous):
        return TTally(dt.time(), previous.tally() + 1)

    @classmethod
    def tally_down(cls, dt, previous):
        return TTally(dt.time(), previous.tally() - 1)

    def time(self):
        return self._time

    def tally(self):
        return self._tally

    def bump(self):
        self._tally += 1

    def is_before(self, dt):
        assert isinstance(dt, datetime)
        return self._time < dt.time()

    def is_after(self, dt):
        assert isinstance(dt, datetime)
        return self._time > dt.time()

    def same_time(self, dt):
        assert isinstance(dt, datetime)
        return self._time == dt.time()

    def __eq__(self, other):
        return self.time() == other.time() and self.tally() == other.tally()

    def __repr__(self):
        return "{} -> {:2d}".format(self.time(), self.tally())

    def __str__(self):
        return self.__repr__()

class Node:
    def __init__(self, data, next=None):
        self._data = data
        self._next = next

    def get(self):
        return self._data

    def next(self):
        return self._next

    def insert(self, data):
        noo = Node(data, self._next)
        self._next = noo

    def __repr__(self):
        p = self
        result = "{\n"
        while p:
            result += "\t{}\n".format(str(p.get()))
            p = p.next()
        result += "}\n"

        return result

    def __str__(self):
        return repr(self)

    @classmethod
    def list_of(cls, *args):
        if len(args) == 0:
            return None

        head = Node(args[0])
        p = head

        for arg in args[1:]:
            p.insert(arg)
            p = p.next()
        return head

    def as_list(self):
        result = []
        p = self

        while p:
            result.append(p.get())
            p = p.next()

        return result


class DayTally:
    def __init__(self, d):
        self._date = d
        self._tallies = Node(TTally(DAY_BEGIN))

    def add(self, begin, end):
        assert (self.date() == begin.date() and self.date() == end.date())
        assert begin.time() <= end.time()
        
        begun = False
        ended = False

        p = self._tallies

        while True:
            pi = p.get()

            # at end of list
            if not p.next():
                if not begun:
                    # gets bumped the next time through the loop if needed
                    p.insert(TTally(begin.time(), p.get().tally()))
                    begun = True
                    p = p.next()
                    continue
                if not ended:
                    ended = True

                    # p is pointing at a node with the same time as the end 
                    # time. Don't bump.
                    if pi.same_time(end):
                        break

                    pi.bump()
                    p.insert(TTally.tally_down(end, p.get()))

                    assert p.next().get().tally() == 0

                    break

            ni = p.next().get()

            if not begun:
                if ni.is_after(begin):
                    # start time is between p time and next time
                    # will bump on next iteration.
                    p.insert(TTally(begin.time(), pi.tally()))
                    begun = True
                if ni.same_time(begin):
                    begun = True
            elif not ended:
                pi.bump()
                if ni.is_after(end):
                    p.insert(TTally(end.time(), pi.tally() - 1))
                    ended = True
                    break
                if ni.same_time(end):
                    ended = True
                    break
            p = p.next();

        assert begun and ended, "Returning from add: begun {}, ended {}".format(begun, ended)
                    
    def get_tallies(self):
        return self._tallies

    def date(self):
        return self._date

def isoparse(string, sep=' '):
    if not string:
        return None
    return datetime.strptime(string, '%Y-%m-%d{}%H:%M:%S'.format(sep))

def getdate(begin, end):
    if begin:
        return begin.date()
    elif end:
        return end.date()
    else:
        return None

def analyze(filename):
    dailies = dict()
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)

        for row in csvreader:
            try:
                begin = isoparse(row[2])
                end = isoparse(row[3])

                d = getdate(begin, end)
                if not d:
                    continue

                k = str(d)

                dt = dailies.get(d, DayTally(d))
                dt.add(begin, end)
                dailies[k] = dt
            except Exception as e:
                print("Failed at record {}\n{}".format(
                    csvreader.line_num, row))
                raise e

    return dailies

def merge(into, sub):
    for date in sub:
        assert date not in into, "Not implemented yet"

        into[date] = sub[date]

def main():
    all_days = dict()

    for filename in sys.argv[1:]:
        dailies = analyze(filename)

        merge(all_days, dailies)

    print all_days

if __name__ == "__main__":
    main()
