#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys,json,re
import xbmc,xbmcgui

def __get_sys_version():
	return sys.version_info.major

def list_addons(addons_path,enabled=False):
	addon_list_dict = []
	for name in os.listdir(addons_path):

		addon_xml_path = os.path.join(addons_path,name,'addon.xml')
		if os.path.exists(addon_xml_path):

			with open(addon_xml_path,'rb',buffering=1024*8) as xml:
				addon_id = re.compile(r'id="(.*?)"',re.DOTALL).search(xml.read().decode('utf-8'))
				if addon_id:

					try:
						query = json.loads(xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.GetAddonDetails","id":1,"params": {"addonid":"%s", "properties": ["enabled"]}}' % addon_id.group(1)))

						if ((query["result"]["addon"]["enabled"] == True) and (enabled == True)):
							addon_list_dict.append({'dir_name':name,'addon_id':addon_id.group(1)})
						elif ((query["result"]["addon"]["enabled"] == False) and (enabled == False)):
							addon_list_dict.append({'dir_name':name,'addon_id':addon_id.group(1)})

					except:
						if enabled == False:addon_list_dict.append({'dir_name':name,'addon_id':addon_id.group(1)})

	return addon_list_dict

def enable_addon(addon_id_list=[]):

	counter = int(0)
	error_counter = int(0)
	dp = xbmcgui.DialogProgress()
	sys_version = __get_sys_version()
	if sys_version == 2:dp.create('[COLOR blue]ADDONS ACTIVATOR[/COLOR]','Update new addons !','Please wait 3 sec ...')
	elif sys_version == 3:dp.create('[COLOR blue]ADDONS ACTIVATOR[/COLOR]','Update new addons !\nPlease wait 3 sec ...')
	dp.update(counter)

	xbmc.executebuiltin('UpdateAddonRepos')
	xbmc.executebuiltin('UpdateLocalAddons')
	xbmc.sleep(3000)

	for addon_id in addon_id_list:

		xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"%s", "enabled":true}}' % addon_id)
		xbmc.sleep(500)
		query = json.loads(xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.GetAddonDetails","id":1,"params": {"addonid":"%s", "properties": ["enabled"]}}' % addon_id))

		try:
			if query["result"]["addon"]["enabled"] == False:continue
		except:continue

		counter += 1
		percent = int(min(counter * 100 / len(addon_id_list) ,100))
		if sys_version == 2:dp.update(percent,'Enable addon:',addon_id)
		elif sys_version == 3:dp.update(percent,'Enable addon:\n' + addon_id)
		
		xbmc.sleep(500)

	dp.close()


def disable_addon(addon_id_list=[]):

	counter = int(0)
	error_counter = int(0)

	dp = xbmcgui.DialogProgress()
	sys_version = __get_sys_version()
	if sys_version == 2:dp.create('[COLOR blue]ADDONS DEACTIVATOR[/COLOR]','Disable addons !','Please wait ...')
	elif sys_version == 3:dp.create('[COLOR blue]ADDONS DEACTIVATOR[/COLOR]','Disable addons !\nPlease wait ...')
	dp.update(counter)

	for addon_id in addon_id_list:

		xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"%s", "enabled":false}}' % addon_id)
		xbmc.sleep(500)
		query = json.loads(xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.GetAddonDetails","id":1,"params": {"addonid":"%s", "properties": ["enabled"]}}' % addon_id))

		try:
			if query["result"]["addon"]["enabled"] == True:continue
		except:continue

		counter += 1
		percent = int(min(counter * 100 / len(addon_id_list) ,100))
		if sys_version == 2:dp.update(percent,'Disable addon:',addon_id)
		elif sys_version == 3:dp.update(percent,'Disable addon:\n' + addon_id)
		xbmc.sleep(500)

	dp.close()