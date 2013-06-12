#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Placed under public domain.
# 2013 İsmail Dönmez <ismail@donmez.ws>

from collections import OrderedDict
from lxml import etree, html
import json
import urllib2
import sys

root = "http://www.burulas.com.tr/hatsorgulama.aspx?hatAdi=99999"
baseUrl = "http://www.burulas.com.tr/hareketSaatleri.aspx"
scheduleDict = {}

def parseSchedule(busName, address):
    tree=html.fromstring(urllib2.urlopen(address).read())

    stopName = None
    for td in tree.xpath('//table[@class="brTable"][1]//td'):
        if td.attrib.get("colspan") in ["1", "2", "3", "4"] and not td.attrib.get("cellpadding"):
            if td.attrib.get("style") == "text-align:justify;padding:5px;":
                route = td.text_content().strip().encode("utf-8")

                keyword = None

                if route.find("DÖNÜŞÜNDE") >= 0:
                    pass
                elif route.find("DÖNÜŞ:") >= 0:
                    keyword = "DÖNÜŞ:"
                elif route.find("DÖNÜŞ :") >= 0:
                    keyword = "DÖNÜŞ :"

                if keyword:
                    if busName == "F/3": # XXX hackity hack
                        (forward, foo, backward) = route.split(keyword)
                    else:
                        (forward, backward) = route.split(keyword)

                    forward = [x.strip() for x in forward.split("-")]
                    backward = [x.strip() for x in backward.split("-")]
                else:
                    forward = [x.strip() for x in route.split("-")]
                    backward = None

                scheduleDict[busName]["forward"] = forward
                scheduleDict[busName]["backward"] = backward

            elif td.attrib.get("style") == None:
                stopName = td.text_content()
                stopName = stopName.encode("utf-8")
                if stopName.find("TARİFE NO") >= 0 or stopName.find("NOT:") >= 0:
                    pass
        elif td.attrib.get("valign") == "top" and td.attrib.get("style") == "padding:5px;":
            day = td[0].text_content()
            hours = []

            hours.append(td[0].tail)
            el = td[0].getnext()
            while el != None:
                hour = etree.tostring(el).replace("<br />","")
                if hour:
                    hours.append(hour)
                el = el.getnext()

            stopDayName = "%s [%s]" % (stopName, day.encode("utf-8"))
            scheduleDict[busName]["hours"][stopDayName] = hours

            if not hours:
                print "Error!"
                sys.exit(1)

def parseBusList():
    tree=html.fromstring(urllib2.urlopen(root).read())
    for link in tree.xpath("//body//a"):
        target = link.attrib.get("href")
        if target.find("hareketSaatleri.aspx") >= 0:
            address = "%s?%s" % (baseUrl, target.split("?")[1].encode("utf-8"))
            busName = target.split("hat=")[1].encode("utf-8")

            scheduleDict[busName] = OrderedDict()
            scheduleDict[busName]["forward"] = None
            scheduleDict[busName]["backward"] = None
            scheduleDict[busName]["url"] = address
            scheduleDict[busName]["hours"] = OrderedDict()

            print "%s - %s" % (busName, address)
            parseSchedule(busName, address)

if __name__ == "__main__":
    parseBusList()

    fp = open("hours.json","wb")
    fp.write(json.dumps(scheduleDict, sort_keys=False,
                        indent=4, separators=(',', ': ')))
    fp.close()
