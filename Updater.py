 
 #updater file for program

#os to rename the files
import os
#requests for downloading update. 
import requests
basicLog("updater.py",f"Starting Update")    
 
mainName = 'Main.py'

 #Renaming old file to _Old Might need a thread since the file is running live. 
#os.rename(mainName,"Main_Old.py")
#basicLog("updater.py",f"Rename Complete")    

 
#Downloading new version
try:
 
     #Downloading new update
    r = requests.get(update_link_pull, allow_redirects=True)
    #Writing new update to Main.py file
    with open(f"Main.py", 'w') as writeFile:
        writeFile.write(r.text)
        basicLog("updater.py",f"Update Complete")  
            
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    logger("readFile", e, fname, exc_tb.tb_lineno) 


basicLog("updater.py",f"Starting NEWWWW Main")
print("Update Complete - Program Starting Up!")
os.system(f"python3 {mainName}")
 

