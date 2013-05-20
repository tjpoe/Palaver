#!/usr/bin/env python

# This script is hacky, maybe it should work using sockets.
# Or dbus, or w/e
# -*- coding: cp1252 -*-
import pynotify, time, os, subprocess

try:
	os.chdir("Microphone")
except:
	print "Currently in",os.getcwd()
PWD=str(os.getcwd()) # Our full path

def transText(text):
	text = text.replace("\n",'')
	home = subprocess.Popen("echo $HOME", shell=True, stdout=subprocess.PIPE).communicate()[0].replace('\n','')
	with open(home+"/.palaver.d/UserInfo") as f:
		for each in f:
			line = each.replace('\n','')
			if line.startswith("LANG="):
				language = line.replace("LANG=","").replace(" ","")
	if language == "en":
		return text
	else:
		f1 = open("Translations/"+language)
		f = f1.read().decode("utf-8")
		f1.close()
		f=f.split("\n")
		for l in f:
			l = l.replace('\n','')
			if l != "":
				o,n = l.split("=")
				if o == text:
					return n
	return text


pynotify.init("Speech Recognition")

n = pynotify.Notification(transText("Please wait"),
                          "",
                          PWD+"/Not_Ready/stop.png")
# If we start up the server in a script, it should first show
# not ready.
n.show()

while True:
    # To make everything silent
    while os.path.exists("silence"):
        sleep(.1)
    i = 0
    while os.path.exists("pycmd_record"):
        if i >=64:
            i = 0
            continue
        if i < 32:
            n.update(transText("Recording"),
                     "",
                     PWD+"/Recording/thumbs/rec"+ str((i+1))+".gif")
        if i >= 32:
            n.update(transText("Recording"),
                     "",
                     PWD+"/Recording/thumbs/rec"+ str(64-i)+".gif")
        n.show()
        i += 8
        time.sleep(.1)
    i = 0
    while os.path.exists("pycmd_wait"):
        n.update(transText("Performing recognition"),
                 "",
                 PWD+"/Waiting/wait-"+str(i)+".png")
        n.show()
        time.sleep(.1)
        i += 1;
        if i > 17:
            i = 0
    i = 0
    while os.path.exists("pycmd_done"):
        n.update(transText("Done"),
                 " ",
                 " ")
        n.show()
        try:
            os.rename("pycmd_done","pycmd_nocmd")
        except:
            pass
    i = 0
    while os.path.exists("pycmd_result"):
        f = open("result");
       
        title = transText(f.readline())
     	print title
        image = f.readline()
        
        tmp = f.readline()
        
        body = ""
        while tmp != '':
            body += image
            image = tmp
            tmp = f.readline()
            
        if title == '\n' or title == '':
            title = " "
        if body == '\n' or body == '':
            body = " "
        else:
            if body[-1:] == '\n':
                body = body[:-1]
        if image == '\n' or image == '':
            image = " "
        else:
            if image[-1:] == '\n':
                image = image[:-1]
          
        n.update(title,body,image)
        n.show()
        try:
            os.rename("pycmd_result","pycmd_nocmd")
        except:
            pass
    while os.path.exists("pycmd_stop"):
    
        n.update(transText("Please wait"),
                 "",
                 PWD+"/Not_Ready/stop.png")
        n.show()
        try:
            os.rename("pycmd_stop","pycmd_nocmd")
        except:
            pass
    time.sleep(.1)
