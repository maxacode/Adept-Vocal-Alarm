## Adept-Vocal-Alarm
#Smart alarm that will go off X amount of time before and voice the Message
#!/usr/bin/python



from pip import main

logFile = "logging.log"
try:
    
    #from distutils.log import error
    import platform
    #To downline files vai HTTP
    import requests
    import shutil
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
    
    #grepper import config parser
    #Config Parser and CSV Reader
    from configparser import ConfigParser
    import csv
    #end grepper

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
    traces_sample_rate=1.0,
    release = "Adept-Alarm@2.3",
    )
 
    global sentryRun
    sentryRun = False

    #Refrences:
    #https://docs.python-requests.org/en/latest/user/quickstart/#passing-parameters-in-urls

###########################################################################
# Static Variables Section
   
     #Current App Version 
    app_version = 2.3

    #Min before time to ring alarm
     
    global specificAlarm
    specificAlarm = 0
 
    #OS this is running on: 
    global OSystem
    if "macOS" in platform.platform():
        OSystem = "mac"
    else:
        OSystem = "win"
        from cgitb import handler
        from ctypes import WinError
        from re import fullmatch
    
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
        basicLog("readConfigINI", "Starting to reading of teh COnfig File - Line 98")
        #Remove after this goes public
       # os.chdir('adept-venv\Adept-Vocal-Alarm')
       # print(os.getcwd())
        config.read("config.ini")
               
        #min before time before to ring alarm
        global minBeforeAlarm
        minBeforeAlarm = config.get('DEFAULTS', 'minutes before time to ring alarm')
        return minBeforeAlarm
        #checkForUpdate()
###########################################################################
# Update Section

    def checkForUpdate():
        #getting Version and URL update
        minBeforeAlarm = readConfigINI()
        basicLog("checkforUpdate", "Starting Updater")
       
        updaterLink = config.get('Ignore_Program_Config', 'updater link')
        updateFile = config.get('Ignore_Program_Config', 'update file')
        url = config.get('Ignore_Program_Config', 'update file text')
        
        basicLog("checkforUpdate",f"Updater Link: {updaterLink}")

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
            forceUpdate = r_new[2]

            basicLog("checkforUpdate", f"new version: {app_version_pull} | Udpate Link: {update_link_pull} | Outdated by: {outdated_by} ")
            #Chekcing if new version is higher then updating. 
            if app_version_pull > app_version:
                basicLog("checkForUpdate",f"Downloading Updater.py")    
                try:
                    #Downloading UpdaterFile
                    r = requests.get(updaterLink, allow_redirects=True)
                    #Writing new update to Updater.py file
                    with open(f"SupportingFiles\\Updater.py", 'w') as writeFile:
                        writeFile.write(r.text)
                        basicLog("checkForUpdate",f"Update Complete")  
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    logger("checkForUpdate", e, fname, exc_tb.tb_lineno)
                    #logging.flush()

                if "True" in forceUpdate:
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
    def getFileName():
        fileName = None
        basicLog("readFile","Starting Function - reading File")
        #Gettinf file name in directory:
        dateTime = str(datetime.datetime.now())
        dateToday = dateTime[5:11]
        for (dirpath, dirnames, filenames) in walk("."):
            for x in filenames:
              #  print(x)
            #    print(dateToday[1:2], dateToday[4:5])
                if dateToday[1:2] in x and dateToday[4:5] in x:
                    
                    fileName = x
                    print(f"Found the Alarms File: {x}\n")
                    basicLog("readFile", f"Found the Alarms File: {x}\n")
                    return fileName,dateToday

    def addColon(alarm0):
        try:
            if ":" not in alarm0:
                if len(alarm0) == 3:
                    alarm0Done = alarm0[0] + ":" + alarm0[1:]
                    return alarm0Done
                elif len(alarm0) == 4:
                    alarm0Done = alarm0[:2] + ":" + alarm0[2:]   
                    return alarm0Done
            else:
                return alarm0

        except Exception as e:
            print("208 Error")
            print(e)

    def readFile():
        alarmMsgDict = []
        fileName, dateToday = getFileName()
       # print(fileName)
        if fileName != None:
        #Reading file to extract alarms and text.
            #Reading Vars form Config.ini
            config = ConfigParser()
  
            config.read("config.ini")
            configSections = config.sections()
            firstColumn = configSections[1]
            secondColumn = configSections[2]
            thirdColum = configSections[3]

            #firstColumn = 'First_Column_Voice'
            #secondColumn = 'Second_Column_Voice'
            #thirdColum = 'Third_Column_Location'
            fullMsg = ''
            #basicLog("readFile", "Opening CSV File")
            file = open(fileName)
            csvreader = csv.reader(file)

            #Looping through each allarm and adding to full msg
            for alarm in csvreader:
                try:
                    if "Time:" in alarm:
                        continue
                    elif alarm[0] == '':
                        continue
                    elif alarm[0].count(":") > 0:
                        #print(f"{alarm[0]} Has Colon")
                        alarm[0] = alarm[0].replace(":","")
                        #print(alarm[0])
                    if not(alarm[0].isdigit()):
                        print(f"\n{alarm[0]} is not a Number! Skipping it. \n")
                        continue 
                #Checking format of Time:
                    alarm0 = alarm[0]
                 #   print(alarm0)
                    #basicLog("readFile", "Changing time based if it has : or no")

                   # if ":" not in alarm0:
                    basicLog("ReadFile", f"Sending Alarm to colon function: {alarm0}")
                    alarm0Done = addColon(alarm0)
                  # else:
                       # alarm0Done = alarm0
                    #print(alarm0Done)
                #Full Message of this Alarm
                    #basicLog("readFile", "Compiling full msg")
                  
                    try:
                      #  print("1st") # print(config.get(firstColumn, (alarm[1].lower())))

                        firstMsg = config.get(firstColumn, (alarm[1].lower()))
                    except:
                        firstMsg = "-"
                    try:
                       # print("2nd")
                        secondMsg =  config.get(secondColumn, alarm[2].lower())
                    except:
                        secondMsg = "-"
                    try:
                       # print("Third")
                        thirdMsg = config.get( thirdColum, alarm[3].lower())
                    except:
                        thirdMsg = "-"
                    
                   # print("Full Msg")
                  
                    fullMsg = alarm0Done, firstMsg, secondMsg, thirdMsg
                  #  print(fullMsg)
                    basicLog("readFile", "Done with full msg")
                    alarmMsgDict.append(fullMsg)
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    logger("readFile", e, fname, exc_tb.tb_lineno) 
                    # e = str(e)
                    # if firstColumn in e:
                    #     fullMsg = alarm0Done, config.get(secondColumn, alarm[2].lower()), config.get( thirdColum, alarm[3].lower())
                    #     alarmMsgDict.append(fullMsg)
                    # elif secondColumn in e:
                    #     fullMsg = alarm0Done, config.get( firstColumn, alarm[1].lower()), config.get( thirdColum, alarm[3].lower())
                    #     alarmMsgDict.append(fullMsg)

                    # elif thirdColum in e:
                    #     fullMsg = alarm0Done, config.get( firstColumn, alarm[1].lower()),  config.get(secondColumn, alarm[2].lower())
                    #     alarmMsgDict.append(fullMsg)
                    
                    # else:
                    #     print(e)
            file.close()
        else:
            print(f"\n !!!!! CAUTION !!!!!!!!!!!!!! \n Can Not Find a file Named: {dateToday} rename your CSV file to this.")
            input("Press Enter to Run Again")
            readFile()
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
                time.sleep(.75)
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
                _thread.start_new_thread( alarmTimer, (str(alarmMsgDict[specificAlarm][0]), alarmMsgDict[specificAlarm], numAlarm, numOfAlarms ) )
                print(f"Alarm: {specificAlarm + 1} / {numOfAlarms} = {alarmMsgDict[specificAlarm]}")
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

    def alarmTimer( alarm, msg, numAlarm, numOfAlarms):
        basicLog("alarmTimer",f"Starting AlarmTimer Function Vars: alarm: {alarm} | msg: {msg} | numAlarm: {numAlarm}")
        try:
            global time_diff
            #Adding 12 hours to alaram if its under 12 - time reasonning - need to make better
            currentAlarm = alarm
            alarmSplit = currentAlarm.split(":")

            if int(alarmSplit[0]) < 7:
                alarmSplit[0] = int(alarmSplit[0]) + 12
                        
            # Converting the alarm time to seconds
            #print(f"286 {alarmSplit}")
            time_sec = int(alarmSplit[0])*3600 + (int(alarmSplit[1]))*60
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
            #print(f"FIRST: Time left for alarm {alarm} is %s\n" % datetime.timedelta(seconds=time_diff))

            #If time difference is negative, it means the alarm is passed by -x H/M/Seconds.
            #Put this back:             if time_diff > -100 and time_diff < 60:
            if time_diff > -10: #and time_diff < 50:
                #Put this back:  randInt = random.randint(10,50)
                randInt = random.randint(1, 30)
                #numAlarm+=1
                time_diff = time_diff + randInt
            elif time_diff < -100:
                print(f"-----ALARM PASSED-----\n")
                basicLog(f"alarmTimer",f"-----ALARM PASSED----- {alarm} {msg}")
                #numAlarm +=1
                
                if (numAlarm+1) == (numOfAlarms):
                    basicLog("PlayAudio", f"Did all alarms! {numAlarm+1}/{numOfAlarms}")
                    print("Done with All Alarms - Closing in a few seconds..")
                    #if time_diff > 0:
                    time.sleep(2)
                    sentrySend()
                exit()
                #sys.stderr.write("CHANGE BACK TO EXIT 384")
                #print("CHANGE BACK TO exit 384")
            else:
                print(f"-----ALARM PASSED-2----\n")
                basicLog(f"alarmTimer",f"------ALARM PASSED - Else----{alarm} {msg}")
             #   # before it was: exit() 
                exit()

            # Displaying the time left for alarm
            print(f"Alarm Will Go Off in: %s\n" % datetime.timedelta(seconds=time_diff))
            basicLog("alarmTimer", f"Time left for alarm is {alarm} | {msg} | {datetime.timedelta(seconds=time_diff)}")
            
            # Sleep until the time at which alarm rings
            if time_diff > 0:
                time.sleep(time_diff)
            else:
                time.sleep(.5)
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
            print(f"Did Alarm: {numAlarm+1}/{numOfAlarms} | Time: {alarm}\n")
            basicLog("playAudio", f"DONE: {msg} - File Local: {msgFull} - ")
            basicLog("PlayAudio", f"Did Alarm: {numAlarm+1}/{numOfAlarms}")
            if (numAlarm+1) == (numOfAlarms):
                basicLog("PlayAudio", f"Did all alarms! {numAlarm+1}/{numOfAlarms}")
                print("Done with All Alarms - Closing in a few seconds..")
                if time_diff > 0:
                    time.sleep(2)
                    sentrySend()
                #print("Done with all alarms 358")

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

        global sentryRun
        if sentryRun == False:
            print("Execution Time In Seconds: ", str(time.time() - t1))
            basicLog("Sentry", f"Execution Time In Seconds: {str(time.time() - t1)}")
            print("Closing Program Shortly")
            
            sentryRun = True
            ipv4API1 =  'https://icanhazip.com/'
            
            try:
                host_name = socket.gethostname()
                host_ip_private = socket.gethostbyname(host_name)
            except Exception as e:
                host_name = 'Host-Name: Null'
                host_ip_private = 'Private-IP: Null'

            try:
                host_ip_public = urllib.request.urlopen(ipv4API1).read().decode('utf8')  
            except Exception as e:
                host_ip_public = "Public_IP: Null"
                basicLog('Sentry Send', f"Trying to get Public IP: {e}")
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
            logData = open(f"SupportingFiles{slash}{logFile}", encoding="utf8")
            data = logData.read()
            logData.close()
            host_name = socket.gethostname()
            configure_scope(lambda scope: scope.add_attachment(path=f"SupportingFiles{slash}{logFile}"))
            capture_exception(AttributeError(" ## " + host_name + " | " + str(datetime.datetime.now())))
            # capture_message(datetime.datetime.now())
            #print("Closing Now")
            #time.sleep(1)
        try:
         #   print("sys.exit()")
            sys.exit()
        except:
            print("\n\n ##### You May now Close the Program ##### \n\n")
            exit()

         
   ###########################################################################
    # Def config File
    def configIni():
        #Default Values:
        print("Creating Default Config File!")
        ipv4API1 =  'https://icanhazip.com/'
        minBeforeAlarm = 5
        
        try:
            host_name = socket.gethostname()
            host_ip_private = socket.gethostbyname(host_name)     
        except Exception as e:
            host_name = "Null Host"
            host_ip_private = "Null Private IP"
            print(e)
        host_username =  os.getlogin()
        host_platform = platform.platform()

        #Whre to save Config file 
        logDir = (r".")
        try:
            host_ip_public = urllib.request.urlopen(ipv4API1).read().decode('utf8')
        except:
            host_ip_public = 'Null Public IP'

        #Init of config parser
        config = ConfigParser()

        #Function for creating INI
        def createINI():
 
            firstRunTime = datetime.datetime.now()
            #These are the default variables. they can be changed if user wants.
            config['DEFAULTS'] = {
                'Minutes Before Time to Ring Alarm'         : minBeforeAlarm,
            }

            #Config Parset for First_Column_Voice
            config['First_Column_Voice'] = {
                'SR' : 'Stop Run',
                'E'  : 'End of Algo',
                'S'  : 'Start of Big Run',
                'B'  : 'Big Bar (continuation)',
                'CB' : 'China Bought',
                'CS' : 'China Sold',
                'LB' : 'London Bought',
                'LB' : 'London Sold',
                'HB' : 'Hank Buy',
                'HS' : 'Hank Sell',
                'DT' : 'Double Top',
                'DB' : 'Double Bottom'
            }

            #Config Parset for Second_Column_Voice
            config['Second_Column_Voice'] = {
                'D'  :  'Doublewide',
                'T'  :  'Triplewide',
                'M'  :  'Maybe',
                'SR' :  'Stop Run'
            }

            #Config Parset for Third_Column_Location
            config['Third_Column_Location'] = {
                'C'   :    'China',
                'L'   :    'London', 
                'B'   :    'Both'
            }

            #Config Parset for System_Info
            config['Ignore_Program_Config'] = {
                'First Run'                 :   True,
                'Install Date & Time: '     :   firstRunTime,
                'Host Machine Name: '       :   host_name,
                'Host Machine Private IP: ' :   host_ip_private,
                'Host machine Public ip'    :   host_ip_public,
                'Host Username: '           :   host_username,
                'Host Platform: '           :   host_platform,
                'Updater Link'              :   "https://raw.githubusercontent.com/maxacode/Adept-Vocal-Alarm/main/SupportingFiles/Updater.py",
                'Update File'               :   "SupportingFiles\\Updater.py",
                'Update File Text'          :   "https://raw.githubusercontent.com/maxacode/Adept-Vocal-Alarm/main/SupportingFiles/Update.txt",
            }

            with open(logDir + f'{slash}config.ini','w') as configfile:
                config.write(configfile)
                pass
            print("Done Creating Config File")
        createINI()
 
    ###########################################################################
    # Main Section
    if __name__ == "__main__":
        #Logging setup.
        #print(os.getcwd())
        print(f"\n\n%%%%%%%%%%%%%%%%%% Starting Adept Vocal Alarm Now!! v:{app_version} %%%%%%%%%%%%%%%%%%\n\n Initilizing - please wait a few seconds \n\n")
        #Time usage:
        t1 = time.time()
        #Memory usage:
       # print("Memory (Before: {}Mb".format(mem_p))
        audioFolder = ("SupportingFiles" + slash + "Audio")
        #Creating Audio folder and/or removing contents
        try:
            #basicLog("Main", "Creating SuuportingFiles and Audio Folder . ")
            os.mkdir("SupportingFiles")
        except:
            pass

        if exists(audioFolder):
            shutil.rmtree(audioFolder)
            os.mkdir(audioFolder)
        else:
            try:
                os.mkdir(audioFolder)          
            except:
                pass

        if exists("config.ini"):
            pass
        else:
            configIni()
        try:
            if exists(f"SupportingFiles{slash}{logFile}"):
                os.remove(f"SupportingFiles{slash}{logFile}")
        except:
            logFile = "logging2.log"

        format= "%(asctime)s | %(levelname)s |  %(message)s"
        
        logging.basicConfig(format = format, filename=f'SupportingFiles{slash}{logFile}', encoding='utf-8', level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S %p')
        logging.info(f"\n\n                 %%%%%%%%%%%%%%%%%% Main Program start {app_version}%%%%%%%%%%%%%%%%%%\n")
        checkForUpdate()
        #readConfigINI()
        #Waiting so threads can run and not stop. 
        while 1:
            pass
except KeyboardInterrupt:
    print("Closing Out!")
    sentrySend()

except Exception as e:
    print(f"Main Except: \n\n{e}\n")
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    try:
        logger("Main Except", e, fname, exc_tb.tb_lineno)
    except:
        print("Main Except: Notifiy Developer!")
    #sentrySend()
    input("\n \n Press enter to Exit!")
    sys.exit()
