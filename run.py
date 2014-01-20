#!/usr/bin/python
# -*- coding:utf-8 -*-
# Author:heulizeyang@gmail.com

import os
import sys
from lib import testLogic

if __name__ == "__main__":
	sys.path.append(os.getcwd())
	import lib.testLogic
	testLogic.test_running()
	# print "-" * 30 + "Test End " + "-" * 30
	# print "全部执行完成"
