######################################################################################
#
#	CcloudTv - v0.01
#
######################################################################################
import re, urllib

# Set global variables
TITLE = "Ccloud Tv"
PREFIX = "/video/ccloudtv"
ART = "art-default.jpg"
ICON = "icon-ccloudtv.png"
ICON_LIST = "icon-list.png"
ICON_SEARCH = "icon-search.png"
ICON_SERIES = "icon-series.png"
ICON_QUEUE = "icon-queue.png"

BASE_URL = ""
DEV_URL = "/ch/l/tv"
items_dict = {} # using dictionary for search
DISABLED_NAMES = ['shspiderman']

######################################################################################

def Start():

	ObjectContainer.title1 = TITLE
	ObjectContainer.art = R(ART)
	DirectoryObject.thumb = R(ICON_LIST)
	DirectoryObject.art = R(ART)
	VideoClipObject.thumb = R(ICON_SERIES)
	VideoClipObject.art = R(ART)
	
	HTTP.ClearCache()
	#HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0'

	
######################################################################################
# Menu hierarchy

@handler(PREFIX, TITLE, art=ART, thumb=ICON)
def MainMenu():
	
	webUrl = Prefs['web_url']
	oc = ObjectContainer(title2=TITLE)
	ChHelper = ' (Refresh List)'
	ChHelper2 = ' (Initialize this Channel List once before Search, Search Queue and Bookmark menu are made available)'
	if items_dict <> {}:
		ChHelper = ''
		ChHelper2 = ' - Listing retrieved'
		oc.add(InputDirectoryObject(key = Callback(Search, items_dict=items_dict), title='Search', summary='Search Channel', prompt='Search for...'))
		oc.add(DirectoryObject(key = Callback(SearchQueueMenu, title = 'Search Queue', items_dict=items_dict), title = 'Search Queue', summary='Search using saved search terms', thumb = R(ICON_SEARCH)))
	oc.add(DirectoryObject(key = Callback(ShowMenu, title = 'Channels', webUrl = webUrl), title = 'Channels' + ChHelper, summary = 'Channels' + ChHelper2, thumb = R(ICON)))
	if items_dict <> {}:
		oc.add(DirectoryObject(key = Callback(Bookmarks, title='My Channel Bookmarks', items_dict=items_dict), title = 'My Channel Bookmarks', thumb = R(ICON_QUEUE)))
	
	# preCache
	if Prefs['use_precache']:
		try:
			if webUrl <> None and webUrl.startswith('http'):
				BASE_URL = webUrl + DEV_URL
				try:
					page_data = HTTP.Request(BASE_URL).content
					page_elems = HTML.ElementFromString(page_data)
					
					fetch_urls = page_elems.xpath(".//div[@class='table-title']//script//@src")
					for eachFetchUrl in fetch_urls:
					
						bool = True
						for name in DISABLED_NAMES:
							if name in eachFetchUrl:
								bool = False
								break
						
						if 'names.js' in eachFetchUrl and bool:
							#Log("eachFetchUrl------------- " + eachFetchUrl)
							try:
								HTTP.PreCache(eachFetchUrl)
							except:
								page_data_r = ''
				except:
					page_data_r = ''
		except:
			page_data_r = ''

	return oc

@route(PREFIX + "/showMenu")
def ShowMenu(title, webUrl):
	oc = ObjectContainer(title2=title)
	abortBool = True
	
	if items_dict <> {}:
		oc.add(InputDirectoryObject(key = Callback(Search, items_dict=items_dict), title='Search', summary='Search Channel', prompt='Search for...'))	
	
	if webUrl <> None and webUrl.startswith('http'):
		BASE_URL = webUrl + DEV_URL
		try:
			page_data = HTTP.Request(BASE_URL).content
			page_elems = HTML.ElementFromString(page_data)
			page_data = ''
			
			fetch_urls = page_elems.xpath(".//div[@class='table-title']//script//@src")
			for eachFetchUrl in fetch_urls:
			
				bool = True
				for name in DISABLED_NAMES:
					if name in eachFetchUrl:
						bool = False
						break
				
				if 'names.js' in eachFetchUrl and bool:
					#Log("eachFetchUrl------------- " + eachFetchUrl)
					try:
						page_data_r = HTTP.Request(eachFetchUrl).content
						page_data = page_data + '\n' + page_data_r
					except:
						page_data_r = ''
			
			#page_data = filter(lambda x: not re.match(r'^\s*$', x), page_data)
			page_data = page_data.replace('(','')
			page_data = page_data.replace(')','')
			page_data = page_data.replace('"','')
			page_data = page_data.replace('.','')
			page_data = page_data.replace('=','')
			#Log(page_data)
			
			channels = page_elems.xpath(".//table[@class='list']//tr")
			count = 0
			
			for eachCh in channels:
				channelNum = eachCh.xpath(".//td[@class='text-center']//a//text()")[0]
				channelUrl = eachCh.xpath(".//td[@class='text-left']//a//@href")[0]

				try:
					channelId0 = channelUrl.split('/')
					channelId = channelId0[len(channelId0)-1].replace('tv','')
					srcStr = 'documentgetElementById'+channelId+'textContent'
					#Log("srcStr----------" + srcStr)
					
					channelDesc = re.findall(srcStr+'(.*?);', page_data, re.S)[0]
					#Log("channelDesc----------" + channelDesc)
				except:
					channelDesc = eachCh.xpath(".//td[@class='text-left']//a//text()")[0]
				
				items_dict[count] = {'channelNum': channelNum, 'channelDesc': channelDesc, 'channelUrl': channelUrl}
				count = count + 1
				
				#Log("channelUrl--------------" + str(channelUrl))
				title = unicode('Channel: ' + channelNum + ' (' + channelDesc + ')')
				
				oc.add(DirectoryObject(key = Callback(ChannelPage, url = channelUrl, title = title, summary = channelDesc, channelNum=channelNum), title = title, thumb = R(ICON_SERIES)))
			abortBool = False	
		except:
			BASE_URL = ""
			abortBool = True
	
	if items_dict <> {}:
		oc.add(InputDirectoryObject(key = Callback(Search, items_dict=items_dict), title='Search', summary='Search Channel', prompt='Search for...'))
	
	if abortBool:
		return ObjectContainer(header=title, message='No Channels Available. Please check website URL !')
	return oc
	
@route(PREFIX + '/channelpage')
def ChannelPage(url, title, summary, channelNum):

	oc = ObjectContainer(title2=title)
	
	try:
		#Log("----------- url ----------------")
		#Log(url)
		oc.add(CreateVideoClipObject(
			url = GetRedirector(url),
			title = title,
			thumb = R(ICON_SERIES),
			summary = summary))
	except:
		url = ""
	
	if Check(channelNum=channelNum,url=url):
		oc.add(DirectoryObject(
			key = Callback(RemoveBookmark, title = title, channelNum = channelNum, url = url),
			title = "Remove Bookmark",
			summary = 'Removes the current Channel from the Boomark queue',
			thumb = R(ICON_QUEUE)
		))
	else:
		oc.add(DirectoryObject(
			key = Callback(AddBookmark, channelNum = channelNum, url = url),
			title = "Bookmark Channel",
			summary = 'Adds the current Channel to the Boomark queue',
			thumb = R(ICON_QUEUE)
		))
	
	if items_dict <> {}:
		oc.add(InputDirectoryObject(key = Callback(Search, items_dict=items_dict), title='Search', summary='Search Channel', prompt='Search for...'))	
	return oc
	
####################################################################################################
# Gets the redirecting url for .m3u8 streams
@route(PREFIX + '/getredirector')
def GetRedirector(url):

	redirectUrl = url
	try:
		if '.m3u8' not in redirectUrl:
			page = urllib.urlopen(url)
			redirectUrl = page.geturl()
			#Log("Redirecting url ----- : " + redirectUrl)
	except:
		redirectUrl = url

	return redirectUrl
#
# IPTV (Author: Cigaras)
# https://forums.plex.tv/index.php/topic/83083-iptvbundle-plugin-that-plays-iptv-streams-from-a-m3u-playlist/?hl=iptv
# https://github.com/Cigaras/IPTV.bundle
#
# Copyright © 2013-2015 Valdas Vaitiekaitis

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# Version 1.0.10
#
####################################################################################################
@route(PREFIX + '/createvideoclipobject')
def CreateVideoClipObject(url, title, thumb, summary, container = False):
		
	#Log("CreateVideoClipObject--------------" + str(url))
	vco = VideoClipObject(
		key = Callback(CreateVideoClipObject, url = url, title = title, thumb = thumb, summary = summary, container = True),
		#rating_key = url,
		url = url,
		title = title,
		summary = summary,
		thumb = thumb,
		items = [
			MediaObject(
				#container = Container.MP4,	 # MP4, MKV, MOV, AVI
				#video_codec = VideoCodec.H264, # H264
				#audio_codec = AudioCodec.AAC,  # ACC, MP3
				#audio_channels = 2,			# 2, 6
				parts = [
					PartObject(
						key = GetVideoURL(url = url, live = True)
					)
				],
				optimized_for_streaming = True
			)
		]
	)

	if container:
		return ObjectContainer(objects = [vco])
	else:
		return vco
	return vc

####################################################################################################
def GetVideoURL(url, live):

	#url = 'http://wpc.c1a9.edgecastcdn.net/hls-live/20C1A9/cnn/ls_satlink/b_828.m3u8?Vd?u#bt!25'
	
	if url.startswith('rtmp') and Prefs['rtmp']:
		Log.Debug('*' * 80)
		Log.Debug('* url before processing: %s' % url)
		#if url.find(' ') > -1:
		#	playpath = GetAttribute(url, 'playpath', '=', ' ')
		#	swfurl = GetAttribute(url, 'swfurl', '=', ' ')
		#	pageurl = GetAttribute(url, 'pageurl', '=', ' ')
		#	url = url[0:url.find(' ')]
		#	Log.Debug('* url_after: %s' % RTMPVideoURL(url = url, playpath = playpath, swfurl = swfurl, pageurl = pageurl, live = live))
		#	Log.Debug('*' * 80)
		#	return RTMPVideoURL(url = url, playpath = playpath, swfurl = swfurl, pageurl = pageurl, live = live)
		#else:
		#	Log.Debug('* url_after: %s' % RTMPVideoURL(url = url, live = live))
		#	Log.Debug('*' * 80)
		#	return RTMPVideoURL(url = url, live = live)
		Log.Debug('* url after processing: %s' % RTMPVideoURL(url = url, live = live))
		Log.Debug('*' * 80)
		return RTMPVideoURL(url = url, live = live)
	elif url.startswith('mms') and Prefs['mms']:
		return WindowsMediaVideoURL(url = url)
	else:
		return HTTPLiveStreamURL(url = url)
		
####################################################################################################
@route(PREFIX + "/search", items_dict=dict)
def Search(items_dict, query):

	oc = ObjectContainer(title2='Search Results')
	Dict['MyCustomSearch'+query] = query
	Dict.Save()
	
	if items_dict <> None:
		dict_len = len(items_dict)
		if dict_len == 0:
			return ObjectContainer(header='Search Results', message='No Channels loaded ! Initialize Channel list first.')
		
		start = 0
		end = 0
		if '~' in query:
			split = query.split('~')
			try:
				start = int(split[0])
				end = int(split[1])
			except:
				start = 0
				end = 0
		try:
			for x in items_dict:
				channelNum = items_dict[x]['channelNum']
				channelDesc = items_dict[x]['channelDesc']
				channelUrl = items_dict[x]['channelUrl']
				title = unicode('Channel: ' + channelNum + ' (' + channelDesc + ')')
				#Log("channelDesc--------- " + channelDesc)
				
				if query.lower() in channelDesc.lower() or query == channelNum:
					oc.add(DirectoryObject(key = Callback(ChannelPage, url = channelUrl, title = title, summary = channelDesc, channelNum=channelNum), title = title, thumb = R(ICON_SERIES)))
				elif '~' in query and int(channelNum) > start-1 and int(channelNum) < end+1:
					oc.add(DirectoryObject(key = Callback(ChannelPage, url = channelUrl, title = title, summary = channelDesc, channelNum=channelNum), title = title, thumb = R(ICON_SERIES)))
		except:
			return ObjectContainer(header='Search Results', message='No Channels Available. Please check website URL !')
	else:
		return ObjectContainer(header='Search Results', message='Channels need to be loaded before search can be performed !')
	
	if len(oc) == 0:
		return ObjectContainer(header='Search Results', message='No Channels Available based on Search query')
	return oc

######################################################################################
@route(PREFIX + "/searchQueueMenu", items_dict=dict)
def SearchQueueMenu(title, items_dict):
	oc2 = ObjectContainer(title2='Search Using Term')
	#add a way to clear bookmarks list
	oc2.add(DirectoryObject(
		key = Callback(ClearSearches),
		title = "Clear Search Queue",
		thumb = R(ICON_SEARCH),
		summary = "CAUTION! This will clear your entire search queue list!"
		)
	)
	for each in Dict:
		query = Dict[each]
		#Log("each-----------" + each)
		#Log("query-----------" + query)
		if 'MyCustomSearch' in each and query != 'removed':
			oc2.add(DirectoryObject(key = Callback(Search, query = query, items_dict=items_dict), title = query, thumb = R(ICON_SEARCH))
		)

	return oc2	
	
######################################################################################
# Clears the Dict that stores the search list
	
@route(PREFIX + "/clearsearches")
def ClearSearches():

	for each in Dict:
		if 'MyCustomSearch' in each:
			Dict[each] = 'removed'
	Dict.Save()
	return ObjectContainer(header="Search Queue", message='Your Search Queue list will be cleared soon.')
	
######################################################################################
# Loads bookmarked shows from Dict.  Titles are used as keys to store the show urls.

@route(PREFIX + "/bookmarks", items_dict=dict)	
def Bookmarks(items_dict, title):

	oc = ObjectContainer(title1 = title)
	
	if items_dict <> None:
		dict_len = len(items_dict)
		if dict_len == 0:
			return ObjectContainer(header='Bookmarks', message='No Channels loaded ! Channel list needs to be initialized first.')
		try:
			for each in Dict:
				for x in items_dict:
					channelNum = items_dict[x]['channelNum']
					channelDesc = items_dict[x]['channelDesc']
					channelUrl = items_dict[x]['channelUrl']
					title = 'Channel: ' + channelNum + ' (' + channelDesc + ')'
					#Log("channelDesc--------- " + str(channelDesc))
					
					if channelNum == each and Dict[each] <> 'removed' and 'MyCustomSearch' <> each:
						oc.add(DirectoryObject(key = Callback(ChannelPage, url = channelUrl, title = title, summary = channelDesc, channelNum=channelNum), title = title, thumb = R(ICON_SERIES)))
		except:
			return ObjectContainer(header='Bookmarks', message='No Channels Available. Please check website URL !')
	else:
		return ObjectContainer(header='Bookmarks', message='Channels need to be loaded before search can be performed !')
	
	#add a way to clear bookmarks list
	oc.add(DirectoryObject(
		key = Callback(ClearBookmarks),
		title = "Clear Bookmarks",
		thumb = R(ICON_QUEUE),
		summary = "CAUTION! This will clear your entire bookmark list!"
		)
	)
	
	if len(oc) == 1:
		return ObjectContainer(header='Bookmarks', message='No Bookmarked Videos Available')
	return oc

######################################################################################
# Checks a show to the bookmarks list using the title as a key for the url
@route(PREFIX + "/checkbookmark")	
def Check(channelNum, url):
	bool = False
	url = Dict[channelNum]
	#Log("url check-----------" + str(url))
	if url != None and url <> 'removed':
		bool = True
	
	return bool

######################################################################################
# Adds a Channel to the bookmarks list using the title as a key for the url
	
@route(PREFIX + "/addbookmark")
def AddBookmark(channelNum, url):
	
	Dict[channelNum] = url
	url = Dict[channelNum]
	#Log("url add-----------" + str(url))
	Dict.Save()
	return ObjectContainer(header= 'Channel: ' + channelNum, message='This Channel has been added to your bookmarks.')
######################################################################################
# Removes a Channel to the bookmarks list using the title as a key for the url
	
@route(PREFIX + "/removebookmark")
def RemoveBookmark(title, channelNum, url):
	
	#url = Dict[title]
	#Log("url remove-----------" + str(url))
	Dict[title] = 'removed'
	Dict[channelNum] = 'removed'
	Dict.Save()
	return ObjectContainer(header='Channel: '+channelNum, message='This Channel has been removed from your bookmarks.')	
######################################################################################
# Clears the Dict that stores the bookmarks list
	
@route(PREFIX + "/clearbookmarks")
def ClearBookmarks():

	for channelNum in Dict:
		url = Dict[channelNum]
		if url <> 'removed':
			Dict[channelNum] = 'removed'
			#Log("url remove-----------" + str(url))
	Dict.Save()
	return ObjectContainer(header="My Bookmarks", message='Your bookmark list will be cleared soon.')