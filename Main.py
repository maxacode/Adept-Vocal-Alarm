## Adept-Vocal-Alarm
#Smart alarm that will go off X amount of time before and voice the Message
#!/usr/bin/python

try:
    
    #from distutils.log import error
    import platform
    #To downline files vai HTTP
    import requests
    import os
    #Logg all to file
    import logging
    #Running each alarm in a seperat thread
    import _thread
    #Dates 
    import time
    import datetime
    #Random number generator for file names
    import random
    from random import randrange
    #Execute sys level logging
    import sys
    #To delete folder 
    import shutil

    #Config Parser and CSV Reader
    from configparser import ConfigParser
    import csv

    #Toget all files and find the correct CSV
    from os import walk
    from genericpath import exists

    #Text to Speach TTS
    import gtts
    from playsound import playsound

    #Socket To get sys info
    import socket, urllib
 
###########################################################################
# Sentry plug for monitoirng
    from sentry_sdk import capture_exception
    from sentry_sdk import capture_message
    from sentry_sdk import set_level
    from sentry_sdk.scope import Scope
    from sentry_sdk import configure_scope, push_scope
    from sentry_sdk.api import capture_exception

    import sentry_sdk
    set_level("warning")

    sentry_sdk.init(
    "https://6a1650e68ecc49c28f29608441772004@o1176942.ingest.sentry.io/6275427",
    traces_sample_rate=1.0
    )
 

    #Refrences:
    #https://docs.python-requests.org/en/latest/user/quickstart/#passing-parameters-in-urls

###########################################################################
# Static Variables Section
   
     #Current App Version 
    app_version = 1.7

    #Min before time to ring alarm
    alarmBefore = 1
    global specificAlarm
    specificAlarm = 0
 
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
        #Gettinf file name in directory:
        dateTime = str(datetime.datetime.now())
        dateToday = dateTime[5:11]
        for (dirpath, dirnames, filenames) in walk("."):
            for x in filenames:
              #  print(x)
                if dateToday[1:2] in x and dateToday[3:5] in x:
                    fileName = x
                    print(f"Found the Alarms File: {x}\n")
                    break
            break

        if exists(fileName):
        #Reading file to extract alarms and text.
           
            #Reading Vars form Config.ini
            config = ConfigParser()
  
            config.read("config.ini")
            firstColumn = 'First_Column_Voice'
            secondColumn = 'Second_Column_Voice'
            thirdColum = 'Third_Column_Location'
            fullMsg = ''
            file = open(fileName)
            csvreader = csv.reader(file)

            #Looping through each allarm and adding to full msg
            for alarm in csvreader:
                try:
                    
                    if "Time:" in alarm:
                        continue
                    elif alarm[0] == '':
                        break
                   
                #Checking format of Time:
                    alarm0 = alarm[0]
                 #   print(alarm0)
                    if ":" not in alarm0:
                      #  print(203)
                        if len(alarm0) == 3:
                            alarm0Done = alarm0[0] + ":" + alarm0[1:]
                        elif len(alarm0) == 4:
                            alarm0Done = alarm0[:2] + ":" + alarm0[2:]
                    else:
                        alarm0Done = alarm0
                    #print(alarm0Done)
                #Full Message of this Alarm
                    fullMsg = alarm0Done, config.get( firstColumn, alarm[1].lower()),  config.get(secondColumn, alarm[2].lower()), config.get( thirdColum, alarm[3].lower())
                    alarmMsgDict.append(fullMsg)
 
                except Exception as e:
             
                    e = str(e)
                    if firstColumn in e:
                        fullMsg = alarm0Done, config.get(secondColumn, alarm[2].lower()), config.get( thirdColum, alarm[3].lower())
                        alarmMsgDict.append(fullMsg)
                    elif secondColumn in e:
                        fullMsg = alarm0Done, config.get( firstColumn, alarm[1].lower()), config.get( thirdColum, alarm[3].lower())
                        alarmMsgDict.append(fullMsg)

                    elif thirdColum in e:
                        fullMsg = alarm0Done, config.get( firstColumn, alarm[1].lower()),  config.get(secondColumn, alarm[2].lower())
                        alarmMsgDict.append(fullMsg)
                    
                    else:
                        continue
            file.close()
        else:
            print(f"\n !!!!! CAUTION !!!!!!!!!!!!!! \n Can Not Find a file Named: {dateToday} rename your CSV file to this.")
         # !!!!!!! To alwasy go off in 10 seconds from now. 
 
           # curr_time = str(datetime.datetime.now())
          #  curr_time = curr_time[10:16]
          #  alarmMsgDict = [(curr_time, "Double Bottom", "Stop Run", "China")]
                ## !!! Above from this delete 
      
        #Var for keeping track each ALarm line during loop and name to save Audio file as. 
        global specificAlarm
        
        specificAlarm = 0
        #Starting loop to launch each alarm in a thread.
        global numOfAlarms
        numOfAlarms = len(alarmMsgDict)
        #print(alarmMsgDict)
        while specificAlarm < numOfAlarms:
           
            try:
                time.sleep(1)
               # print(alarmMsgDict[specificAlarm])
                basicLog("readFile",f"Starting Alarm: {alarmMsgDict[specificAlarm]}")
                #print(f"\n\n============================ \n \n-----Starting alarm for: {alarmMsgDict[specificAlarm]}")
                #Checking if next alarm is same time:
                # if float(alarmMsgDict[specificAlarm][0][3:]) == float(alarmMsgDict[specificAlarm+1][0][3:]):
                #     print("If 243")
                #     time.sleep(10)
                # elif float(alarmMsgDict[specificAlarm][0][3:]) == float(alarmMsgDict[specificAlarm+1][0][3:]) - 1):
                #     print("Elif 245")
                #     time.sleep(10)
                numAlarm = specificAlarm
                _thread.start_new_thread( alarmTimer, (str(alarmMsgDict[specificAlarm][0]), alarmMsgDict[specificAlarm], numAlarm ) )
                print(f"Alarm: {specificAlarm + 1} / {numOfAlarms} --- {alarmMsgDict[specificAlarm]}")
                specificAlarm+= 1
                numAlarm+=1
                
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                logger("readFile", e, fname, exc_tb.tb_lineno)           
                specificAlarm+=1
                continue

    ###########################################################################
    # Timer Section!!!!!!!!

    def alarmTimer( alarm, msg, numAlarm):
        basicLog("alarmTimer","Starting AlarmTimer Function")
        try:
            global time_diff
            #Adding 12 hours to alaram if its under 12 - time reasonning - need to make better
            currentAlarm = alarm
            alarmSplit = currentAlarm.split(":")

            if int(alarmSplit[0]) < 7:
                alarmSplit[0] = int(alarmSplit[0]) + 12
                        
            # Converting the alarm time to seconds
            #print(f"286 {alarmSplit}")
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
            if time_diff > -100 and time_diff < 60:
                #Put this back:  randInt = random.randint(10,50)
                randInt = random.randint(10, 50)
                #numAlarm+=1
                time_diff = randInt
            elif time_diff < -100:
                print(f"-----ALARM PASSED-----\n")
                basicLog(f"alarmTimer",f"-----ALARM PASSED----- {alarm} {msg}")
                #numAlarm +=1
                
                exit()
           # else:
            #    print(f"-----ALARM PASSED-----\n")
              #  basicLog(f"alarmTimer",f"------ALARM PASSED - Else----{alarm} {msg}")
             #   # before it was: exit() 
                #exit()

            # Displaying the time left for alarm
            print(f"-----Time left for alarm {alarm} is %s\n" % datetime.timedelta(seconds=time_diff))
            basicLog("alarmTimer", f"Time left for alarm is {alarm} | {msg} | {datetime.timedelta(seconds=time_diff)}")
            
            # Sleep until the time at which alarm rings
             
            time.sleep(time_diff)
            playAudio(currentAlarm, msg, numAlarm)
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger("alarmTimer", e , fname, exc_tb.tb_lineno)
            
    ###########################################################################
    # Alarm Section


    def playAudio(alarm,msg,numAlarm):
        
        basicLog("playAudio","Starting playAudio Function")
        try:
            specificAlarm2 = 0
            specificAlarm2 += randrange(2,9999)
            #Full name of file Audio+alarm+msg and .mp3    
            msgFull = audioFolder + slash + str(specificAlarm2) + ".mp3"
            basicLog("playAudio", f"Downloading Audio: {msgFull}")
            #API call to get the mp3 file
            if "London" in msg:
               # print("London Message")
                engineTTS = gtts.gTTS((str(msg)) , lang='en', tld="co.uk")
            elif "China" in msg:
                pass
            else:
                #print("Normal EN Com")
                engineTTS = gtts.gTTS((str(msg)) , lang='en', tld="com")
   
            #Saving the file
            currTime = datetime.datetime.now()
            try:
                engineTTS.save(msgFull)
            except:
                engineTTS = gtts.gTTS((str(msg)) , lang='en', tld="com")
                specificAlarm2 += randrange(2,9999)
                msgFull = audioFolder + slash + str(specificAlarm2) + ".mp3"
                engineTTS.save(msgFull)
            #Playing the file. 
            playsound(msgFull)
            print(f"Downloaded and Played Audio: {msgFull} - ")
            basicLog("playAudio", f"Downloaded and Played Audio: {msgFull}")
            basicLog("PlayAudio", f"Did Alarm: {numAlarm+1}/{numOfAlarms}")
            if (numAlarm+1) == (numOfAlarms):
                basicLog("PlayAudio", f"Did all alarms! {numAlarm+1}/{numOfAlarms}")
                
                if time_diff > 0:
                    time.sleep(time_diff + 10)
                    sentrySend()
                #print("Done with all alarms 358")
        
            quit()

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
    # SENTRY reporting Section
    def sentrySend():
        print("Closing Program Shortly")
        
        ipv4API1 =  'https://icanhazip.com/'
        
        try:
            host_name = socket.gethostname()
            host_ip_private = socket.gethostbyname(host_name)
            host_ip_public = urllib.request.urlopen(ipv4API1).read().decode('utf8')  
        except Exception as e:
            pass
        host_username =  os.getlogin()
        host_platform = platform.platform()

        sysInfo = f"OS: {platform.platform()} | Version: {platform.version()} | Private IP: {host_ip_private} | Public IP: {host_ip_public} | Host_Username {host_username} | App Version: {app_version} "
        basicLog("Main",f"Current Version: {app_version}")
        #System info Log
        basicLog("Main",sysInfo)
        sentry_sdk.set_context("character", {
            "Host Name": host_name,
            "Private IP": host_ip_private,
            "Public IP": host_ip_public,
            "Host Username": host_username,
            "Host Platform": host_platform,
            "App version": app_version,
        })
        logData = open(f"SupportingFiles{slash}logging.log", encoding="utf8")
        data = logData.read()
        host_name = socket.gethostname()
        configure_scope(lambda scope: scope.add_attachment(path=f"SupportingFiles{slash}logging.log"))
        capture_exception(AttributeError(" ## " + host_name + " | " + str(datetime.datetime.now())))
        # capture_message(datetime.datetime.now())
        print("Closing Now")
        time.sleep(3)
        quit()
         
    
    ###########################################################################
    # Main Section
    if __name__ == "__main__":
        #Logging setup.
        print("\n\n%%%%%%%%%%%%%%%%%% Starting Adept Vocal Alarm Now!! %%%%%%%%%%%%%%%%%%\n")
        os.remove(f"SupportingFiles{slash}logging.log")

        format= "%(asctime)s | %(levelname)s |  %(message)s"
        
        logging.basicConfig(format = format, filename='SupportingFiles/logging.log', encoding='utf-8', level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S %p')
        logging.info("\n\n                 %%%%%%%%%%%%%%%%%% Main Program start %%%%%%%%%%%%%%%%%%\n")

        
        
        
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
except KeyboardInterrupt:
    print("Closing Out!")
    quit()
     

except Exception as e:
    print(f"Main Except: \n\n{e}\n")
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    logger("Main Except", e, fname, exc_tb.tb_lineno)
