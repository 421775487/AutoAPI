#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys,os
import httplib
from xml.dom import minidom

sys.path.append("/usr/home/zeyang/autoapi/config")
from sysconfig import *
from my_log import *
import deal_string

# xml object
class xmlObject():
	os.chdir("/usr/home/zeyang/autoapi/data/case/status/")

	def __init__(self):
		return

	def get_attrvalue(self,node,attrname):
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

	def get_xml_data(self, filename):
		try:
			doc = minidom.parse(filename)
			root = doc.documentElement
			# resolve the XXX.api.xml file
			if 'api.xml' in filename:
				api_list = {}

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

				api_list['host'], api_list['url'], api_list['apiname'], api_list['protocol'] \
				, api_list['des'], api_list['islogin'], api_list['ip'], api_list['method'],  \
				api_list['group'] = api_host_v, api_url_v, api_apiname_v, api_protocol_v,    \
				api_des_v,api_islogin_v,api_ip_v,api_method_v,api_group_v
				return api_list

			elif 'case.xml' in filename:
				os.chdir("/usr/home/zeyang/autoapi/data/case/status")
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
					# expect value must be format before U use.
					if case_wish_v[:1] == '{':
						b = deal_string.re_str(case_wish_v)
						a = eval(b)
					else:
						a = case_wish_v
					case_check_v = self.get_attrvalue(case_wish[0], 'check')
					# get the param list
					p_nodes = self.get_xmlnode(c, 'p')
					# get need run case
					p_list = {}
					for p in p_nodes:
						p_key = self.get_nodevalue(p)
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
				plan_person = self.get_xmlnode(root, 'person')
				plan_times = self.get_xmlnode(root, 'times')

				plan_person_v = self.get_nodevalue(plan_person[0])
				plan_times_v = self.get_nodevalue(plan_times[0])

				plan_list = {}
				plan_api = self.get_xmlnode(root,'api')
				plan_api_list = {}
				for plan in plan_api:
					api = self.get_nodevalue(plan)
					group = self.get_attrvalue(api, 'group')
					plan_api_list[gourp] = api
				plan_list['person'], plan_list['times'], plan_list['api'] = plan_person_v, plan_times_v, plan_api_list
				return plan_list
		except Exception, e:
			logger.error(e)

	'''
	# format the params
	# old: a=1 b=2 c=3
	# new: a=1&b=2&c=3
	'''
	def format_param(self, params):
		try:
			pstr = ''
			for key in params.keys():
				pstr = pstr + str(key) + "=" + params[key] + "&"
			return pstr[:-1]
		except:
			print 'format the case params error.'
			logger.error('when deal the case.xml, format params occur error.')
