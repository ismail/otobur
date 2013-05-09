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

linesWhereWePurelySuck = ["14/F", "26/B", "94", "B/41B", "E/2", "S/2"]
linesWithWrongData = ["6/F2", "35/S", "38"]
linesWithCrapData = ["35/C", "38/B", "38/D", "B/4", "B/34", "80"]

whiteListedLines = ["4/G", "6/F1", "15/A", "26/A", "92"]
blacklistedLines = linesWithWrongData + linesWithCrapData + linesWhereWePurelySuck

dayKeywords = ["HAFTAİÇİ", "HAFTA İÇİ", "CUMARTESİ", "PAZAR"]

fixupTimeDict =  {
    "00" : "24",
    "01" : "25",
    "02" : "26",
    "03" : "27",
}

def compareTime(t1, t2):
    # Sanitize this shit, we only need first 5 characters XX:YY
    t1 = "".join(list(t1)[:5]).replace(".",":")
    t2 = "".join(list(t2)[:5]).replace(".",":")

    h,m = t1.split(":")
    h = fixupTimeDict.get(h, h)
    vt1 = int(h)*60 + int(m)

    h,m = t2.split(":")
    h = fixupTimeDict.get(h, h)
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

def parseHourListStructured(content):
    content = content.encode("utf-8")
    content = content.replace("\t","")
    content = content.split("\xc2\xa0")
    hours = []

    for hour in content:
        if hour.isspace():
            continue

        entries = hour.split("\r\n")
        entries = [x.strip() for x in entries if x.strip() != '']
        hours.append(entries)

    return hours

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

def parseDescription(content):
    content = content.encode("utf-8")
    content = content.replace("\t","")
    content = content.replace("\xc2\xa0","")
    content = content.replace("\r","")
    content = content.split("\n")

    index = 0
    for line in content:
        if re.match("\d\d:\d\d", line.strip()):
            index = content.index(line)
            content = content[:index]
            break

    content = [x.strip() for x in content if x.strip() != '']
    return content

def parseStops(content):
    parsedStops = []

    for line in content:
        stops = line.split("-")
        if len(stops) >= 3:
            line = line.replace("GİDİŞ", "")
            line = line.replace("DÖNÜŞ", "")
            line = line.replace("GÜZERGAHI", "")
            line = line.replace("GÜZERGAH", "")
            line = line.replace("GÜZERGÂH", "")
            line = line.replace("(", "")
            line = line.replace(")", "")
            line = line.replace(":", "")
            stops = line.split("-")
            parsedStops.append([x.strip() for x in stops if x.strip() != ''])

    return parsedStops

def parseHeaders(headers, timeLength):
    headerLength = len(headers)

    stopRow = []
    dayRow = []

    for i in reversed(range(0, timeLength)):
        dayRow.append(headers[headerLength - 1 -i])

    # This is the usual case
    start = len(headers)-timeLength*2-1

    # Cheat the start, this let us parse less stuff
    for header in headers:
        if (header.find("GÜZERGAH") >= 0) or (header.find("GÜZERGÂH") >= 0): # they did it for lolz
            index = headers.index(header)
            if start < index:
                start = index+1

    for header in headers[start:-timeLength]:
        dayKeyword = any([header.find(keyword) >= 0 for keyword in dayKeywords])
        if not dayKeyword:
            continue

        stopRow.append(header)

    if len(stopRow) > 0:
        # First two items might be duplicates
        if len(stopRow) >= 2 and (stopRow[0] == stopRow[1]):
            stopRow.pop(0)

        index = 0
        splitCount = len(dayRow) / len(stopRow)
        for i in range(0, len(dayRow)):
            dayRow[i] = "%s [%s]" % (stopRow[index], dayRow[i])

            if (i+1) % splitCount == 0:
                index += 1

    return dayRow

def parseTable(table, structured):
    rows = table.xpath("//tbody/tr")

    description = ""
    for row in rows[:6]:
        description += row.text_content()
    description = parseDescription(description)

    for row in rows[2:]:
        content = row.text_content().strip()
        if re.match("\d\d:\d\d", content):
            if structured:
                timeTable = parseHourListStructured(content)
            else:
                timeTable = parseHourList(content)
            break

    if not structured:
        timeTable = splitTimeTable(timeTable)

    hours = OrderedDict()
    headerList = parseHeaders(description, len(timeTable))

    index = 0
    for header in headerList:
        hours[header] = timeTable[index]
        index += 1

    return (parseStops(description), hours)

def parsePage(doc, structured=False):
    tableList = doc.xpath("/html//table")

    for table in tableList:
        try:
            for key in table.attrib['style'].split(";"):
                if key.find("width") >= 0:
                    width = key.split(":")[1].strip().rstrip("px;")
                    if width.find("%") < 0:
                        return parseTable(table, structured)
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
        print url
        structured = (key in whiteListedLines)
        doc = html.fromstring(urllib2.urlopen(url).read())

        if not key in timeTableDict.keys():
            timeTableDict[key] = OrderedDict()
            timeTableDict[key]["backward"] = None
            timeTableDict[key]["forward"] = None
            timeTableDict[key]["hours"] = {}
            timeTableDict[key]["url"] = None

        timeTableDict[key]["url"] = url
        (stops, timeTableDict[key]["hours"]) = parsePage(doc, structured)

        length = len(stops)
        if length > 0:
            timeTableDict[key]["forward"] = stops[0]
            if length > 1:
                timeTableDict[key]["backward"] = stops[1]

        time.sleep(0.2)

if __name__ == "__main__":
    setupBus()
    setupTimeline()

    fp = open("hours.json","wb")
    fp.write(json.dumps(timeTableDict, sort_keys=False,
                        indent=4, separators=(',', ': ')))
    fp.close()
