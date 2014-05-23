# -*- coding: utf-8 -*-
"""
Created on Wed Apr 30 00:25:16 2014
Project	:Image Tagger
Version	:0.0.1
@author	:macrobull

"""

__version__ = '0.0.1'

api_key = "2c7260ce509a2b73137a63ceb7e6f78cfba9176f"

#url_web_saucenao = "http://saucenao.com/search.php?db=999&url={url}"
url_web_saucenao = "http://saucenao.com/search.php?{data}"
#url_web_saucenao_pixivOnly = "http://saucenao.com/search.php?db=58&url={url}"

fname_pixiv_parttern = "{user} - {title} ({work_id}@{user_id})[{tags}]{{{tools}}}"

dropboxed = True
opt_tagFile = opt_renameFile = False


import os, sys, re, time, io
import urllib, json
from optparse import OptionParser
from PIL import Image
import lxml.html as lhtml
from lxml.etree import HTMLParser

reload(sys)
sys.setdefaultencoding('utf-8')

utf8Parser = HTMLParser(encoding="utf-8")

defaultFilter = re.compile('.*\..*p.*g')

def clearifyText(s):
	s = s.replace('\n','')
	s = ' '.join([t for t in s.split(' ') if t])
	s = '\t'.join([t for t in s.split('\t') if t])
	return s

def getFileList(path, filter=defaultFilter):
	r = []
	for file in os.listdir(path):
		if os.path.isdir(file):
			r += getFileList(path, filter)
		elif filter.match(file):
			r.append(os.path.join(path,file))
	return r

def getFileUrl(path):
	return  'http://' + urllib.quote( path.replace( '/home/macrobull/Dropbox/Public/', 'dl.dropboxusercontent.com/u/73985358/'))


def parsePixivTag(pixiv_id):
	pixivcomUrl = "http://zh.pixiv.com/works/{pixiv_id}"

	req = pixivcomUrl.format(pixiv_id=pixiv_id)
	#print req
	res = urllib.urlopen(req).read()
	#print res
	html = lhtml.fromstring(res, parser = utf8Parser)

	info = dict(
		title = html.xpath('//h1[@class="title"]')[0].text,
		work_id = pixiv_id
	)

	for item in html.xpath('//div[@class]'):
		if 'author-summary' in item.attrib['class'].split():
			info['user_id'] = item.xpath('./a')[0].attrib['href'].split('/')[-1]
			info['user'] = ''.join(item.xpath('./a')[0].itertext())

		if 'work-data' in item.attrib['class'].split():
			info['meta'] = ' '.join(item.itertext())

		if 'work-caption' in item.attrib['class'].split():
			info['discription'] = ' '.join(item.itertext())

		if 'tags' in item.attrib['class'].split():
			for tag in item.xpath('./ul'):
				if 'added-tags' in tag.attrib['class'].split():
					info['tags'] = ' '.join(tag.itertext())

	for item in info:
		info[item] = clearifyText(info[item])

	return info


def getInfobyUrlinSaucenao(url):
	data = dict(
		output_type = 2,
		api_key = api_key,
		testmode = 1,
		db = 99,
		numres = 1,
		url = url
	)

	index_parser = {
		5 : 'pixiv',
		6 : 'pixiv',
		8 : 'seiga',
		10 : 'drawr',
		11 : 'nijie'
	}

	try:
		data = urllib.urlencode(data)
		req = url_web_saucenao.format(data=data)
		res = urllib.urlopen(req).read()
		res = json.JSONDecoder().decode(res)

		if float(res['results'][0]['header']['similarity']) < 75:
			raise ValueError("Low similarity")

		source = res['results'][0]['header']['index_id']
		info = res['results'][0]['data']
		if source in index_parser:
			source = index_parser[source]
			if source == 'pixiv' :
				info = parsePixivTag(info['pixiv_id'])
		else:
			source = 'unkown'

		return source, info, 24

	except BaseException, e:
		return None, {'error':e}, 10


def getInfobyUrlinGoogle(url):
	return None, None, 1


def getTagbyUploadinSaucenao():
	pass

def getTagbyUploadinGoogle():
	pass

def getInfobyUrl(url, sites = [getInfobyUrlinSaucenao, getInfobyUrlinGoogle]):
	for site in sites:
		source, res, cd = site(url)
		if source:
			return source, res, cd
	return None, None, 1

def getInfobyUpload(path, sites = [getTagbyUploadinSaucenao, getTagbyUploadinGoogle]):

	thumbSize = (150,150)
	image = Image.open(path)
	image.thumbnail(thumbSize, Image.ANTIALIAS)
	imageData = io.BytesIO()
	image.save(imageData,format='jpg')


	for site in sites:
		source, res, cd = site({'file': ("image.png", imageData.getvalue())})
		if source:
			return source, res, cd


	imageData.close()
	return None, None, 1

def tagFile(path):
	pass

def renameFile(path):
	pass

def run():

	epilog = '''
		testing...
	'''

	parser = OptionParser(version='%prog ' + __version__,
		usage="%prog [options] DIRECTORY",
		epilog=epilog)

	options, args = parser.parse_args()

	if len(args):
		path = args[0]
	else:
		path = os.curdir

	fileList = getFileList(path)[20:]
	#print fileList[:20]
	#return 0

	for i, file in enumerate(fileList):
		cd = 0
		if dropboxed:
			url = getFileUrl(file)
			source, info, cd= getInfobyUrl(url)
		else:
			source, info, cd = getInfobyUpload(file)

		print '\n', i, os.path.basename(file), source, ':\n\t',
		if info:
			for key in info:
				print key,':', info[key], ', ',

			if opt_tagFile:
				tagFile(file)#, info['tag'])

			if opt_renameFile:
				renameFile(file)

		if cd:
			time.sleep(cd)

		#return 0


#run()
if len(sys.argv)>2:
	st = int(sys.argv[1])
	fn = sys.argv[2]
f = open(fn,'w')
for i in xrange(st, 43202092):
	try:
		z = parsePixivTag(repr(i))
		#print z['tags']
		try:
			z['tools'] = z['meta'].split('\t')[2]
		except IndexError, e:
			z['tools'] = ''
		print fname_pixiv_parttern.format(**z)
		f.write(fname_pixiv_parttern.format(**z)+'\n')

	except BaseException, e:
		print i, e
		f.flush()






'''
def getTagbyUrlinSaucenaoHtml(url):
	def guessSource(info):
		text = ' '.join(info).lower()
		if text.find('pixiv id')>=0: return 'pixiv'
		if text.find('creator')>=0: return 'danbooru'

		return 'unkown'

	data = urllib.urlencode({'db' : '999', 'url' : url})
	req = url_web_saucenao.format(data=data)
	#print req
	res = urllib.urlopen(req).read()
	print res
	html = lhtml.fromstring(res)
	res = []
	for item in html.xpath('//td[@class="resulttablecontent"]'):
		text = item.xpath('.//text()')
		info = dict( confid = text[0], head_title = text[1] )
		text = text[2:]
		while text:
			key = text.pop(0)
			if key.find(':')>0:
				info[key[:key.find(':')]] = text.pop(0)

		res.append(info)

		return guessSource(info), info

	return None, None
'''
