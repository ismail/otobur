#!/usr/bin/env python

from subprocess import check_output
import json

linesURL="http://www.bursa.bel.tr/mobil/json.php?islem=hatlar"
stopsURL="http://www.bursa.bel.tr/mobil/json.php?islem=hat_durak&hat="
hoursURL="http://www.bursa.bel.tr/mobil/json.php?islem=durak_saatler&durak=%s&hat=%s"

def parseLines():
    data = check_output(["./jsonify.sh", linesURL])
    data = json.loads(data)
    for d in data:
        print("### %s" % d["g_adi"])
        parseStops(d["g_adi"])

def parseStops(line):
    data = check_output(["./jsonify.sh", "%s%s" % (stopsURL, line)])
    data = json.loads(data)
    for d in data:
        print("\t-> %s" % d["DurakAdi"])
        parseHours(line, d["DurakKodu"])

def parseHours(line, stop):
    data = check_output(["./jsonify.sh", hoursURL % (stop, line)])
    data = json.loads(data)
    for d in data:
        print("\t\t-> %s" % d)

if __name__ == "__main__":
    parseLines()


