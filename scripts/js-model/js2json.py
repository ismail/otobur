#!/usr/bin/env python

from subprocess import check_output
import json

linesURL="http://www.bursa.bel.tr/mobil/json.php?islem=hatlar"
stopsURL="http://www.bursa.bel.tr/mobil/json.php?islem=hat_durak&hat="
hoursURL="http://www.bursa.bel.tr/mobil/json.php?islem=durak_saatler&durak=%s&hat=%s"

scheduleDict = {}

def parseLines():
    data = check_output(["./jsonify.sh", linesURL])
    data = json.loads(data)
    for d in data:
        lineName = d["g_adi"]
        scheduleDict[lineName] = {}
        print("### %s" % lineName)
        parseStops(lineName)

def parseStops(lineName):
    data = check_output(["./jsonify.sh", "%s%s" % (stopsURL, lineName)])
    data = json.loads(data)
    for d in data:
        stopName = d["DurakAdi"]
        stopCode = d["DurakKodu"]
        scheduleDict[lineName][stopName] = {}

        print("\t-> %s" % stopName)
        parseHours(lineName, stopCode, stopName)

def parseHours(lineName, stopCode, stopName):
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
