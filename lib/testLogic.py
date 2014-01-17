#!/usr/bin/python
# -*- coding:utf-8 -*-
# Author：zeyang@staff.sina.com.cn

import time
import resolveXML
import multiThread
import dealString

ALL_API_NUM = 0
ALL_CASE_NUM = 0

# data prepare, get the test infomation
def before_test():
	""" 获取测试计划 """
	global ALL_API_NUM
	global ALL_CASE_NUM
	
	try:
		plan_filename = sys.argv[1]
	except IndexError, e:
		print "No test plan. stop running ..."
		exit()

	xml = resolveXML.xmlObject()
	plan = xml.get_xml_data(plan_filename)
	print "待测接口列表: " + str(plan['api'])
	
	ALL_API_NUM = len(plan['api'])

	for n in range(len(plan['api'])):
		# get testing api infomatino
		api_filename = plan['api'][n] + ".api.xml"
		api = xml.get_xml_data(api_filename)

		# get testing case infomation
		case_filename = plan['api'][n] + ".case.xml"
		cases = xml.get_xml_data(case_filename)
		running_case = select_run_case(cases)

		ALL_CASE_NUM += len(running_case)

		# muilt thread
		testQ = multiThread.TestQ(plan['api'][n], running_case)
		testQ.start()
		time.sleep(2)
		testQ.stop

		print str(plan['api'][n]) + "执行完成。"
		

# simple run one case
# param  : string(apiname), string(caseid)
# return : re_str(res)
def one_case_run(apiname, caseid):
	xml = xmlObject()

	apifile = apiname + ".api.xml"
	casefile = apiname + ".case.xml"

	api = xml.get_xml_data(apifile, 'api')
	allcase = xml.get_xml_data(casefile, 'case')

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
	return dealString.re_str(res)


# pick up all the running case. 
def select_run_case(case):
	''' pick up the running case while run = 1 '''
	run_case = []
	for n in range(len(case)):
		if case[n]['run'] == '1':
			run_case.append(case[n])
		else:
			continue
	return run_case


# print test infomation
def print_info():
	global start_time
	global end_time
	import time
	start_time = time.ctime()
