# -*- coding:utf-8 -*-
# string lib
# split the value check

import string
import my_log

# return list
def format_check(str):
	value = str.split(',')
	return value

def com_string(list):
	for i in range(len(list)):
		list[i] = list[i] + ","
		res += list[i]
	return res[:-1]

def format_str(str):
	value = str.split('-')
	return value

# compare the expect value with the real value
# oldv : the expect value - string format
# newv : the real value - string format
# value : check point - list
# return TRUE or FALSE
def compare_value(oldv, newv, check=""):
	expect_value = oldv
	real_value = newv
	if check == "":
		for key in expect_value.keys(): 
			if key not in real_value.keys():
				return False
			else:
				# 检查该key对应的value是否为dict类型
				if isinstance(expect_value[key], dict):
					compare_value(expect_value[key], real_value[key])
				else:
					if expect_value[key] == real_value[key]:
						continue
					else:
						return False
		return True	
	# 暂不考虑局部校验逻辑
	else:
		pass

# deal false & true & NONE in json
# tran "false true " into "False True"
# return: string 
def re_str(str):
	''' resolve string '''
	try:
		str = list(str)
		for n in range(len(str)):
			if str[n] == 'f':
				if str[n-1] == ':' and str[n+1] == 'a':
					str[n] = 'F'
				else:
					continue
			elif str[n] == 't':
				if str[n-1] == ':' and str[n+1] == 'r':
					str[n] = 'T'
				else:
					continue
			elif str[n] == 'n':
				if str[n-1] == ':' and str[n+1] == 'u' and str[n+2] == 'l' and str[n+3] == 'l':
					str[n] = 'N'
					str[n+1] = 'o'
					str[n+2] = 'n'
					str[n+3] = 'e'
			elif str[n] == '"':
				if str[n-1] not in [',',':','{','}','"','\\'] and str[n+1] not in [',',':','{','}','"']: 
					str.append('')
					for x in range(len(str),n,-1):
						str[x-1] = str[x-2]
					str[n] = "\\"
				else:
					continue
			else:
				continue
		str = "".join(str)
		return str
	except:
		print "deal the string error."
		my_log.logger.error('tran json into dict occur error.')
		exit()

# compare all keys
def list_all_dict(dict_a):
	if isinstance(dict_a,dict): #使用isinstance检测数据类型 
		for x in range(len(dict_a)):
			temp_key = dict_a.keys()[x]
			temp_value = dict_a[temp_key]
			print"%s : %s" %(temp_key,temp_value)
			list_all_dict(temp_value) #自我调用实现无限遍历

