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
 
import requests

#Refrences:
#https://docs.python-requests.org/en/latest/user/quickstart/#passing-parameters-in-urls

app_version = "1.1"
 
url = "https://raw.githubusercontent.com/maxacode/Adept-Vocal-Alarm/main/Update.txt"
r = requests.get(url, allow_redirects=True)
#print(r.text)
r_new = r.text.split('\n')
#print(r_new)
app_version_pull = r_new[0]
update_link_pull = r_new[1]
 

if app_version_pull > app_version:
    print(f"Your Version is Outdated by {int(app_version_pull)-int(app_version)}")
    updateQ = input("Update Available, Update Now (Y/N): ")
    if updateQ.lower() == "y":
        print("Downloading Update!")
        #Code here to say how long it will take.
        #Download complete then install here. 
 



print("Hello World!")