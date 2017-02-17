# Adapted from
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
import transcoder, common, common_fnc, livestreamer_fnc
import os, sys, re, time, urllib2, urlparse

# clients that dont require rtmp transcoding
RTMP_TRANSCODE_CLIENTS = ['Plex Web']

MP4_VIDEOS = ['googlevideo.com','googleusercontent.com','blogspot.com']
INCOMPATIBLE_URL_SERVICES = ['stream.mslive.in','stream.north.kz','stream.sportstv.com.tr','www.youtube.com','stream.canalsavoir.tv']
COMPATIBLE_URL_SERVICES = ['167.114.102.27']

try:
	res_folder_path = os.getcwd().split("?\\")[1].split('Plug-in Support')[0]+"Plug-ins/CcloudTv.bundle/Contents/Resources/"
except:
	res_folder_path = os.getcwd().split("Plug-in Support")[0]+"Plug-ins/CcloudTv.bundle/Contents/Resources/"
if res_folder_path not in sys.path:
	sys.path.append(res_folder_path)
	
URL_CACHE = {}
	
####################################################################################################
@route(common.PREFIX + '/createvideoclipobject', allow_sync=True)
def CreateVideoClipObject(url, title, thumb, summary, session, inc_container = False, transcode = False, dontUseURLServ=False, rating=None, content_rating=None, duration=None, studio=None, year=None, genres=None, actors=None, writers=None, directors=None):

	if '.m3u8' in url and inc_container == False and GetUrlCacheStatus(url):
		URL_CACHE.clear()
		Thread.Create(GetAndPopUrl, {}, url)
	
	if rating != None:
		rating = float(rating)
	if duration != None:
		duration = int(duration)
	if year != None:
		year = int(year)
	genres_a = []
	if genres != None:
		for g in genres.split(','):
			if g != '':
				genres_a.append(g.strip())
			
	writers_a = []
	if writers != None:
		for w in writers.split(','):
			if w != '':
				writers_a.append(w.strip())
			
	directors_a = []
	if directors != None:
		for d in directors.split(','):
			if d != '':
				directors_a.append(d.strip())
		
	roles_a = []
	if actors != None:
		for r in actors.split(','):
			if r != '':
				roles_a.append(r.strip())
		
	vco = ''
	
	if inc_container == False and '.m3u8' not in url:
		is_streamlink = livestreamer_fnc.CheckLivestreamer(url=url)
		if is_streamlink:
			vco = livestreamer_fnc.Qualities(title=title, url=url, summary=summary, thumb=thumb, art=thumb, is_streamlink=is_streamlink)
			if vco != None:
				if Prefs['debug']:
					Log("Using Livestreamer API")
				return vco
			else:
				if Prefs['debug']:
					Log("Not Using Livestreamer API")
	
	if '.mp3' in url or '.aac' in url or 'mmsh:' in url:
		container = Container.MP4
		audio_codec = AudioCodec.AAC
		
		if '.mp3' in url:
			container = 'mp3'
			audio_codec = AudioCodec.MP3
		elif '.aac' in url:
			container = 'aac'
			audio_codec = AudioCodec.AAC
			
		vco = TrackObject(
			key = Callback(CreateVideoClipObject, url = url, title = title, thumb = thumb, summary = summary, session = session, inc_container = True, dontUseURLServ=dontUseURLServ, rating=rating, duration=duration),
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
	elif '.mp4' in url and '.m3u8' not in url and url.startswith('http'):
		# we will base64 encode the url, so that any conflicting url service does not interfere
		vco = VideoClipObject(
			url = "ccloudtv://" + E(JSON.StringFromObject(({"url":url, "title": title, "summary": summary, "thumb": thumb, "rating": rating, "duration": duration, "content_rating": content_rating, "studio": studio, "year": year, "genres": genres, "writers": writers, "directors": directors, "roles": actors}))),
			title = title,
			thumb = thumb,
			rating = rating,
			duration = duration,
			content_rating = content_rating,
			year = year,
			studio = studio,
			genres = genres_a,
			summary = summary
		)
	elif common_fnc.ArrayItemsInString(MP4_VIDEOS, url) and '.m3u8' not in url and url.startswith('http'):
		# we will base64 encode the url, so that any conflicting url service does not interfere
		vco = VideoClipObject(
			url = "ccloudtv://" + E(JSON.StringFromObject(({"url":url, "title": title, "summary": summary, "thumb": thumb, "rating": rating, "duration": duration, "content_rating": content_rating, "studio": studio, "year": year, "genres": genres, "writers": writers, "directors": directors, "roles": actors}))),
			title = title,
			thumb = thumb,
			rating = rating,
			duration = duration,
			content_rating = content_rating,
			year = year,
			studio = studio,
			genres = genres_a,
			summary = summary
		)
	elif '.m3u8' not in url and 'rtmp:' in url and transcode and Prefs['use_transcoder']: # transcode case
		
		#if inc_container:
		file = "file:///" + res_folder_path.replace('\\','/').replace(' ','%20') + "MyPreRoll.mp4"
		live_folder_path = Prefs['transcode_server_local']
		bool = transcoder.Transcoder(url, live_folder_path, session , '.m3u8', file, False, True, False)
		
		if bool:
			if 'Host' in Request.Headers:
				host = Request.Headers['Host']
				host = host.replace('-','.')
			else:
				host = None
			if Prefs['debug']:
				Log("Host ---------------- " + str(host))
			url = Prefs['transcode_server'] + session + '.m3u8'
			
		vco = VideoClipObject(
			key = Callback(CreateVideoClipObject, url = url, title = title, thumb = thumb, summary = summary, session = session, inc_container = True, transcode=transcode, dontUseURLServ=dontUseURLServ, rating=rating, duration=duration),
			#rating_key = url,
			url = url,
			title = title,
			summary = summary,
			thumb = thumb,
			rating = rating,
			duration = duration,
			items = [
				MediaObject(
					#container = Container.MP4,	 # MP4, MKV, MOV, AVI
					#video_codec = VideoCodec.H264, # H264
					#audio_codec = AudioCodec.AAC,  # ACC, MP3
					#audio_channels = 2,			# 2, 6
					#container = container,
					#audio_codec = audio_codec,
					parts = [PartObject(key = GetVideoURL(url = url, live = True, transcode=transcode, finalPlay=inc_container))],
					optimized_for_streaming = True
				)
			]
		)
	else:
		url_serv = None
		if not dontUseURLServ and common_fnc.ArrayItemsInString(COMPATIBLE_URL_SERVICES, url) and not common_fnc.ArrayItemsInString(INCOMPATIBLE_URL_SERVICES, url):
			if Prefs['debug']:
				Log("Finding URLService for " + url)
			url_serv = URLService.ServiceIdentifierForURL(url)
		if url_serv <> None:
			if Prefs['debug']:
				Log("Using URLService for " + url)
			p = re.compile(ur'^((http[s]?|ftp):\/)?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)(.*)?(#[\w\-]+)?$')
			remote_host = re.search(p, url).group(3)
			vco = VideoClipObject(
				url = remote_host + "ccloudtv2://" + E(JSON.StringFromObject(({"url":url, "title": title, "summary": summary, "thumb": thumb, "rating": rating, "duration": duration}))),
				title = title,
				summary = summary,
				rating = rating,
				duration = duration,
				thumb = thumb
			)
		else:
			if url.endswith('.ts') and inc_container:
				parts = []
				rangeX = rangeX = 1000
				for x in range(0,rangeX):
					po = PartObject(key = GetVideoURL(url = url, live = True, transcode=transcode, finalPlay=inc_container), duration = 86400000)
					parts.append(po)
					
				vco = VideoClipObject(
					key = Callback(CreateVideoClipObject, url = url, title = title, thumb = thumb, summary = summary, session = session, inc_container = True, dontUseURLServ=dontUseURLServ, rating=rating, duration=duration),
					rating_key = title,
					#url = url,
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
							parts = parts,
							optimized_for_streaming = Prefs["optimized_for_streaming"]
						)
					]
				)
			else:
				vco = VideoClipObject(
					key = Callback(CreateVideoClipObject, url = url, title = title, thumb = thumb, summary = summary, session = session, inc_container = True, dontUseURLServ=dontUseURLServ, rating=rating, duration=duration),
					rating_key = title,
					#url = url,
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
							parts = [PartObject(key = GetVideoURL(url = url, live = True, transcode=transcode, finalPlay=inc_container), duration = 86400000)],
							optimized_for_streaming = Prefs["optimized_for_streaming"]
						)
					]
				)
				

	if inc_container:
		return ObjectContainer(objects = [vco])
	else:
		return vco
		
####################################################################################################
def GetVideoURL(url, live, transcode, finalPlay, **kwargs):

	#url = 'http://wpc.c1a9.edgecastcdn.net/hls-live/20C1A9/cnn/ls_satlink/b_828.m3u8?Vd?u#bt!25'
	
	if '.m3u' in url and '.ts' in url:
		#return HTTPLiveStreamURL(url=url) # does not work - retrieves only single segment
		return PlayVideoLive(url=url) # playing .ts segments as PartObjects
	elif url.startswith('rtmp') and not transcode:
		if Prefs['debug']:
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
	else:
		if transcode and finalPlay:
			time.sleep(10) # give some delay for transcoding to begin - remember output m3u8 is not instant
			
		if transcode:
			return HTTPLiveStreamURL(url=url)

		return HTTPLiveStreamURL(url = GetMyRedUrl(url, finalPlay))

####################################################################################################
@indirect
def PlayVideoLive(url):

	return HTTPLiveStreamURL(url=url)
	#return Redirect(url)
	#return IndirectResponse(VideoClipObject, key=url, http_headers=http_headers)
	
def GetAndPopUrl(url):
	if Prefs["debug"]:
		Log("GetAndPopUrl Thread for %s" % url)
	URL_CACHE['Alive-%s' % E(url)] = True
	redurl = GetRedirect(url, 5)
	if redurl == None:
		redurl = GetRedirect(url, 8, url)
	if redurl == None:
		redurl = url
	URL_CACHE[url] = redurl
	URL_CACHE['ts'] = time.time()
	URL_CACHE['Alive-%s' % E(url)] = False

def GetMyRedUrl(url, finalPlay):
	if url in URL_CACHE:
		url = URL_CACHE[url]
	elif finalPlay and ('Alive-%s' % E(url)) in URL_CACHE and URL_CACHE['Alive-%s' % E(url)] == True:
		time.sleep(0.5)
	return url
	
def GetUrlCacheStatus(url):
	key = 'Alive-%s' % E(url)
	if (key not in URL_CACHE) or (key in URL_CACHE and URL_CACHE[key] == False and int(time.time())-int(URL_CACHE['ts']) > 1000):
		return True
	else:
		return False

def GetRedirect(url, timeout, ref=None):
	class HTTPRedirectHandler(urllib2.HTTPRedirectHandler):
		def redirect_request(self, req, fp, code, msg, headers, newurl):
			newreq = urllib2.HTTPRedirectHandler.redirect_request(self,
				req, fp, code, msg, headers, newurl)
			if newreq is not None:
				self.redirections.append(newreq.get_full_url())
			return newreq
	
	redirectHandler = HTTPRedirectHandler()
	redirectHandler.max_redirections = 10
	redirectHandler.redirections = []

	opener = urllib2.build_opener(redirectHandler)
	opener = urllib2.install_opener(opener)
	
	headers = {}
	headers['User-Agent'] = common.USER_AGENT
	
	if ref != None:
		headers['Referer'] = '%s://%s/' % (urlparse.urlparse(url).scheme, urlparse.urlparse(url).netloc)

	request = urllib2.Request(url, headers=headers)

	try:
		response = urllib2.urlopen(request, timeout=int(timeout))
		for redURL in redirectHandler.redirections:
			#urlList.append(redURL) # make a list, might be useful
			url = redURL
			if Prefs["debug"]:
				Log("Redirect: %s" % url)
		return url
	except urllib2.HTTPError as response:
		Log('URL: %s' % url)
		Log('Error: %s' % response)
		return None
