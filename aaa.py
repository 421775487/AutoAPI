#!/usr/bin/python

import threading
import time

class MyThread(threading.Thread):
	def run(self):
		print 'diaoyong run()'
		print 'running : ' + self.name
		for i in range(5):
			print self.isAlive()
			time.sleep(2)	
			print self.name + ' run time: ' + str(time.ctime())

def test():
	for i in range(5):
		t = MyThread()
		print '\n' + t.name
		print 'start time: ' + str(time.ctime())
		t.start()
		time.sleep(100)

if __name__ == '__main__':
	test()
