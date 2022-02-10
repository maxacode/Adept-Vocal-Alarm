#!/usr/bin/python3

import _thread
import time

# Define a function for the thread
def print_time( threadName, delay):
   count = 0
   while count < 5:
      time.sleep(delay)
      print(threadName, count)
      count += 1
      print ("%s: %s" % ( threadName, time.ctime(time.time()) ))

# Create two threads as follows
try:
    alarmMsgDict = {'10:29':1,'10:29':4}
    print(alarmMsgDict.keys()
    for alarm, msg in alarmMsgDict.items():
 
        name = "Thread-" + str(msg)
        _thread.start_new_thread( print_time, (alarm, msg, ) )
except:
   print ("Error: unable to start thread")

while 1:
   pass