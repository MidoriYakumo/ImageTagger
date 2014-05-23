# -*- coding: utf-8 -*-
"""
Created on Wed Apr 30 00:25:16 2014
Project	:Image Tagger
Version	:0.0.1
@author	:macrobull

"""

__version__ = '0.0.1'

url = "http://danbooru.donmai.us/posts?page={page}&search=&tags=hakurei_reimu"

import os, sys, re, time, io
import urllib, json
from PIL import Image
import lxml.html as lhtml
from lxml.etree import HTMLParser

reload(sys)
sys.setdefaultencoding('utf-8')

utf8Parser = HTMLParser(encoding="utf-8")

page = sys.argv[1]


try:
	while True:
		html = urllib.urlopen(url.format(page=page)).read()
		root = lhtml.fromstring(html)
		link = root.xpath('//a[@rel="next"]')[0].attrib['href']
		page = link[link.find('page=')+5:link.find('&')]
		print page
except ValueError, e:
	print e



