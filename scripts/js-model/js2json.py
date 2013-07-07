#!/usr/bin/env python

from multiprocessing import Pool
from subprocess import check_output
import json

linesURL="http://www.bursa.bel.tr/mobil/json.php?islem=hatlar"
stopsURL="http://www.bursa.bel.tr/mobil/json.php?islem=hat_durak&hat="
hoursURL="http://www.bursa.bel.tr/mobil/json.php?islem=durak_saatler&durak=%s&hat=%s"
concurrentConnections = 16

def parseLines():
    data = check_output(["./jsonify.sh", linesURL])
    data = json.loads(data)
    lines = []
    for d in data:
        lineName = d["g_adi"]
        lineName = lineName.encode("utf-8")
        lines.append(lineName)

    p = Pool(concurrentConnections)
    p.map(parseStops, lines)

def parseStops(lineName):
    print("## %s" % lineName)
    scheduleDict = {}
    scheduleDict[lineName] = {}
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

def dumpJSON():
    print(json.dumps(scheduleDict, sort_keys=False,
                    indent=4, separators=(',', ': ')))

if __name__ == "__main__":
    parseLines()

    with open("schedule.json", "wb") as fp:
        fp.write(json.dumps(scheduleDict, sort_keys=False,
                            indent=4, separators=(',', ': ')))

