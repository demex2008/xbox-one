#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys,requests,re
import xbmcgui

def __get_sys_version():
	return sys.version_info.major

__requests_codes_dict__ = {

    100:'continue',
    101:'switching_protocols',
    102:'processing',
    103:'checkpoint',
    122:'uri_too_long',
    200:'ok',
    201:'created',
    202:'accepted',
    203:'non_authoritative_info',
    204:'no_content',
    205:'reset_content',
    206:'partial_content',
    207:'multi_status',
    208:'already_reported',
    226:'im_used',

    300:'multiple_choices',
    301:'moved_permanently',
    302:'found',
    303:'see_other',
    304:'not_modified',
    305:'use_proxy',
    306:'switch_proxy',
    307:'temporary_redirect',
    308:'permanent_redirect',

    400:'bad_request',
    401:'unauthorized',
    402:'payment_required',
    403:'forbidden',
    404:'not_found',
    405:'method_not_allowed',
    406:'not_acceptable',
    407:'proxy_authentication_required',
    408:'request_timeout',
    409:'conflict',
    410:'gone',
    411:'length_required',
    412:'precondition_failed',
    413:'request_entity_too_large',
    414:'request_uri_too_large',
    415:'unsupported_media_type',
    416:'requested_range_not_satisfiable',
    417:'expectation_failed',
    418:'im_a_teapot',
    421:'misdirected_request',
    422:'unprocessable_entity',
    423:'locked',
    424:'failed_dependency',
    425:'unordered_collection',
    426:'upgrade_required',
    428:'precondition_required',
    429:'too_many_requests',
    431:'header_fields_too_large',
    444:'no_response',
    449:'retry_with',
    450:'blocked_by_windows_parental_controls',
    451:'unavailable_for_legal_reasons',
    499:'client_closed_request',

    500:'internal_server_error',
    501:'not_implemented',
    502:'bad_gateway',
    503:'service_unavailable',
    504:'gateway_timeout',
    505:'http_version_not_supported',
    506:'variant_also_negotiates',
    507:'insufficient_storage',
    509:'bandwidth_limit_exceeded',
    510:'not_extended',
    511:'network_authentication_required'}

def repository_checker(addons_path,timeout=15,headers={}):

	repo_list = []
	repo_list = [elem for elem in os.listdir(addons_path) if elem.startswith('repo') or elem.startswith('repository')]
	repo_list_len  = len(repo_list)

	counter = int(0)
	info_str = str('')

	dp = xbmcgui.DialogProgress()
	sys_version = __get_sys_version()
	if sys_version == 2:dp.create('[COLOR blue]REPOSITORY CHECKER[/COLOR]','Check repos !','Please wait ...')
	elif sys_version == 3:dp.create('[COLOR blue]REPOSITORY CHECKER[/COLOR]','Check repos !\nPlease wait ...')
	dp.update(counter)

	for repo in repo_list:

		info_str += '[COLOR blue]{0}[/COLOR]:\n'.format(repo)
		repo_xml_path = os.path.join(addons_path,repo,'addon.xml')
		if os.path.exists(repo_xml_path):

			status_code = ''
			status_info = ''
			with open(repo_xml_path,'rb',buffering=1024*8) as xml:
				for url,type in re.compile('>(.*?)(<\/info>|<\/checksum>|<\/datadir>)').findall(xml.read().decode('utf-8')):

					try:
						req = requests.get(url=url,stream=False,verify=False,timeout=timeout,headers=headers)
						status_info = __requests_codes_dict__[req.status_code]
						req.close()
					except Exception as e:
						status_code = str('Error')
						status_info = str(e)

					info_str +='{0} {1} : {2}\n'.format(type,status_code,status_info)
					if dp.iscanceled():break

			info_str +='\n'

		counter +=1
		percent = int(min(counter * 100 / repo_list_len ,100))
		if sys_version == 2:dp.update(percent,'Check repo :',repo)
		elif sys_version == 3:dp.update(percent,'Check repo :\n' + repo)
		if dp.iscanceled():break

	dp.close()
	
	if info_str:xbmcgui.Dialog().textviewer(heading='REPOSITORY CHECKER',text=info_str)