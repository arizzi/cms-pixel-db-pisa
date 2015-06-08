#!/usr/bin/env python
# enable debugging
import shutil

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

import tempfile
import tarfile

def csv_files(members):
    tars=[]
    for tarinfo in members:
	print "h",tarinfo.name
        if re.match("^[^/.]+\.csv",tarinfo.name) :
            tars.append(tarinfo)
    return tars



print "Content-Type: text/html"
print
print "<html>\n        <head>\n         </head><body>"      


action = form.getfirst('submit', 'empty')
#print "<pre> %s" % action
# Avoid script injection escaping the user input
action = cgi.escape(action)
if action == "Upload" :
	print "<pre>"
	# Get filename here.
	fileitem = form['filename']
	# Test if the file was uploaded
	if fileitem.filename:
	  directory_name = tempfile.mkdtemp()
          #print directory_name
	  fn = os.path.basename(fileitem.filename)
	  open('/tmp/' + fn, 'wb').write(fileitem.file.read())
	  files=[]
  	  if re.match('.*\.csv$',fn) :
		print "Single CSV found"
		files=['/tmp/' + fn]
  	  elif re.match('.*\.tar.gz$',fn) or re.match('.*\.tgz$',fn) :
		print "Tar gz found"
		tar = tarfile.open('/tmp/' + fn,"r:gz")
		toextract=csv_files(tar)
		print "Files found: ", toextract
		tar.extractall(path=directory_name,members=toextract)
		tar.close()
		for f in toextract:
			files.append(directory_name+"/"+f.name)
		print files
	  else :
		print "unknown format"
		exit(0)

	  for fname in files :
		print "working on ",fname
    		f=open(fname,mode="U") 
		dic={}
		rocs={}
	        for l in f:
		#	print l
			m=re.match("^(.*?):\s*([^\s]*)\s*$",l)
			m2=re.match("^Comment:(.*)$",l)
			if m or m2 :
			    if m:
				dic[m.group(1).upper()]=m.group(2)	
			    else :
				dic["COMMENT"]=m2.group(1)	

			else :
			        m1=re.match("^(.*),([0-1][0-9])\s*$",l)
				if m1 :
					i=int(m1.group(2))
					rocs[i]=m1.group(1)
		print dic
                sensorid = dic["SENSOR_ID"]
                baremoduleid = dic["BARE_MODULE_ID"]
		buildDate=dic["BUILTON"]
		center=dic["CENTER"]
		sender=dic["BB_COMPANY"]
                print "## New Bare Module! ###################"
                print "Sensor ID: ", sensorid 
                print "BareModule ID: ", baremoduleid 
		print "Full info", dic,rocs
	        rocids=""
                for i in xrange(0,16):
			rocid=rocs[i]
#                        print rocid
                        rocids+="%s,"%rocid
#                print rocids
#                print buildDate
		#create a transfer for the following operations TODO: use sender and center from apache writers/ folder auth 
		t = pdb.insertTransfer(Transfer(cgi.escape(form.getfirst('Sender', sender)),center))
		#insert sensor
		s  = pdb.getSensor(sensorid)
		if not s:
		    print "## ERROR ## The Sensor %s does not exist in our DB, please add it first" % sensorid
	        else :
	            print "Sensor %s has been found" % sensorid

		print "</pre>"
 		#if sensor inserted or existed, make baremodule	
	        if s :
                    bm  = pdb.getBareModule(baremoduleid)
		    if not bm :
			 try :
				 mm=re.match("(.*-.*-.*_.*h.*m).*",dic["BUILTON"])
				 d=mm.group(1)
				 dd=datetime.strptime(d,"%Y-%m-%d_%Hh%Mm")
			 except :
				 print "Cannot parse datetime, using current datetime.... you can later edit this field in the baremodule inventory if you want to change it<br>"
				 dd=datetime.now()
			 print "Build date used %s<br>"%dd
		         bm = BareModule(baremoduleid,rocids,sensorid,t.TRANSFER_ID,sender,TYPE=dic["TYPE"],COMMENT=dic["COMMENT"],BUILTON=dd,status="INSTOCK")
		         if pdb.insertBareModule(bm)  :
                	    print "<br><b> Bare module %s  inserted </b>" % baremoduleid
			 else :
                	    print "<br><b> ## ERROR ## Bare module %s insertion failed </b>" % baremoduleid
		    else:
                        print "<b>## ERROR ## BareModule %s already exists</b> <br>" % baremoduleid
			
	  os.unlink('/tmp/' + fn)
          #os.removedirs(directory_name)
	  shutil.rmtree(directory_name)
	  print "</pre><a href=/cgi-bin/view.cgi?objName=BareModule>back to BareModule inventory</a>"

    
else :
 print '''<html>
<body>
<h1>Upload BareModule to the inventory</h1>
You should upload here either a single CSV or a tar.gz with several CSV (no subfolders, no particular naming beside ending in .csv)
<br>
If you see any error, please report by mail to Andrea and Tommaso.
<br>
   <form enctype="multipart/form-data" 
                     action="uploadBareModuleData.cgi" method="post">
   <p>Datasheet Filename: <input type="file" name="filename" /></p>
   <p><input type="submit" name="submit" value="Upload" /></p>
   </form>

<br>
Example Format:
<pre>
Sensor_id: S322310-08-1
Bare_module_ID: B322310-08-1
BB_company: DESY
Comment: test bare module
Builton: 2015-01-27_14h15m_1422364542
Module_assembly: #WaferXYID, RocPositionInBareModule
ACGN06X-30A,00
ACGN06X-49D,01
ACGN06X-49C,02
ACGN06X-48D,03
ACGN06X-46D,04
ACGN06X-46C,05
ACGN06X-45D,06
ACGN06X-45C,07
ACGN06X-35A,08
ACGN06X-34A,09
ACGN06X-33A,10
ACGN06X-32A,11
ACGN06X-47C,12
ACGN06X-47D,13
ACGN06X-48C,14
ACGN06X-31A,15
type: NotReworked
center: DESY
</pre>
</body>
</html> '''


