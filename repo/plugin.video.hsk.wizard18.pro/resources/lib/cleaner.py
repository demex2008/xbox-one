#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys,os,shutil,math
import xbmc,xbmcgui

def __get_sys_version():
	return sys.version_info.major

def get_convert_size(size):
	if ( size == 0 ):return '0 B'
	units = (' B',' KB',' MB',' GB',' TB',' PB',' EB',' ZB',' YB' )
	i = int( math.floor( math.log(size,1024)))
	p = math.pow(1024,i)
	size = "%.3f" % round((size / p ),3)
	return '{}{}'.format(size,units[i])

def get_directory_size(dir_path):
	size = int(0)
	for path,dirs,files in os.walk(dir_path,topdown=False,onerror=None,followlinks=True):
		for file in files:
			full_file_path = os.path.join(path, file)
			size += int(os.path.getsize(full_file_path))
	return int(size)

def delete_file(file_path):
	if os.path.exists(file_path):
		os.unlink(file_path)

def delete_directory(dir_path):
	if os.path.exists(dir_path):
		shutil.rmtree(dir_path,ignore_errors=True)

def list_directory(dir_path):
	directories_list_dict = []
	for name in os.listdir(dir_path):
		type = ''
		full_path = os.path.join(dir_path,name)
		if os.path.isfile(full_path):type = 'file'
		elif os.path.isdir(full_path):type = 'dir'
		directories_list_dict.append({'dir_name':name,'dir_path':full_path,'type':type})
	return directories_list_dict

def delete_addon_or_settings(addon_or_settings_path):
	if os.path.exists(addon_or_settings_path):
		shutil.rmtree(addon_or_settings_path,ignore_errors=True)
	if os.path.exists(addon_or_settings_path):return False
	else:return True

def clean_thumbnails(thumbnails_path):
	if os.path.exists(thumbnails_path):
		shutil.rmtree(thumbnails_path,ignore_errors=True)
		xbmc.sleep(500)
	dir_list = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','video']
	for dir in dir_list:
		dir_path = os.path.join(thumbnails_path,dir)
		if not os.path.exists(dir_path):
			os.makedirs(dir_path)

def clean_temp_and_Packages_and_thumbnails_silent(temp_path,packages_path,thumbnails_path):
	if os.path.exists(temp_path):
		shutil.rmtree(temp_path,ignore_errors=True)	  
	if os.path.exists(packages_path):
		shutil.rmtree(packages_path,ignore_errors=True)
	clean_thumbnails(thumbnails_path)

def clean_temp_and_Packages(temp_path,packages_path):

	i = xbmcgui.Dialog().yesno('[COLOR blue]CLEANER[/COLOR]','TEMP         = ' + str(get_convert_size(get_directory_size(temp_path))) + '\nPACKAGES = ' + str(get_convert_size(get_directory_size(packages_path))),nolabel='[COLOR red]Exit[/COLOR]',yeslabel='[COLOR lime]Clean[/COLOR]')
	if i > 0:

		if os.path.exists(temp_path):
			shutil.rmtree(temp_path,ignore_errors=True)	  
		if os.path.exists(packages_path):
			shutil.rmtree(packages_path,ignore_errors=True)
		 
		xbmcgui.Dialog().ok('[COLOR blue]CLEANER[/COLOR]','TEMP         = ' + str(get_convert_size(get_directory_size(temp_path))) + '\nPACKAGES = ' + str(get_convert_size(get_directory_size(packages_path))))


def clean_dir(dir_path,cleaner_save_list=[]):

	dp = xbmcgui.DialogProgress()
	sys_version = __get_sys_version()
	if sys_version == 2:dp.create('[COLOR blue]CLEANER[/COLOR]','Clean data !','Please wait ...')
	elif sys_version == 3:dp.create('[COLOR blue]CLEANER[/COLOR]','Clean data !\nPlease wait ...')
	dp.update(0)

	files_list = []
	counter = int(0)
	files_list = list(os.walk(dir_path,topdown=False,onerror=None,followlinks=True))
	list_len = sum(len(files) for path,dirs,files in files_list)

	for root,dirs,files in files_list:

		for dir in dirs:
			path = os.path.join(root,dir)
			if not any((x in path for x in cleaner_save_list)):

				if os.path.islink(path):
					try:os.unlink(path)
					except:pass
				else:
					try:os.rmdir(path)
					except:pass

		for file in files:
			path = os.path.join(root,file)
			if not any((x in path for x in cleaner_save_list)):

				try:os.unlink(path)
				except:pass

			counter +=1
			try:
				percent = int(min(counter * 100 / list_len,100))
				if sys_version == 2:dp.update(percent,'Clean data :',path)
				elif sys_version == 3:dp.update(percent,'Clean data :\n' + path)
			except:pass

		if dp.iscanceled():
			dp.close()
			return False

	dp.close()
	return True