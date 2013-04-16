# -*- coding: utf-8 -*-
from lxml import html
import urllib2
import sys

def cleanup(x):
    x = x.replace("\r", "")
    x = x.replace("\n", "")
    x = x.replace("\t", "")
    x = x.strip()
    return x

def parseRoute(data):
    data = data.encode("utf-8")
    data = data.split("\r\n\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t")
    data = [x.strip() for x in data if x.strip() != '']
    result = [[], []]

    result[0] = data[0].replace("GİDİŞ GÜZERGAHI: ","").split("-")
    result[0] = [cleanup(x) for x in result[0] if x.strip() != '']
    result[1] = data[1].replace("DÖNÜŞ GÜZERGAHI: ","").split("-")
    result[1] = [cleanup(x) for x in result[1] if x.strip() != '']

    print result

def parse():
    url = "http://www.burulas.com.tr/sayfa.aspx?id=552"
    data = html.fromstring(urllib2.urlopen(url).read())
    rows = data.xpath("//tbody/tr")
    routeData = rows[3].text_content()
    hourData = rows[4].text_content()
    parseRoute(routeData)

if __name__ == "__main__":
    parse()

