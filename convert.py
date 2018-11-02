#!/usr/bin/python

import csv
import sys

from datetime import datetime

def asdate(noniso):
    return datetime.strptime(noniso.strip(), "%m.%d.%y").date()

def asdatetime(d, timestamp):
    if not timestamp:
        return None

    t = datetime.strptime(timestamp.strip(), "%H:%M").time()
    return datetime.combine(d, t)

def process(filename):
    with open(filename, 'rb') as csvfile:
        has_header = csv.Sniffer().has_header(csvfile.read(1024))
        csvfile.seek(0)
        csvreader = csv.reader(csvfile)
        csvwriter = csv.writer(sys.stdout)

        if has_header:
            csvreader.next()

        for row in csvreader:
            d = asdate(row[1])
            row[1] = str(d)
            row[2] = asdatetime(d, row[2])
            row[3] = asdatetime(d, row[3])
            csvwriter.writerow(row)

def main():
    for filename in sys.argv[1:]:
        process(filename)

main()
