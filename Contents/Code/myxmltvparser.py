import datetime

CHANNELS = {}

####################################################################################################
def initchannels():
	channels = {}
	XML_URL = Resource.Load(Prefs['epg_guide'], binary = True)
	XML_SOURCE = HTML.ElementFromString(XML_URL, encoding=None)
		
	for key in XML_SOURCE:
		channel = {}
		channels[0] = channel

	CHANNELS = channels


def format_time(timestamp):
	return datetime.datetime.strptime(timestamp[:12], "%Y%m%d%H%M%S")


####################################################################################################
def epgguide(channelID, country, lang, currentTime):
	epgInfo = 'No EPG Info Available'
	if Prefs['debug']:
		Log("currenttime ---------------- " + str(currentTime))
	try:
		for channel in CHANNELS:
			if channel.id in channelID:
				for prog in channel:
					if int(currentTime) > int(format_time(prog.key['start'])) and int(currentTime)+120 < int(format_time(prog.key['stop'])):
						epgInfo = epgInfo + ' | ' + prog + '[ ' + format_time(key['start']) + ' - ' + format_time(key['stop']) + ' ]'
	except:
		pass
	return epgInfo