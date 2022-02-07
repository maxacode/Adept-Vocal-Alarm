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
import urllib
url = "https://github.com/maxacode/Adept-Vocal-Alarm/blob/main/Update.txt"
urllib.urlretrieve(url, "update.txt")

app_version = "1.0.0"
update_link = ""

print("Hello World!")