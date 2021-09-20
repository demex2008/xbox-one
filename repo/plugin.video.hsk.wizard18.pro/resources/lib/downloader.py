#!/usr/bin/python
# -*- coding: utf-8 -*-
import io,requests
import xbmcgui
import sys

def __get_sys_version():
	return sys.version_info.major

def download_cfg_file(url='',cfg_file_path='',auth=None,timeout=30,headers={}):

	try:

		req = requests.get(url=url,stream=False,verify=False,auth=auth,timeout=timeout,headers=headers)
		if req.status_code == 200:
			with open(cfg_file_path,'wb') as cfg:
				cfg.write(req.content)
			
		else:
			xbmcgui.Dialog().ok('REQUESTS INFO','Status code : ' + str(req.status_code))
			return False

	except Exception as e:
		xbmcgui.Dialog().ok('[COLOR red]REQUESTS ERROR[/COLOR]',str(e))
		return False

def download_byte_content(url='',auth=None,timeout=30,headers={}):

	try:

		req = requests.get(url=url,stream=True,verify=False,auth=auth,timeout=timeout,headers=headers)
		if req.status_code == 200:

			dp = xbmcgui.DialogProgress()
			sys_version = __get_sys_version()
			if sys_version == 2:dp.create('[COLOR blue]DOWNLOADER[/COLOR]','Download content !','Please wait ...')
			elif sys_version == 3:dp.create('[COLOR blue]DOWNLOADER[/COLOR]','Download content !\nPlease wait ...')
			dp.update(0)

			chunk_len= int(0)
			bytes = io.BytesIO()
			content_bytes_len = int(req.headers.get('Content-Length'))

			while True:

				chunk = req.raw.read(1024*16)
				if not chunk:break

				chunk_len += len(chunk)
				bytes.write(chunk)
				try:
					percent = int(min(chunk_len * 100 / content_bytes_len ,100))
					dp.update(percent)
				except:pass

				if dp.iscanceled():break

			dp.close()
			req.close()

			if dp.iscanceled():return False
			else:return bytes
			
		else:
			xbmcgui.Dialog().ok('REQUESTS INFO','Status code : ' + str(req.status_code))
			return False

	except Exception as e:
		xbmcgui.Dialog().ok('[COLOR red]REQUESTS ERROR[/COLOR]',str(e))
		return False