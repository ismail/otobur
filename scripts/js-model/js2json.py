#!/usr/bin/env python

from subprocess import check_output
from schedule_pb2 import Schedule, Line, Location
import json

linesURL="http://www.bursa.bel.tr/mobil/json.php?islem=hatlar"
stopsURL="http://www.bursa.bel.tr/mobil/json.php?islem=hat_durak&hat="
hoursURL="http://www.bursa.bel.tr/mobil/json.php?islem=durak_saatler&durak=%s&hat=%s"
# BuKART: http://www.bursa.bel.tr/mobil/json.php?islem=bukart&lat=28.993744&long=40.208102
# DURAKLAR: http://www.bursa.bel.tr/mobil/json.php?islem=durak_ara&ara=


def parseLines():
    data = check_output(["./jsonify.sh", linesURL])
    data = json.loads(data)
    schedule = Schedule()

    for d in data:
        line = schedule.lines.add()
        line.name = d["g_adi"].encode("utf-8")
        line.id = d["g_id"]

        startLoc = Location()
        startLoc.stopName = d["kalkis_yeri"]["Durak"]
        startLoc.cadde = d["kalkis_yeri"]["Cadde"]
        startLoc.mahalle = d["kalkis_yeri"]["Mahalle"]

        endLoc = Location()
        endLoc.stopName = d["varis_yeri"]["Durak"]
        endLoc.cadde = d["varis_yeri"]["Cadde"]
        endLoc.mahalle = d["varis_yeri"]["Mahalle"]

        line.start = startLoc
        line.end = endLoc

        parseStops(line)

def parseStops(line):
    print("## %s" % line.name)

    data = check_output(["./jsonify.sh", "%s%s" % (stopsURL, lineName)])
    data = json.loads(data)
    for d in data:
        stopName = d["DurakAdi"]
        stopCode = d["DurakKodu"]
        stopName = stopName.encode("utf-8")
        stopCode = stopCode.encode("utf-8")
        if stopName.strip():
            stop = line.stops.add()
            stop.direction = d["Yon"]
            stop.code = stopCode
            stop.name = stopName

            loc = Location()
            loc.stopName = stopName
            loc.mahalle = d["Mahalle"]
            loc.cadde = d["Cadde"]
            stop.location = loc

            stop.longitude = d["Long"]
            stop.latitude = d["Lat"]

            parseHours(stop, line.name)

def parseHours(stop, lineName):
    print("\t--> %s" % stop.name)
    data = check_output(["./jsonify.sh", hoursURL % (stop.code, lineName)])
    data = json.loads(data)

    for d in data:


if __name__ == "__main__":
    parseLines()
