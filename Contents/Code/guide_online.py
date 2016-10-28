import playback, common_fnc, myxmltvparser
import datetime, re, time, unicodedata, hashlib, urlparse, types, urllib
import imdb

# Adapted from Expat plugin : http://forums.plex.tv/discussion/193042/rel-expat-tv/p1
# Author : b_caudill21 - http://forums.plex.tv/profile/b_caudill21
#
# eg: 'http://www.locatetv.com/listings/wcvb-abc'
# 
ICON_SERIES = "icon-series.png"

IS_LOCATETV_ACTIVE = False
IS_IMDB_ACTIVE = True

IMDB_OBJ = []

@route(common.PREFIX + '/initimdb')
def InitIMDB():
	# Create the object that will be used to access the IMDb's database.
	try:
		if len (IMDB_OBJ) == 0:
			ia = imdb.IMDb() # by default access the web.
			IMDB_OBJ.append(ia)
			if Prefs['debug']:
				Log("IMDB module Initialized Successfully !")
		else:
			if Prefs['debug']:
				Log("IMDB module is already available !")
	except Exception, e:
		if Prefs['debug']:
			Log("Error in guide_online.py > InitIMDB: " + str(e))
		pass

@route(common.PREFIX + '/check')
def Check(title, videoUrl, listingUrl, country, lang):

	ret = GetListing(title, videoUrl, listingUrl, country, lang)
		
	if ret == None or ret == {}:
		return False
	else:
		return True


@route(common.PREFIX + '/getlisting')
def GetListing(title, videoUrl, listingUrl, country, lang, isMovie=False):

	if 'locatetv.com' in listingUrl and IS_LOCATETV_ACTIVE:
		return GetLocateTvListing(title, videoUrl, listingUrl, country, lang)
	elif ('imdb.com' in listingUrl) or isMovie and IS_IMDB_ACTIVE:
		if Prefs['use_imdb']:
			return GetImdbData(title, videoUrl, listingUrl, country, lang)
		else:
			return None
	elif Prefs['use_epg'] and not isMovie:
		return myxmltvparser.GetXmlListing(title, country, lang)
	else:
		return None
		

@route(common.PREFIX + '/getlocatetvlisting')
def GetLocateTvListing(title, videoUrl, listingUrl, country, lang):

	guideVals = {}
	oc = ObjectContainer(title2=title)
	
	try:
		page = HTML.ElementFromURL(listingUrl, timeout=float(common_fnc.global_request_timeout))
		channels = page.xpath('//li')
		showtitles = []
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
			Log("Error in guide_online.py > GetLocateTvListing: " + str(e))

	return guideVals
	
@route(common.PREFIX + '/createlisting')
def CreateListing(title, videoUrl, listingUrl, transcode, session, country, lang, isMovie=False):

	tvGuide = GetListing(title, videoUrl, listingUrl, country, lang)
	
	if tvGuide == None:
		return ObjectContainer(header='TV Guide Unavailable', message='TV Guide Unavailable for ' + title, title1='TV Guide Unavailable')
	oc = ObjectContainer(title2=title + ' Guide')
	vUrl = videoUrl
	l = len(tvGuide)
	for x in xrange(l):

		if '?' in videoUrl:
			vUrl = videoUrl.replace('?','?n='+str(x)+'&')
		else:
			vUrl = videoUrl + '?n='+str(x)
		oc.add(DirectoryObject(
			key = Callback(common_fnc.ShowMessage, title=tvGuide[x]['showtitles'], message=tvGuide[x]['summary']),
			title = tvGuide[x]['showtitles'] + ' - ' + tvGuide[x]['showtimes'],
			thumb = Resource.ContentsOfURLWithFallback(url = tvGuide[x]['img'], fallback= R(ICON_SERIES)),
			summary = tvGuide[x]['summary']
		))

	return oc
	
###############################################################
# Using http://imdbpy.sourceforge.net/
# Needs to be available under ~/Libraries/Shared/ folder
#
@route(common.PREFIX + '/createimdblisting')
def CreateIMDBListing(title, videoUrl, listingUrl, transcode, session, country, lang, isMovie=True, tvGuide=None):

	if tvGuide == None or len(tvGuide) == 0:
		tvGuide = GetImdbData(title, videoUrl, listingUrl, country, lang)
	if tvGuide == None:
		return ObjectContainer(header='IMDb Info Unavailable', message='IMDb Info Unavailable for ' + title, title1='IMDb Info Unavailable')
	oc = ObjectContainer(title2=title + ' IMDb Info')
	vUrl = videoUrl
	l = len(tvGuide)
	
	for x in xrange(l):
	
		if '?' in videoUrl:
			vUrl = videoUrl.replace('?','?n='+str(x)+'&')
		else:
			vUrl = videoUrl + '?n='+str(x)
		oc.add(DirectoryObject(
			key = Callback(common_fnc.ShowMessage, title=tvGuide[x]['showtitles'], message=tvGuide[x]['showtimes']),
			title = tvGuide[x]['showtitles'],
			thumb = Resource.ContentsOfURLWithFallback(url = tvGuide[x]['img'], fallback= R(ICON_SERIES)),
			summary = tvGuide[x]['showtimes']
		))
		# oc.add(playback.CreateVideoClipObject(
			# url = vUrl,
			# title = tvGuide[x]['showtitles'],
			# thumb = Resource.ContentsOfURLWithFallback(url = tvGuide[x]['img'], fallback= R(ICON_SERIES)),
			# summary = tvGuide[x]['showtimes'],
			# session = session,
			# transcode = transcode
		# ))

	return oc

@route(common.PREFIX + '/getimdbdata')
def GetImdbData(title, videoUrl, url, country, lang):

	if len(IMDB_OBJ) == 0:
		InitIMDB()
		if len(IMDB_OBJ) == 0:
			return None
	
	# Get the object that will be used to access the IMDb's database.	
	ia = IMDB_OBJ[0]

	if Prefs['debug']:
		Log("Searching for IMDB data for: " + title)
	# Search for a movie (get a list of Movie objects).
	s_result = ia.search_movie(title)
	
	the_unt = s_result[0]
	ia.update(the_unt)

	guideVals = {}
	i = 0
	# Print some information.
	cover_url = ''
	try:
		#Log( the_unt['full-size cover url'] )
		cover_url = unicode(the_unt['full-size cover url'])
	except:
		pass
	summary = None
	try:
		#Log( the_unt['plot outline'] )
		summary = the_unt['plot outline']
		guideVals[i] = {'showtitles': 'Plot-Summary', 'showtimes': unicode(summary), 'img': cover_url}
		i+=1
	except:
		pass
		
	try:
		#Log( the_unt['rating'] )
		guideVals[i] = {'showtitles': 'Rating', 'showtimes': unicode(str(the_unt['rating']) + '/10'), 'img': cover_url}
		i+=1
	except:
		pass
		
	try:
		#Log( the_unt['runtime'][0] )
		guideVals[i] = {'showtitles': 'Runtime', 'showtimes': unicode(the_unt['runtime'][0]+' mins.'), 'img': cover_url}
		i+=1
	except:
		pass
		
	try:
		#Log( str(the_unt['certification']) )
		cert = [t for t in the_unt['certification'] if 'USA' in t]
		cert = cert[0].split('::')[0]
		guideVals[i] = {'showtitles': 'Certification', 'showtimes': unicode(cert), 'img': cover_url}
		i+=1
	except:
		pass
		
	try:
		#Log( str(the_unt['genres']) )
		genres = ''
		x=0
		for ca in the_unt['genres']:
			genres += ca
			if x == len(the_unt['genres'])-1:
				break
			else:
				genres += ', '
			x += 1
		guideVals[i] = {'showtitles': 'Genres', 'showtimes': (genres), 'img': cover_url}
		i+=1
	except:
		pass
		
	try:
		#Log( str(the_unt['cast']) )
		cast = ''
		x=0
		for ca in the_unt['cast']:
			cast += ca['name']
			if x > 8 or x >= len(the_unt['cast']):
				break
			else:
				cast += ', '
			x += 1
		guideVals[i] = {'showtitles': 'Cast', 'showtimes': (cast), 'img': cover_url}
		i+=1
	except:
		pass
		
	try:
		#Log( str(the_unt['writers']) )
		writers = ''
		x=0
		for ca in the_unt['writer']:
			writers += ca['name']
			if x == len(the_unt['writer'])-1:
				break
			else:
				writers += ', '
			x += 1
		guideVals[i] = {'showtitles': 'Writers', 'showtimes': (writers), 'img': cover_url}
		i+=1
	except:
		pass
		
	try:
		#Log( str(the_unt['director']) )
		directors = ''
		x=0
		for ca in the_unt['director']:
			directors += ca['name']
			if x == len(the_unt['director'])-1:
				break
			else:
				directors += ', '
			x += 1
		guideVals[i] = {'showtitles': 'Directors', 'showtimes': (directors), 'img': cover_url}
		i+=1
	except:
		pass
		
	try:
		#Log( str(the_unt['distributors']) )
		distributors = ''
		x=0
		for ca in the_unt['distributors']:
			distributors += ca['name']
			break
			x += 1
		guideVals[i] = {'showtitles': 'Distributors', 'showtimes': unicode(distributors), 'img': cover_url}
		i+=1
	except:
		pass
		
	try:
		#Log( the_unt['year'] )
		year = the_unt['year']
		guideVals[i] = {'showtitles': 'Year', 'showtimes': unicode(year), 'img': cover_url}
		i+=1
	except:
		pass
		
	try:
		#Log( the_unt['plot'][0] )
		plot = the_unt['plot'][0]
		if summary == None or (summary <> None and summary != plot):
			guideVals[i] = {'showtitles': 'Plot', 'showtimes': unicode(plot), 'img': cover_url}
			i+=1
	except:
		pass
		
	#Log(str(the_unt.keys()))
		
	return guideVals
	
###############################################################
# Based on IMDB.Bundle
# ToDo - Not Implemented Yet
#
def GetImdbDataOldMethod(title, videoUrl, url, country, lang):

	return None
	
	# Create the object that will be used to access the IMDb's database.
	ia = imdb.IMDb() # by default access the web.

	# Search for a movie (get a list of Movie objects).
	s_result = ia.search_movie('The Untouchables')
	
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