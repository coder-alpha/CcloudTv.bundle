######################################################################################
#
#	CcloudTv
#
######################################################################################
import re, urllib, common, updater
import datetime as DT

# Set global variables
TITLE = common.TITLE
PREFIX = common.PREFIX
ART = "art-default.jpg"
ICON = "icon-ccloudtv.png"
ICON_LIST = "icon-list.png"
ICON_SEARCH = "icon-search.png"
ICON_SERIES = "icon-series.png"
ICON_SERIES_UNAV = "icon-series-unav.png"
ICON_AUDIO = "icon-audio.png"
ICON_QUEUE = "icon-queue.png"
ICON_PAGE = "icon-page.png"
ICON_PREFS = "icon-prefs.png"
ICON_UPDATE = "icon-update.png"

BASE_URL = ""
DEV_URL = "/ch/l/tv"

# using dictionary for temp. storing channel listing
Dict['items_dict'] = {}
DISABLED_NAMES = ['shspiderman']

LIST_VIEW_CLIENTS = ['Android','iOS']

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
	
	oc = ObjectContainer(title2=TITLE)
	ChHelper = ' (Refresh List)'
	ChHelper2 = ' (Initialize this Channel List once before Search, Search Queue and Bookmark menu are made available)'

	if Dict['items_dict'] <> {}:
		ChHelper = ''
		ChHelper2 = ' - Listing retrieved'
	oc.add(DirectoryObject(key = Callback(ShowMenu, title = 'Channels'), title = 'Channels' + ChHelper, summary = 'Channels' + ChHelper2, thumb = R(ICON)))
	
	# preCache
	if Prefs['use_precache']:
		try:
			webUrl = Prefs['web_url']
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
			
	oc.add(DirectoryObject(key = Callback(updater.menu, title='Update Plugin'), title = 'Update Plugin', thumb = R(ICON_UPDATE)))
	oc.add(PrefsObject(title = 'Preferences', thumb = R(ICON_PREFS)))
	return oc

@route(PREFIX + "/showMenu")
def ShowMenu(title):

	oc = ObjectContainer(title2=title)
	
	abortBool = RefreshListing(False)
	if abortBool:
		return ObjectContainer(header=title, message='No Channels Available. Please check website URL under Channel Preferences !')

	oc.add(DirectoryObject(key = Callback(DisplayList, title='List View'), title = 'List View', thumb = R(ICON_PAGE)))
	oc.add(DirectoryObject(key = Callback(DisplayPage, title='Page View', iRange=0), title = 'Page View', thumb = R(ICON_PAGE)))
	oc.add(DirectoryObject(key = Callback(DisplayPageList, title='Page List'), title = 'Page List', thumb = R(ICON_PAGE)))
	oc.add(InputDirectoryObject(key = Callback(Search), thumb = R(ICON_SEARCH), title='Search', summary='Search Channel', prompt='Search for...'))
	oc.add(DirectoryObject(key = Callback(SearchQueueMenu, title = 'Search Queue'), title = 'Search Queue', summary='Search using saved search terms', thumb = R(ICON_SEARCH)))
	oc.add(DirectoryObject(key = Callback(Bookmarks, title='My Channel Bookmarks'), title = 'My Channel Bookmarks', thumb = R(ICON_QUEUE)))
	oc.add(DirectoryObject(key = Callback(Pins, title='My Channel Pins'), title = 'My Channel Pins', thumb = R(ICON_QUEUE)))
	oc.add(DirectoryObject(key = Callback(RefreshListing, doRefresh=True), title = 'Refresh Channels', thumb = R(ICON)))
	
	return oc
	
@route(PREFIX + "/refreshlisting")
def RefreshListing(doRefresh):

	abortBool = True
	webUrl = Prefs['web_url']
	
	if webUrl <> None and webUrl.startswith('http'):
		if Dict['items_dict'] <> {} and not doRefresh:
			return False
		BASE_URL = webUrl + DEV_URL
		try:
			page_data = HTTP.Request(BASE_URL).content
			page_elems = HTML.ElementFromString(page_data)
			page_data = ''
			
			fetch_urls = page_elems.xpath(".//div[@class='table-title']//script//@src")
			for eachFetchUrl in fetch_urls:
				eachFetchUrl = GetRedirector(eachFetchUrl)
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
			
			today = DT.date.today()
			week_ago = today - DT.timedelta(days=7)
			
			for eachCh in channels:
				channelNum = eachCh.xpath(".//td[@class='text-center']//a//text()")[0]
				channelUrl = eachCh.xpath(".//td[@class='text-left']//a//@href")[0]
				channelDesc = ' '
				try:
					channelId0 = channelUrl.split('/')
					channelId = channelId0[len(channelId0)-1].replace('tv','')
					srcStr = 'documentgetElementById'+channelId+'textContent'
					#Log("srcStr----------" + srcStr)
				except:
					pass
					
				try:
					channelDesc = eachCh.xpath(".//td[@class='text-left']//a//text()")[0]
				except:
					pass

				try:
					channelDesc = re.findall(srcStr+'(.*?);', page_data, re.S)[0]
					#Log("channelDesc----------" + channelDesc)
				except:
					pass
				
				if channelDesc == None or channelDesc == 'Loading...' or channelDesc == ' ' or channelDesc == '':
					channelDesc = unicode('Undefined Channel: ' + channelNum)
					
				#Log("channelDesc----------" + channelDesc)
				# get update date and used DirectoryObject tagline for sort feature
				dateStr = getDate(channelDesc,week_ago)
				
				Dict['items_dict'][count] = {'channelNum': channelNum, 'channelDesc': channelDesc, 'channelUrl': channelUrl, 'channelDate': dateStr}
				count = count + 1
				
			abortBool = False
			if doRefresh:
				return ObjectContainer(header='Refresh Successful', message='New Channel listing retrieved !')
		except:
			BASE_URL = ""
			abortBool = True

	if doRefresh:
		return ObjectContainer(header='Refresh Failed', message='Channel listing could not be retrieved !')		
	return abortBool
	
@route(PREFIX + "/displaylist")
def DisplayList(title):
	oc = ObjectContainer(title2=title)

	abortBool = RefreshListing(False)
	if abortBool:
		return ObjectContainer(header=title, message='No Channels Available. Please check website URL under Channel Preferences !')
		
	if Client.Platform not in LIST_VIEW_CLIENTS:
		oc.add(InputDirectoryObject(key = Callback(Search), thumb = R(ICON_SEARCH), title='Search', summary='Search Channel', prompt='Search for...'))
	else:
		oc.add(InputDirectoryObject(key = Callback(Search), thumb = None, title='Search', summary='Search Channel', prompt='Search for...'))
	
	try:
		for count in range(0,len(Dict['items_dict'])):
			
			#items_dict[count] = {'channelNum': channelNum, 'channelDesc': channelDesc, 'channelUrl': channelUrl, 'channelDate': dateStr}
			
			channelNum = Dict['items_dict'][count]['channelNum']
			channelDesc = Dict['items_dict'][count]['channelDesc']
			channelUrl = Dict['items_dict'][count]['channelUrl']
			dateStr = Dict['items_dict'][count]['channelDate']
			
			#Log("channelUrl--------------" + str(channelUrl))
			title = unicode('Channel: ' + channelNum + ' (' + channelDesc + ')')
			
			#Log("title----------" + title)
			
			if Client.Platform not in LIST_VIEW_CLIENTS:
				oc.add(DirectoryObject(key = Callback(ChannelPage, url = channelUrl, title = title, channelDesc = channelDesc, channelNum=channelNum), tagline=dateStr, title = title, thumb = R(ICON_LIST)))
			else:
				oc.add(DirectoryObject(key = Callback(ChannelPage, url = channelUrl, title = title, channelDesc = channelDesc, channelNum=channelNum), tagline=dateStr, title = title, thumb = None))
			
		abortBool = False	
	except:
		abortBool = True
	
	if abortBool:
		return ObjectContainer(header=title, message='No Channels Available. Please check website URL under Channel Preferences !')
		
	if Prefs['use_datesort']:
		oc.objects.sort(key=lambda obj: obj.tagline, reverse=True)
	return oc

@route(PREFIX + "/displaypage")
def DisplayPage(title, iRange):
	oc = ObjectContainer(title2=title)
	
	abortBool = RefreshListing(False)
	if abortBool:
		return ObjectContainer(header=title, message='No Channels Available. Please check website URL under Channel Preferences !')
		
	if Client.Platform not in LIST_VIEW_CLIENTS:
		oc.add(InputDirectoryObject(key = Callback(Search), thumb = R(ICON_SEARCH), title='Search', summary='Search Channel', prompt='Search for...'))
	else:
		oc.add(InputDirectoryObject(key = Callback(Search), thumb = None, title='Search', summary='Search Channel', prompt='Search for...'))
	
	try:
		mCount=0
		for count in range(int(iRange),len(Dict['items_dict'])):
			
			#Dict['items_dict'][count] = {'channelNum': channelNum, 'channelDesc': channelDesc, 'channelUrl': channelUrl, 'channelDate': dateStr}
			
			channelNum = Dict['items_dict'][count]['channelNum']
			channelDesc = Dict['items_dict'][count]['channelDesc']
			channelUrl = Dict['items_dict'][count]['channelUrl']
			dateStr = Dict['items_dict'][count]['channelDate']
			
			#Log("channelUrl--------------" + str(channelUrl))
			title = unicode('Channel: ' + channelNum + ' (' + channelDesc + ')')
			
			#Log("title----------" + title)
			
			if Client.Platform not in LIST_VIEW_CLIENTS:
				oc.add(DirectoryObject(key = Callback(ChannelPage, url = channelUrl, title = title, channelDesc = channelDesc, channelNum=channelNum), tagline=dateStr, title = title, thumb = R(ICON_LIST)))
			else:
				oc.add(DirectoryObject(key = Callback(ChannelPage, url = channelUrl, title = title, channelDesc = channelDesc, channelNum=channelNum), tagline=dateStr, title = title, thumb = None))
			
			if mCount == 9:
				oc.add(DirectoryObject(key = Callback(DisplayPage, title='Page View', iRange=int(iRange)+10), title = 'More >>', thumb = R(ICON_PAGE)))
				break
			mCount = mCount+1
	except:
		return ObjectContainer(header=title, message='No Channels Available. Please check website URL under Channel Preferences !')
		
	return oc
	
@route(PREFIX + "/displaypagelist")
def DisplayPageList(title):
	oc = ObjectContainer(title2=title)
	
	abortBool = RefreshListing(False)
	if abortBool:
		return ObjectContainer(header=title, message='No Channels Available. Please check website URL under Channel Preferences !')
		
	if Client.Platform not in LIST_VIEW_CLIENTS:
		oc.add(InputDirectoryObject(key = Callback(Search), thumb = R(ICON_SEARCH), title='Search', summary='Search Channel', prompt='Search for...'))
	else:
		oc.add(InputDirectoryObject(key = Callback(Search), thumb = None, title='Search', summary='Search Channel', prompt='Search for...'))
	
	try:
		mCount=0
		sCh = '0'
		eCh = '9'
		pageCount=0
		for count in range(0,len(Dict['items_dict'])):
			mCount = mCount+1
			
			channelNum = Dict['items_dict'][count]['channelNum']
			if mCount == 1:
				sCh = channelNum
			
			if mCount == 10 or count == len(Dict['items_dict'])-1:
				oc.add(DirectoryObject(key = Callback(DisplayPage, title='Page View', iRange=(pageCount)), title = 'Channels: ' + str(sCh) + ' - ' + str(channelNum), thumb = R(ICON_PAGE)))
				mCount = 0
				pageCount=pageCount+10
	except:
		return ObjectContainer(header=title, message='No Channels Available. Please check website URL under Channel Preferences !')

	return oc
	
@route(PREFIX + '/getdate')
def getDate(channelDesc,week_ago):
	dateStr = 'Undefined'
	
	# tricky keep in seperate try
	try:
		dateStr = str(week_ago.month) + '/' + str(week_ago.day)
		channelUpDate = channelDesc.replace('Updated:','')
		channelUpDate = channelUpDate.replace('24/7','')
		if '/' in channelUpDate and '-' in channelUpDate:
			dateStr = channelUpDate.split('-')[0]
		elif '/' in channelUpDate and ':' in channelUpDate:
			dateStr = channelUpDate.split(':')[0]
	except:
		dateStr = str(week_ago.month) + '/' + str(week_ago.day)
		
	try:
		if ':' in dateStr:
			dateStr = dateStr.split(':')[0]
	except:
		dateStr = str(week_ago.month) + '/' + str(week_ago.day)
		
	try:
		dateStrS = dateStr.split('/')
		dateStr = str("%02d" % int(dateStrS[0])) + '/' + str("%02d" % int(dateStrS[1]))
	except:
		dateStr = 'Undefined'
		
	#Log("dateStr----------" + dateStr)
	return dateStr



@route(PREFIX + '/channelpage')
def ChannelPage(url, title, channelDesc, channelNum):

	oc = ObjectContainer(title2=title)
	
	try:
		#Log("----------- url ----------------")
		#Log(url)
		furl = GetRedirector(url)
		oc.add(CreateVideoClipObject(
			url = furl,
			title = title,
			thumb = GetChannelThumb(furl),
			summary = channelDesc))
	except:
		url = ""
	
	if CheckBookmark(channelNum=channelNum,url=url):
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
	if CheckPin(url=url):
		oc.add(DirectoryObject(
			key = Callback(RemovePin, url = url),
			title = "Remove Pin",
			summary = 'Removes the current Channel from the Pin list',
			thumb = R(ICON_QUEUE)
		))
	else:
		oc.add(DirectoryObject(
			key = Callback(AddPin, channelNum = channelNum, url = url, channelDesc = channelDesc),
			title = "Pin Channel",
			summary = 'Adds the current Channel to the Pin list',
			thumb = R(ICON_QUEUE)
		))
	
	abortBool = RefreshListing(False)
	if not abortBool:
		oc.add(InputDirectoryObject(key = Callback(Search), thumb = R(ICON_SEARCH), title='Search', summary='Search Channel', prompt='Search for...'))	
	return oc

####################################################################################################
# Gets the redirecting url for .m3u8 streams
@route(PREFIX + '/getchannelthumb')
def GetChannelThumb(url):

	thumb = R(ICON_SERIES_UNAV)
	try:
		if '.m3u8' in url:
			page = HTTP.Request(url).content
			if 'html' not in page and 'div' not in page and '#EXTM3U' in page:
				thumb = R(ICON_SERIES)
		elif '.m3u' in url:
			thumb = R(ICON_SERIES)
		elif '.aac' in url or '.mp3' in url:
			thumb = R(ICON_AUDIO)
	except:
		thumb = R(ICON_SERIES_UNAV)

	return thumb
	
####################################################################################################
# Gets the redirecting url for .m3u8 streams
@route(PREFIX + '/getredirector')
def GetRedirector(url):

	redirectUrl = url
	try:
		if '.m3u8' not in url and '.mp3' not in url and '.aac' not in url and '.m3u' not in url:
			page = urllib.urlopen(url)
			redirectUrl = page.geturl()
	except:
		redirectUrl = url
			
	#Log("Redirecting url ----- : " + redirectUrl)
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
def CreateVideoClipObject(url, title, thumb, summary, inc_container = False):
		
	#Log("CreateVideoClipObject--------------" + str(url))
	vco = ''
	if '.mp3' in url or '.aac' in url:
		container = Container.MP4
		audio_codec = AudioCodec.AAC
		
		if '.mp3' in url:
			container = 'mp3'
			audio_codec = AudioCodec.MP3
		elif '.aac' in url:
			container = 'aac'
			audio_codec = AudioCodec.AAC
			
		vco = TrackObject(
			key = Callback(CreateVideoClipObject, url = url, title = title, thumb = thumb, summary = summary, inc_container = True),
			rating_key = url,
			title = title,
			thumb = thumb,
			summary = summary,
			items = [
				MediaObject(
					parts = [
						PartObject(key=url)
					],
					container = container,
					audio_codec = audio_codec,
					audio_channels = 2
				)
			]
		)
	else:	
		vco = VideoClipObject(
			key = Callback(CreateVideoClipObject, url = url, title = title, thumb = thumb, summary = summary, inc_container = True),
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
					#container = container,
					#audio_codec = audio_codec,
					parts = [
						PartObject(
							key = GetVideoURL(url = url, live = True)
						)
					],
					optimized_for_streaming = True
				)
			]
		)

	if inc_container:
		return ObjectContainer(objects = [vco])
	else:
		return vco

####################################################################################################
def GetVideoURL(url, live):

	#url = 'http://wpc.c1a9.edgecastcdn.net/hls-live/20C1A9/cnn/ls_satlink/b_828.m3u8?Vd?u#bt!25'
	
	if '.m3u' in url and '.m3u8' not in url:
		#return HTTPLiveStreamURL(url=url) # does not work - retrieves only single segment
		return PlayVideoLive(url=url)
	elif url.startswith('rtmp') and Prefs['rtmp']:
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
@indirect
def PlayVideoLive(url):

	return HTTPLiveStreamURL(url=url)
####################################################################################################
@route(PREFIX + "/search")
def Search(query):

	oc = ObjectContainer(title2='Search Results')
	Dict['MyCustomSearch'+query] = query
	
	abortBool = RefreshListing(False)
	if abortBool:
		return ObjectContainer(header=title, message='No Channels Available. Please check website URL under Channel Preferences !')
		
	dict_len = len(Dict['items_dict'])
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
		for x in Dict['items_dict']:
			channelNum = Dict['items_dict'][x]['channelNum']
			channelDesc = Dict['items_dict'][x]['channelDesc']
			channelUrl = Dict['items_dict'][x]['channelUrl']
			dateStr = Dict['items_dict'][x]['channelDate']
			title = unicode('Channel: ' + channelNum + ' (' + channelDesc + ')')
			#Log("channelDesc--------- " + channelDesc)
			
			if query.lower() in channelDesc.lower() or query == channelNum:
				oc.add(DirectoryObject(key = Callback(ChannelPage, url = channelUrl, title = title, channelDesc = channelDesc, channelNum=channelNum), tagline=dateStr, title = title, thumb = R(ICON_LIST)))
			elif '~' in query and int(channelNum) > start-1 and int(channelNum) < end+1:
				oc.add(DirectoryObject(key = Callback(ChannelPage, url = channelUrl, title = title, channelDesc = channelDesc, channelNum=channelNum), tagline=dateStr, title = title, thumb = R(ICON_LIST)))
	except:
		return ObjectContainer(header='Search Results', message='No Channels Available. Please check website URL !')
	
	if len(oc) == 0:
		return ObjectContainer(header='Search Results', message='No Channels Available based on Search query')
		
	if Prefs['use_datesort']:
		oc.objects.sort(key=lambda obj: obj.tagline, reverse=True)
	else:	
		oc.objects.sort(key=lambda obj: obj.title)
		
	Dict['items_dict'] = {}
	Dict.Save()
	abortBool = RefreshListing(False)
	
	return oc

######################################################################################
@route(PREFIX + "/searchQueueMenu")
def SearchQueueMenu(title):
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
			if '~' in query:
				oc2.add(DirectoryObject(key = Callback(Search, query = query), title = query, thumb = R(ICON_PAGE)))
			else:
				oc2.add(DirectoryObject(key = Callback(Search, query = query), title = query, thumb = R(ICON_SEARCH)))
		

	return oc2	
	
######################################################################################
# Clears the Dict that stores the search list
	
@route(PREFIX + "/clearsearches")
def ClearSearches():

	Dict['items_dict'] = {}
	for each in Dict:
		if 'MyCustomSearch' in each:
			Dict[each] = 'removed'
	Dict.Save()
	abortBool = RefreshListing(False)
	return ObjectContainer(header="Search Queue", message='Your Search Queue list will be cleared soon.')
	
######################################################################################
# Loads bookmarked shows from Dict.  Titles are used as keys to store the show urls.

@route(PREFIX + "/bookmarks")	
def Bookmarks(title):

	oc = ObjectContainer(title1 = title)
	
	abortBool = RefreshListing(False)
	if abortBool:
		return ObjectContainer(header=title, message='No Channels Available. Please check website URL under Channel Preferences !')
		
	dict_len = len(Dict['items_dict'])
	if dict_len == 0:
		return ObjectContainer(header='Bookmarks', message='No Channels loaded ! Channel list needs to be initialized first.')
	try:
		for each in Dict:
			for x in Dict['items_dict']:
				channelNum = Dict['items_dict'][x]['channelNum']
				channelDesc = Dict['items_dict'][x]['channelDesc']
				channelUrl = Dict['items_dict'][x]['channelUrl']
				dateStr = Dict['items_dict'][x]['channelDate']
				title = 'Channel: ' + channelNum + ' (' + channelDesc + ')'
				#Log("channelDesc--------- " + str(channelDesc))
				
				if channelNum == each and Dict[each] <> 'removed' and 'MyCustomSearch' not in each:
					oc.add(DirectoryObject(key = Callback(ChannelPage, url = channelUrl, title = title, channelDesc = channelDesc, channelNum=channelNum), tagline=dateStr, title = title, thumb = R(ICON_LIST)))
	except:
		return ObjectContainer(header='Bookmarks', message='No Channels Available. Please check website URL !')
	
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
	
	if Prefs['use_datesort']:
		oc.objects.sort(key=lambda obj: obj.tagline, reverse=True)
	else:	
		oc.objects.sort(key=lambda obj: obj.title)
	return oc

######################################################################################
# Checks a show to the bookmarks list using the title as a key for the url
@route(PREFIX + "/checkbookmark")	
def CheckBookmark(channelNum, url):
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
	Dict['items_dict'] = {}
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
	Dict['items_dict'] = {}
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
	Dict['items_dict'] = {}
	Dict.Save()
	return ObjectContainer(header="My Bookmarks", message='Your bookmark list will be cleared soon.')
	
######### PINS #############################################################################
# Checks a show to the bookmarks list using the title as a key for the url
@route(PREFIX + "/checkpin")	
def CheckPin(url):

	url = GetRedirector(url)
	bool = False
	url = Dict['Plex-Pin-Pin'+url]
	#Log("url check-----------" + str(url))
	if url != None and url <> 'removed':
		bool = True
	
	return bool

######################################################################################
# Adds a Channel to the bookmarks list using the title as a key for the url
	
@route(PREFIX + "/addpin")
def AddPin(channelNum, url, channelDesc):
	
	url = GetRedirector(url)
	Dict['Plex-Pin-Pin'+url] = channelNum + 'Key4Split' + channelDesc + 'Key4Split' + url
	
	#Log("url add-----------" + str(url))
	Dict['items_dict'] = {}
	Dict.Save()
	return ObjectContainer(header= 'Channel: ' + channelNum, message='This Channel has been added to your Pins.')
######################################################################################
# Removes a Channel to the bookmarks list using the title as a key for the url
	
@route(PREFIX + "/removepins")
def RemovePin(url):
	
	channelNum = 'Undefined'
	url = GetRedirector(url)
	#url = Dict[title]
	#Log("url remove-----------" + str(url))
	keys = Dict['Plex-Pin-Pin'+url]
	if 'Key4Split' in keys:
		values = keys.split('Key4Split')
		channelNum = values[0]
		Dict['Plex-Pin-Pin'+url] = 'removed'
		Dict['items_dict'] = {}
		Dict.Save()
	return ObjectContainer(header='Channel: '+channelNum, message='This Channel has been removed from your Pins.')	
######################################################################################
# Clears the Dict that stores the bookmarks list
	
@route(PREFIX + "/clearpins")
def ClearPins():

	for each in Dict:
		keys = Dict[each]
		if 'Key4Split' in keys:
			Dict[each] = 'removed'
			#Log("url remove-----------" + str(url))
	Dict['items_dict'] = {}
	Dict.Save()
	return ObjectContainer(header="My Pins", message='Your Pins list will be cleared soon.')
	
######################################################################################
# Pins
@route(PREFIX + "/pins")	
def Pins(title):

	oc = ObjectContainer(title1 = title)
	
	abortBool = RefreshListing(False)
	if abortBool:
		return ObjectContainer(header=title, message='No Channels Available. Please check website URL under Channel Preferences !')

	try:
		for each in Dict:
			keys = Dict[each]
			if 'Key4Split' in keys:
				values = keys.split('Key4Split')
				channelNum = values[0]
				channelDesc = values[1]
				channelUrl = values[2]
				title = 'Channel: ' + channelNum + ' (' + channelDesc + ')'
				#Log("channelDesc--------- " + str(channelDesc))
				
				if 'removed' not in channelUrl:
					oc.add(DirectoryObject(key = Callback(ChannelPage, url = channelUrl, title = title, channelDesc = channelDesc, channelNum=channelNum), title = title, thumb = R(ICON_LIST)))
	except:
		return ObjectContainer(header='Pins', message='No Channels Available. Please check website URL !')
	
	#add a way to clear pin list
	oc.add(DirectoryObject(
		key = Callback(ClearPins),
		title = "Clear All Pins",
		thumb = R(ICON_QUEUE),
		summary = "CAUTION! This will clear your entire Pins list!"
		)
	)
	
	if len(oc) == 1:
		return ObjectContainer(header='Pins', message='No Pins Available')
	
	oc.objects.sort(key=lambda obj: obj.title)
	return oc