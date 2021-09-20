#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys,os,codecs,re
import xbmc,xbmcgui,xbmcaddon,xbmcplugin,urllib,io
from io import BytesIO

def __get_sys_version():
	return sys.version_info.major

def __fix_encoding__(path):
	if __get_sys_version() == 2:

		if sys.platform.startswith('win'):return path.decode('utf-8')
		else:return path.decode('utf-8').encode('ISO-8859-1')

	elif __get_sys_version() == 3:return path


def __quote_plus__(s):
	if __get_sys_version() == 2:return urllib.quote_plus(s)
	elif __get_sys_version() == 3:return urllib.parse.quote_plus(s)
	
def __unquote_plus__(s):
	if __get_sys_version() == 2:return urllib.unquote_plus(s)
	elif __get_sys_version() == 3:return urllib.parse.unquote_plus(s)

__addon__ =  xbmcaddon.Addon()
__addon_id__ = __addon__.getAddonInfo('id')
__addon_path__ = __fix_encoding__(__addon__.getAddonInfo('path'))
__addon_icon__ = __fix_encoding__(__addon__.getAddonInfo('icon'))
special_path_home = __fix_encoding__(xbmc.translatePath('special://home'))

sys.path.append(os.path.join(__addon_path__,'resources','libs'))
import zipfile
import requests

request_timeout = 10

request_headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
	'Accept-Language':'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
	'Cache-Control':'max-age=0',
	'Connection':'keep-alive',
	'Upgrade-Insecure-Requests':'1'
	}

cleaner_save_list = [__addon_id__,'service.hsk.archive.installer','service.hsk.private.archive.installer','Addons27.db','Textures13.db','kodi.log']
extract_save_list = [__addon_id__]

if __addon__.getSetting('save_sources') == 'true':
	cleaner_save_list = cleaner_save_list + ['sources.xml']
	extract_save_list = extract_save_list + ['sources.xml']
if __addon__.getSetting('save_favourites') == 'true':
	cleaner_save_list = cleaner_save_list + ['favourites.xml']
	extract_save_list = extract_save_list + ['favourites.xml']
if __addon__.getSetting('save_advancedsettings') == 'true':
	cleaner_save_list = cleaner_save_list + ['advancedsettings.xml']
	extract_save_list = extract_save_list + ['advancedsettings.xml']

def add_dir(title,url,img,mode):
    u=sys.argv[0]+'?title=' + __quote_plus__(title) + '&url=' + __quote_plus__(url) + '&img=' + __quote_plus__(img) + '&mode=' + str(mode)
    lis=xbmcgui.ListItem(title,path=url)
    lis.setInfo(type='Video',infoLabels={'Title':title} )
    lis.setArt({'icon':img,'poster':img,'banner':img,})
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=lis,isFolder=True)

def load_zip_content(url,timeout,headers={}):

    try:

        req = requests.get(url,stream=True,timeout=timeout,headers=headers)
        if req.status_code == 200:

            dp = xbmcgui.DialogProgress()
            dp.create('[COLOR blue]DOWNLOAD ZIP CONTENT[/COLOR]','Loading data !\nPlease wait ...')
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

                if dp.iscanceled():
                    dp.close()
                    sys.exit(0)

            dp.close()
            return bytes

    except Exception as exc:
        xbmcgui.Dialog().ok('[COLOR red]DOWNLOAD ZIP CONTENT ERROR[/COLOR]',str(exc))
        sys.exit(0)

def clean_kodi(dir_path,save_list_array=[]):

    try:

        dp = xbmcgui.DialogProgress()
        dp.create('[COLOR blue]KODI CLEANER[/COLOR]','Clean data !\nPlease wait ...')
        dp.update(0)

        files_list = []
        counter = int(0)
        files_list = list(os.walk(dir_path,topdown=False,onerror=None,followlinks=True))
        list_len = sum(len(files) for path,dirs,files in files_list)

        for root,dirs,files in files_list:

            for dir in dirs:
                path = os.path.join(root,dir)
                if not any((x in path for x in save_list_array)):

                    if os.path.islink(path):
                        try:os.unlink(path)
                        except:pass
                    else:
                        try:os.rmdir(path)
                        except:pass

            for file in files:
                path = os.path.join(root,file)
                if not any((x in path for x in save_list_array)):

                    try:os.unlink(path)
                    except:pass

                counter +=1
                try:
                    percent = int(min(counter * 100 / list_len,100))
                    dp.update(percent,'Clean data :\n' + path)
                except:pass

            if dp.iscanceled():
                dp.close()
                return False

        dp.close()
        return True

    except Exception as exc:
        xbmcgui.Dialog().ok('[COLOR red]KODI CLEANER ERROR[/COLOR]',str(exc))
        sys.exit(0)

def extract_zip(bytes,extract_path,zip_pwd=None,save_list_array=[]):

    try:
        
        
        dp = xbmcgui.DialogProgress()
        dp.create('[COLOR blue]EXTRACT ZIP[/COLOR]','Unpacking data !\nPlease wait ...')
        dp.update(0)
	
        zip = zipfile.ZipFile(bytes,mode='r',compression=zipfile.ZIP_STORED,allowZip64=True)

        count = int(0)
        list_len = len(zip.infolist())
        for item in zip.infolist():

            count += 1
            try:
                percent = int(min(count * 100 / list_len ,100))
                dp.update(percent,'Unpacking data:\n' + item.filename)
            except:pass

            if not any((x in item.filename for x in save_list_array)):
                try:zip.extract(item,path=extract_path,pwd=zip_pwd)
                except:pass

            if dp.iscanceled():
                zip.close()
                dp.close()
                sys.exit(0)

        zip.close()
        dp.close()

    except Exception as exc:
        xbmcgui.Dialog().ok('[COLOR red]EXTRACT ZIP ERROR[/COLOR]',str(exc))
        sys.exit(0)

def close_kodi(special_path_home):

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

		xbmcgui.Dialog().ok('[COLOR red]DANGER ![/COLOR]','[COLOR red]Android system discovered ![/COLOR]\n[COLOR red]Force the termination of the program ![/COLOR]\n[COLOR red]Do not exit the program via Exit or Quit !\nPress OK ![/COLOR]')
		if 'kodi'in special_path_home.lower():xbmc.executebuiltin('StartAndroidActivity("","android.settings.APPLICATION_DETAILS_SETTINGS","","package:org.xbmc.kodi")')
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

def get_params():

	param=[]
	paramstring=sys.argv[2]

	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')

		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]

		pairsofparams=cleanedparams.split('&')
		param={}

		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')

			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
				
		return param
		
params=get_params()

title=None
url=None
img=None
mode=None

try:title=__unquote_plus__(params['title'])
except:pass
try:url=__unquote_plus__(params['url'])
except:pass
try:img=__unquote_plus__(params['img'])
except:pass
try:mode=int(__unquote_plus__(params['mode']))
except:pass


if mode == None:
	add_dir('[COLOR blue]INSTALL BACKUP FROM SERVER[/COLOR]','',__addon_icon__,0)
	add_dir('[COLOR blue]INSTALL BACKUP FROM ZIP FILE[/COLOR]','',__addon_icon__,2)

elif mode == 0:

	with codecs.open(os.path.join(__addon_path__,'data.txt')) as fi:
		for url in fi:
			if url:
				url = url.strip()
				try:
					req = requests.get(url,stream=False,timeout=request_timeout,headers=request_headers)
					if req.status_code == 200:

						content = req.text
						for file_name in re.compile('href="(.*?).zip"').findall(content):
							file_name = file_name.strip()
							img = re.compile(file_name + '(.jpg|.png|.gif)').search(content)
							if img:img = img.group(0)
							else:img = ''

							file = file_name + '.zip'
							add_dir(file,url+file,url+img,1)
				except:pass

elif mode == 1:

	bytes = load_zip_content(url,request_timeout,request_headers)
	xbmc.sleep(500)
	clean_kodi(special_path_home,save_list_array=cleaner_save_list)
	xbmc.sleep(500)
	extract_zip(bytes,special_path_home,save_list_array=extract_save_list)
	xbmc.sleep(500)
	close_kodi(special_path_home)

elif mode == 2:

	zip_path = 	xbmcgui.Dialog().browse(1,'[COLOR blue]KODI BACKUP ZIP ?[/COLOR]','files','.zip|.ZIP', False,False)
	if zip_path:

		clean_kodi(special_path_home,save_list_array=cleaner_save_list)
		xbmc.sleep(500)
		extract_zip(zip_path,special_path_home,save_list_array=extract_save_list)
		xbmc.sleep(500)
		close_kodi(special_path_home)

	else:sys.exit(0)

xbmcplugin.endOfDirectory(handle=int(sys.argv[1]),succeeded=True,updateListing=False,cacheToDisc=False)