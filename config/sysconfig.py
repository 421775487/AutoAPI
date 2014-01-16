# -*-coding:utf-8 -*-
# author:zeyang@staff.sina.com.cn
# time:2013-12-12
# Version:1.0
# config.py:save the testing needed information

import os
_WORKSPACE = os.getcwd()[:-7]

uname = "yangzl296017245"
pwd = 13397276388

# test app information.
source = "4125898983"
access_token = "2.00mG98WBnnqNVEfe7acc1871Kgp6XC"

# api reference information
apiRef = {
'STATUS':\
	{'apis':['queryid','querymid','show'],\
	'name':'微博组接口',\
	'path':_WORKSPACE + '/data/api/status'},
'OPEN':\
	{'apis':[],\
	'name':'平台组接口',\
	'path':_WORKSPACE + '/data/api/open'},
'OAUTH':\
	{'apis':[],\
	'name':'授权组接口',\
	'path':_WORKSPACE + '/data/api/oauth'}
}

# path
PLANPATH = _WORKSPACE + '/plan'
_APIPATH = _WORKSPACE + '/data/api'
_CASEPATH = _WORKSPACE + '/data/case'
