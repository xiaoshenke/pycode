

import importlib
import os
import sys
from remotefile.test3 import *

def main():      #invoke general function
	eval('funcA')('hello')
	return

sys.path.append('/Users/dashu/Desktop/pserver/remotefile')
def main2():    #invoke class member function
	mod = __import__('test3',globals(),locals(),True,-1)
	print(dir(mod))
	classA = getattr(mod,'ClassA')
	obj = classA()
	for attr in dir(obj):
		if attr[0] != '_':
			func = getattr(obj,attr)
			print(dir(func))
			if hasattr(func,'__call__'):
				print(getattr(func,'im_class')) #test3.ClassA
				print(getattr(func,'im_func'))  #<function test at 0x106898ed8>
				print(getattr(func,'im_self'))  #<test3.ClassA instance at 0x10689c3b0>
				pass
				#func()
	return	

if __name__ == '__main__':
	main2()