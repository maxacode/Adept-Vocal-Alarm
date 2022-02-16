randomString = 'print("Hello World")'


import _thread
import os
import readline

file = 'testing.py'

with open("Update.txt", "r") as updateFile:
    firstline = updateFile.readline()
    if firstline == '1.1':
        print(firstline)




exec(open('test2.py').read())

#def updateFile():
    #exec(compile(open(file).read(), file, data))
    #os.remove('testing.py')
 
    #with open(file) as f:
      #  code = compile(f.read(), "somefile.py", 'exec')
      #  exec(code)
    

#_thread.start_new_thread( updateFile, ())