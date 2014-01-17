#!/usr/bin/python
# -*- coding:utf-8 -*-
# Author：zeyang@staff.sina.com.cn

ALL_API_NUM = 0
ALL_CASE_NUM = 0

import resolveXML
import time

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

		print plan['api'][n] + " 测试用例数:" + str(len(running_case))
	
		testQ = TestQ(plan['api'][n], running_case)
		testQ.start()
		time.sleep(1)
		testQ.stop

		print str(plan['api'][n]) + "执行完成。"

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
