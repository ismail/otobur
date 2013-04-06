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
clock_dict = OrderedDict()
timeTableDict = {}

def compareTime(t1, t2):
    h,m = t1.split(" ")[0].split(":")
    vt1 = int(h)*60 + int(m)

    h,m = t2.split(" ")[0].split(":")
    vt2 = int(h)*60 + int(m)

    return (vt1 > vt2)

def splitTimeTable(hours):
    timeTable = [[]]

    prevHour = hours[0]
    for currentHour in hours[1:]:
        if compareTime(prevHour, currentHour):
            timeTable.append([])

        timeTable[len(timeTable)-1].append(currentHour)
        prevHour = currentHour

    return timeTable

def parseTable(table):
    for row in table.xpath("//tbody/tr"):
        content = row.text_content().strip()
        if re.match("\d\d:\d\d", content):
            content = content.encode("utf-8")
            content = content.replace("\xc2\xa0","")
            hours = content.replace("\t","").split("\r\n")
            timeTable = [hour.strip() for hour in hours if hour != '']
            return splitTimeTable(timeTable)
            break

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
                clock_dict[line_name] = "%s/%s" % (base_url, td.attrib['href'])
        except KeyError:
            pass

def setupTimeline():
    for key in clock_dict.keys():
        url = clock_dict[key]
        doc = html.fromstring(urllib2.urlopen(url).read())

        if not key in timeTableDict.keys():
            timeTableDict[key] = {}
            timeTableDict[key]["url"] = None
            timeTableDict[key]["hours"] = None

        timeTableDict[key]["url"] = url
        timeTableDict[key]["hours"] = parsePage(doc)
        print json.dumps(timeTableDict, sort_keys=True,
                                        indent=4, separators=(',', ': '))
        time.sleep(5)

if __name__ == "__main__":
    setupBus()
    setupTimeline()
