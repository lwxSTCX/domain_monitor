﻿#coding=utf-8
import os
import time

"""
监听WVS扫描
"""
while not os.path.exists("../result.txt"):
	time.sleep(10)
	print 'listen ......'
print 'starting  wvs scan'