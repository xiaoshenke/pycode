# coding=utf-8
import time
import sys
def output():
	i = 1
	while True:
		#print "this is %s time output"%i
		msg = "this is %s time output"%i
	
		# FIXME:have to use sys.stdout...
		sys.stdout.write(msg)	
		sys.stdout.write('\n')
		sys.stdout.flush()
	
		time.sleep(3)
		i=i+1
		if i>= 3:
			break
	

if __name__=="__main__":
	output()

