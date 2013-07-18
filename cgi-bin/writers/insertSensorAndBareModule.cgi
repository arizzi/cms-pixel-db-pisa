#!/usr/bin/env python
# enable debugging
import cgitb
from datetime import *
cgitb.enable()

import sys
sys.path.append("../../PixelDB")
from storm.properties import *
from storm.references import *
from storm import *
from PixelDB import *
import random


pdb = PixelDBInterface(operator="webfrontend",center="cern")
pdb.connectToDB()


import re
import cgi
form = cgi.FieldStorage() # instantiate only once!

print "Content-Type: text/html"
print
print "<html>\n        <head>\n         </head><body>"      


action = form.getfirst('submit', 'empty')
# Avoid script injection escaping the user input
action = cgi.escape(action)
if action == "submit" :
    sensor = cgi.escape(form.getfirst('Sensor', 'empty'))
    if sensor == 'empty' :
      print "No sensor ID given!" 
    else :   
      if sensor[0] != 'S' :
        print "Sensor name should start with <b>S</b>, pre-pending it automtically ==> <b>S%s</b><br>" % (sensor)
        sensor= "S%s"%(sensor)
      t = pdb.insertTransfer(Transfer(cgi.escape(form.getfirst('Sender', 'Unknown')),"HERE"))
      s  = pdb.getSensor(sensor)
      if not s :
         s = Sensor(sensor,t.TRANSFER_ID,"OLD")
         if pdb.insertSensor(s) :
		print "<br><b> Sensor inserted </b>"
      else :
         print "Sensor already exists<br>"
      if s : 
         baremodule = re.sub('S','B',sensor)
         print "Creating BareModule with ID %s <br>" % (baremodule)
         print "List of ROCs"
	 allrocs = ""
         for i in range (0,16) :
             rocid=cgi.escape(form.getfirst('Roc%s'%i, ''))
             if rocid != '' :
               roc = pdb.getRoc(rocid)
               if not roc :
	    	print "ROC %s not found" % (rocid)
             if allrocs != "" :
                allrocs += ','
	     allrocs +=  "%s" % (rocid)
         print allrocs
         bm = BareModule(baremodule,allrocs,sensor,t.TRANSFER_ID,cgi.escape(form.getfirst('Sender', 'Unknown')))
	 if pdb.insertBareModule(bm)  :
		print "<br><b> Bare module inserted </b>"
   
     
    
else : 
    print "<form action=insertSensorAndBareModule.cgi method=POST>"
    print 'Sensor ID (e.g. S12345-18-2): <input type="text" name="Sensor"><br>'
    print 'Sensor type: <select name=type><option value="old">Old Analog Full Module</option><option value="old">Old Analog Half Module</option><option value="new">Digital</option></select><br>'
    print 'Received from : <input type="text" name="Sender"><br>'
    print 'ROC IDs:<br>'
    for i in range(0,16) :
        print i,': <input type="text" name="Roc%s"><br>' % (i)

    print "<input type=\"submit\" name=submit value=submit>"    
    print "</form>"    

