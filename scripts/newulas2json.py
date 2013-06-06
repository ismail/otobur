#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Placed under public domain.
# 2013 İsmail Dönmez <ismail@donmez.ws>

from lxml import html
import urllib2

root = "http://www.burulas.com.tr/hatsorgulama.aspx?hatAdi=99999"
baseUrl = "http://www.burulas.com.tr/hareketSaatleri.aspx"

def do_parse(address):
    address = address.encode("utf-8")
    tree=html.fromstring(urllib2.urlopen(address).read())
    for td in tree.xpath('//table[@class="brTable"][1]//td'):
        if td.attrib.get("colspan") in ["2", "4"] and not td.attrib.get("cellpadding"):
            if td.attrib.get("style") == "text-align:justify;padding:5px;":
                print "Route: %s" % td.text_content()
            elif td.attrib.get("style") == None:
                print "Stop: %s" % td.text_content()
        elif td.attrib.get("valign") == "top" and td.attrib.get("style") == "padding:5px;":
            print "Timetable: %s" % td.text_content()

tree=html.fromstring(urllib2.urlopen(root).read())
for link in tree.xpath("//body//a"):
    target = link.attrib.get("href")
    if target.find("hareketSaatleri.aspx") >= 0:
        address = "%s?%s" % (baseUrl, target.split("?")[1])
        print address
        do_parse(address)
