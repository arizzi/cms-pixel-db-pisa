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

from openpyxl import load_workbook
import re
import cgi
import os 
form = cgi.FieldStorage() # instantiate only once!

print "Content-Type: text/html"
print
print "<html>\n        <head>\n         </head><body>"      


action = form.getfirst('submit', 'empty')
print "<pre> %s" % action
# Avoid script injection escaping the user input
action = cgi.escape(action)
if action == "Upload" :
	print "<pre>"
	# Get filename here.
	fileitem = form['filename']
	# Test if the file was uploaded
	if fileitem.filename:
	  fn = os.path.basename(fileitem.filename)
	  open('/tmp/' + fn, 'wb').write(fileitem.file.read())
          wb = load_workbook(filename = '/tmp/' + fn)
  	  modules = wb.get_sheet_names()
	  for module in modules :
             if re.match(".+-.+-.+",module) :
                print "## New Module! ###################"
                ws = wb.get_sheet_by_name(module);
                (batch,wafer,pos) = re.split("-",module)
                batchid = batch
                sensorid = "S%s-%s-%s" % (batch,wafer,pos)
                baremoduleid = "M%s-%s-%s" % (batch,wafer,pos)
                waferid = "%s-%s"% (batch,wafer)
                buildDate = ws.cell("B2").value

                print "Module: ", module
                print "Batch: ", batch, " Wafer ", wafer, " Pos ", pos
                print "Sensor ID: ", sensorid 
                print "BareModule ID: ", baremoduleid 
                print "Wafer ID: ", waferid 
                rocids=""
                for i in xrange(15,30):
                        rocid="%s-%s"%(ws.cell(row=i,column=2).value,ws.cell(row=i,column=3).value)
                        print rocid
                        rocids+="%s,"%rocid
                print rocids
                print buildDate
		#create a transfer for the following operations TODO: use sender and center from apache writers/ folder auth 
		t = pdb.insertTransfer(Transfer(cgi.escape(form.getfirst('Sender', 'Unknown')),"HERE"))
		#first check the batch
                b = pdb.getBatch(batchid)
		if not b:
		   print "Batch %s is new, inserting it..." % batchid
		   b = Batch(BATCH_ID=batchid, TRANSFER_ID=t.TRANSFER_ID, PRODCENTER="FIXME")  
                   if pdb.insertBatch(b) :
			print "OK<br>"
		   else :
			print "FAILED<br>"
 
		#then check the wafer
                w = pdb.getWafer(waferid)
		if not w:
		   print "Wafer %s is new, inserting it..." % waferid 
                   w = Wafer(WAFER_ID=waferid, BATCH_ID=batchid, TRANSFER_ID=t.TRANSFER_ID)
		   if pdb.insertWafer(w) :
                        print "OK<br>"
                   else :
                        print "FAILED<br>"
		#insert sensor
		s  = pdb.getSensor(sensorid)
		if not s :
	           s = Sensor(sensorid,t.TRANSFER_ID,"OLD",cgi.escape(form.getfirst('Sender', 'Unknown')),WAFER_ID=waferid)
	   	   if pdb.insertSensor(s) :
                     print "<br><b> Sensor %s inserted </b>" % sensorid
	           else :
                     print "<br><b> Insertion of sensor %s failed! </b>" % sensorid
		     s =None
						
	        else :
	            print "Sensor %s already exists<br>" % sensorid

 		#if sensor inserted or existed, make baremodule	
	        if s :
                    bm  = pdb.getBareModule(baremoduleid)
		    if not bm :
		         bm = BareModule(baremoduleid,rocids,sensorid,t.TRANSFER_ID,cgi.escape(form.getfirst('Sender', 'Unknown')))
		         if pdb.insertBareModule(bm)  :
                	    print "<br><b> Bare module %s  inserted </b>" % baremoduleid
			 else :
                	    print "<br><b> Bare module %s insertion failed </b>" % baremoduleid
		    else:
                        print "BareModule %s already exists<br>" % baremoduleid
			
	  os.unlink('/tmp/' + fn)



    
else :
 print '''<html>
<body>
   <form enctype="multipart/form-data" 
                     action="uploadSensorDataSheet.cgi" method="post">
   <p>Datasheet Filename: <input type="file" name="filename" /></p>
   <p><input type="submit" name="submit" value="Upload" /></p>
   </form>
</body>
</html> '''


