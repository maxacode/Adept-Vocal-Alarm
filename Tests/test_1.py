import requests
import pytest

updateLink = "https://raw.githubusercontent.com/maxacode/Adept-Vocal-Alarm/main/SupportingFiles/Update.txt"

##UPDATE Functionality:
def test_Updatelinks():
    #Can connect to UpdateLink 
    print("### Update Functionality")

    r = requests.get(updateLink, allow_redirects=True)
    assert "<Response [200]>" in str(r)
    r_new = r.text.split('\n')
    return r_new
#Version Number
def test_VersionCheck():
    r_new = test_Updatelinks()
    assert 2.2== float(r_new[0])
#Update link for Main.exe
def test_UpdateLink():
    r_new = test_Updatelinks()
    assert "https://github.com/maxacode/Adept-Vocal-Alarm/blob/main/Updates/Main.exe?raw=true" == r_new[1]
#Force update Check:
def test_ForceUpdate():
    r_new = test_Updatelinks()
    assert "True" == str(r_new[2])

#Updater.py download
updaterLink = "https://raw.githubusercontent.com/maxacode/Adept-Vocal-Alarm/main/SupportingFiles/Updater.py"
def test_UpdaterPy():
    print("### Updater.py Check")
    r = requests.get(updaterLink, allow_redirects=True)
    assert "<Response [200]>" in str(r)
    assert "os.rename(mainName)" in  str(r.text)