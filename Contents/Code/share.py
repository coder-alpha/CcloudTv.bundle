import datetime as DT
import urllib2, common, common_fnc
import json

MY_TOKEN = "UTBFdFZHOXJaVzQ9"
data = "test data"
COMMIT_URL = "aHR0cDovLzk0LjIzLjM1LjQyL2NDbG91ZFR2L1BsZXhDb21taXQucGhw"

ARRAY_COMITTED_URLS = []

@route(common.PREFIX + '/commit')
def commit(curl, data):

	try:
		#Log("----------------------------------------------------- ")
		#dateToday = DT.datetime.utcnow()
		#commit_time = str(dateToday.month) + '/' + str(dateToday.day) + '/' + str(dateToday.year)
		#commit_time = str(dateToday + ' UTC')
		#Log("commit_time --------- " + commit_time)
		#Log("data ------------- " + data)

		attempt = 0
		while (attempt < 2):
			page = HTTP.Request(common_fnc.decode(COMMIT_URL) + '?token=' +  common_fnc.decode(MY_TOKEN)).content
			elems = HTML.ElementFromString(page)
			try:
				auth = elems.xpath(".//div[@class='validate']//@value")[0]
			except:
				auth = None
			if 'Ready for cCloud TV Commit' in page and auth <> None:
				content = common_fnc.encode(data)
				#Log("content = " + content)
				# make commit
				try:
					resp = HTTP.Request(common_fnc.decode(COMMIT_URL) + '?token=' +  common_fnc.decode(MY_TOKEN) + '&data=' + content + '&validate=' + auth).content
					if 'Success: Data Comitted to cCloud TV' in resp:
						ARRAY_COMITTED_URLS.append(curl)
						return True
				except:
					pass
					#print(e.reason)
			else:
				return False
			attempt = attempt + 1
		
	except:
		return False
	
	return False

@route(common.PREFIX + '/isCommitted')
def isCommitted(curl):

	try:
		if curl in str(ARRAY_COMITTED_URLS):
			return True
	except:
		pass
		
	return False
	
@route(common.PREFIX + '/isConfirmCommitted')
def isConfirmCommitted(curl):

	try:
		page = HTTP.Request(common_fnc.decode(COMMIT_URL) + '?token=' + common_fnc.decode(MY_TOKEN) + '&confirm=' + common_fnc.encode(curl)).content
		if 'Confirmed Commit' in page:
			return True
	except:
		pass
		
	return False
	
def ResetCommits(page_data):

	try:
		for vals in Dict:
			try:
				#Log(vals + '    ' + Dict[vals])
				if ('Plex-Share-Pin' in vals and Dict[vals] in page_data) or 'removed' in Dict[vals]:
					Dict[vals] = None
			except:
				pass
	except:
		pass
		
	Dict.Save()
