#!/usr/bin/env python
from collections import defaultdict
from subprocess import check_output
from otobur_pb2 import Schedule, Line, Location
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

        startLoc = line.start
        tmp = d["kalkis_yeri"].split(";")
        startLoc.stopName = tmp[0].split(": ")[1]
        startLoc.cadde = tmp[1].split(": ")[1]
        startLoc.mahalle = tmp[2].split(": ")[1]

        endLoc = line.end
        tmp = d["varis_yeri"].split(";")
        endLoc.stopName = tmp[0].split(": ")[1]
        endLoc.cadde = tmp[1].split(": ")[1]
        endLoc.mahalle = tmp[2].split(": ")[1]

        parseStops(line)

    with open("schedule.data", "wb") as fp:
        fp.write(schedule.SerializeToString())

def parseStops(line):
    print("## %s" % line.name)

    data = check_output(["./jsonify.sh", "%s%s" % (stopsURL, line.name)])
    data = json.loads(data)
    for d in data:
        stopName = unicode(d["DurakAdi"])
        stopCode = unicode(d["DurakKodu"])
        if stopName.strip():
            stop = line.stops.add()
            stop.direction = int(d["Yon"])
            stop.code = stopCode
            stop.name = stopName

            loc = stop.location
            loc.stopName = stopName
            loc.mahalle = d["Mahalle"]
            loc.cadde = d["Cadde"]

            stop.longitude = d["Long"]
            stop.latitude = d["Lat"]
            stop.order = int(d["Sira"])

            parseHours(stop, line.name)

def parseHours(stop, lineName):
    print("\t--> %s" % stop.name)
    data = check_output(["./jsonify.sh", hoursURL % (stop.code, lineName)])
    data = json.loads(data)

    hourDict = defaultdict(list)

    for d in data:
        hourDict[d["kisagun"]].append(d["dakika"])

    for d in hourDict.keys():
        timeLine = stop.timeLine
        time = timeLine.time.add()
        time.day = d
        time.hours= "|".join(hourDict[d])

if __name__ == "__main__":
    parseLines()
