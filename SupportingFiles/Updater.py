 
 #updater file for program

#os to rename the files
import os
#requests for downloading update. 
import requests
import time
#basicLog("updater.py",f"Starting Update")    
import sys
mainName = 'Main.py'

 #Renaming old file to _Old Might need a thread since the file is running live. 
#os.rename(mainName,"Main_Old.py")
basicLog("updater.py",f"Rename Complete")    

 
#Downloading new version
try:
    
     #Downloading new update
    r = requests.get(update_link_pull, allow_redirects=True)
    #Writing new update to Main.py file
    open(mainName, 'wb').write(r.content)

except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(e)
    logger("readFile", e, fname, exc_tb.tb_lineno) 

print("Update Complete - run 'Main.py' Again!")
time.sleep(10)
try:
    basicLog("updater.py",f"New Main with Python")
    os.system(f"python {mainName}")

except:
    basicLog("updater.py",f"New Main with Python3 :")

    os.system(f"python3 {mainName}")

