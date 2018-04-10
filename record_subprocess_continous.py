# coding=utf-8
import os
import sys
from subprocess import *
import errno
import thread
import threading
from threading import Timer
import threadpool

THREAD_POOL_NUM = 10
pool = threadpool.ThreadPool(THREAD_POOL_NUM)
pro_map={}
pro_lock = threading.Lock()

def record_output_func(pid):
	(process,msg) = pro_map[pid]
	stdout = process.stdout
	while True:
		out = stdout.readline()
		if out == '' and process.poll() != None:
			print 'sub process seems quit,so stop record message'
			break
		while not pro_lock.acquire():
			pass
		(_,msg) = pro_map[pid]
		#if msg == None:
		#	pro_lock.release()
		#	break

		msg = msg+out
		pro_map[pid] = (process,msg)
		pro_lock.release()

# return None if pid not exists or process has terminated
def get_message_2(pid):
	if not pid or pid not in pro_map:
		return None
	while not pro_lock.acquire():
		pass
	(process,message) = pro_map[pid]
	pro_map[pid] = (process,"")
	pro_lock.release()

	# TODO: seems has bug	
	# only del once find message is empty and subprocess is down
	if pid_terminated(pid) and (message == '' or len(message) == 0 ) :
		del pro_map[pid]
	return message 

# fail to append worker,return -1
def start_proess(args):
	if not args or len(args) == 0:
		return -1
	if pool._requests_queue.full():
		return -1
 
	process = Popen(args, stdout=PIPE, stderr=STDOUT)
	pro_map[process.pid] = (process,"")
	#requests = threadpool.makeRequests(download_func,arg_list)

	requests = threadpool.makeRequests(record_output_func,[process.pid])
	[pool.putRequest(req) for req in requests]
	return process.pid


def pid_terminated(pid):
	try:
		os.getpgid(pid)
		return False
	except:
		return True

# Deprecated
# return None if pid not exists or process has terminated
def get_message(pid,timeout=10):
	if not pid or pid not in pro_map:
		return None
	import functools
	message = run_with_timeout(timeout,"",functools.partial(read_out_func,pro_map[pid].stdout))
	#if pro_map[pid].poll != None:
	if pid_terminated(pid):
		try:
			print "process with pid:%s terminated,remove from map"%pid
			del pro_map[pid]
		except:
			pass
	return message 

# Deprecated
# ref: https://stackoverflow.com/questions/10756383/timeout-on-subprocess-readline-in-python
# this easy func has 1 big problem is that timeout is not accurate...
# so can't be used in those cases where timeout must be very accurate
def run_with_timeout(timeout, default, f, *args, **kwargs):
    if not timeout:
        return f(*args, **kwargs)
    try:
        timeout_timer = Timer(timeout, thread.interrupt_main)
        timeout_timer.start()
        result = f(*args, **kwargs)
        return result
    except KeyboardInterrupt:
        return default
    finally:
        timeout_timer.cancel()

# Deprecated
def read_out_func(pipe):
	msg = ""
	try:
		while True:
			line = pipe.readline()
			msg = msg+line
	finally:
		return msg


