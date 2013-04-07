#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Placed under public domain.
# 2013 İsmail Dönmez <ismail@donmez.ws>

from collections import OrderedDict
import json
from lxml import html
import urllib2
import re
import sys
import time

address="http://www.burulas.com.tr/sayfa.aspx?id=393"
base_url="http://www.burulas.com.tr"
clockDict = OrderedDict()
timeTableDict = OrderedDict()
blacklistedLines = ["35/C", "38/B", "38/D"]

def compareTime(t1, t2):
    # Sanitize this shit, we only need first 5 characters XX:YY
    t1 = "".join(list(t1)[:5]).replace(".",":")
    t2 = "".join(list(t2)[:5]).replace(".",":")

    h,m = t1.split(":")
    vt1 = int(h)*60 + int(m)

    h,m = t2.split(":")
    vt2 = int(h)*60 + int(m)

    return (vt1 > vt2)

def splitTimeTable(hours):
    timeTable = [[hours[0]]]

    prevHour = hours[0]
    for currentHour in hours[1:]:
        if compareTime(prevHour, currentHour):
            timeTable.append([])

        timeTable[len(timeTable)-1].append(currentHour)
        prevHour = currentHour

    return timeTable

def parseHourList(content):
    l = list(content)
    hours = []

    index = 0
    for character in l:
        if character.isspace():
            continue

        try:
            if len(hours[index]) >= 5:
                if character.isdigit():
                    index += 1
            hours[index] += character
        except IndexError:
            hours.append(character)

    return hours

def parseTable(table):
    parsedDescription = False
    description = []

    for row in table.xpath("//tbody/tr"):
        content = row.text_content().strip()
        if not parsedDescription:
            content = content.encode("utf-8")
            description = re.sub("\d\d:\d\d.*", "", content)
            #print description
            parsedDescription = True

        if re.match("\d\d:\d\d", content):
            timeTable = parseHourList(content)
            return splitTimeTable(timeTable)


def parsePage(doc):
    tableList = doc.xpath("/html//table")

    for table in tableList:
        try:
            for key in table.attrib['style'].split(";"):
                if key.find("width") >= 0:
                    width = key.split(":")[1].strip().rstrip("px;")
                    if width.find("%") < 0:
                        return parseTable(table)
        except KeyError:
            pass

def setupBus():
    tree = html.fromstring(urllib2.urlopen(address).read())
    for td in tree.xpath('/html/body//tbody/tr/td/a'):
        try:
            if "Hareket Saatleri" in td.attrib['title']:
                line_name = td.attrib['title'].split(" ")[0]
                clockDict[line_name] = "%s/%s" % (base_url, td.attrib['href'])
        except KeyError:
            pass

def setupTimeline():
    for key in clockDict.keys():
        if key in blacklistedLines:
            continue

        url = clockDict[key]
        #print url
        doc = html.fromstring(urllib2.urlopen(url).read())

        if not key in timeTableDict.keys():
            timeTableDict[key] = {}
            timeTableDict[key]["url"] = None
            timeTableDict[key]["hours"] = None

        timeTableDict[key]["url"] = url
        timeTableDict[key]["hours"] = parsePage(doc)
        time.sleep(0.1)

if __name__ == "__main__":
    setupBus()
    setupTimeline()
    print json.dumps(timeTableDict, sort_keys=True,
                                    indent=4, separators=(',', ': '))
