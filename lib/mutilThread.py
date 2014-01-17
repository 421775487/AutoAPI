# -*- coding:utf-8 -*-

import time
import threading

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
					dependapi = eval(dependa)
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