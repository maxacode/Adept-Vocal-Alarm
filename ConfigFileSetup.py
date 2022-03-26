#Creation of Default Config File:

#importing parser
from configparser import ConfigParser
#Getting current time and date modules
from datetime import datetime
#Importing socket to get host IP/name
import socket
#Platform for System info
import platform
#os 
import os
#URL lib to get public ip
import urllib.request
 


#Default Values:
ipv4API1 =  'https://icanhazip.com/'
minBeforeAlarm = 5
 
try:
    host_name = socket.gethostname()
    host_ip_private = socket.gethostbyname(host_name)     
except Exception as e:
    print(e)
    

host_username =  os.getlogin()
host_platform = platform.platform()

#Whre to save Config file 

logDir = (r".")

#starting config file creation
try:
    host_ip_public = urllib.request.urlopen(ipv4API1).read().decode('utf8')

    #Init of config parser
    config = ConfigParser()

    #Function for creating INI
    def createINI():
        firstRunTime = datetime.now()
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
            'Updater Link'              :   "https://raw.githubusercontent.com/maxacode/Adept-Vocal-Alarm/main/Updater.py",
            'Update File'               :   "SupportingFiles\\Updater.py",
            'Update File Text'          :   "https://raw.githubusercontent.com/maxacode/Adept-Vocal-Alarm/main/SupportingFiles/Update.txt",
        }


        with open(logDir + '\config.ini','w') as configfile:
            config.write(configfile)
            pass

except Exception as e:
    print("ConfigFile could not be finished: {}".format(e))



#Running Only this code if this file is so - That way user can re-run config program.
if __name__ == "__main__":
    #Running the function to test. Leave commenetd when packaging file.
    print("Starting Config File Creation")
    createINI()
    print("Done Creating Config File look at 'config.ini' \n Open in Text Editor (notepad, sublime) But NOt In Word")
