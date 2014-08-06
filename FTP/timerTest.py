#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-08-06 14:43:49
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os

from threading import Timer
import time

timer_interval=1
def delayrun():
    print 'running'

t=Timer(timer_interval,delayrun)
t.start()
while True:
    time.sleep(5)
    print 'main running'