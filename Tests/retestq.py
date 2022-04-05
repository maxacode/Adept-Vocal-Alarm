import datetime

nowTime = str(datetime.datetime.now())
hour = nowTime[10:13]
min = str(int(nowTime[14:16]) + 5)
alarm = hour + ":" + min
print(alarm)