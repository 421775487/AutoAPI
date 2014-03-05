#!/usr/bin/python
# -*- coding:utf-8 -*-
# Author：heulizeyang@gmail.com

from __future__ import division
import sys
import time
import urllib
import my_log
import resolveXML
import multiThread
import dealString
import httplib

ALL_API_NUM = 0
ALL_CASE_NUM = 0

# data prepare, get the test infomation
def test_running():
	""" 获取测试计划 """
	global ALL_API_NUM
	global ALL_CASE_NUM
	
	autoapi_start = time.time()
	try:
		plan_filename = sys.argv[1]
	except IndexError, e:
		print "No test plan. stop running ..."
		exit()

	xml = resolveXML.xmlObject()
	plan = xml.get_xml_data(plan_filename)
	print "待测接口列表: " + str(plan['api'])
	
	ALL_API_NUM = len(plan['api'])

	testQ = []
	for n in range(len(plan['api'])):
		group = plan['group'][n]
		# get testing api infomatino
		api_filename = plan['api'][n] + ".api.xml"
		api = xml.get_xml_data(api_filename, group)
		# 输出debug信息,可注释
		my_log.logger.info(api_filename + "解析成功...")

		# get testing case infomation
		case_filename = plan['api'][n] + ".case.xml"
		cases = xml.get_xml_data(case_filename, group)
		my_log.logger.info(case_filename + "解析成功...")
		
		running_case = select_run_case(cases)
		

		# 执行用例总数自增
		ALL_CASE_NUM += len(running_case)

		# muilt thread
		# put into thread group
		testQ.append(multiThread.TestQ(api, running_case))

	start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	for i in range(len(testQ)):
		testQ[i].start()
		
	for i in range(len(testQ)):
		testQ[i].stop()
	end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	time.sleep(0.9)

	autoapi_end = time.time()
	exe_time = (autoapi_end - autoapi_start)*1000 - 900

	print "\n" + "="*30
	print "测试开始时间:" + start_time
	print "测试结束时间:" + end_time
	print "用例总数:" + str(ALL_CASE_NUM)
	print "测试通过:" + str(multiThread.RUN_SUCCESS)
	print "测试不通过:" + str(multiThread.RUN_FAILED)

	succ_rate = multiThread.RUN_SUCCESS/ALL_CASE_NUM*100
	fail_rate = multiThread.RUN_FAILED/ALL_CASE_NUM*100

	print "成功率:%.2f%%"  %succ_rate
	print "失败率:%.2f%%"  %fail_rate
	print "程序运行时间: %.2f" %exe_time + "ms"

# simple run one case
# param  : string(apiname), string(caseid)
# return : re_str(res)
def one_case_run(group, apiname, caseid):
	xml = resolveXML.xmlObject()
	apifile = apiname + ".api.xml"
	casefile = apiname + ".case.xml"
	api = xml.get_xml_data(apifile, group)
	allcase = xml.get_xml_data(casefile, group)

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
	params = urllib.urlencode(case['params'])
	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
	apiUrl = api['url']
	conn.request(api['method'], apiUrl, params, headers)
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

# testing report
def test_result():
	return

# 处理参数依赖中参数格式
def get_param(param, res):
	key = param[0]
	if key in res.keys():
		if len(param) == 1:
			return res[key]
		else:
			param.remove(param[0])
			get_param(param, res[key])
	else:
		print "接口执行失败"
		exit()

# 接口依赖前的接口执行和参数处理
# info为，号分割的字符串
def before_case_run(info):
	while info != None:
		beforeInfo = dealString.format_check(info)
		group = beforeInfo[0]
		api = beforeInfo[1]
		caseid = beforeInfo[2]
		if len(info) == 3:
			one_case_run(group, api, caseid)
			return
		# 长度为4，需要考虑参数依赖
		else:
			param = dealString.format_str(beforeInfo[3])
			maxlen = len(param)
			paramString = "needdata_" + param[maxlen-1]
			result = one_case_run(group, api, caseid)
			# print result
			res = {}
			res[paramString] = get_param(param, eval(result))
			# print res
			# {u'needdata_id': 3680080389412734}
			return res

# 在case中查找和替换
def set_file(case, keyparam):
	return