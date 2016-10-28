# https://github.com/coryo/Livestreamer.bundle
# Modified from Livestreamer.bundle
# Author: coryo
#

import common, common_fnc, streamlink

@route(common.PREFIX+'/CheckLivestreamer')
def CheckLivestreamer(url):
	""" only checks if livestreamer has a plugin to support this url, might still return no streams """
	
	try:
		streams = streamlink.streams(url)
		if Prefs['debug']:
			Log("Streamlink can handle the url %s" % url)
		return True
	except:
		pass
		
	return False

@route(common.PREFIX+'/qualities')
def Qualities(title, url, summary, thumb, art, is_streamlink):
	""" get streams from url with livestreamer, list the qualities, return none if none available """
	
	if is_streamlink:
		try:
			streams = streamlink.streams(url)
		except:
			pass

	new_streams = list()
	for quality in streams:
		if is_streamlink:
			st = stream_type_streamlink(streams[quality])
		if (st == "HLSStream") or (st == "HTTPStream"):
			surl = streams[quality].url
			new_streams.append(u"{}|{}|{}".format(st, quality, surl))

	if not new_streams:
		return None
		
	thumb = thumb if thumb != 'na' else ''
	art = art if art != 'na' else ''
	final_streams = "livestreamerccloud://" + u"title={},summary={},url={},thumb={},art={}|||".format(title, (E(JSON.StringFromObject(summary))), (E(JSON.StringFromObject(url))), thumb, art) + "||".join(new_streams)
	#final_streams = "livestreamerccloud://" + (E(JSON.StringFromObject({"url": url, "title": title, "summary": summary, "thumb": thumb, "art": art})) +"$$$") + (E(JSON.StringFromObject("||".join(new_streams))))

	vco = VideoClipObject(
		url=final_streams,
		title=title,
		summary=summary,
		thumb=thumb if thumb else None,
		art=art if art else None
		)

	return vco
	
def stream_type_streamlink(stream):
	""" get a string for the stream type """
	
	if isinstance(stream, streamlink.stream.HLSStream):
		return "HLSStream"
	elif isinstance(stream, streamlink.stream.HDSStream):
		return "HDSStream"
	elif isinstance(stream, streamlink.stream.AkamaiHDStream):
		return "AkamaiHDStream"
	elif isinstance(stream, streamlink.stream.HTTPStream):
		return "HTTPStream"
	elif isinstance(stream, streamlink.stream.RTMPStream):
		return "RTMPStream"
	return None
	
# def stream_type_livestreamer(stream):
	# """ get a string for the stream type """
	# if isinstance(stream, livestreamer.stream.HLSStream):
		# return "HLSStream"
	# elif isinstance(stream, livestreamer.stream.HDSStream):
		# return "HDSStream"
	# elif isinstance(stream, livestreamer.stream.AkamaiHDStream):
		# return "AkamaiHDStream"
	# elif isinstance(stream, livestreamer.stream.HTTPStream):
		# return "HTTPStream"
	# elif isinstance(stream, livestreamer.stream.RTMPStream):
		# return "RTMPStream"
	# return None