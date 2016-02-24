import common, urllib2, string, random, base64, datetime, redirect_follower

global_request_timeout = 10

GOOD_RESPONSE_CODES = ['200','206']

####################################################################################################
# Get HTTP response code (200 == good)
@route(common.PREFIX + '/gethttpstatus')
def GetHttpStatus(url):
	try:
		conn = urllib2.urlopen(url, timeout = global_request_timeout)
		resp = str(conn.getcode())
	except StandardError:
		resp = '0'
	if Prefs['debug']:
		Log(url +' : HTTPResponse = '+ resp)
	return resp
	

####################################################################################################
# Get HTTP response code (200 == good)
@route(common.PREFIX + '/followredirectgethttpstatus')
def FollowRedirectGetHttpStatus(url):
	try:
		response = redirect_follower.GetRedirect(url,global_request_timeout)
		if response <> None:
			resp = str(response.getcode())
	except:
		resp = '0'
	if Prefs['debug']:
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
	except:
		redirectUrl = url
	if Prefs['debug'] and url != redirectUrl:
		Log(url + "Redirecting to : " + redirectUrl)
	return redirectUrl
	
####################################################################################################
# Gets the redirecting url 
@route(common.PREFIX + '/getredirectingurl')
def GetRedirectingUrl(url):

	#Log("Url ----- : " + url)
	redirectUrl = url
	try:
		response = redirect_follower.GetRedirect(url, global_request_timeout)
		if response <> None:
			return response.geturl()
	except:
		redirectUrl = url
			
	#Log("Redirecting url ----- : " + redirectUrl)
	return redirectUrl
	
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
def GetAttribute(text, attribute, delimiter1 = '="', delimiter2 = '"'):
	x = text.find(attribute)
	if x > -1:
		y = text.find(delimiter1, x + len(attribute)) + len(delimiter1)
		z = text.find(delimiter2, y)
		if z == -1:
			z = len(text)
		return unicode(text[y:z].strip())
	else:
		return ''
		
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