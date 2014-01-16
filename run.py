#!/usr/bin/python
# -*- coding:utf-8 -*-
# au:zyeang@staff.sina.com.cn
# data:2013.12                
# version:1.0                 
# import moudle & config.

import sys
import os
import httplib
import threading
import time

sys.path.append(os.getcwd())
from config.sysconfig import *
from lib.my_log import *
from lib.resolve_xml import *
from lib.deal_string import *

class TestQ(threading.Thread):
	def __init__(self, api, cases):
		threading.Thread.__init__(self)
		self.api = api
		print self.api
		self.cases = cases
	
	def run(self):
		if self.api['protocol'] == 'http':
			for n in range(len(self.cases)):
				print "执行测试用例:" + str(self.cases[n]['cid'])
				conn = httplib.HTTPSConnection(self.api['host'])
				apiUrl = self.api['url'] + "?" + self.cases[n]['all_param']
				conn.request(api['method'], apiUrl)
				backinfo = conn.getresponse()
				ret_res = backinfo.read()
				now_res = eval(re_str(ret_res))
				# deal wish result.
				expect = self.cases[n]['wish']
				if str(expect)[:1] == 'a':
					dependa = expect[3:]
					dependapi =eval(dependa)
					depend_key = dependapi.keys()
					depend_value = dependapi.values()
					depend_expect = one_case_run(depend_key[0], depend_value[0])
				else:
					depend_expect = cases[n]['wish']

				print "	预期结果: " + str(depend_expect)
				print " 实际结果: " + str(now_res)
				if self.cases[n]['check'] == 'no':
					print " 校验全部字段值."
					if now_res == depend_expect:
						print " " + self.cases[n]['des'] + " test success."
					else:
						print " " + self.cases[n]['des'] + " test failed"
				else:
					check_param = format_check(cases[n]['check'])
					print " 校验参数:" + str(check_param)
					compare_res = compare_value(check_param, depend_expect, re_str(now_res))
					if 'False' in compare_res:
						print ' ' + self.cases[n]['des'] + 'test failed'
					else:
						print " " + self.cases[n]['des'] + 'test success'
		else:
			pass

	def stop(self):
		self.thread_stop = True

# change dir
def change_dir(PATH):
	os.chdir(PATH)

# simple run one case
# param  : string(apiname), string(caseid)
# return : re_str(res)
def one_case_run(apiname, caseid):
	os.chdir("/usr/home/zeyang/autoapi/data/api/status/")
	oooxml = xmlObject()
	apifile = apiname + ".api.xml"
	hhhxml = xmlObject()
	casefile = apiname + ".case.xml"
	api = oooxml.get_xml_data(apifile) 
	os.chdir("/usr/home/zeyang/autoapi/data/case/status/")
	allcase = hhhxml.get_xml_data(casefile)
	case = {}
	for i in range(len(allcase)):
		for key in allcase[i]:
			if caseid == allcase[i]['cid']:
				case = allcase[i]
			else:
				continue
	if api['protocol'] == 'http':
		conn = httplib.HTTPConnection(api['host'])
	else:
		conn = httplib.HTTPSConnection(api['host'])
	apiUrl = api['url'] + "?" + case['all_param']
	conn.request(api['method'], apiUrl)
	backinfo = conn.getresponse()
	res = backinfo.read()
	return re_str(res)

# http or https request
def run_test(api, cases):
	if api['protocol'] == 'http':
		for n in range(len(cases)):
			print "执行测试用例:" + str(cases[n]['cid'])
			conn = httplib.HTTPSConnection(api['host'])
			apiUrl = api['url'] + "?" + cases[n]['all_param']
			conn.request(api['method'], apiUrl)
			backinfo = conn.getresponse()
			ret_res = backinfo.read()
			now_res = eval(re_str(ret_res))
			# deal wish result.
			expect = cases[n]['wish']
			if str(expect)[:1] == 'a':
				dependa = expect[3:]
				dependapi =eval(dependa)
				depend_key = dependapi.keys()
				depend_value = dependapi.values()
				depend_expect = one_case_run(depend_key[0], depend_value[0])
			else:
				depend_expect = cases[n]['wish']

			print "	预期结果: " + str(depend_expect)
			print "	实际结果: " + str(now_res)
			if cases[n]['check'] == 'no':
				print "	校验全部字段值."
				if now_res == depend_expect:
					print "	" + cases[n]['des'] + " test success."
				else:
					print "	" + cases[n]['des'] + " test failed"
			else:
				check_param = format_check(cases[n]['check'])
				print "	校验参数:" + str(check_param)
				compare_res = compare_value(check_param, depend_expect, re_str(now_res))
				if 'False' in compare_res:
					print '	' + cases[n]['des'] + 'test failed'
				else:
					print "	" + cases[n]['des'] + 'test success'
	else:
		pass

# get xml file
# print test information
def prepare_test():
	""" 获取测试计划 """
	print "-" * 30 + "Test Start" + "-" * 30
	change_dir(PLANPATH)
	try:
		plan_filename = sys.argv[1]
	except IndexError,e:
		print "there is no test plan. stop running..."
		logger.error(e)
		exit()
	print "待执行测试计划:" + plan_filename
	xml = xmlObject()
	plan = xml.get_xml_data(plan_filename)
	print "待测接口列表:" + str(plan['api'])
	
	for n in range(len(plan['api'])):
		os.chdir("/usr/home/zeyang/autoapi/data/api/status/")

		# 获取api的配置信息
		api_xml = xmlObject()
		api_filename = plan['api'][n] + ".api.xml"
		api = api_xml.get_xml_data(api_filename)

		# 获取case的配置信息
		os.chdir("/usr/home/zeyang/autoapi/data/case/status/")
		case_xml = xmlObject()
		case_filename = plan['api'][n] + ".case.xml"
		cases = case_xml.get_xml_data(case_filename)
		to_run_case = pick_run_case(cases)
		print str(n+1) + ". " + plan['api'][n] + " ----- case num:" + str(len(to_run_case))
	
		testQ = TestQ(plan['api'][n], to_run_case)
		testQ.start()
		time.sleep(10)
		testQ.stop
		print str(plan['api'][n]) + "执行完成。"

# pick up all the running case.
def pick_run_case(case):
	''' pick up the running case while run = 1 '''
	run_case = []
	for n in range(len(case)):
		if case[n]['run'] == '1':
			run_case.append(case[n])
		else:
			continue
	return run_case
        
if __name__ == "__main__":
	prepare_test()
	print "-" * 30 + "Test End " + "-" * 30
