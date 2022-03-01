## Adept-Vocal-Alarm
#Smart alarm that will go off X amount of time before and voice the Message
#!/usr/bin/python

"""
Initial Release:
    Update mechanism 
    Read file 
    List confirmations
    Run once and can’t change unless run again (Refresh from File)


Later Release:
    Dynamic updates in program.
    Multiple voices

"""
 
#from distutils.log import error
import platform
from turtle import update
import requests
import os
import logging
import threading
import _thread
import time
import datetime
import random
import sys
#To delete folder 
import shutil


#Refrences:
#https://docs.python-requests.org/en/latest/user/quickstart/#passing-parameters-in-urls

###########################################################################
# Static Variables Section

#Current App Version 
app_version = 1.3
#Min before time to ring alarm
alarmBefore = 1
#Text to Speach TTS
import gtts
from playsound import playsound
#Where to save audio files
audioFolder = 'Audio/'
updaterLink = "https://raw.githubusercontent.com/maxacode/Adept-Vocal-Alarm/main/Updater.py"
updateFile = "Updater.py"

 

    ###########################################################################
    # Update Section
def checkForUpdate():
    #getting Version and URL update
    url = "https://raw.githubusercontent.com/maxacode/Adept-Vocal-Alarm/main/Update.txt"
    r = requests.get(url, allow_redirects=True)
    r_new = r.text.split('\n')

    if "404: Not Found" in r_new:
        print("Error in Update, try again/contact developer!")
    else:
        app_version_pull = float(r_new[0])
        update_link_pull = r_new[1]
        outdated_by = (float(app_version_pull))-(float(app_version))
    
        #Chekcing if new version is higher then updating. 
        if app_version_pull > app_version:
            if "Force_Update" in update_link_pull:
                basicLog("checkForUpdate",f"Downloading Updater.py")    
                try:
                    #Downloading UpdaterFile
                    r = requests.get(updaterLink, allow_redirects=True)
                    #Writing new update to Updater.py file
                    with open(f"Updater.py", 'w') as writeFile:
                        writeFile.write(r.text)
                        basicLog("checkForUpdate",f"Update Complete")  
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    logger("checkForUpdate", e, fname, exc_tb.tb_lineno) 

                basicLog("checkForUpdate",f"Forcing Update")    
                #Starting Updare file
                exec(compile(open(updateFile).read(),updateFile,  'exec'))
                exit()

            print(f"Your Version is Outdated by {str(outdated_by)[:4]}")
            updateQ = input("Update Available, Update Now (Y/N): ")
            basicLog("checkForUpdate",f"Update: {updateQ}")
            if updateQ.lower() == "y":
                print("\nUpdating now! Please wait a few milliseconds. Program will Continue after Update \n")
                exec(compile(open(updateFile).read(),updateFile,  'exec'))
                exit()
       
    readFile()


###########################################################################
# ReadFile Section
def readFile():
    basicLog("readFile","Starting Function - reading File")
   # print(f"Time Now: {datetime.datetime.now()}")
    x = 0
    alarmMsgDict = ['20:21','I Love You Kelsey!']
    while x < len(alarmMsgDict):
        try:
            basicLog("readFile",f"Starting Alarm: {alarmMsgDict[x], alarmMsgDict[x+1]}")
            print(f"Starting alarm for: {alarmMsgDict[x], alarmMsgDict[x+1]}")
            _thread.start_new_thread( alarmTimer, (alarmMsgDict[x], alarmMsgDict[x+1], ) )
            x+= 2
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger("readFile", e, fname, exc_tb.tb_lineno)           
            x+=2
            continue

###########################################################################
# Timer Section!!!!!!!!

def alarmTimer( alarm, msg):
    basicLog("alarmTimer","Starting AlarmTimer Function")
    try:
       # print(alarm,msg)
        currentAlarm = alarm
        alarmSplit = currentAlarm.split(":")
        if int(alarmSplit[0]) < 8:
            #print(f"{alarmSplit[0]} alarm split")
            alarmSplit[0] = int(alarmSplit[0]) + 12
          #  print(f"{alarmSplit[0]} alarm split after *12")
        # Converting the alarm time to seconds
        time_sec = int(alarmSplit[0])*3600 + (int(alarmSplit[1])-alarmBefore)*60
      #  print(f"time_sec: {time_sec}")
        # Getting current time and converting it to seconds
        curr_time = datetime.datetime.now()
      #  print(f"Current Time: {curr_time}")
        curr_sec = curr_time.hour*3600 + curr_time.minute*60 + curr_time.second
      #  print(f"CurrentSec: {curr_sec}")
        # Calculating the number of seconds left for alarm
        time_diff = time_sec - curr_sec
        time_diff_show = (f"Time Now: {curr_sec} \n Alarm in: Seconds: {time_diff} | Minutes: {round(time_diff/60)} | Hours: {round(time_diff/60/60)} for alarm: {currentAlarm}")
      #  print(time_diff_show)
        basicLog("alarmTimer",time_diff_show)
        #If time difference is negative, it means the alarm is for next day.
        if time_diff > -100 and time_diff < 60:
            randInt = random.randint(1,45)
            time_diff = randInt
        elif time_diff < -110:
            print("------ALARM PASSED----")
            basicLog("alarmTimer","------ALARM PASSED----")
            exit()
        elif time_diff > 0:
            pass
        else:
            basicLog("alarmTimer","------ALARM PASSED - Else----")
            exit() 

        # Displaying the time left for alarm
        print("\nTime left for alarm is %s" % datetime.timedelta(seconds=time_diff))
        basicLog("alarmTimer", f"Time left for alarm is {datetime.timedelta(seconds=time_diff)}")

        # Sleep until the time at which alarm rings
        time.sleep(time_diff)
        playAudio(currentAlarm, msg)   
    except Exception as e:
         exc_type, exc_obj, exc_tb = sys.exc_info()
         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
         logger("alarmTimer", e , fname, exc_tb.tb_lineno)
        
###########################################################################
# Alarm Section


def playAudio(alarm,msg):
    basicLog("playAudio","Starting playAudio Function")
    try:
        #Full name of file Audio+alarm+msg and .mp3    
        msgFull = audioFolder + alarm + " " + msg + ".mp3"
        basicLog("playAudio", f"Downloading Audio: {msgFull}")
        #API call to get the mp3 file
        engineTTS = gtts.gTTS(alarm+msg, lang='ru')
        #Saving the file
        engineTTS.save(msgFull)
        #Playing the file. 
        playsound(msgFull)
        basicLog("playAudio", f"Downloaded and Played Audio: {msgFull} ")

    except Exception as e:
         exc_type, exc_obj, exc_tb = sys.exc_info()
         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
         logger("playAudio", e, fname, exc_tb.tb_lineno)
         pass
        
###########################################################################
# Logging Function Section
def logger(functionName, exc_type, fname, lineNumber):
    logging.error(f"Function: {functionName} | exc_type: {exc_type} | Line Number: {lineNumber} | FileName: {fname}")

def basicLog(functionName,logMsg):
    logging.info(f"Function: {functionName} | Message: {logMsg}")

###########################################################################
# Main Section
if __name__ == "__main__":
    #Logging setup.
    print("\n\n%%%%%%%%%%%%%%%%%% Starting Adept Vocal Alarm Now!! %%%%%%%%%%%%%%%%%%\n")
    format= "%(asctime)s | %(levelname)s |  %(message)s"
    logging.basicConfig(format = format, filename='logging.log', encoding='utf-8', level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info("\dn\n                 %%%%%%%%%%%%%%%%%% Main Program start %%%%%%%%%%%%%%%%%%\n")
    basicLog("Main",f"Current Version: {app_version}")
    #System info Log
    basicLog("Main",f"OS: {platform.platform()} | Version: {platform.version()}")

    #Creating Audio folder and/or removing contents
    try:
        basicLog("Main", "Creating Audio File . ")
        os.mkdir(audioFolder)
    except:
        basicLog("Main", "Deleting Contents of Audio File and creating a new one. ")
        shutil.rmtree(audioFolder)
        os.mkdir(audioFolder)

    checkForUpdate()
    #Waiting so threads can run and not stop. 
    while 1:
        pass
