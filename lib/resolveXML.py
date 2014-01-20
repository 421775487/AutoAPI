#!/usr/bin/python
# -*- coding:utf-8 -*-
# Author:heulizeyang@gmail.com

import sys
import os
import dealString

from xml.dom import minidom
from config import sysconfig
import my_log

class xmlObject():
	def __init__(self):
		return

	def get_attrvalue(self, node, attrname):
		if node:
			return node.getAttribute(attrname)
		else: ''

	def get_nodevalue(self, node, index = 0):
		if node:
			return node.childNodes[index].nodeValue
		else: ''
	
	def get_xmlnode(self, node, name):
		if node:
			return node.getElementsByTagName(name)
		else: ''

	def get_xml_data(self, filename, kind = None):
		

		if 'api.xml' in filename:
			# 默认存在API组配置,否则异常
			try:
				p = sysconfig.apiRef[kind]
			except Exception, e:
				print "No group config, please check your sysconfig.py !"
				my_log.logger.error(e)
			os.chdir(p['apipath'])

			try:
				doc = minidom.parse(filename)
				root = doc.documentElement
			except Exception, e:
				print "Resolve XML file ERROR, please check your XML format !"
				my_loglogger.error(e)

			api_host = self.get_xmlnode(root, 'host')
			api_url = self.get_xmlnode(root, 'url')
			api_apiname = self.get_xmlnode(root, 'apiname')
			api_protocol = self.get_xmlnode(root, 'protocol')
			api_des = self.get_xmlnode(root, 'des')
			api_islogin = self.get_xmlnode(root, 'islogin')
			api_method = self.get_xmlnode(root, 'method')
			api_ip = self.get_xmlnode(root, 'ip')
			api_group = self.get_xmlnode(root, 'group')

			api_host_v = self.get_nodevalue(api_host[0])
			api_url_v = self.get_nodevalue(api_url[0])
			api_apiname_v = self.get_nodevalue(api_apiname[0])
			api_protocol_v = self.get_nodevalue(api_protocol[0])
			api_des_v = self.get_nodevalue(api_des[0]).encode('utf-8')
			api_islogin_v = self.get_nodevalue(api_islogin[0])
			api_method_v = self.get_nodevalue(api_method[0])
			api_ip_v = self.get_nodevalue(api_ip[0])
			api_group_v = self.get_nodevalue(api_group[0])

			api_list = {}
			api_list['host'], api_list['url'], api_list['apiname'], api_list['protocol'] \
			, api_list['des'], api_list['islogin'], api_list['ip'], api_list['method'],  \
			api_list['group'] = api_host_v, api_url_v, api_apiname_v, api_protocol_v,    \
			api_des_v,api_islogin_v,api_ip_v,api_method_v,api_group_v
			return api_list

		elif 'case.xml' in filename:
			try:
				p = sysconfig.apiRef[kind]
			except Exception, e:
				print "No group config, please check your sysconfig.py !"
				my_log.logger.error(e)
			os.chdir(p['casepath'])
			try:
				doc = minidom.parse(filename)
				root = doc.documentElement
			except Exception, e:
				print "Resolve XML file ERROR, please check your XML format !"
				my_loglogger.error(e)

			case_nodes = self.get_xmlnode(root,'case')
			case_list = []
			for c in case_nodes:
				list = {}
				case_des = self.get_xmlnode(c, 'des')
				case_wish = self.get_xmlnode(c, 'wish')
				case_run = self.get_xmlnode(c, 'run')
				case_cid = self.get_xmlnode(c, 'cid')
							
				case_des_v = self.get_nodevalue(case_des[0]).encode('utf-8')
				case_wish_v = self.get_nodevalue(case_wish[0])
				case_run_v = self.get_nodevalue(case_run[0])
				case_cid_v = self.get_nodevalue(case_cid[0])
					
				if case_wish_v[:1] == '{':
					b = dealString.re_str(case_wish_v)
					a = eval(b)
				else:
					a = case_wish_v
				case_check_v = self.get_attrvalue(case_wish[0], 'check')
				p_nodes = self.get_xmlnode(c, 'p')
				p_list = {}
				for p in p_nodes:
					p_key = self.get_nodevalue(p)
					if p_key == 'SOURCE':
						p_list['source'] = sysconfig.SOURCE
					elif p_key == "ACCESS_TOKEN":
						P_list['access_token'] = sysconfig.ACCESS_TOKEN
					else:
						p_value = self.get_attrvalue(p, 'value')
						p_list[p_key] = p_value
				if case_check_v == '':
					list['des'],list['wish'],list['params'],list['all_param'],list['check'], list['run'], list['cid']= \
					case_des_v, a, p_list, self.format_param(p_list), 'no', case_run_v, case_cid_v
				else:
					list['des'],list['wish'],list['params'],list['all_param'],list['check'], list['run'], list['cid'] = \
					case_des_v, a, p_list, self.format_param(p_list), case_check_v, case_run_v, case_cid_v
				case_list.append(list)
			return case_list

		else:
			os.chdir(sysconfig._PLANPATH)
			try:
				doc = minidom.parse(filename)
				root = doc.documentElement
			except Exception, e:
				print "Resolve XML file ERROR, please check your XML format !"
				my_loglogger.error(e)

			plan_person = self.get_xmlnode(root, 'person')
			plan_times = self.get_xmlnode(root, 'times')

			plan_person_v = self.get_nodevalue(plan_person[0])
			plan_times_v = self.get_nodevalue(plan_times[0])

			plan = {}
			group_list = []
			plan_api_list = []

			plan_api = self.get_xmlnode(root,'api')
			for p_api in plan_api:
				api = self.get_nodevalue(p_api)
				group = self.get_attrvalue(p_api, 'group')
				group_list.append(group)
				plan_api_list.append(api)

			plan['person'], plan['times'], plan['api'], plan['group'] = \
			plan_person_v, plan_times_v, plan_api_list, group_list
			return plan


	# connect the params with its value 
	# before format : a = 1, b = 2, c = 3 ...
	# after  format : a=1&b=2&c=3...  
	def format_param(self, params):
		''' format all the params '''
		try:
			pstr = ''
			for key in params.keys():
				pstr = pstr + str(key) + "=" + params[key] + "&"
			return pstr[:-1]
		except:
			print 'format the case params error.'
			my_log.logger.error('when deal the case.xml, format params occur error.')
