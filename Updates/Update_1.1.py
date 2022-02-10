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
 
from turtle import update
import requests
import os
import logging
import threading
import _thread
import time
import datetime
import random

#Refrences:
#https://docs.python-requests.org/en/latest/user/quickstart/#passing-parameters-in-urls

###########################################################################
# Static Variables Section

#Current App Version 
app_version = 1.0
#Min before time to ring alarm
alarmBefore = 1
#Text to Speach TTS
import gtts
from playsound import playsound
#Where to save audio files
audioFolder = 'Audio/'

 

    ###########################################################################
    # Update Section
def checkForUpdate():
    #getting Version and URL update
    url = "https://raw.githubusercontent.com/maxacode/Adept-Vocal-Alarm/main/Update.txt"
    r = requests.get(url, allow_redirects=True)
    r_new = r.text.split('\n')
    app_version_pull = float(r_new[0])
    update_link_pull = r_new[1]
    outdated_by = (app_version_pull)-(app_version)
    
    #Chekcing if new version is higher then updating. 
    if app_version_pull > app_version:
        print(f"Your Version is Outdated by {str(outdated_by)[:4]}")
        #updateQ = input("Update Available, Update Now (Y/N): ")
        updateQ = "n"
        if updateQ.lower() == "y":
            print("Downloading Update!")
            #Renaming old file to _Old Might need a thread since the file is running live. 
            #os.rename("Main.py","Main_Old.py")
            #Code here to say how long it will take.
            #Download complete then install here. 
            #Downloading new version
            r = requests.get(update_link_pull, allow_redirects=True)
            open(f"MainV"+app_version_pull+".py", 'w').write(r.text)
            readFile()
        else:
            #print("Invalid Input")
            readFile()


###########################################################################
# ReadFile Section
def readFile():
    x = 0 
    alarmMsgDict = ['2:30','DoubleWide',240, '- Double wide']
    print(x)
    while x < len(alarmMsgDict):
        try:
            logging.info(f"!!!!ReadFile Func starting alarm for: {alarmMsgDict[x], alarmMsgDict[x+1]}")
            _thread.start_new_thread( alarmTimer, (alarmMsgDict[x], alarmMsgDict[x+1], ) )
            x+= 2
        except Exception as Error:
            print(Error)
            x+=2
            continue
                
 





###########################################################################
# Timer Section

def alarmTimer( alarm, msg):
    try:
        print(alarm,msg)
        currentAlarm = alarm
        alarmSplit = currentAlarm.split(":")
        if int(alarmSplit[0]) >= 0 and int(alarmSplit[0])< 12:
            print(f"{alarmSplit[0]} alarm split")
            alarmSplit[0] = int(alarmSplit[0]) + 12
            print(f"{alarmSplit[0]} alarm split after *12")
        # Converting the alarm time to seconds
        time_sec = int(alarmSplit[0])*3600 + (int(alarmSplit[1])-alarmBefore)*60
        print(f"time_sec: {time_sec}")
        # Getting current time and converting it to seconds
        curr_time = datetime.datetime.now()
        print(f"Current Time: {curr_time}")
        curr_sec = curr_time.hour*3600 + curr_time.minute*60 + curr_time.second
        print(f"CurrentSec: {curr_sec}")
        # Calculating the number of seconds left for alarm
        time_diff = time_sec - curr_sec
        print(f"Time Diff: {time_diff}")
        #If time difference is negative, it means the alarm is for next day.
        if time_diff > -100 and time_diff < 60:
            print("------Time_Diff= 10----")
            randInt = random.randint(1,45)
            time_diff = randInt
        elif time_diff < -110:
            print("------ALARM PASSED----")
            exit()
        elif time_diff > 0:
            pass
        else:
            print("------ALARM PASSED - Else ----")
            exit() 
        # Displaying the time left for alarm
        print("Time left for alarm is %s" % datetime.timedelta(seconds=time_diff))
        # Sleep until the time at which alarm rings
        time.sleep(time_diff)
        playAudio(currentAlarm, msg)
    except Exception as Error:
        print(Error)
        pass
         

###########################################################################
# Alarm Section


def playAudio(alarm,msg):
    #Full name of file Audio+alarm+msg and .mp3    
    msgFull = audioFolder + alarm + " " + msg + ".mp3"
    #API call to get the mp3 file
    engineTTS = gtts.gTTS(alarm+msg)
    #Saving the file
    engineTTS.save(msgFull)
    #Playing the file. 
    playsound(msgFull)

###########################################################################
# Threads Section



if __name__ == "__main__":
    logFormat = "%(asctime)s: %(message)s"
    logging.basicConfig(filename='Log.mdl', encoding='utf-8', level=logging.INFO)
    logging.basicConfig(format=logFormat, level=logging.INFO,datefmt="%H:%M:%S")
    logging.info("Main Program start: ")        


    checkForUpdate()
    while 1:
        pass