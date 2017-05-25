import os, urllib2, string, random, base64, datetime 
import common, redirect_follower, playback, common

global_request_timeout = 10

GOOD_RESPONSE_CODES = ['200','206']

####################################################################################################
# Get HTTP response code (200 == good)
@route(common.PREFIX + '/gethttpstatus')
def GetHttpStatus(url, timeout=global_request_timeout):
	try:
		headers = {'User-Agent': common.USER_AGENT,
		   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		   'Accept-Encoding': 'none',
		   'Accept-Language': 'en-US,en;q=0.8',
		   'Connection': 'keep-alive',
		   'Referer': url}
	   
		if '|' in url:
			url_split = url.split('|')
			url = url_split[0]
			headers['Referer'] = url
			for params in url_split:
				if '=' in params:
					param_split = params.split('=')
					param = param_split[0].strip()
					param_val = urllib2.quote(param_split[1].strip(), safe='/=&')
					headers[param] = param_val

		if 'http://' in url or 'https://' in url:
			req = urllib2.Request(url, headers=headers)
			conn = urllib2.urlopen(req, timeout=timeout)
			resp = str(conn.getcode())
		else:
			resp = '200'
	except Exception as e:
		resp = '0'
		if Prefs['debug']:
			Log('Error common_fnc.py > GetHttpStatus: ' + str(e))
			Log(url +' : HTTPResponse = '+ resp)
	return resp
	

####################################################################################################
# Get HTTP response code (200 == good)
@route(common.PREFIX + '/followredirectgethttpstatus')
def FollowRedirectGetHttpStatus(url, timeout=global_request_timeout):
	try:
		response = redirect_follower.GetRedirect(url,timeout)
		if response <> None:
			resp = str(response.getcode())
	except Exception as e:
		resp = '0'
		if Prefs['debug']:
			Log('Error common_fnc.py > FollowRedirectGetHttpStatus: ' + str(e))
			Log(url +' : HTTPResponse = '+ resp)
	return resp
	
####################################################################################################
# Gets the redirecting url for .m3u8 streams
@route(common.PREFIX + '/getredirector')
def GetRedirector(url):

	#Log("Url ----- : " + url)
	redirectUrl = url
	try:
		if ('.m3u8' or '.mp3' or '.aac' or '.m3u' or '/udp/' or 'udp:') not in url and '.mp4' not in url and not ArrayItemsInString(playback.MP4_VIDEOS, url):
			#page = urllib2.urlopen(url, timeout = global_request_timeout)
			#redirectUrl = page.geturl()
			redirectUrl = GetRedirectingUrl(url)
	except Exception as e:
		if Prefs['debug']:
			Log('Error common_fnc.py > GetRedirector: ' + str(e))
		redirectUrl = url
	return redirectUrl
	
####################################################################################################
# Gets the redirecting url 
@route(common.PREFIX + '/getredirectingurl')
def GetRedirectingUrl(url):

	#Log("Url ----- : " + url)
	redirectUrl = url
	try:
		response = redirect_follower.GetRedirect(url, 7)
		if response <> None:
			return response.geturl()
	except:
		redirectUrl = url
			
	Log("Redirecting url ----- : " + redirectUrl)
	return redirectUrl
	
####################################################################################################

@route(common.PREFIX + '/showmessage')
def ShowMessage(title, message):
	return ObjectContainer(header=title, message=message, title1=title)
	
@route(common.PREFIX + '/id_generator')
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))
	
@route(common.PREFIX + '/shuffle')
def shuffle(list):
	result = []
	cloneList = []
	for item in list:
		cloneList.append(item)
	for i in range(len(cloneList)):
		element = random.choice(cloneList)
		cloneList.remove(element)
		result.append(element)
	return result

def getSession():
	if 'X-Plex-Client-Identifier' in str(Request.Headers):
		return str(Request.Headers['X-Plex-Client-Identifier'])
	elif 'X-Plex-Target-Client-Identifier' in str(Request.Headers):
		return str(Request.Headers['X-Plex-Target-Client-Identifier'])
	elif 'User-Agent' in str(Request.Headers) and 'X-Plex-Token' in str(Request.Headers):
		return 'UnknownClient-'+encode(str(Request.Headers['User-Agent']) + str(Request.Headers['X-Plex-Token'][:3]))[:10]
	else:
		return 'UnknownPlexClientSession'

def getProduct():
	if 'X-Plex-Product' in str(Request.Headers):
		return str(Request.Headers['X-Plex-Product'])
	else:
		return 'UnknownPlexProduct'
	
def getPlatform():
	if 'X-Plex-Platform' in str(Request.Headers):
		return str(Request.Headers['X-Plex-Platform'])
	else:
		return 'UnknownPlexPlatform'
	
def getDevice():
	if 'X-Plex-Device' in str(Request.Headers):
		return str(Request.Headers['X-Plex-Device'])
	else:
		return 'UnknownPlexDevice'
		
def getDeviceName():
	if 'X-Plex-Device-Name' in str(Request.Headers):
		return str(Request.Headers['X-Plex-Device-Name'])
	else:
		return 'UnknownPlexDeviceName'
		
def getPlexHeaders():
	return str(Request.Headers)
	
####################################################################################################
# search array item's presence in string
@route(common.PREFIX + "/arrayitemsinstring")
def ArrayItemsInString(arr, mystr):

	for item in arr:
		if item in mystr:
			return True
			
	return False
	
####################################################################################################
# Parses attributes 
# IPTV (Author: Cigaras)
# https://forums.plex.tv/index.php/topic/83083-iptvbundle-plugin-that-plays-iptv-streams-from-a-m3u-playlist/?hl=iptv
# https://github.com/Cigaras/IPTV.bundle
#
# Copyright © 2013-2015 Valdas Vaitiekaitis
# Modified by CA, 2016
#
def GetAttribute(text, attribute, delimiter1 = '="', delimiter2 = '"'):
	x = text.find(attribute)
	if x > -1:
		y = text.find(delimiter1, x + len(attribute)) + len(delimiter1)
		z = text.find(delimiter2, y)
		if z == -1:
			z = len(text)
		
		retStr = unicode(text[y:z].strip())
		if attribute.lower() != 'tvg-logo' and 'http' in retStr:
			y = text.find('=', x + len(attribute)) + len(' ')
			z = text.find(' ', y)
			if z == -1:
				z = len(text)
			retStr = unicode(text[y:z].strip())

		if '=' in retStr:
			retStr = retStr.split('=')[1]
		if ',' in retStr:
			retStr = retStr.split(',')[0]
		return retStr
	else:
		return ''

#######################################################################################################
# url decode		
def urldecode(string):
	return urllib2.unquote(string)
		
#######################################################################################################
# base64 decode
@route(common.PREFIX + '/decode')
def decode(str):

	return base64.b64decode(str)
	
# base64 encode
@route(common.PREFIX + '/encode')
def encode(str):

	return base64.b64encode(str)
	
#######################################################################################################
# Gets the raw Pastebin link
def getRawPastebinLink(url):
	try:
		urlsplit = url.replace('://','').split('/')
		fixedLink = 'http://www.pastebin.com/raw/' + urlsplit[1]
	except:
		fixedLink = None
	return fixedLink
	
# Gets the raw Pastebin link
def getDatePastebinLink(content):
	try:
		content = content.strip('Untitled. a guest ')
		date = str(content.split('<b>')[0].strip())
		if 'hour' in date:
			dt = date.split(' ')
			date = ' ' + str("{0:0=2d}".format(int(dt[0].strip()))) + ' hours ago'
		elif 'day' in date:
			dt = date.split(' ')
			date = str("{0:0=2d}".format(int(dt[0].strip()))) + ' days ago'
		#date = datetime.datetime.strptime(date, '%M %d, %y').strftime('%y-%m-%d')
	except:
		pass
	return date
	
def month_string_to_number(string):
	m = {'jan': 1,
		'feb': 2,
		'mar': 3,
		'apr':4,
		'may':5,
		'jun':6,
		'jul':7,
		'aug':8,
		'sep':9,
		'oct':10,
		'nov':11,
		'dec':12
	}
	return m[string]
	
#######################################################################################################
