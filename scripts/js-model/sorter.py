#!/usr/bin/env python

import otobur_pb2
import re
import sys

# Regular expression to match a consecutive run of digits.
integer_pattern = re.compile('([0-9]+)')

def compare_lines(x, y):
    val_x = [coerce(c) for c in integer_pattern.split(x) if c != '']
    val_y = [coerce(c) for c in integer_pattern.split(y) if c != '']

    return cmp(val_x, val_y)

def compare_stops(x, y):
    direction_x = x.direction
    direction_y = y.direction
    order_x = x.order
    order_y = y.order

    if direction_x == direction_y:
        return order_x - order_y
    elif direction_x < direction_y:
        return -1
    else:
        return 1

def coerce(s):
    if s.isdigit():
        return int(s)
    else:
        return s

def copy_line(line, new_line):
    new_line.name = line.name
    new_line.id = line.id

    copy_location(line.start, new_line.start)
    copy_location(line.end, new_line.end)

    for stop in sorted(line.stops, cmp=compare_stops):
        new_stop = new_line.stops.add()
        copy_stop(stop, new_stop)

def copy_stop(stop, new_stop):
    new_stop.direction = stop.direction
    new_stop.code = stop.code
    new_stop.name = stop.name
    copy_location(stop.location, new_stop.location)
    new_stop.latitude = stop.latitude
    new_stop.longitude = stop.longitude
    new_stop.order = stop.order
    copy_timeline(stop.timeLine, new_stop.timeLine)

def copy_location(loc, new_loc):
    new_loc.stopName = loc.stopName
    new_loc.mahalle = loc.mahalle
    new_loc.cadde = loc.cadde

def copy_timeline(old_timeline, new_timeline):
    for t in old_timeline.time:
        time = new_timeline.time.add()
        time.day = t.day
        time.hours = t.hours

if __name__ == "__main__":
    schedule = otobur_pb2.Schedule()
    new_schedule = otobur_pb2.Schedule()

    schedule.ParseFromString(open(sys.argv[1],"rb").read())
    for line in sorted(schedule.lines, key=lambda line: line.name, cmp=compare_lines):
        new_line = new_schedule.lines.add()
        copy_line(line, new_line)

    with open("sorted.data", "wb") as fp:
        fp.write(new_schedule.SerializeToString())
