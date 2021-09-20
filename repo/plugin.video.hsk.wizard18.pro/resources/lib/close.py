#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys,os
import xbmc,xbmcgui

def close_kodi(home_path):

	if xbmc.getCondVisibility('System.Platform.Windows'):
		try:os.system('@ECHO off')
		except:pass
		try:os.system('TSKKILL Kodi*')
		except:pass
		try:os.system('TASKKILL /IM Kodi* /T /F')
		except:pass

	elif xbmc.getCondVisibility('System.Platform.Android'):
		try: os.system('adb shell kill org.xbmc.kodi')
		except: pass
		try:os.system('adb shell am force-stop org.xbmc.kodi')
		except:pass

		xbmcgui.Dialog().ok('[COLOR red]DANGER ![/COLOR]','[COLOR red]Android system discovered ![/COLOR]','[COLOR red]Force the termination of the program ![/COLOR]','[COLOR red]Do not exit the program via Exit or Quit !\nPress OK ![/COLOR]')
		if 'kodi'in home_path.lower():xbmc.executebuiltin('StartAndroidActivity("","android.settings.APPLICATION_DETAILS_SETTINGS","","package:org.xbmc.kodi")')
		else:xbmc.executebuiltin('StartAndroidActivity("","android.settings.APPLICATION_SETTINGS","","")')
		sys.exit(0)

	elif xbmc.getCondVisibility('System.Platform.Linux') or xbmc.getCondVisibility('System.Platform.Darwin'):
		try:os.system('killall Kodi')
		except:pass
		try:os.system('killall -9 Kodi')
		except:pass
		try:os.system('killall -9 kodi.bin')
		except:pass

	elif xbmc.getCondVisibility('System.Platform.OSX'):
		try:os.system('killall AppleTV')
		except:pass
		try:os.system('killall -9 AppleTV')
		except:pass

	elif xbmc.getCondVisibility('System.Platform.Linux.RaspberryPi'):
		try:os.system('sudo initctl stop kodi')
		except:pass

	xbmcgui.Dialog().ok('[COLOR red]DANGER ![/COLOR]','[COLOR red]Program could not be stopped ![/COLOR]\n[COLOR red]Force the termination of the program ![/COLOR]\n[COLOR red]Do not exit the program via Exit or Quit ![/COLOR]')
	sys.exit(0)