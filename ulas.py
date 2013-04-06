#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Placed under public domain.
# 2013 İsmail Dönmez <ismail@donmez.ws>

from collections import OrderedDict
from lxml import html
import urllib2
import re
import sys
import time

address="http://www.burulas.com.tr/sayfa.aspx?id=393"
base_url="http://www.burulas.com.tr"
clock_dict = OrderedDict()

if __name__ == "__main__":
    tree = html.fromstring(urllib2.urlopen(address).read())
    for td in tree.xpath('/html/body//tbody/tr/td/a'):
        try:
            if "Hareket Saatleri" in td.attrib['title']:
                line_name = td.attrib['title'].split(" ")[0]
                clock_dict[line_name] = "%s/%s" % (base_url, td.attrib['href'])
        except KeyError:
            pass

    for key in clock_dict.keys():
        url = clock_dict[key]
        url = "http://www.burulas.com.tr/sayfa.aspx?id=685"
        doc = html.fromstring(urllib2.urlopen(url).read())
        tableList = doc.xpath("/html//table")
        for table in tableList:
            try:
                if table.attrib['cellpadding'] == "1" and table.attrib['cellspacing'] == "0": 
                    for row in table.xpath("./tbody//tr"):
                        if re.search("\d\d:\d\d", row.text_content()):
                            for column in row.xpath("./td"):
                                hours = column.text_content().replace(u'\xa0','').replace('\t','').split("\r\n")
                                print [ x for x in hours if x != "" ]
            except KeyError:
                pass

        sys.exit(0)
        time.sleep(5)
