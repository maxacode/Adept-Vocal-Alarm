## Adept-Vocal-Alarm
#Smart alarm that will go off X amount of time before and voice the Message

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
 
import requests, os

#Refrences:
#https://docs.python-requests.org/en/latest/user/quickstart/#passing-parameters-in-urls

app_version = 1.0
 
url = "https://raw.githubusercontent.com/maxacode/Adept-Vocal-Alarm/main/Update.txt"
r = requests.get(url, allow_redirects=True)
#print(r.text)
r_new = r.text.split('\n')
#print(r_new)
app_version_pull = float(r_new[0])
update_link_pull = r_new[1]
outdated_by = (app_version_pull)-(app_version)
 

if app_version_pull > app_version:
    print(f"Your Version is Outdated by {str(outdated_by)[:4]}")
    updateQ = input("Update Available, Update Now (Y/N): ")
    if updateQ.lower() == "y":
        print("Downloading Update!")
        #Renaming old file to _Old Might need a thread since the file is running live. 
           #os.rename("Main.py","Main_Old.py")
        #Code here to say how long it will take.
        #Download complete then install here. 
        #Downloading new version
        r = requests.get(update_link_pull, allow_redirects=True)
        open(f"MainV"+app_version_pull+".py", 'w').write(r.text)




print("Hello World!")