import csv

from configparser import ConfigParser

import os
from socket import create_server


#Reading Vars form Config.ini
config = ConfigParser()
print(os.getcwd())
config.read("config.ini")
firstColumn = 'First_Column_Voice'
secondColumn = 'Second_Column_Voice'
thirdColum = 'Third_Column_Location'
 
file = open("alarms.csv")
csvreader = csv.reader(file)

header = next(csvreader)
rows = []
for alarm in csvreader:
    try:
       # print(alarm)
        if "Time" in alarm:
            continue
        elif alarm[0] == '':
            break


 
    #Full Message of this Alarm
        fullMsg = alarm[0], config.get( firstColumn, alarm[1].lower()),  config.get(secondColumn, alarm[2].lower()), config.get( thirdColum, alarm[3].lower())

        print(fullMsg)
    except Exception as e:
        e = str(e)
        if firstColumn in e:
            fullMsg = alarm[0], config.get(secondColumn, alarm[2].lower()), config.get( thirdColum, alarm[3].lower())
            print(fullMsg)
        elif secondColumn in e:
            fullMsg = alarm[0], config.get( firstColumn, alarm[1].lower()), config.get( thirdColum, alarm[3].lower())
            print(fullMsg)
        elif thirdColum in e:
            fullMsg = alarm[0], config.get( firstColumn, alarm[1].lower()),  config.get(secondColumn, alarm[2].lower())
            print(fullMsg)
            
        else:
            continue
        