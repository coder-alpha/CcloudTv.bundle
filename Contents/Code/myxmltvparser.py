from datetime import datetime, timedelta
import calendar
import time

CHANNELS = {}
POSTER_UNAV = 'http://i.imgur.com/0snKSZt.png'
GUIDE_HRS = 12

####################################################################################################
def initchannels():
	
	try:
		CHANNEL_ID_REPLACER = []
		Channel_ID_Replacer_File = Resource.Load("Channels_ReplaceID.json", binary = True)
		CHANNEL_ID_REPLACER = JSON.ObjectFromString(Channel_ID_Replacer_File, encoding=None)
	except:
		pass
		
	ALL_XML_GUIDE_FILES = []
	XML_FILES = Prefs['epg_guide']
	
	if XML_FILES <> None:
		if (';' or ',' or ' ') in XML_FILES:
			XML_FILES = None
			if ';' in XML_FILES:
				xml_files = XML_FILES.split(';')
			elif ',' in XML_FILES:
				xml_files = XML_FILES.split(',')
			elif ' ' in XML_FILES:
				xml_files = XML_FILES.split(' ')
			if xml_files <> None and len(xml_files) > 0:
				for file in xml_files:
					ALL_XML_GUIDE_FILES.append(file.strip())
		else:
			ALL_XML_GUIDE_FILES.append(XML_FILES)
	
	if len(ALL_XML_GUIDE_FILES) > 0:
		for XML_FILE in ALL_XML_GUIDE_FILES:
			if XML_FILE <> None and (XML_FILE.startswith('http://') or XML_FILE.startswith('https://')):
				XML_SOURCE = XML.ElementFromURL(XML_FILE, encoding=None)
			else:
				XML_URL = Resource.Load(XML_FILE, binary = True)
				XML_SOURCE = XML.ElementFromString(XML_URL, encoding=None)
				
			if XML_SOURCE != None:
				if Prefs['debug']:
					Log("Start Loading XML Guide: " + XML_FILE)
				
				count = 0
				try:
					for programme in XML_SOURCE.findall("./programme"):
						count = count + 1
						channel = programme.get('channel')
						if len(CHANNEL_ID_REPLACER) > 0 and channel in CHANNEL_ID_REPLACER.keys():
							try:
								channel = CHANNEL_ID_REPLACER[channel]['ReplaceVal']
							except:
								pass
						title = programme.find('title').text
						desc = programme.find('desc')
						if desc == None:
							desc = 'Item Summary Unavailable'
						else:
							desc = desc.text
						img = programme.find('img')
						if img == None:
							img = POSTER_UNAV
						else:
							img = img.text 	
						start = datetime_from_utc_to_local(programme.get('start'))
						stop = datetime_from_utc_to_local(programme.get('stop'))
						item = {'start': start, 'stop': stop, 'title': title, 'desc': desc, 'img': img, 'order': count}
						CHANNELS.setdefault(channel, {})[count] = item
				except:
					pass
				if Prefs['debug']:
					Log("Finished Loading XML Guide: " + XML_FILE)

	return None
	
def datetime_from_utc_to_local(input_datetime):

	#Get local offset from UTC in seconds
	local_offset_in_seconds = calendar.timegm(time.localtime()) - calendar.timegm(time.gmtime(time.mktime(time.localtime())))
	#split time from offset
	input_datetime_split = input_datetime.split(" ")
	input_datetime_only = input_datetime_split[0]
	# Convert input date to a proper date
	input_datetime_only_dt = datetime.strptime(input_datetime_only, '%Y%m%d%H%M%S')
	# If exists - convert input_offset_only to seconds otherwise set to 0
	if len(input_datetime_split) > 1:
		input_offset_only = input_datetime_split[1]
		input_offset_mins, input_offset_hours = int(input_offset_only[3:]), int(input_offset_only[:-2])
		input_offset_in_total_seconds = (input_offset_hours * 60 * 60) + (input_offset_mins * 60);
	else:
		input_offset_in_total_seconds = 0
	#Get the true offset taking into account local offset
	true_offset_in_seconds = local_offset_in_seconds + input_offset_in_total_seconds
	# add the true_offset to input_datetime
	local_dt = input_datetime_only_dt + timedelta(seconds=true_offset_in_seconds)
	return local_dt

####################################################################################################
def format_time(timestamp):
	return datetime.strptime(timestamp[:12], "%Y%m%d%H%M%S")

####################################################################################################
def epgguide(channelID, country, lang):
	epgInfo = ''
	currentTime = datetime.today()
	
	try:
		if channelID in CHANNELS.keys():
			items_list = CHANNELS[channelID].values()
			for item in items_list:
				if item['start'] <= (currentTime + timedelta(hours = GUIDE_HRS)) and item['stop'] > currentTime:
					epgInfo = epgInfo + '\n' + item['start'].strftime('%H:%M') + ' ' + item['title']
	except:
		pass
		
	if epgInfo == '':
		epgInfo = 'EPG Info Unavailable for ' + channelID + ' in Guide'
	return epgInfo
	
####################################################################################################
def epgguideWithDesc(channelID, country, lang):
	epgInfo = ''
	currentTime = datetime.today()
	
	try:
		if channelID in CHANNELS.keys():
			items_list = CHANNELS[channelID].values()
			for item in items_list:
				if item['start'] <= (currentTime + timedelta(hours = GUIDE_HRS)) and item['stop'] > currentTime:
					epgInfo = epgInfo + '\n' + item['start'].strftime('%H:%M') + ' ' + item['title'] + ' - ' + item['desc']
	except:
		pass
		
	if epgInfo == '':
		epgInfo = 'EPG Info Unavailable for ' + channelID + ' in Guide'
	return epgInfo
	
####################################################################################################
def GetXmlListing(channelID, country, lang):
	guideVals = {}
	currentTime = datetime.today()
	x = 0
	try:
		if channelID in CHANNELS.keys():
			items_list = CHANNELS[channelID].values()
			for item in items_list:
				if item['start'] <= (currentTime + timedelta(hours = GUIDE_HRS)) and item['stop'] > currentTime:
					guideVals[x] = {'showtitles': unicode(item['title']), 'showtimes': (item['start'].strftime('%H:%M')), 'summary': (item['desc']), 'img': (item['img'])}
					x = x+1
	except:
		pass

	return guideVals
	
####################################################################################################
def epgguideCurrent(channelID, country, lang):
	epgInfo = ''
	currentTime = datetime.today()
	
	try:
		if channelID in CHANNELS.keys():
			items_list = CHANNELS[channelID].values()
			for item in items_list:
				if item['start'] <= (currentTime + timedelta(hours = 3)) and item['stop'] > currentTime:
					epgInfo = ' (' + item['title'] + ')'
					break
	except:
		pass

	return epgInfo