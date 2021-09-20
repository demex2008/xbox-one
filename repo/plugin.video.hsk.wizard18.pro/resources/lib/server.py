#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests,re
import xbmcgui
	
def get_backup_dict_list(url='',auth=None,timeout=15,headers={},server_encoding=''):

	try:

		backups_dict_list = []
		if not url.endswith('/'):url = url + '/'

		req = requests.get(url=url,stream=False,verify=False,auth=auth,timeout=timeout,headers=headers)
		req.encoding = '{0}'.format(server_encoding)
		if req.status_code == 200:

			content = req.text
			for backup_name in re.compile(r'href="(.*?)\.zip"').findall(content):

				backup_name = backup_name.strip()
				backup_url = url + backup_name + '.zip'
				
				backup_image_url = ''
				if backup_name + '.png' in content:
					backup_image_url = url + backup_name + '.png'
				elif backup_name + '.svg' in content:
					backup_image_url = url + backup_name + '.svg'
				elif backup_name + '.gif' in content:
					backup_image_url = url + backup_name + '.gif'
				elif backup_name + '.jpg' in content:
					backup_image_url = url + backup_name + '.jpg'
				elif backup_name + '.jpeg' in content:
					backup_image_url = url + backup_name + '.jpeg'
					
				backup_plot_text = ''
				if backup_name + '.txt' in content:
					backup_plot_url = url + backup_name + '.txt'
					req = requests.get(url=backup_plot_url,stream=False,verify=False,auth=auth,timeout=timeout,headers=headers)
					req.encoding = '{0}'.format(server_encoding)
					if req.status_code == 200:backup_plot_text = req.text

				backups_dict_list.append({'backup_name':backup_name,'backup_url':backup_url,'backup_img_url':backup_image_url,'backup_plot_text':backup_plot_text})

			return backups_dict_list
		
		else:
			xbmcgui.Dialog().ok('[COLOR red]REQUESTS INFO[/COLOR]','Status code : ' + str(req.status_code))
			return False

	except Exception as e:
		xbmcgui.Dialog().ok('[COLOR red]REQUESTS ERROR[/COLOR]',str(e))
		return False


def get_addons_or_settings_dict_list(url='',auth=None,timeout=15,headers={},server_encoding=''):

	try:

		addons_or_settings_dict_list = []
		if not url.endswith('/'):url = url + '/'

		req = requests.get(url=url,stream=False,verify=False,auth=auth,timeout=timeout,headers=headers)
		req.encoding = '{0}'.format(server_encoding)
		if req.status_code == 200:

			content = req.text
			for addon_or_settings_name in re.compile(r'href="(.*?)\.zip"').findall(content):

				addon_or_settings_name = addon_or_settings_name.strip()
				addon_or_settings_url = url + addon_or_settings_name + '.zip'
				
				addons_or_settings_image_url = ''
				if addon_or_settings_name + '.png' in content:
					addons_or_settings_image_url = url + addon_or_settings_name + '.png'
				elif addon_or_settings_name + '.svg' in content:
					addons_or_settings_image_url = url + addon_or_settings_name + '.svg'
				elif addon_or_settings_name + '.gif' in content:
					addons_or_settings_image_url = url + addon_or_settings_name + '.gif'
				elif addon_or_settings_name + '.jpg' in content:
					addons_or_settings_image_url = url + addon_or_settings_name + '.jpg'
				elif addon_or_settings_name + '.jpeg' in content:
					addons_or_settings_image_url = url + addon_or_settings_name + '.jpeg'
				
				addons_or_settings_plot_text = ''
				if addon_or_settings_name + '.txt' in content:
					addons_or_settings_plot_url = url + addon_or_settings_name + '.txt'
					req = requests.get(url=addons_or_settings_plot_url,stream=False,verify=False,auth=auth,timeout=timeout,headers=headers)
					req.encoding = '{0}'.format(server_encoding)
					if req.status_code == 200:addons_or_settings_plot_text = req.text

				addons_or_settings_dict_list.append({'addon_or_settings_name':addon_or_settings_name,'addon_or_settings_url':addon_or_settings_url,'addons_or_settings_image_url':addons_or_settings_image_url,'addons_or_settings_plot_text':addons_or_settings_plot_text})

			return addons_or_settings_dict_list
		
		else:
			xbmcgui.Dialog().ok('[COLOR red]REQUESTS INFO[/COLOR]','Status code : ' + str(req.status_code))
			return False

	except Exception as e:
		xbmcgui.Dialog().ok('[COLOR red]REQUESTS ERROR[/COLOR]',str(e))
		return False