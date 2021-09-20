#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys
import xbmcgui

def __get_sys_version():
	return sys.version_info.major

if __get_sys_version() == 2:import fixetzipfile as zipfile
elif __get_sys_version() == 3:import zipfile

def check_zip(zip_path):
	try:zip = zipfile.ZipFile(zip_path,mode='r',compression=zipfile.ZIP_STORED,allowZip64=True)
	except BadZipfile:return False
	return True

def extract_zip(zip_path,extract_path,zip_pwd='',extract_save_list=[]):

	if __get_sys_version() == 2:zip_pwd=zip_pwd
	elif __get_sys_version() == 3:zip_pwd=bytes(zip_pwd,'utf-8')

	dp = xbmcgui.DialogProgress()
	sys_version = __get_sys_version()
	if sys_version == 2:dp.create('[COLOR blue]EXTRACTOR[/COLOR]','Extract data !','Please wait ...')
	elif sys_version == 3:dp.create('[COLOR blue]EXTRACTOR[/COLOR]','Extract data !\nPlease wait ...')
	dp.update(0)

	try:zip = zipfile.ZipFile(zip_path,mode='r',compression=zipfile.ZIP_STORED,allowZip64=True)
	except BadZipfile:return False

	count = int(0)
	list_len = len(zip.infolist())
	for item in zip.infolist():

		count += 1
		try:
			percent = int(min(count * 100 / list_len ,100))
			if sys_version == 2:dp.update(percent,'Extract data:',item.filename)
			elif sys_version == 3:dp.update(percent,'Extract data:\n' + item.filename)
		except:pass

		if not any((x in item.filename for x in extract_save_list)):
			try:zip.extract(item,path=extract_path,pwd=zip_pwd)
			except:pass
			

		if dp.iscanceled():break

	zip.close()
	dp.close()

	if dp.iscanceled():return False
	else:return True