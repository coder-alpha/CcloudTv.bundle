######################################################################################
#
#	CcloudTv
#
######################################################################################
import re, urllib, common, updater
import myxmltvparser
import datetime as DT
from datetime import datetime

# Set global variables
TITLE = common.TITLE
PREFIX = common.PREFIX
ART = "art-default.jpg"
ICON = "icon-ccloudtv.png"
ICON_VIDEO = "icon-video.png"
ICON_AUDIO = "icon-audio.png"
ICON_SERIES = "icon-series.png"
ICON_SERIES_UNAV = "icon-series-unav.png"
ICON_GENRES = "icon-genres.png"
ICON_GENRE = "icon-genre.png"
ICON_LANGUAGES = "icon-languages.png"
ICON_COUNTRIES = "icon-countries.png"
ICON_LISTVIEW = "icon-listview.png"
ICON_PAGE = "icon-paged.png"
ICON_PAGELIST = "icon-pagelist.png"
ICON_NEXT = "icon-next.png"
ICON_SEARCH = "icon-search.png"
ICON_SEARCH_QUEUE = "icon-search-queue.png"
ICON_PIN = "icon-pin.png"
ICON_BOOKMARK = "icon-bookmark.png"
ICON_LOCK = "icon-lock.png"
ICON_UNLOCK = "icon-unlock.png"
ICON_PREFS = "icon-prefs.png"
ICON_UPDATE = "icon-update.png"
ICON_UPDATE_NEW = "icon-update-new.png"
ICON_RECENT = "icon-recent.png"

BASE_URL = ""

# using dictionary for temp. storing channel listing
Dict['items_dict'] = {}

# set clients thats should display content as list
LIST_VIEW_CLIENTS = ['Android','iOS']

# genre listing
GENRE_ARRAY = []

# language listing
LANGUAGE_ARRAY = []
LANGUAGE_ARRAY_POP = ['English','Spanish','Hindi','Russian']
# country listing
COUNTRY_ARRAY = []
COUNTRY_ARRAY_POP = ['US','UK','IN','RU']

GENRE_SYNM_SPORTS = ['Sport']
GENRE_SYNM_ENTERTAINMENT = ['Entertainemt']
GENRE_SYNM_ENTERTAINMENT_NEWS = ['Entertainemt/News']

CCLOUDTV_DB_URL = "http://tiny.cc/Plex"
FALLBACK_STATIC_DB_URL = 'http://tiny.cc/PlexFallback'

######################################################################################

def Start():

	ObjectContainer.title1 = TITLE
	ObjectContainer.art = R(ART)
	DirectoryObject.thumb = R(ICON_SERIES)
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
	
	oc.add(DirectoryObject(key = Callback(Pins, title='My Channel Pins'), title = 'My Channel Pins', thumb = R(ICON_PIN)))
	
	oc.add(PrefsObject(title = 'Preferences', thumb = R(ICON_PREFS)))
	oc.add(DirectoryObject(key = Callback(DefineAccessControl, title='Access Control'), title = 'Access Control', summary='Set/Remove Temporary Access', thumb = R(ICON_LOCK)))
	
	if updater.update_available()[0]:
		oc.add(DirectoryObject(key = Callback(updater.menu, title='Update Plugin'), title = 'Update (New Available)', thumb = R(ICON_UPDATE_NEW)))
	else:
		oc.add(DirectoryObject(key = Callback(updater.menu, title='Update Plugin'), title = 'Update (Running Latest)', thumb = R(ICON_UPDATE)))
	
	return oc
	
@route(PREFIX + "/updatecheck")
def UpdateCheck():
	oc = ObjectContainer(title2='Update')
	if VerifyAccess():
		if updater.update_available()[0]:
			oc.add(DirectoryObject(key = Callback(updater.menu, title='Update Plugin'), title = 'Update (New Available)', thumb = R(ICON_UPDATE_NEW)))
		else:
			oc.add(DirectoryObject(key = Callback(updater.menu, title='Update Plugin'), title = 'Update (Running Latest)', thumb = R(ICON_UPDATE)))
	else:
		if updater.update_available()[0]:
			oc.add(DirectoryObject(key = Callback(NoAccess), title = 'Update (New Available)', thumb = R(ICON_UPDATE_NEW)))
		else:
			oc.add(DirectoryObject(key = Callback(NoAccess), title = 'Update (Running Latest)', thumb = R(ICON_UPDATE)))
	return oc
	
@route(PREFIX + "/verifyaccess")
def VerifyAccess():
	if not Prefs['show_adult'] and Dict['AccessPin'] != Prefs['access_pin']:
		return False
	else:
		return True
	
@route(PREFIX + "/defineaccesscontrol")
def DefineAccessControl(title):
	oc = ObjectContainer(title2=title)
	oc.add(InputDirectoryObject(key = Callback(SetTempKey), thumb = R(ICON_UNLOCK), title='Set Access Key', summary='Set Temporary Access Key', prompt='Set Access..'))
	oc.add(DirectoryObject(key = Callback(ClearAccessKey), thumb = R(ICON_LOCK), title='Clear Access Key', summary='Clear Temporary Access Key'))
	return oc
	
@route(PREFIX + "/settempkey")
def SetTempKey(query):
	Dict['items_dict'] = {}
	Dict['AccessPin'] = query;
	Dict.Save()
	return ObjectContainer(header='Access Key', message='Your Temporary Access Key ' + query + ' has been saved.')

@route(PREFIX + "/noaccess")
def NoAccess():
	return ObjectContainer(header='Update Plugin', message='Requires Parental Access Control. Enable via Channel Preferences or set under Access Control Menu first.')
	
@route(PREFIX + "/clearaccesskey")
def ClearAccessKey():
	Dict['items_dict'] = {}
	Dict['AccessPin'] = '';
	Dict.Save()
	return ObjectContainer(header='Access Key', message='Your Temporary Access Key has been cleared.')
	
@route(PREFIX + "/showMenu")
def ShowMenu(title):

	oc = ObjectContainer(title2=title)
	
	abortBool = RefreshListing(False)
	if abortBool:
		return ObjectContainer(header=title, message='No Channels Available. Please check website URL under Channel Preferences !')

	oc.add(DirectoryObject(key = Callback(DisplayList, title='List View'), title = 'List View', thumb = R(ICON_LISTVIEW)))
	oc.add(DirectoryObject(key = Callback(DisplayPage, title='Page View', iRange=0), title = 'Page View', thumb = R(ICON_PAGE)))
	oc.add(DirectoryObject(key = Callback(DisplayPageList, title='Page List'), title = 'Page List', thumb = R(ICON_PAGELIST)))
	oc.add(DirectoryObject(key = Callback(DisplayGenreMenu, title='Category'), title = 'Category', thumb = R(ICON_GENRES)))
	oc.add(DirectoryObject(key = Callback(DisplayLanguageMenu, title='Language'), title = 'Language', thumb = R(ICON_LANGUAGES)))
	oc.add(DirectoryObject(key = Callback(DisplayCountryMenu, title='Country'), title = 'Country', thumb = R(ICON_COUNTRIES)))
	oc.add(DirectoryObject(key = Callback(ShowRecentMenu, title='Recent'), title = 'Recent', thumb = R(ICON_RECENT)))
	oc.add(InputDirectoryObject(key = Callback(Search), thumb = R(ICON_SEARCH), title='Search', summary='Search Channel', prompt='Search for...'))
	oc.add(DirectoryObject(key = Callback(SearchQueueMenu, title = 'Search Queue'), title = 'Search Queue', summary='Search using saved search terms', thumb = R(ICON_SEARCH_QUEUE)))
	oc.add(DirectoryObject(key = Callback(Bookmarks, title='My Channel Bookmarks'), title = 'My Channel Bookmarks', thumb = R(ICON_BOOKMARK)))
	oc.add(DirectoryObject(key = Callback(RefreshListing, doRefresh=True), title = 'Refresh Channels', thumb = R(ICON)))
	
	return oc
	
@route(PREFIX + "/refreshlisting")
def RefreshListing(doRefresh):

	abortBool = True
	webUrl = CCLOUDTV_DB_URL
	try:
		webUrl = GetRedirector(CCLOUDTV_DB_URL)
	except:
		pass
		
	webUrl2 = Prefs['web_url_priv']
	try:
		if 'http' not in webUrl2:
			webUrl2 = FALLBACK_STATIC_DB_URL
			
		webUrl2 = GetRedirector(webUrl2)
		page_data = HTTP.Request(webUrl2).content
		
		if '.m3u8' in page_data:
			pass
		else:
			webUrl2 = FALLBACK_STATIC_DB_URL
	except:
		webUrl2 = FALLBACK_STATIC_DB_URL
		
	try:
		webUrl2 = GetRedirector(webUrl2)
	except:
		pass
		
	XML_SOURCE = ""
	try:
		if Prefs['use_epg'] and not Prefs['epg_guide'].startswith('http://'):
			XML_URL = Resource.Load(Prefs['epg_guide'], binary = True)
			XML_SOURCE = HTML.ElementFromURL(XML_URL)
			myxmltvparser.initchannels(XML_SOURCE)
	except:
		pass
		
	if webUrl <> None and webUrl.startswith('http'):
		if Dict['items_dict'] <> {} and not doRefresh:
			return False
		try:
			Dict['items_dict'] = {}
			page_data = ""
			page_data1 = ""
			page_data2 = ""
			try:
				page_data1 = HTTP.Request(webUrl).content
			except:
				pass
			try:
				page_data2 = HTTP.Request(webUrl2).content
			except:
				pass
			try:
				page_data = page_data1 + "||" + page_data2
			except:
				pass
				
			page_data = page_data.strip()
			channels = page_data.split('||')

			count = 0
			now = str(datetime.now()).replace(':','').replace('-','').replace(' ', '')[0:14]
			today = DT.date.today()
			week_ago = today - DT.timedelta(days=7)
			del GENRE_ARRAY[:]
			del LANGUAGE_ARRAY[:]
			del COUNTRY_ARRAY[:]
			
			lastchannelNum = '-1'
			
			for eachCh in channels:
				skip = False
				if eachCh.startswith('//'):
					pass
				else:
					chMeta = eachCh.split(';')
					channelNum = ' '
					channelUrl = ' '
					logoUrl = None
					channelDesc = ' '
					desc = 'Unknown'
					country = 'Unknown'
					lang = 'Unknown'
					genre = 'Unknown'
					views = 'Unknown'
					active = 'Unknown'
					onair = 'Unknown'
					channelID = 'Unknown'
					dateStrM = channelDesc
					
					try:
						if chMeta[0] <> None:
							channelNum = chMeta[0].strip()
							if channelNum == '!':
								channelNum = '00'
							
							if int(channelNum) <= int(lastchannelNum):
								channelNum = str(int(lastchannelNum)+1)
							
							lastchannelNum = channelNum
							channelNum = "{0:0=4d}".format(int(channelNum))
						if chMeta[1] <> None:
							if 'Help' in chMeta[1] and 'IPTV' in chMeta[1]:
								channelDesc = ' '
								skip = True
							else:
								channelDesc = unicode(chMeta[1])
						if chMeta[2] <> None:
							genre = chMeta[2].strip()
							genre = FixGenre(genre)
							if genre in GENRE_ARRAY:
								pass
							elif genre != '!':
								GENRE_ARRAY.append(genre)
						if chMeta[3] <> None:
							country = chMeta[3]
							country = FixCountry(country)
							
							if country in COUNTRY_ARRAY:
								pass
							elif country != '!':
								COUNTRY_ARRAY.append(country)
						if chMeta[4] <> None:
							lang = chMeta[4]
							lang = FixLanguage(lang)
							
							if lang in LANGUAGE_ARRAY:
								pass
							elif lang != '!':
								LANGUAGE_ARRAY.append(lang)
						if chMeta[5] <> None:
							channelUrl = chMeta[5]
						if len(chMeta) >= 7 and chMeta[6] <> None:
							logoUrl = chMeta[6]
						if len(chMeta) >= 8 and chMeta[7] <> None:
							dateStrM = chMeta[7]
							
						desc = channelDesc
					except:
						pass
					
					if channelDesc == None or channelDesc == 'Loading...' or channelDesc == ' ' or channelDesc == '':
						channelDesc = unicode('Undefined Channel: ' + channelNum)
					
					if Prefs['use_epg']:
						epgInfo = myxmltvparser.epgguide(channelID, now)
					else:
						epgInfo = 'EPG Not Yet Implemented'
						
					#Log("channelDesc----------" + channelDesc)
					# get update date and used DirectoryObject tagline for sort feature
					dateStr = ' '
					try:
						dateStr = getDate(dateStrM,week_ago)
					except:
						pass
						
					mature = 'N'
					try:
						mature = isAdultChannel(channelDesc)
					except:
						pass
						
					if mature == 'N':
						if genre == 'Adult' or genre == "Public-Adult":
							mature = 'Y'
					
					try:
						if not skip:
							Dict['items_dict'][count] = {'channelNum': channelNum, 'channelDesc': channelDesc, 'channelUrl': channelUrl, 'channelDate': dateStr, 'desc': desc, 'country': country, 'lang': lang, 'genre': genre, 'views': views, 'active': active, 'onair': onair, 'mature': mature, 'epg': epgInfo, 'logoUrl': logoUrl}
							count = count + 1
					except:
						pass
				
			abortBool = False
			if doRefresh:
				return ObjectContainer(header='Refresh Successful', message= lastchannelNum + ' Channels retrieved !')
		except:
			BASE_URL = ""
			abortBool = True

	if doRefresh:
		return ObjectContainer(header='Refresh Failed', message='Channel listing could not be retrieved !')		
	return abortBool
	
@route(PREFIX + "/showRecentMenu")
def ShowRecentMenu(title):

	oc = ObjectContainer(title2=title)
	
	abortBool = RefreshListing(False)
	if abortBool:
		return ObjectContainer(header=title, message='No Channels Available. Please check website URL under Channel Preferences !')

	oc.add(DirectoryObject(key = Callback(RecentListing, title='Today'), title = 'Today', thumb = R(ICON_RECENT)))
	oc.add(DirectoryObject(key = Callback(RecentListing, title='Since Yesterday'), title = 'Since Yesterday', thumb = R(ICON_RECENT)))
	oc.add(DirectoryObject(key = Callback(RecentListing, title='Since Last 3 Days'), title = 'Since Last 3 Days', thumb = R(ICON_RECENT)))
	oc.add(DirectoryObject(key = Callback(RecentListing, title='Since Last 7 Days'), title = 'Since Last 7 Days', thumb = R(ICON_RECENT)))
	oc.add(DirectoryObject(key = Callback(RecentListing, title='Since Last 30 Days'), title = 'Since Last 30 Days', thumb = R(ICON_RECENT)))
	return oc
	
@route(PREFIX + "/RecentListing")
def RecentListing(title):
	oc = ObjectContainer(title2=title)
	
	filterD = DT.date.today()
	if title == 'Since Yesterday':
		filterD = filterD - DT.timedelta(days=1)
	elif title == 'Since Last 3 Days':
		filterD = filterD - DT.timedelta(days=3)
	elif title == 'Since Last 7 Days':
		filterD = filterD - DT.timedelta(days=7)
	elif title == 'Since Last 30 Days':
		filterD = filterD - DT.timedelta(days=30)
	filterDate = datetime.combine(filterD, datetime.min.time())
	
	abortBool = RefreshListing(False)
	if abortBool:
		return ObjectContainer(header=title, message='No Channels Available. Please check website URL under Channel Preferences !')
		
	if Client.Platform not in LIST_VIEW_CLIENTS:
		oc.add(InputDirectoryObject(key = Callback(Search), thumb = R(ICON_SEARCH), title='Search', summary='Search Channel', prompt='Search for...'))
	else:
		oc.add(InputDirectoryObject(key = Callback(Search), thumb = None, title='Search', summary='Search Channel', prompt='Search for...'))
	
	try:
		for count in range(0,len(Dict['items_dict'])):
			
			channelNum = Dict['items_dict'][count]['channelNum']
			channelDesc = Dict['items_dict'][count]['channelDesc']
			channelUrl = Dict['items_dict'][count]['channelUrl']
			dateStr = Dict['items_dict'][count]['channelDate']
			#Log("Date===========  " + dateStr)
			dateStrA = dateStr.split('/')
			dateObj = datetime(int(dateStrA[2]), int(dateStrA[0]), int(dateStrA[1]))
			
			title = unicode(channelDesc)
			
			desc = 'Unknown'
			country = 'Unknown'
			lang = 'Unknown'
			genre = 'Unknown'
			views = 'Unknown'
			active = 'Unknown'
			onair = 'Unknown'
			mature = 'Unknown'
			logoUrl = None
			
			try:
				logoUrl = Dict['items_dict'][count]['logoUrl']
				mature = Dict['items_dict'][count]['mature']
				desc = Dict['items_dict'][count]['desc']
				country = Dict['items_dict'][count]['country']
				lang = Dict['items_dict'][count]['lang']
				genre = Dict['items_dict'][count]['genre']
				views = Dict['items_dict'][count]['views']
				active = Dict['items_dict'][count]['active']
				onair = Dict['items_dict'][count]['onair']
			except:
				pass
			
			abortBool2 = ChannelFilters(active=active, onair=onair, lang=lang, country=country, mature=mature)
			
			summaryStr = '#: ' + channelNum + ' | '+ desc + ' | Genre:' + genre + ' | Country:' + country + ' | Language:' + lang + ' | ' + views + ' Views'
				
			#Log("Date===========  " + dateStr + " = " + str(dateObj) + " = " + str(filterDate))
				
			if not abortBool2 and dateObj >= filterDate:
				if Client.Platform not in LIST_VIEW_CLIENTS:
					oc.add(DirectoryObject(key = Callback(ChannelPage, url = channelUrl, title = title, channelDesc = summaryStr, channelNum=channelNum, logoUrl=logoUrl), tagline=dateStr, summary = summaryStr, title = title, thumb = Resource.ContentsOfURLWithFallback(url = logoUrl, fallback= R(ICON_SERIES))))
				else:
					oc.add(DirectoryObject(key = Callback(ChannelPage, url = channelUrl, title = title, channelDesc = summaryStr, channelNum=channelNum, logoUrl=logoUrl), tagline=dateStr, summary = summaryStr, title = title, thumb = None))
			
		abortBool = False	
	except:
		abortBool = True
	
	if abortBool:
		return ObjectContainer(header=title, message='No Channels Available. Please check website URL under Channel Preferences !')
		
	if Prefs['use_datesort']:
		oc.objects.sort(key=lambda obj: obj.tagline, reverse=True)
	return oc
	
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
			title = unicode(channelDesc)
			#Log("title----------" + title)
			
			desc = 'Unknown'
			country = 'Unknown'
			lang = 'Unknown'
			genre = 'Unknown'
			views = 'Unknown'
			active = 'Unknown'
			onair = 'Unknown'
			mature = 'Unknown'
			epgInfo = ''
			logoUrl = None
			
			try:
				logoUrl = Dict['items_dict'][count]['logoUrl']
				mature = Dict['items_dict'][count]['mature']
				desc = Dict['items_dict'][count]['desc']
				country = Dict['items_dict'][count]['country']
				lang = Dict['items_dict'][count]['lang']
				genre = Dict['items_dict'][count]['genre']
				views = Dict['items_dict'][count]['views']
				active = Dict['items_dict'][count]['active']
				onair = Dict['items_dict'][count]['onair']
				epgInfo = Dict['items_dict'][count]['epg']
			except:
				pass
			
			abortBool2 = ChannelFilters(active=active, onair=onair, lang=lang, country=country, mature=mature)
			
			summaryStr = '#: ' + channelNum + ' | '+ desc + ' | Genre:' + genre + ' | Country:' + country + ' | Language:' + lang
			if epgInfo != '':
				summaryStr = summaryStr + ' | ' + epgInfo
				
			if not abortBool2:
				if Client.Platform not in LIST_VIEW_CLIENTS:
					if logoUrl <> None:
						oc.add(DirectoryObject(key = Callback(ChannelPage, url = channelUrl, title = title, channelDesc = summaryStr, channelNum=channelNum, logoUrl=logoUrl), tagline=dateStr, summary = summaryStr, title = title, thumb = logoUrl))
					else:
						oc.add(DirectoryObject(key = Callback(ChannelPage, url = channelUrl, title = title, channelDesc = summaryStr, channelNum=channelNum, logoUrl=logoUrl), tagline=dateStr, summary = summaryStr, title = title, thumb = R(ICON_SERIES)))
				else:
					oc.add(DirectoryObject(key = Callback(ChannelPage, url = channelUrl, title = title, channelDesc = summaryStr, channelNum=channelNum, logoUrl=logoUrl), tagline=dateStr, summary = summaryStr, title = title, thumb = None))
			
		abortBool = False	
	except:
		abortBool = True
	
	if abortBool:
		return ObjectContainer(header=title, message='No Channels Available. Please check website URL under Channel Preferences !')
		
	if Prefs['use_datesort']:
		oc.objects.sort(key=lambda obj: obj.tagline, reverse=True)
	return oc

@route(PREFIX + "/displaygenremenu")
def DisplayGenreMenu(title):
	oc = ObjectContainer(title2=title)
	for genre in GENRE_ARRAY:
		if genre == 'Adult':
			if Prefs['show_adult'] or Dict['AccessPin'] == Prefs['access_pin']:
				oc.add(DirectoryObject(key = Callback(DisplayGenreLangConSort, titleGen=genre, type="Category"), title = genre, thumb = R(ICON_GENRE)))
		else:
			oc.add(DirectoryObject(key = Callback(DisplayGenreLangConSort, titleGen=genre, type="Category"), title = genre, thumb = R(ICON_GENRE)))
			
	oc.objects.sort(key=lambda obj: obj.title)
	return oc

@route(PREFIX + "/displaylanguagemenu")
def DisplayLanguageMenu(title):
	oc = ObjectContainer(title2=title)
	
	LastSaveLanguage = ' '
	if Dict['LastUsed'+title] <> None:
		LastSaveLanguage = Dict['LastUsed'+title]
		oc.add(DirectoryObject(key = Callback(DisplayGenreLangConSort, titleGen=LastSaveLanguage, type="Country"), title = LastSaveLanguage, thumb = R(ICON_GENRE)))
	for language in LANGUAGE_ARRAY_POP:
		if language != LastSaveLanguage:
			oc.add(DirectoryObject(key = Callback(DisplayGenreLangConSort, titleGen=language, type="Language"), title = language, thumb = R(ICON_GENRE)))
	for language in sorted(LANGUAGE_ARRAY):
		if language not in LANGUAGE_ARRAY_POP and language != LastSaveLanguage:
			oc.add(DirectoryObject(key = Callback(DisplayGenreLangConSort, titleGen=language, type="Language"), title = language, thumb = R(ICON_GENRE)))
			
	#oc.objects.sort(key=lambda obj: obj.title)
	return oc
	
@route(PREFIX + "/displaycountrymenu")
def DisplayCountryMenu(title):
	oc = ObjectContainer(title2=title)
	oc2 = []
	
	LastSaveCountry = ' '
	if Dict['LastUsed'+title] <> None:
		LastSaveCountry = Dict['LastUsed'+title]
		oc.add(DirectoryObject(key = Callback(DisplayGenreLangConSort, titleGen=LastSaveCountry, type="Country"), title = common.getCountryName(LastSaveCountry), thumb = R(ICON_GENRE)))
	for country in COUNTRY_ARRAY_POP:
		if country != LastSaveCountry:
			oc.add(DirectoryObject(key = Callback(DisplayGenreLangConSort, titleGen=country, type="Country"), title = common.getCountryName(country), thumb = R(ICON_GENRE)))
	for country in sorted(COUNTRY_ARRAY):
		if country not in COUNTRY_ARRAY_POP and country != LastSaveCountry:
			oc2.append(DirectoryObject(key = Callback(DisplayGenreLangConSort, titleGen=country, type="Country"), title = common.getCountryName(country), thumb = R(ICON_GENRE)))
	if len(oc2) > 0:
		for o in sorted(oc2, key=lambda obj: obj.title):
			oc.add(o)
			
	#oc.objects.sort(key=lambda obj: obj.title)
	return oc
	
@route(PREFIX + "/displaygenresort")
def DisplayGenreLangConSort(titleGen, type):

	if type == 'Country':
		oc = ObjectContainer(title2=common.getCountryName(titleGen))
	else:
		oc = ObjectContainer(title2=titleGen)
	abortBool = RefreshListing(False)
	
	if abortBool:
		return ObjectContainer(header=titleGen, message='No Channels Available. Please check website URL under Channel Preferences !')
		
	try:
		for count in range(0,len(Dict['items_dict'])):
			
			#items_dict[count] = {'channelNum': channelNum, 'channelDesc': channelDesc, 'channelUrl': channelUrl, 'channelDate': dateStr}
			
			channelNum = Dict['items_dict'][count]['channelNum']
			channelDesc = Dict['items_dict'][count]['channelDesc']
			channelUrl = Dict['items_dict'][count]['channelUrl']
			dateStr = Dict['items_dict'][count]['channelDate']
			
			#Log("channelUrl--------------" + str(channelUrl))
			title = unicode(channelDesc)
			#Log("title----------" + title)
			tkey = 'Unknown'
			desc = 'Unknown'
			country = 'Unknown'
			lang = 'Unknown'
			genre = 'Unknown'
			views = 'Unknown'
			active = 'Unknown'
			onair = 'Unknown'
			mature = 'Unknown'
			epgInfo = ''
			logoUrl = None
			try:
				logoUrl = Dict['items_dict'][count]['logoUrl']
			except:
				pass	
			try:
				mature = Dict['items_dict'][count]['mature']
				desc = Dict['items_dict'][count]['desc']
				country = Dict['items_dict'][count]['country']
				lang = Dict['items_dict'][count]['lang']
				genre = Dict['items_dict'][count]['genre']
				views = Dict['items_dict'][count]['views']
				active = Dict['items_dict'][count]['active']
				onair = Dict['items_dict'][count]['onair']
				epgInfo = Dict['items_dict'][count]['epg']
			except:
				pass
			
			if type == 'Category':
				tkey = genre
			elif type == 'Language':
				tkey = lang
			elif type == 'Country':
				tkey = country
			
			abortBool2 = ChannelFilters(active=active, onair=onair, lang=lang, country=country, mature=mature)
			
			summaryStr = '#: ' + channelNum + ' | '+ desc + ' | Genre:' + genre + ' | Country:' + country + ' | Language:' + lang
			#Log(summaryStr)
			if epgInfo != '':
				summaryStr = summaryStr + ' | ' + epgInfo
				
			if not abortBool2 and (titleGen == tkey or ('/' in tkey and titleGen in tkey.split('/'))):
				if Client.Platform not in LIST_VIEW_CLIENTS:
					if logoUrl <> None:
						oc.add(DirectoryObject(key = Callback(ChannelPage, url = channelUrl, title = title, channelDesc = summaryStr, channelNum=channelNum, logoUrl=logoUrl), tagline=dateStr, summary = summaryStr, title = title, thumb = logoUrl))
					else:
						oc.add(DirectoryObject(key = Callback(ChannelPage, url = channelUrl, title = title, channelDesc = summaryStr, channelNum=channelNum, logoUrl=logoUrl), tagline=dateStr, summary = summaryStr, title = title, thumb = R(ICON_SERIES)))
				else:
					oc.add(DirectoryObject(key = Callback(ChannelPage, url = channelUrl, title = title, channelDesc = summaryStr, channelNum=channelNum, logoUrl=logoUrl), tagline=dateStr, summary = summaryStr, title = title, thumb = None))
			
		abortBool = False	
	except:
		abortBool = True
	
	if abortBool:
		return ObjectContainer(header=title, message='No Channels Available. Please check website URL under Channel Preferences !')
		
	if Prefs['use_datesort']:
		oc.objects.sort(key=lambda obj: obj.tagline, reverse=True)
	else:	
		oc.objects.sort(key=lambda obj: obj.title)
	
	if Client.Platform not in LIST_VIEW_CLIENTS:
		oc.add(InputDirectoryObject(key = Callback(Search), thumb = R(ICON_SEARCH), title='Search', summary='Search Channel', prompt='Search for...'))
	else:
		oc.add(InputDirectoryObject(key = Callback(Search), thumb = None, title='Search', summary='Search Channel', prompt='Search for...'))
	
	Dict['LastUsed'+type] = titleGen
	Dict.Save()
	
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
			title = unicode(channelDesc)
			#Log("title----------" + title)
			
			desc = 'Unknown'
			country = 'Unknown'
			lang = 'Unknown'
			genre = 'Unknown'
			views = 'Unknown'
			active = 'Unknown'
			onair = 'Unknown'
			mature = 'Unknown'
			epgInfo = ''
			logoUrl = None
			
			try:
				logoUrl = Dict['items_dict'][count]['logoUrl']
			except:
				pass
			try:
				mature = Dict['items_dict'][count]['mature']
				desc = Dict['items_dict'][count]['desc']
				country = Dict['items_dict'][count]['country']
				lang = Dict['items_dict'][count]['lang']
				genre = Dict['items_dict'][count]['genre']
				views = Dict['items_dict'][count]['views']
				active = Dict['items_dict'][count]['active']
				onair = Dict['items_dict'][count]['onair']
				epgInfo = Dict['items_dict'][count]['epg']
			except:
				pass
			
			#Log("mature -----------------" + mature)
			abortBool2 = ChannelFilters(active=active, onair=onair, lang=lang, country=country, mature=mature)
			
			summaryStr = '#: ' + channelNum + ' | '+ desc + ' | Genre:' + genre + ' | Country:' + country + ' | Language:' + lang
			if epgInfo != '':
				summaryStr = summaryStr + ' | ' + epgInfo
			
			if not abortBool2:
				if Client.Platform not in LIST_VIEW_CLIENTS:
					if logoUrl <> None:
						oc.add(DirectoryObject(key = Callback(ChannelPage, url = channelUrl, title = title, channelDesc = summaryStr, channelNum=channelNum, logoUrl=logoUrl), tagline=dateStr, summary = summaryStr, title = title, thumb = logoUrl))
					else:
						oc.add(DirectoryObject(key = Callback(ChannelPage, url = channelUrl, title = title, channelDesc = summaryStr, channelNum=channelNum, logoUrl=logoUrl), tagline=dateStr, summary = summaryStr, title = title, thumb = R(ICON_SERIES)))
				else:
					oc.add(DirectoryObject(key = Callback(ChannelPage, url = channelUrl, title = title, channelDesc = summaryStr, channelNum=channelNum, logoUrl=logoUrl), tagline=dateStr, summary = summaryStr, title = title, thumb = None))
				
			if mCount == 9:
				oc.add(DirectoryObject(key = Callback(DisplayPage, title='Page View', iRange=int(iRange)+10), title = 'More >>', thumb = R(ICON_NEXT)))
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
	
	dateStr = str(week_ago.month) + '/' + str(week_ago.day) + '/' + str(week_ago.year)
	
	dateStrS = channelDesc.split('/')
	if len(dateStrS) == 3:
		dateStr = channelDesc
		return dateStr
	
	# tricky keep in seperate try
	try:
		if 'Updated' in channelDesc:
			dateStr = str(week_ago.month) + '/' + str(week_ago.day)
			channelUpDate = channelDesc.replace('Updated:','')
			channelUpDate = channelUpDate.replace('24/7','')
			if '/' in channelUpDate and '-' in channelUpDate:
				dateStr = channelUpDate.split('-')[0]
			elif '/' in channelUpDate and ':' in channelUpDate:
				dateStr = channelUpDate.split(':')[0]
	except:
		dateStr = str(week_ago.month) + '/' + str(week_ago.day) + '/' + str(week_ago.year)
		
	try:
		if ':' in dateStr:
			dateStr = dateStr.split(':')[0]
	except:
		dateStr = str(week_ago.month) + '/' + str(week_ago.day)
		
	try:
		dateStrS = dateStr.split('/')
		dateStr = str("%02d" % int(dateStrS[0])) + '/' + str("%02d" % int(dateStrS[1]))
		if len(dateStrS) > 2:
			if len(dateStrS[2]) == 2:
				dateStr = dateStr + '/20' + str("%02d" % int(dateStrS[2]))
			elif len(dateStrS[2]) == 4:
				dateStr = dateStr + '/' + str(dateStrS[2])
		else:
			dateStr = dateStr + '/' + str(week_ago.year)
	except:
		dateStr = str(week_ago.month) + '/' + str(week_ago.day) + '/' + str(week_ago.year)
		
	#Log("dateStr----------" + dateStr)
	return dateStr



@route(PREFIX + '/channelpage')
def ChannelPage(url, title, channelDesc, channelNum, logoUrl):

	oc = ObjectContainer(title2=title)
	
	try:
		#Log("----------- url ----------------")
		#Log(url)
		furl = GetRedirector(url)
		oc.add(CreateVideoClipObject(
			url = furl,
			title = title,
			thumb = GetChannelThumb(furl,logoUrl),
			summary = channelDesc))
	except:
		url = ""
	
	if CheckBookmark(channelNum=channelNum,url=url):
		oc.add(DirectoryObject(
			key = Callback(RemoveBookmark, title = title, channelNum = channelNum, url = url),
			title = "Remove Bookmark",
			summary = 'Removes the current Channel from the Boomark queue',
			thumb = R(ICON_BOOKMARK)
		))
	else:
		oc.add(DirectoryObject(
			key = Callback(AddBookmark, channelNum = channelNum, url = url),
			title = "Bookmark Channel",
			summary = 'Adds the current Channel to the Boomark queue',
			thumb = R(ICON_BOOKMARK)
		))
	if CheckPin(url=url):
		oc.add(DirectoryObject(
			key = Callback(RemovePin, url = url),
			title = "Remove Pin",
			summary = 'Removes the current Channel from the Pin list',
			thumb = R(ICON_PIN)
		))
	else:
		oc.add(DirectoryObject(
			key = Callback(AddPin, channelNum = channelNum, url = url, title = title, channelDesc = channelDesc, logoUrl=logoUrl),
			title = "Pin Channel",
			summary = 'Adds the current Channel to the Pin list',
			thumb = R(ICON_PIN)
		))
	
	abortBool = RefreshListing(False)
	if not abortBool:
		oc.add(InputDirectoryObject(key = Callback(Search), thumb = R(ICON_SEARCH), title='Search', summary='Search Channel', prompt='Search for...'))	
	return oc

####################################################################################################
# Gets the redirecting url for .m3u8 streams
@route(PREFIX + '/getchannelthumb')
def GetChannelThumb(url, logoUrl):

	thumb = R(ICON_SERIES_UNAV)
	try:
		if '.m3u8' in url:
			page = HTTP.Request(url).content
			if 'html' not in page and 'div' not in page and '#EXTM3U' in page:
				thumb = logoUrl
		elif '.m3u' in url or '.mp4' in url:
			thumb = logoUrl
		elif '.aac' in url or '.mp3' in url:
			thumb = logoUrl
	except:
		thumb = R(ICON_SERIES_UNAV)

	return thumb
	
	
####################################################################################################
# Filter channels based on preferences
@route(PREFIX + '/channelfilters')
def ChannelFilters(active, onair, lang, country, mature):
	
	abortBool2 = False
	if Prefs['show_active'] and active == 'N':
		abortBool2 = True
	if Prefs['show_onair'] and onair == 'N':
		abortBool2 = True
	if Prefs['show_lang'] <> None and lang != 'Unknown' and unicode(Prefs['show_lang']).strip().lower() != unicode(lang).strip().lower():
		abortBool2 = True
	if Prefs['show_country'] <> None and Prefs['show_country'] != 'ALL' and country != 'Unknown' and Prefs['show_country'] != country:
		abortBool2 = True	
	if not Prefs['show_adult'] and mature == 'Y' and Dict['AccessPin'] != Prefs['access_pin']:
		abortBool2 = True
		
	return abortBool2
	
####################################################################################################
# is Channel Adult rated based on '18+' keyword
@route(PREFIX + '/isadultchannel')
def isAdultChannel(channelDesc):
	
	adult = 'N'
	if '18+' in channelDesc:
		adult = 'Y'
		
	return adult
	
####################################################################################################
# Gets the redirecting url for .m3u8 streams
@route(PREFIX + '/getredirector')
def GetRedirector(url):

	redirectUrl = url
	try:
		if '.m3u8' not in url and '.mp3' not in url and '.aac' not in url and '.m3u' not in url and '.mp4' not in url:
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
	elif '.mp4' in url and '.m3u8' not in url:
		vco = VideoClipObject(
			url = url + '&&&' + title,
			title = title,
			thumb = thumb,
			summary = summary
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
		for count in Dict['items_dict']:
			channelNum = Dict['items_dict'][count]['channelNum']
			channelDesc = Dict['items_dict'][count]['channelDesc']
			channelUrl = Dict['items_dict'][count]['channelUrl']
			dateStr = Dict['items_dict'][count]['channelDate']
			title = unicode(channelDesc)
			#Log("channelDesc--------- " + channelDesc)
			
			desc = 'Unknown'
			country = 'Unknown'
			lang = 'Unknown'
			genre = 'Unknown'
			views = 'Unknown'
			active = 'Unknown'
			onair = 'Unknown'
			mature = 'Unknown'
			epgInfo = ''
			logoUrl = None
			
			try:
				logoUrl = Dict['items_dict'][count]['logoUrl']
				mature = Dict['items_dict'][count]['mature']
				desc = Dict['items_dict'][count]['desc']
				country = Dict['items_dict'][count]['country']
				lang = Dict['items_dict'][count]['lang']
				genre = Dict['items_dict'][count]['genre']
				views = Dict['items_dict'][count]['views']
				active = Dict['items_dict'][count]['active']
				onair = Dict['items_dict'][count]['onair']
				epgInfo = Dict['items_dict'][count]['epg']
			except:
				pass
			
			abortBool2 = ChannelFilters(active=active, onair=onair, lang=lang, country=country, mature=mature)
			
			summaryStr = '#: ' + channelNum + ' | '+ desc + ' | Genre:' + genre + ' | Country:' + country + ' | Language:' + lang
			if epgInfo != '':
				summaryStr = summaryStr + ' | ' + epgInfo
			
			if not abortBool2 and query.lower() in channelDesc.lower() or query == channelNum:
				if logoUrl <> None:
					oc.add(DirectoryObject(key = Callback(ChannelPage, url = channelUrl, title = title, channelDesc = summaryStr, channelNum=channelNum, logoUrl=logoUrl), tagline=dateStr, summary = summaryStr, title = title, thumb = logoUrl))
				else:
					oc.add(DirectoryObject(key = Callback(ChannelPage, url = channelUrl, title = title, channelDesc = summaryStr, channelNum=channelNum, logoUrl=logoUrl), tagline=dateStr, summary = summaryStr, title = title, thumb = R(ICON_SERIES)))
			elif '~' in query and int(channelNum) > start-1 and int(channelNum) < end+1:
				if not Prefs['show_adult'] and mature == 'Y' and Dict['AccessPin'] != Prefs['access_pin']:
					pass
				else:
					if logoUrl <> None:
						oc.add(DirectoryObject(key = Callback(ChannelPage, url = channelUrl, title = title, channelDesc = summaryStr, channelNum=channelNum, logoUrl=logoUrl), tagline=dateStr, summary = summaryStr, title = title, thumb = logoUrl))
					else:
						oc.add(DirectoryObject(key = Callback(ChannelPage, url = channelUrl, title = title, channelDesc = summaryStr, channelNum=channelNum, logoUrl=logoUrl), tagline=dateStr, summary = summaryStr, title = title, thumb = R(ICON_SERIES)))
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
		#for each in Dict:
		#Log("each--------- " + str(each))
		for x in Dict['items_dict']:
			#Log("x--------- " + str(x))
			channelNum = Dict['items_dict'][x]['channelNum']
			#Log("channelNum--------- " + str(channelNum))
			
			channelDesc = Dict['items_dict'][x]['channelDesc']
			channelUrl = Dict['items_dict'][x]['channelUrl']
			dateStr = Dict['items_dict'][x]['channelDate']
			title = channelDesc
			#Log("channelDesc--------- " + str(channelDesc))
			
			desc = 'Unknown'
			country = 'Unknown'
			lang = 'Unknown'
			genre = 'Unknown'
			views = 'Unknown'
			epgInfo = ''
			logoUrl = None
		
			try:
				desc = Dict['items_dict'][x]['desc']
				country = Dict['items_dict'][x]['country']
				lang = Dict['items_dict'][x]['lang']
				genre = Dict['items_dict'][x]['genre']
				views = Dict['items_dict'][x]['views']
				epgInfo = Dict['items_dict'][x]['epg']
			except:
				pass
			try:
				logoUrl = Dict['items_dict'][x]['logoUrl']
			except:
				pass
			
			summaryStr = '#: ' + channelNum + ' | ' + desc + ' | Genre:' + genre + ' | Country:' + country + ' | Language:' + lang
			if epgInfo != '':
				summaryStr = summaryStr + ' | ' + epgInfo
			
			mature = 'N'
			try:
				mature = isAdultChannel(channelDesc)
			except:
				pass
			
			if not Prefs['show_adult'] and mature == 'Y' and Dict['AccessPin'] != Prefs['access_pin']:
				pass
			else:
				if Dict[str((channelNum))] <> None and Dict[str((channelNum))] <> 'removed' and 'MyCustomSearch' not in Dict[str((channelNum))]:
					#Log("channelDesc--------- " + str(channelDesc) + " " + summaryStr + " " + dateStr + " " + str(logoUrl))
					if logoUrl <> None:
						oc.add(DirectoryObject(key = Callback(ChannelPage, url = channelUrl, title = title, channelDesc = summaryStr, channelNum=channelNum, logoUrl=logoUrl), tagline=dateStr, summary = summaryStr, title = title, thumb = logoUrl))
					else:
						oc.add(DirectoryObject(key = Callback(ChannelPage, url = channelUrl, title = title, channelDesc = summaryStr, channelNum=channelNum, logoUrl=logoUrl), tagline=dateStr, summary = summaryStr, title = title, thumb = R(ICON_SERIES)))
	except:
		return ObjectContainer(header='Bookmarks', message='No Channels Available. Please check website URL !')
	
	if Prefs['use_datesort']:
		oc.objects.sort(key=lambda obj: obj.tagline, reverse=True)
	else:	
		oc.objects.sort(key=lambda obj: obj.title)
		
	#add a way to clear bookmarks list
	oc.add(DirectoryObject(
		key = Callback(ClearBookmarks),
		title = "Clear Bookmarks",
		thumb = R(ICON_BOOKMARK),
		summary = "CAUTION! This will clear your entire bookmark list!"
		)
	)
	
	if len(oc) == 1:
		return ObjectContainer(header='Bookmarks', message='No Bookmarked Videos Available')
		
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
def AddPin(channelNum, url, title, channelDesc, logoUrl):
	
	url = GetRedirector(url)
	Dict['Plex-Pin-Pin'+url] = channelNum + 'Key4Split' + title + 'Key4Split' + channelDesc + 'Key4Split' + url + 'Key4Split' + logoUrl
	
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
	
	try:
		for each in Dict:
			keys = Dict[each]
			if 'Key4Split' in keys:
				values = keys.split('Key4Split')
				logoUrl = None
				if len(values) >= 4:
					channelNum = values[0]
					title = values[1]
					channelDesc = values[2]
					channelUrl = values[3]
					if len(values) >= 5:
						logoUrl = values[4]
				else:
					channelNum = values[0]
					channelDesc = values[1]
					channelUrl = values[2]
					title = channelDesc
				#Log("channelDesc--------- " + str(channelDesc))
				
				desc = 'Unknown'
				country = 'Unknown'
				lang = 'Unknown'
				genre = 'Unknown'
				views = 'Unknown'
				epgInfo = ''
			
				try:
					desc = Dict['items_dict'][x]['desc']
					country = Dict['items_dict'][x]['country']
					lang = Dict['items_dict'][x]['lang']
					genre = Dict['items_dict'][x]['genre']
					views = Dict['items_dict'][x]['views']
					epgInfo = Dict['items_dict'][x]['epg']
				except:
					pass
					
				summaryStr = '#: ' + channelNum + ' | '+ desc + ' | Genre:' + genre + ' | Country:' + country + ' | Language:' + lang
				if epgInfo != '':
					summaryStr = summaryStr + ' | ' + epgInfo
				
				mature = 'N'
				try:
					mature = isAdultChannel(title)
				except:
					pass
					
				if not Prefs['show_adult'] and mature == 'Y' and Dict['AccessPin'] != Prefs['access_pin']:
					pass
				else:
					if 'removed' not in channelUrl:
						if logoUrl <> None:
							oc.add(DirectoryObject(key = Callback(ChannelPage, url = channelUrl, title = title, channelDesc = summaryStr, channelNum=channelNum, logoUrl=logoUrl), title = title, thumb = logoUrl))
						else:
							oc.add(DirectoryObject(key = Callback(ChannelPage, url = channelUrl, title = title, channelDesc = summaryStr, channelNum=channelNum, logoUrl=logoUrl), title = title, thumb = R(ICON_SERIES)))
	except:
		return ObjectContainer(header='Pins', message='No Channels Available. Please check website URL !')
	
	oc.objects.sort(key=lambda obj: obj.title)
	#add a way to clear pin list
	oc.add(DirectoryObject(
		key = Callback(ClearPins),
		title = "Clear All Pins",
		thumb = R(ICON_PIN),
		summary = "CAUTION! This will clear your entire Pins list!"
		)
	)
	
	if len(oc) == 1:
		return ObjectContainer(header='Pins', message='No Pinned Videos Available')
	
	return oc

######################################################################################
# Fix Genre
@route(PREFIX + "/fixgenre")	
def FixGenre(genre):

	if genre in GENRE_SYNM_SPORTS:
		genre = 'Sports'
	elif genre in GENRE_SYNM_ENTERTAINMENT:
		genre = 'Entertainment'
	elif genre in GENRE_SYNM_ENTERTAINMENT_NEWS:
		genre = 'Entertainment/News'
		
	if Prefs['merge_cats'] and 'Public-' in genre:
		genre = genre.replace('Public-','')
	
	return genre
	
####################################################################################################
# Fix Language
@route(PREFIX + "/fixlanguage")	
def FixLanguage(lang):

	if lang.lower() == 'indian':
		lang = 'Hindi'
	elif lang.lower() == 'unk':
		lang = 'Unknown'
	return lang
	
####################################################################################################
# Fix Country
@route(PREFIX + "/fixcountry")	
def FixCountry(country):

	if country.lower() == 'gb':
		country = 'UK'
	elif country.lower() == 'usa':
		country = 'US'
		
	if len(country) > 2 and '/' not in country:
		#Log("country1 ----- " + country)
		country = common.COUNTRY_ARRAY_LIST.get(country.lower(),"UNK").upper()
		#Log("country2 ----- " + country)
		
	return country