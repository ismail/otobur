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
        parseStops(lineName)

def parseStops(lineName):
    print("## %s" % lineName)

    data = check_output(["./jsonify.sh", "%s%s" % (stopsURL, lineName)])
    data = json.loads(data)
    for d in data:
        stopName = d["DurakAdi"]
        stopCode = d["DurakKodu"]
        stopName = stopName.encode("utf-8")
        stopCode = stopCode.encode("utf-8")
        if stopName.strip():
            parseHours(scheduleDict, lineName, stopCode, stopName)

    return scheduleDict

def parseHours(scheduleDict, lineName, stopCode, stopName):
    scheduleDict[lineName][stopName] = {}
    print("\t--> %s" % stopName)
    data = check_output(["./jsonify.sh", hoursURL % (stopCode, lineName)])
    data = json.loads(data)

    for d in data:
        try:
            scheduleDict[lineName][stopName][d["kisagun"]]
        except KeyError:
            scheduleDict[lineName][stopName][d["kisagun"]] = []
        finally:
            scheduleDict[lineName][stopName][d["kisagun"]].append(d["dakika"])

if __name__ == "__main__":
    parseLines()

    with open("schedule_v2.json", "wb") as fp:
        fp.write(json.dumps(final_schedule, sort_keys=False,
                            indent=4, separators=(',', ': ')))

