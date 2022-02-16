


 #A updater file that runs seperately. !!@

testFileName = "testing.py"
currentVersionFile = "FileVersion.txt"
updateTextFile = 'Update.txt'


def readUpateVersionNum( ):
    #Getting current file version number
    with open(currentVersionFile, "r") as x:
        xupdateLines = x.readlines()
    #getting update file version
    with open(updateTextFile, "r") as newUpdate: 
        updateLines = newUpdate.readlines()
        newVersion = updateLines[0][:3]

    #if diffent versions then update current file
    if updateLines[0][:3] != xupdateLines[0]:
        print("Update Needed")
       # thisFileVersion = updateLines[0][:3]
        with open(currentVersionFile, 'w') as y:
            y.writelines(updateLines[0][:3])



readUpateVersionNum()
        
 