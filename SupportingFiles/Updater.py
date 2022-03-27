 
 #updater file for program

#os to rename the files
import os
#requests for downloading update. 
import requests
import time
#basicLog("updater.py",f"Starting Update")    
import sys
mainName = 'Main.exe'
os.remove(mainName)
import shutil
 #Renaming old file to _Old Might need a thread since the file is running live. 
#os.rename(mainName,"Main_Old.py")
basicLog("updater.py",f"Delete Complete")    

 
#Downloading new version
try:
    
     #Downloading new update
  #  r = requests.get(update_link_pull, allow_redirects=True)
    #Writing new update to Main.py file
  #  open(mainName, 'wb').write(r.content)
    with requests.get(update_link_pull, stream=True) as r:
        with open(mainName, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(e)
    logger("readFile", e, fname, exc_tb.tb_lineno) 

time.sleep(5)
try:
    basicLog("updater.py",f"running new Main.exe")
    os.system(mainName)

except:
    basicLog("updater.py",f"Failed running new Main.exe | Telling user to run")

    print("Update Complete - run 'Main.exe' Again!")

