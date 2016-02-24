import os, subprocess, signal # for os.path and os.kill
import time, common_fnc

# End Of Line: Windows <CR><LF> or Linux <LF> or <CR> only; split on these, with no capture
RE_EOL        = Regex('(?:(?:\r\n)?|(?:\n)?|(?:\r)?)')
# all commas not between quotes; split on commas with no capture
RE_COMMAS     = Regex('(?:,)(?=(?:[^\"]|\"[^\"]*\")*$)')

VLC_APP_FILE = 'vlc'

VLC_INSTANCES = []
VLC_EXT_INSTANCES = []

####################################################################################################
# VLC Transcoder
# based on code from VLC Plex channel / Author: walktheway
# http://forums.plex.tv/discussion/96270/vlc-channel/p1
# https://github.com/wtw2/VLC_Channel
####################################################################################################
# defaults
# transcode_opts = transcode{vcodec=h264,fps=20,vb=512,scale=1,acodec=ac3,ab=128,channels=2,samplerate=44100,venc=x264{aud,profile=high,level=60,keyint=15,bframes=0,ref=1,nocabac}}
# hls_opts = seglen=3,delsegs=true,numsegs=5
# vlc rtmp://srvvenus.canaldoboi.com/livecb/livestream --sout  #transcode{vcodec=h264,fps=20,vb=512,scale=1,acodec=ac3,venc=x264{aud,profile=high,level=60,keyint=15,bframes=0,ref=1,nocabac}}:std{access=livehttp{seglen=3,delsegs=false,numsegs=5,initial-segment-number=1,index=stream.m3u8,index-url=stream-########.ts},mux=ts{use-key-frames},dst=stream-########.ts}
#
# vlc rtmp://srvvenus.canaldoboi.com/livecb/livestream --sout  #transcode{vcodec=h264,fps=20,vb=512,scale=1,acodec=ac3,venc=x264{aud,profile=high,level=60,keyint=15,bframes=0,ref=1,nocabac}}:std{access=http,mux=ts{use-key-frames},dst=:8081/stream.mp4}
#
# vlc rtmp://srvvenus.canaldoboi.com/livecb/livestream --sout #duplicate{dst="http{mux=ts,dst=:8081/video.mp4}"}
#
#
def Transcoder(url, live_folder_path, session, ext, local_file, preRoll, mainRoll, preInit):
	
	transcode_prog = Prefs['transcode_prog']
	if transcode_prog <> None and transcode_prog != '':
		VLC_APP_FILE = transcode_prog
	transcode_opts = Prefs['transcode_opt1']
	hls_opts = Prefs['transcode_opt2']
	server_url = Prefs['transcode_server']
	
	if preRoll:
		#local_file = 'https://www.youtube.com/watch?v=u2s5vwvo5wQ'
		
		transcode_cmd = VLC_APP_FILE + ' ' + local_file + ' --sout=#'+transcode_opts+':std{access=livehttp{'+hls_opts+',index='+live_folder_path+session+ext+',index-url='+session+'-t########.ts},mux=ts{use-key-frames},dst='+live_folder_path+session+'-t########.ts}'
		if Prefs['debug']:
			Log("----------------Starting PreRoll Transcoder---------------------")
			Log(transcode_cmd)
		vlc_proc0 = subprocess.Popen(transcode_cmd, 102400)
		if Prefs['debug']:
			Log("---VLC Instance---" + str(vlc_proc0.pid))
			#Dict[session] = {'pid' : str(vlc_proc.pid)}
			#VLC_INSTANCES.append(str(vlc_proc.pid))
			Log("---------------- Transcoder Running---------------------")
		Thread.Create(CloseInstanceAfter, {}, vlc_proc0.pid, 30)
	
	if mainRoll:
		transcode_cmd = VLC_APP_FILE + ' ' + ' ' + url + ' --sout=#'+transcode_opts+':std{access=livehttp{'+hls_opts+',index='+live_folder_path+session+ext+',index-url='+session+'-########.ts},mux=ts{use-key-frames},dst='+live_folder_path+session+'-########.ts}'
		if Prefs['debug']:
			Log("----------------Starting MainRoll Transcoder---------------------")
			Log(transcode_cmd)
		vlc_proc = subprocess.Popen(transcode_cmd, 102400)
		if Prefs['debug']:
			Log("---VLC Instance---" + str(vlc_proc.pid))

		session = common_fnc.getSession()
		Dict[session] = {'pid' : str(vlc_proc.pid)}
		VLC_INSTANCES.append(str(vlc_proc.pid))
		if Prefs['debug']:
			Log("---------------- Transcoder Running---------------------")
	
	Dict.Save()
	return True
	
	
	
####################################################################################################
#   This function checks to see if the application is running.
#   It does not determine if the application was launched by this Plex channel.
#       app_app_file - application file name only (with extension)
#
#	app_app_file = VLC_APP_FILE
#
def AppRunning():
	Log.Debug("EXECUTING: AppRunning()")
	# get PID for vlc.exe if running
	procs = subprocess.check_output(['tasklist', '/fo', 'csv']) # get the list of processes
	procs = RE_EOL.split(procs)
#	Log.Debug("@@@@@@@ " +JSON.StringFromObject(procs))
	procEntry = [row for row in procs if row.find(VLC_APP_FILE) > 0] # CSV list of lines; find line(s)
	if len(procEntry) > 0:
		if len(procEntry) > 1: # multiple instances of App are running
			Log.Debug("# App Procs= " + str(len(procEntry)))
#		Log.Debug("@@@@@@@ " +procEntry[0])
		procArray = [val.replace('"','') for val in RE_COMMAS.split(procEntry[0])] # CSV list of values
#		Log.Debug("@@@@@@@ "+JSON.StringFromObject(procArray))
		ret = int(procArray[1]) # set the indicator
#		Log.Debug("@@@@@@@ "+str(ret))
	else:
		ret = -1
	Log.Debug("APP_PID= "+str(ret))
	return ret
	
####################################################################################################
#   This function checks to see if the application is running - all instances.
#   It does not determine if the application was launched by this Plex channel.
#   It will then try and kill all the running processes based on its pid
#
#	
def CloseAllInstances():

	vlc_app_pid = AppRunning()
	while vlc_app_pid != -1:
		if vlc_app_pid in VLC_INSTANCES:
			Log("----------------Closing VLC---------------------")
			os.kill(int(vlc_app_pid), signal.SIGTERM)
		time.sleep(1)
		vlc_app_pid = AppRunning()

def CloseThisSessionPidInstance():

	try:
		session  = common_fnc.getSession()
		#Log(" ------------ Existing session " + session)
		pid = Dict[session]['pid']
		if pid <> None and pid != -1:
			#Log(" ------------ Existing pid " + pid)
			ClosePidInstance(pid)
			Dict[session]['pid'] = -1
			Dict.Save()
	except:
		pass
		
def ClosePidInstance(vlc_app_pid):

	try:
		#Log("----------------Closing VLC---------------------")
		os.kill(int(vlc_app_pid), signal.SIGTERM)
	except:
		pass
		

def GetAllExtVlcInstances():
	
	vlc_app_pid = AppRunning()
	while vlc_app_pid != -1 and vlc_app_pid not in VLC_EXT_INSTANCES and vlc_app_pid not in VLC_INSTANCES:
		if vlc_app_pid not in VLC_EXT_INSTANCES and vlc_app_pid not in VLC_INSTANCES:
			VLC_EXT_INSTANCES.append(vlc_app_pid)
			#Log("----------------VLC Ext Instance Added---------------------")
		vlc_app_pid = AppRunning()
		
def IsTranscoding():
	session = common_fnc.getSession()
	pid = Dict[session]['pid']
	return check_pid(pid) 
	
def check_pid(pid):        
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True
		
def CloseInstanceAfter(pid, xtime):

	time.sleep(xtime)
	ClosePidInstance(pid)
	return
	