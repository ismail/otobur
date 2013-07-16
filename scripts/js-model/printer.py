#!/usr/bin/env python

import otobur_pb2
import sys

if __name__ == "__main__":
    schedule = otobur_pb2.Schedule()

    if sys.argv[1] == "-":
        schedule.ParseFromString(sys.stdin.read())
    else:
        schedule.ParseFromString(open(sys.argv[1],"rb").read())

    for line in schedule.lines:
        print("++ %s" % line.name.encode("utf-8"))
        print("\tID: %s" % line.id.encode("utf-8"))
        print("\tStart:")
        print("\t\tStop Name: %s" % line.start.stopName.encode("utf-8"))
        print("\t\tMahalle: %s" % line.start.mahalle.encode("utf-8"))
        print("\t\tCadde: %s" % line.start.cadde.encode("utf-8"))
        print("\tEnd:")
        print("\t\tStop Name: %s" % line.end.stopName.encode("utf-8"))
        print("\t\tMahalle: %s" % line.end.mahalle.encode("utf-8"))
        print("\t\tCadde: %s" % line.end.cadde.encode("utf-8"))

        for stop in line.stops:
            print("\t+ %s" % stop.name.encode("utf-8"))
            print("\t\tDirection: %s" % stop.direction)
            print("\t\tCode: %s" % stop.code)
            print("\t\tStop Name: %s" % stop.location.stopName.encode("utf-8"))
            print("\t\tMahalle: %s" % stop.location.mahalle.encode("utf-8"))
            print("\t\tCadde: %s" % stop.location.cadde.encode("utf-8"))
            print("\t\tLatitude: %s" % stop.latitude)
            print("\t\tLongitude: %s" % stop.longitude)
            print("\t\tOrder: %s" % stop.order)
            print("\t\tTimeLine:")
            for t in stop.timeLine.time:
                print("\t\tDay: %s" % t.day.encode("utf-8"))
                print("\t\tHours: %s" % t.hours)



