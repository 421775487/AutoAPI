# -*- coding:utf-8 -*-
# Author:heulizeyang@gmail.com

import sys
import time
import threading
import my_log
import dealString
import httplib
import testLogic

reload(sys)
sys.setdefaultencoding("utf-8")

class TestQ(threading.Thread):
	def __init__(self, api, cases):
		threading.Thread.__init__(self)
		self.api = api
		self.cases = cases
	
	def run(self):
		for n in range(len(self.cases)):
			print "\t执行" + self.api['apiname'] + "接口测试用例" + self.cases[n]['cid']

			# http connection
			# 后期可能会考虑用urllib2替换httplib
			if self.api['protocol'] == 'http':
				conn = httplib.HTTPConnection(self.api['host'])
			else:
				conn = httplib.HTTPSConnection(self.api['host'])
			apiUrl = self.api['url'] + "?" + self.cases[n]['all_param']
			conn.request(self.api['method'], apiUrl)
			backinfo = conn.getresponse()
			ret_res = backinfo.read()

			# 接口返回的JSON数据中，存在python无法识别数据
			# 如: php boolean  false true
			# 如：返回带引号的URL
			# 需要将false true(php常量)转化成python False True
			try:
				now_res = eval(dealString.re_str(ret_res))
			except Exception, e:
				print "tran the RETURN (JSON format) ERROR ."
				print self.api['apiname'] + "接口测试用例" + str(self.cases[n]['cid']) + "执行失败"
				my_log.logger.error(e)
				exit()

			expect = self.cases[n]['wish']

			# 检查预期结果格式，是否存在接口依赖
			# 例如接口A的用例1的预期结果，是调用接口B的用例3得到
			if str(expect)[:1] == 'a':
				depend_api = eval(expect[3:])
				depend_key = depend_api.keys()
				depend_value = depend_api.values()
				depend_expect = testLogic.one_case_run(depend_key[0], depend_value[0])
			else:
				depend_expect = self.cases[n]['wish']

			#print "\t预期结果: " + str(depend_expect)
			#print "\t实际结果: " + str(now_res)

			# 默认校验全部，暂不考虑局部校验
			# if self.cases[n]['check'] == 'no':
			#  	if now_res == depend_expect:
			#		print " " + self.cases[n]['des'] + " test success."
			#	else:
			#		print " " + self.cases[n]['des'] + " test failed"
			# else:
			#	check_param = format_check(cases[n]['check'])
			#	print " 校验参数:" + str(check_param)
			compare_res = dealString.compare_value(depend_expect, now_res)
			if compare_res:
				print "\t" + self.api['apiname'] + "接口用例" + self.cases[n]['des'] + "测试通过"
			else:
				print "\t" + self.api['apiname'] + "接口用例" + self.cases[n]['des'] + "测试不通过"

	# thread stop
	def stop(self):
		self.thread_stop = True
		#print "\n\t" + self.api['apiname'] + "执行完成。"