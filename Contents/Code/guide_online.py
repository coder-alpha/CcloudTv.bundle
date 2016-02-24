import playback, common_fnc
import datetime, re, time, unicodedata, hashlib, urlparse, types, urllib

# Adapted from Expat plugin : http://forums.plex.tv/discussion/193042/rel-expat-tv/p1
# Author : b_caudill21 - http://forums.plex.tv/profile/b_caudill21
#
# eg: 'http://www.locatetv.com/listings/wcvb-abc'
# 
ICON_SERIES = "icon-series.png"


@route(common.PREFIX + '/check')
def Check(title, videoUrl, listingUrl):

	ret = GetListing(title, videoUrl, listingUrl)
		
	if ret == None or ret == {}:
		return False
	else:
		return True


@route(common.PREFIX + '/getlisting')
def GetListing(title, videoUrl, listingUrl):

	if 'locatetv.com' in listingUrl:
		return GetLocateTvListing(title, videoUrl, listingUrl)
	elif 'imdb.com' in listingUrl:
		return GetImdbData(title, videoUrl, listingUrl)
	else:
		return None
		

@route(common.PREFIX + '/getlocatetvlisting')
def GetLocateTvListing(title, videoUrl, listingUrl):

	guideVals = {}
	oc = ObjectContainer(title2=title)
	
	try:
		page = HTML.ElementFromURL(listingUrl, timeout=float(common_fnc.global_request_timeout))
		channels = page.xpath('//li')
		
		for channel in channels:
			showtitles = channel.xpath('//a[@class="pickable"][1]//text()')
			showtitles2 = channel.xpath('//li[@class="title withPackshot"]//a//img//@title')
			showtimes = channel.xpath('//li[@class="time"]//text()')
			img = channel.xpath('//li[@class="title withPackshot"]//a//img//@alt')
			
		l = len(showtitles)
		for x in xrange(l):
			summary = 'Description Unavailable'
			try:
				summary = channel.xpath('//*//li['+str(x+2)+']//ul//li[2]//div//p//text()')[0]
			except:
				pass
			showtitle = showtitles[x]
			if showtitles[x] != showtitles2[x]:
				try:
					showtitle += ' : ' + showtitles2[x]
				except:
					pass
			guideVals[x] = {'showtitles': unicode(showtitle), 'showtimes': showtimes[x], 'summary': summary, 'img': img[x]}
			#if Prefs['debug']:
			#	Log(guideVals[x])
	except Exception, e:
		if Prefs['debug']:
			Log("Error in guide_online.py > GetLocateTvListing" + str(e))

	return guideVals
	
@route(common.PREFIX + '/createlisting')
def CreateListing(title, videoUrl, listingUrl, transcode, session):

	tvGuide = GetListing(title, videoUrl, listingUrl)
	
	if tvGuide == None:
		return None
	oc = ObjectContainer(title2=title)
	vUrl = videoUrl
	l = len(tvGuide)
	for x in xrange(l):

		if '?' in videoUrl:
			vUrl = videoUrl.replace('?','?n='+str(x)+'&')
		else:
			vUrl = videoUrl + '?n='+str(x)
		oc.add(playback.CreateVideoClipObject(
			url = vUrl,
			title = tvGuide[x]['showtitles'] + ' - ' + tvGuide[x]['showtimes'],
			thumb = Resource.ContentsOfURLWithFallback(url = tvGuide[x]['img'], fallback= R(ICON_SERIES)),
			summary = tvGuide[x]['summary'],
			session = session,
			transcode = transcode
		))

	return oc
	
###############################################################
# Based on IMDB.Bundle
# ToDo - Not Implemented Yet
#
def GetImdbData(title, videoUrl, url):

	return None
	
	metadata = {}
	try:
		movie = XML.ElementFromURL(url, cacheTime=3600)

		d = {}
		name,year = get_best_name_and_year(guid, lang, None, None, d)
		if name is not None:
			metadata.title = name

		# Runtime.
		if int(movie.get('runtime')) > 0:
			metadata.duration = int(movie.get('runtime')) * 60 * 1000

		# Genres.
		metadata.genres.clear()
		genreMap = {}
		
		for genre in movie.xpath('genre'):
			id = genre.get('id')
			genreLang = genre.get('lang')
			genreName = genre.get('genre')
		
		if not genreMap.has_key(id) and genreLang in ('en', lang):
			genreMap[id] = [genreLang, genreName]
			
		elif genreMap.has_key(id) and genreLang == lang:
			genreMap[id] = [genreLang, genreName]
		
		keys = genreMap.keys()
		keys.sort()
		for id in keys:
			metadata.genres.add(genreMap[id][1])

		# Directors.
		metadata.directors.clear()
		for director in movie.xpath('director'):
			metadata.directors.add(director.get('name'))
		
		# Writers.
		metadata.writers.clear()
		for writer in movie.xpath('writer'):
			metadata.writers.add(writer.get('name'))
		
		# Actors.
		metadata.roles.clear()
		for movie_role in movie.xpath('actor'):
			role = metadata.roles.new()
		if movie_role.get('role'):
			role.role = movie_role.get('role')
		#role.photo = headshot_url
		role.actor = movie_role.get('name')
			
		# Studio
		if movie.get('company'):
			metadata.studio = movie.get('company')
		
		# Tagline.
		if len(movie.get('tagline')) > 0:
			metadata.tagline = movie.get('tagline')
		
		# Content rating.
		if movie.get('content_rating'):
			metadata.content_rating = movie.get('content_rating')
	 
		# Release date.
		if len(movie.get('originally_available_at')) > 0:
			elements = movie.get('originally_available_at').split('-')
		if len(elements) >= 1 and len(elements[0]) == 4:
			metadata.year = int(elements[0])

		if len(elements) == 3:
			metadata.originally_available_at = Datetime.ParseDate(movie.get('originally_available_at')).date()
			
		# Country.
		try:
			metadata.countries.clear()
			if movie.get('country'):
				country = movie.get('country')
				country = country.replace('United States of America', 'USA')
				metadata.countries.add(country)
		except:
			pass
		
	except:
		print "Error obtaining Plex movie data for", guid

	m = re.search('(tt[0-9]+)', metadata.guid)
	if m and not metadata.year:
		id = m.groups(1)[0]
		# We already tried Freebase above, so go directly to Google
		(title, year) = self.findById(id, skipFreebase=True)
		metadata.year = int(year)

	return metadata
	

def parseIMDBTitle(title, url):

	titleLc = title.lower()

	result = {
	'title':	None,
	'year':	 None,
	'type':	 'movie',
	'imdbId': None,
	}

	try:
		(scheme, host, path, params, query, fragment) = urlparse.urlparse(url)
		path		= re.sub(r"/+$","",path)
		pathParts = path.split("/")
		lastPathPart = pathParts[-1]

		if host.count('imdb.') == 0:
			## imdb is not in the server.. bail
			return None

		if lastPathPart == 'quotes':
			## titles on these parse fine but are almost
			## always wrong
			return None

		if lastPathPart == 'videogallery':
			## titles on these parse fine but are almost
			## always wrong
			return None

		# parse the imdbId
		m = re.search('/(tt[0-9]+)/?', path)
		imdbId = m.groups(1)[0]
		result['imdbId'] = imdbId

		## hints in the title
		if titleLc.count("(tv series") > 0:
			result['type'] = 'tvseries'
		elif titleLc.endswith("episode list"):
			result['type'] = 'tvseries'
		elif titleLc.count("(tv episode") > 0:
			result['type'] = 'tvepisode'
		elif titleLc.count("(vg)") > 0:
			result['type'] = 'videogame'
		elif titleLc.count("(video game") > 0:
			result['type'] = 'videogame'

		# NOTE: it seems that titles of the form
		# (TV 2008) are made for TV movies and not
		# regular TV series... I think we should
		# let these through as "movies" as it includes
		# stand up commedians, concerts, etc

		# NOTE: titles of the form (Video 2009) seem
		# to be straight to video/dvd releases
		# these should also be kept intact
		
		# hints in the url
		if lastPathPart == 'episodes':
			result['type'] = 'tvseries'

		# Parse out title, year, and extra.
		titleRx = '(.*) \(([^0-9]+ )?([0-9]+)(/.*)?.*?\).*'
		m = re.match(titleRx, title)
		if m:
			# A bit more processing for the name.
			result['title'] = cleanupIMDBName(m.groups()[0])
			result['year'] = int(m.groups()[2])
			
		else:
			longTitleRx = '(.*\.\.\.)'
			m = re.match(longTitleRx, title)
			if m:
				result['title'] = cleanupIMDBName(m.groups(1)[0])
				result['year']	= None

		if result['title'] is None:
			return None

		return result
	except:
		return None
 
def cleanupIMDBName(s):
	imdbName = re.sub('^[iI][mM][dD][bB][ ]*:[ ]*', '', s)
	imdbName = re.sub('^details - ', '', imdbName)
	imdbName = re.sub('(.*:: )+', '', imdbName)
	imdbName = HTML.ElementFromString(imdbName).text

	if imdbName:
		if imdbName[0] == '"' and imdbName[-1] == '"':
			imdbName = imdbName[1:-1]
		return imdbName

	return None

def safe_unicode(s,encoding='utf-8'):
	if s is None:
		return None
	if isinstance(s, basestring):
		if isinstance(s, types.UnicodeType):
			return s
		else:
			return s.decode(encoding)
	else:
		return str(s).decode(encoding)