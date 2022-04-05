import requests
import pytest
import time
import warnings

#Main File functions:
from Main import *

updateLink = "https://raw.githubusercontent.com/maxacode/Adept-Vocal-Alarm/main/SupportingFiles/Update.txt"

##UPDATE Functionality:
def test_Updatelinks():
    #Can connect to UpdateLink 
    print("### Update Functionality")

    r = requests.get(updateLink, allow_redirects=True)
    assert "<Response [200]>" in str(r)
    r_new = r.text.split('\n')
    return r_new
#Version Number
def test_VersionCheck():
    r_new = test_Updatelinks()
    assert 2.2== float(r_new[0])
#Update link for Main.exe
def test_UpdateLink():
    r_new = test_Updatelinks()
    assert "https://github.com/maxacode/Adept-Vocal-Alarm/blob/main/Updates/Main.exe?raw=true" == r_new[1]
#Force update Check:
def test_ForceUpdate():
    r_new = test_Updatelinks()
    assert "True" == str(r_new[2])

#Updater.py download
updaterLink = "https://raw.githubusercontent.com/maxacode/Adept-Vocal-Alarm/main/SupportingFiles/Updater.py"
def test_UpdaterPy():
    print("### Updater.py Check")
    r = requests.get(updaterLink, allow_redirects=True)
   # time.sleep(2)
    assert "<Response [200]>" in str(r)
    assert "#updater file for program" in  str(r.text)

## Testing output
def test_configIni(capsys):
    print("### CreateIni Main Function")
    configIni()
    stdout, stderr = capsys.readouterr()
    assert "Creating Default Config File!" in  stdout
    assert "Done Creating Config File" in stdout
#Getting minBeforeAlarm from Config File Function
def test_readConfig():
    print("### Test of Reading Config File")
    assert readConfigINI() == str(5)

#Testing getting file name 
def test_getFileName():
    print("### Testing ability to get file name by date")
    dateTime = str(datetime.datetime.now())
    dateToday = dateTime[5:11]
    assert dateToday[1:2] and dateToday[4:5] in getFileName()[0]

#Testing for changes that need to be made to go to Production
def test_backToProdCode(capsys):
    alarmTimer("10:10", "Test Messge", 0,5)
    stdout, stderr = capsys.readouterr()
 
    if "CHANGE BACK TO exit 384" in stdout:
        warnings.warn(UserWarning("PROD Change Back"))

#testing various alarm time formats
def test_AlarmTimes(capsys):
    nowTime = str(datetime.datetime.now())
    hour = nowTime[10:13]
    min = str(int(nowTime[14:16]) + 5)
    alarm = hour + ":" + min

    alarmTimer(alarm, "Test Messge", 0,5)
    stdout, stderr = capsys.readouterr()
    #print(stdout)
    assert "Alarm Will Go Off in:" in stdout

#test adding colon:
@pytest.mark.parametrize("alarmTime, expectedOutput",
                [
                    ("12:34", "12:34"),
                    ("1234", "12:34"),
                    ('2:34', "2:34"),
                    ("234", "2:34"),
                ])
def test_addColon(alarmTime, expectedOutput):
    print(f"Testing Adding Colon on: {alarmTime} --> {expectedOutput}")
    assert addColon(alarmTime) == expectedOutput

@pytest.mark.parametrize("alarm, msg, numAlarm, totalNumAlarms",
                       [
                            ("5:29","test 1", 1, 10),
                            ("5:29","test 2", 2, 10),
                            ("5:29","test 3", 3, 10),
                            ("5:29","test 4", 10, 10),
                        ])
def test_AlarmTimes(capsys, alarm, msg, numAlarm, totalNumAlarms):
    print(f"alarm: {alarm} | msg: {msg} | numAlarm: {numAlarm} | total: {totalNumAlarms}")
  #  nowTime = str(datetime.datetime.now())
   # hour = nowTime[10:13]
    #min = str(int(nowTime[14:16]) + 5)
    #alarm = hour + ":" + min
    alarmTimer(alarm, msg, numAlarm, totalNumAlarms)
    stdout, stderr = capsys.readouterr()
   # print(stdout)
    assert "Alarm Will Go Off in:" in stdout

    