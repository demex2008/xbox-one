#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys,shutil
import xbmc,xbmcgui

def read_log(addon,log_file_path,error_log_file_path,log_mode='log'):

	if os.path.exists(error_log_file_path):
		os.unlink(error_log_file_path)

	if os.path.exists(log_file_path):
	
		if log_mode == 'log':

			with open(log_file_path,'rb',buffering=1024*8) as fi:
				log_file_content = fi.read().decode('utf-8')
				xbmcgui.Dialog().textviewer(heading='[COLOR blue]LOG READER[/COLOR]',text=log_file_content.replace('ERROR:','[COLOR red]ERROR[/COLOR]:').replace('WARNING:','[COLOR orange]WARNING[/COLOR]:'))

		elif log_mode == 'ip_log':
		
			ip = addon.getSetting('webinterface_ip').strip()
			if not ip:
				ip = xbmc.getIPAddress()
				addon.setSetting('webinterface_ip',ip)

			port = addon.getSetting('webinterface_port').strip()

			username = addon.getSetting('webinterface_username').strip()
			password = addon.getSetting('webinterface_password').strip()

			shutil.copyfile(log_file_path,error_log_file_path)
			xbmc.startServer(iTyp=xbmc.SERVER_WEBSERVER,bStart=True,bWait=False)
			xbmcgui.Dialog().ok('[COLOR blue]IP LOG ADDRESS[/COLOR]','[COLOR red]http://' + username + ':' + password + '@' + ip + ':' + port + '/kodi.log[/COLOR]\n[COLOR blue]Activate the addon under web interface:[/COLOR]\n[COLOR blue]Settings - Services - Control - Allow remote control via HTTP[/COLOR]')
			xbmc.startServer(iTyp=xbmc.SERVER_WEBSERVER,bStart=False,bWait=False)

	else:xbmcgui.Dialog().ok('[COLOR red]LOG READER ERROR[/COLOR]','No log file found !')