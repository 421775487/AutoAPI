#!/usr/bin/python

AUTHOR = 0

def hhh():
	global AUTHOR
	for i in range(5):
		AUTHOR += i  
	print AUTHOR

def aaa():
	global AUTHOR
	print AUTHOR
	AUTHOR = 100
	print AUTHOR

if __name__ == "__main__":
	print AUTHOR
	hhh()
	aaa()
	hhh()
