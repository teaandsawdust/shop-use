#!/usr/bin/python

from __future__ import print_function

import csv
import sys

from datetime import datetime
from datetime import timedelta

GUESS_DURATION = timedelta(hours=2)

class NoTimesException(Exception):
    pass

def asdate(noniso):
    return datetime.strptime(noniso.strip(), "%m.%d.%y").date()

def asdatetime(d, timestamp):
    if not timestamp:
        return None

    t = datetime.strptime(timestamp.strip(), "%H:%M").time()
    return datetime.combine(d, t)

def begin_end(row):
    return row[2], row[3]

def normalize(row):
    begin, end = begin_end(row)

    if not(begin or end):
        raise NoTimesException

    if begin and end:
        pass
    elif begin:
        end = begin + GUESS_DURATION
        if end.date() > begin.date():
            end = datetime.combine(begin.date(), DAY_END)
    else:
        begin = end - GUESS_DURATION
        if begin.date() < end.date():
            begin = datetime.combine(end.date(), DAY_BEGIN)

    return begin, end

def validate(row):
    begin, end = begin_end(row)

    assert begin and end, "begin = {}, end = {}".format(begin, end)

    assert begin <= end, "{} Begin time {} is after end time {}".format(
                begin.date(), begin.time(), end.time())

def process(filename):
    result = True
    with open(filename, 'r') as csvfile:
        has_header = csv.Sniffer().has_header(csvfile.read(1024))
        csvfile.seek(0)
        csvreader = csv.reader(csvfile)
        csvwriter = csv.writer(sys.stdout)

        if has_header:
            next(csvreader)

        for row in csvreader:
            d = asdate(row[1])
            row[1] = str(d)
            row[2] = asdatetime(d, row[2])
            row[3] = asdatetime(d, row[3])

            try:
                row[2], row[3] = normalize(row)
                validate(row)
            except NoTimesException as e:
                print("WARNING {}:{} {} No begin or end time - skipped" \
                        .format(filename, csvreader.line_num, d),
                        file=sys.stderr)
            except AssertionError as e:
                print("ERROR {}:{} {}".format(
                        filename, csvreader.line_num, e), file=sys.stderr)
                result = False

            csvwriter.writerow(row)
    return result

def main():
    result = True
    for filename in sys.argv[1:]:
        result = result and process(filename)

    return 0 if result else 1

exit(main())
