# coding=utf-8

import backfill_biz


if __name__=="__main__":
	cmd = ["python","/Users/dashu/Desktop/leaf/wrapper_server/app/main/fake_output_string.py"]
	pid = backfill_biz.start_proess(cmd)
	print "pid:%s"%pid
	while True:
		msg = backfill_biz.get_message_2(pid)
		if msg:
			print msg
		if msg == None:
			print "msg is None,so break"
			#pass
			break
		import time
		time.sleep(1)
	backfill_biz.pool.dismissWorkers(backfill_biz.THREAD_POOL_NUM,True)

