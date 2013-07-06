#!/usr/bin/env python

from subprocess import Popen, PIPE
import json

linesURL="http://www.bursa.bel.tr/mobil/json.php?islem=hatlar"

def parseLines():
    proc = Popen(["./jsonify.sh %s" % linesURL], stdout=PIPE)
    json = proc.communicate()[0]
    print(json)

if __name__ == "__main__":
    parseLines()


