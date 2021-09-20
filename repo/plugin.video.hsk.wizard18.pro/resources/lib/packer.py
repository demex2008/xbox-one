#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys,time
import xbmc,xbmcgui

def __get_sys_version():
	return sys.version_info.major

if __get_sys_version() == 2:import fixetzipfile as zipfile
elif __get_sys_version() == 3:import zipfile

def zip_dir(dir_path,zip_save_path,base_dir=True):

	dp = xbmcgui.DialogProgress()
	sys_version = __get_sys_version()
	if sys_version == 2:dp.create('[COLOR blue]ZIPPER[/COLOR]','Create zip archive !','Please wait ...')
	elif sys_version == 3:dp.create('[COLOR blue]ZIPPER[/COLOR]','Create zip archive !\nPlease wait ...')
	dp.update(0)

	dir_path = os.path.abspath(dir_path)
	zip_save_path = os.path.abspath(zip_save_path)

	pv = sys.version[0:6]
	dt = time.strftime('%d%m%Y%H%M%S')
	bv = xbmc.getInfoLabel('System.BuildVersion')[0:5]
	new_archive_name = 'KB_BV_{0}_PV_{1}_DT_{2}'.format(bv,pv,dt)

	zip_full_save_path = os.path.join(zip_save_path,new_archive_name + '.zip')
	zip = zipfile.ZipFile(zip_full_save_path,mode='w',compression=zipfile.ZIP_STORED,allowZip64=True)

	count = int(0)
	files_list = []

	files_list = list(os.walk(dir_path,topdown=False,onerror=None,followlinks=True))
	list_len = sum(len(files) for path,dirs,files in files_list)

	root_len = len(dir_path)
	if base_dir == True:root_len = root_len - len(os.path.basename(dir_path))

	for root,dirs,files in files_list:

		for file in files:
			path = os.path.join(root,file)
			archive_name = os.path.join(os.path.abspath(root)[root_len:],file)
			try:zip.write(path,archive_name,zipfile.ZIP_DEFLATED)
			except:pass

			count += 1
			try:
				percent = int(min(count * 100 / list_len ,100))
				dp.update(percent)
			except:pass

			if dp.iscanceled():break

	zip.close()
	dp.close()

	if dp.iscanceled():return False
	else:return True