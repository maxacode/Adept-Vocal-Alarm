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
from genericpath import exists
from itertools import count
from random import randrange
from unicodedata import name


try:
    
    #from distutils.log import error
    import platform
    import requests
    import os
    import logging
    import _thread
    import time
    import datetime
    import random
    import sys
    #To delete folder 
    import shutil
    #Config Parser
    from configparser import ConfigParser
    import csv

    from configparser import ConfigParser
 

    #Refrences:
    #https://docs.python-requests.org/en/latest/user/quickstart/#passing-parameters-in-urls

###########################################################################
# Static Variables Section
   
     #Current App Version 
    app_version = 1.4

    #Min before time to ring alarm
    alarmBefore = 1
    global specificAlarm
    specificAlarm = 0
    #Text to Speach TTS
    import gtts
    from playsound import playsound

    #OS this is running on: 
    global OSystem
    if "macOS" in platform.platform():
        OSystem = "mac"
    else:
        OSystem = "win"
    
    #Where to save audio files
    if OSystem == "mac":
        slash = "/"
    else:
        slash = "\\"

 

###########################################################################
# Read config file Section
    def readConfigINI():
        global config
        config = ConfigParser()
        #Remove after this goes public
       # os.chdir('adept-venv\Adept-Vocal-Alarm')
       # print(os.getcwd())
        config.read("config.ini")
        
        
        #min before time before to ring alarm
        global minBeforeAlarm
        minBeforeAlarm = config.get('DEFAULTS', 'minutes before time to ring alarm')
        
  
 

        checkForUpdate()
###########################################################################
# Update Section

    def checkForUpdate():
        #getting Version and URL update

        updaterLink = config.get('Ignore_Program_Config', 'updater link')
        updateFile = config.get('Ignore_Program_Config', 'update file')
        url = config.get('Ignore_Program_Config', 'update file text')
        
         
        #Downloaind Update Info text file
        r = requests.get(url, allow_redirects=True)
        r_new = r.text.split('\n')

        if "404: Not Found" in r_new:
            print("Error in Update, try again/contact developer!")
            pass
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
        alarmMsgDict = []
        basicLog("readFile","Starting Function - reading File")
        
        if exists("alarms.csv"):
        #Reading file to extract alarms and text.
           
            #Reading Vars form Config.ini
            config = ConfigParser()
  
            config.read("config.ini")
            firstColumn = 'First_Column_Voice'
            secondColumn = 'Second_Column_Voice'
            thirdColum = 'Third_Column_Location'
            fullMsg = ''
            file = open("alarms.csv")
            csvreader = csv.reader(file)
 
            for alarm in csvreader:
                try:
                    
                    if "Time:" in alarm:
                        continue
                    elif alarm[0] == '':
                        break
                   
                #Full Message of this Alarm
                    fullMsg = alarm[0], config.get( firstColumn, alarm[1].lower()),  config.get(secondColumn, alarm[2].lower()), config.get( thirdColum, alarm[3].lower())
                    alarmMsgDict.append(fullMsg)
 
                except Exception as e:
             
                    e = str(e)
                    if firstColumn in e:
                        fullMsg = alarm[0], config.get(secondColumn, alarm[2].lower()), config.get( thirdColum, alarm[3].lower())
                        alarmMsgDict.append(fullMsg)
                    elif secondColumn in e:
                        fullMsg = alarm[0], config.get( firstColumn, alarm[1].lower()), config.get( thirdColum, alarm[3].lower())
                        alarmMsgDict.append(fullMsg)

                    elif thirdColum in e:
                        fullMsg = alarm[0], config.get( firstColumn, alarm[1].lower()),  config.get(secondColumn, alarm[2].lower())
                        alarmMsgDict.append(fullMsg)
                    
                    else:
                        continue
            file.close()
        else:
         # !!!!!!! To alwasy go off in 10 seconds from now. 
 
            curr_time = str(datetime.datetime.now())
            curr_time = curr_time[10:19]
            alarmMsgDict = [curr_time ,"('820', '!!!!Double Bottom', 'Stop Run')"]
                ## !!! Above from this delete 
      
        #Var for keeping track each ALarm line during loop and name to save Audio file as. 
        global specificAlarm
        specificAlarm = 0
        #Starting loop to launch each alarm in a thread.
         
        while specificAlarm < len(alarmMsgDict):
           
            try:
                basicLog("readFile",f"Starting Alarm: {alarmMsgDict[specificAlarm]}")
                print(f"\n\n============================ \n \n-----Starting alarm for: {alarmMsgDict[specificAlarm]}")
                _thread.start_new_thread( alarmTimer, (str(alarmMsgDict[specificAlarm][0]), alarmMsgDict[specificAlarm], ) )
                specificAlarm+= 1
                time.sleep(5)
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                logger("readFile", e, fname, exc_tb.tb_lineno)           
                specificAlarm+=1
                continue

    ###########################################################################
    # Timer Section!!!!!!!!

    def alarmTimer( alarm, msg):
        basicLog("alarmTimer","Starting AlarmTimer Function")
        try:

            #Adding 12 hours to alaram if its under 12 - time reasonning - need to make better
            currentAlarm = alarm
            alarmSplit = currentAlarm.split(":")

            if int(alarmSplit[0]) < 7:
                alarmSplit[0] = int(alarmSplit[0]) + 12
                        
            # Converting the alarm time to seconds
            time_sec = int(alarmSplit[0])*3600 + (int(alarmSplit[1])-alarmBefore)*60
            #Subtracting global minBeforeAlarm
            time_sec -= (int(minBeforeAlarm)*60)
            
             # Getting current time and date it to seconds
            curr_time = datetime.datetime.now()
            curr_sec = curr_time.hour*3600 + curr_time.minute*60 + curr_time.second
            
             # Calculating the number of seconds left for alarm
            time_diff = time_sec - curr_sec
            time_diff_show = (f"Time Now: {curr_sec} - Alarm Time: {time_sec} \n Alarm in: Seconds: {time_diff} \
| Minutes: {round(time_diff/60)} | Hours: {round(time_diff/60/60)} for alarm: {currentAlarm}")
           #
            #print(time_diff_show)
            basicLog("alarmTimer",time_diff_show)
            
            #If time difference is negative, it means the alarm is passed by -x H/M/Seconds.
            #Put this back:             if time_diff > -100 and time_diff < 60:
            if time_diff > -1000 and time_diff < 6000:
                #Put this back:  randInt = random.randint(10,50)
                randInt = random.randint(1,10) + random.randint(1,15)
                time_diff = randInt
            elif time_diff < -11110:
                print(f"-----ALARM PASSED-----")
                basicLog(f"alarmTimer","-----ALARM PASSED----- {alarm} {msg}")
                exit()
            elif time_diff > 0:
                pass
            else:
                print(f"-----ALARM PASSED-----")
                basicLog(f"alarmTimer","------ALARM PASSED - Else----{alarm} {msg}")
                # before it was: exit() 
                pass

            # Displaying the time left for alarm
            print(f"-----Time left for alarm {alarm} is %s" % datetime.timedelta(seconds=time_diff))
            basicLog("alarmTimer", f"Time left for alarm is {alarm} | {msg} | {datetime.timedelta(seconds=time_diff)}")

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
            specificAlarm = 0
            specificAlarm += randrange(2,9999)
            #Full name of file Audio+alarm+msg and .mp3    
            msgFull = audioFolder + slash + str(specificAlarm) + ".mp3"
            basicLog("playAudio", f"Downloading Audio: {msgFull}")
            #API call to get the mp3 file
            #Accents 
            engineTTS = gtts.gTTS((str(msg)) , lang='en', tld="co.uk")

            #London:             engineTTS = gtts.gTTS(alarm+msg, lang='en', tld="co.uk")
            #Saving the file
            currTime = datetime.datetime.now()
            try:
                engineTTS.save(msgFull)
            except:
                specificAlarm += randrange(2,9999)
                msgFull = str(specificAlarm) + ".mp3"
                engineTTS.save(msgFull)
            #Playing the file. 
            playsound(msgFull)
            print(f"Downloaded and Played Audio: {msgFull} ")
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
        logging.basicConfig(format = format, filename='SupportingFiles/logging.log', encoding='utf-8', level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S %p')
        logging.info("\n\n                 %%%%%%%%%%%%%%%%%% Main Program start %%%%%%%%%%%%%%%%%%\n")
        basicLog("Main",f"Current Version: {app_version}")
        #System info Log
        basicLog("Main",f"OS: {platform.platform()} | Version: {platform.version()}")
        
        audioFolder = ("SupportingFiles" + slash + "Audio")
        #Creating Audio folder and/or removing contents
        try:
            basicLog("Main", "Creating Audio File . ")
            os.mkdir(audioFolder)
        except:
            basicLog("Main", "Deleting Contents of Audio File and creating a new one. ")
            shutil.rmtree(audioFolder)
            os.mkdir(audioFolder)

        readConfigINI()
        #Waiting so threads can run and not stop. 
        while 1:
            pass
        
except Exception as e:
    print(f"Main Except: \n\n{e}\n")
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    logger("Main Except", e, fname, exc_tb.tb_lineno)