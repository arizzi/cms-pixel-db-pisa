#!/usr/bin/env python

# enable debugging
import sys
import cgitb
from datetime import *
cgitb.enable()
import re
import cgi


print "Content-Type: text/html"
print
print "<html>\n        <head>\n         "      
print '''

'''
sys.path.append("../../PixelDB")

from storm.properties import *
from storm.references import *
from storm import *
from PixelDB import *
import random

pdb = PixelDBInterface(operator="webfrontend",center="cern")
pdb.connectToDB()


form = cgi.FieldStorage() # instantiate only once!
action = form.getfirst('submit', 'empty')
action = cgi.escape(action)
objName = form.getfirst('objName', 'empty')
if objName != "" :
# Avoid script injection escaping the user input
  objName = cgi.escape(objName)
  objType = eval(objName)

  if re.match("test",objName,flags=re.IGNORECASE) : 
    ID="TEST_ID"
    objID = form.getfirst(ID, 'empty')
    objID = cgi.escape(objID)
    filterValue=int(objID)  
  else:
    ID=objName+"_ID"
    ID=ID.upper()
    objID = form.getfirst(ID, 'empty')
    if objName == "Transfer"  or objName == "Data" or objName == "Session":
      objID = cgi.escape(objID)
      filterValue=int(objID)
    else :
      objID = cgi.escape(objID)
      filterValue=unicode(objID)  

  filter=eval(objName+"."+ID)
#ilter=objName+"."+ID
#print "filter ",filter,"=",filterValue, objName,ID
  columns = []
  i =0 
  o = None
  keys=objType.__dict__.keys()
  for attr in keys:
     if  type(eval(objName+"."+attr)) is properties.PropertyColumn or  type(eval(objName+"."+attr)).__name__ == "date"  or  type(eval(objName+"."+attr)).__name__ == "datetime":
           columns.append(attr) 
  objects = pdb.store.find(objType,filter==filterValue)
  if objects.count() != 1 : 
      aux=pdb.store.find(objType).any()
#       o =eval(objName+"()")
      print "<h1> Create new %s </h1>" % objName 
  else :
       o = objects[0]	
       aux = None		
if action == "Validate" :
   print "boh"

if action == "Insert" :
  if  aux :
     buildString=objName+"("
     for c in columns:
           columnType=type(eval("aux."+c))
           adate=date(2000,1,1)
           print columnType		
           if columnType == type(adate) :
                d=form.getfirst(c, "")
		try: 
		        dd=datetime.strptime(d,"%Y-%m-%d")
		except:
			dd=date.today()
		buildString+=" "+c+"=dd,"
           elif columnType == unicode : 
		buildString+=" "+c+"=\""+form.getfirst(c, "")+"\","
	   elif columnType == int :
		buildString+=" "+c+"=int("+form.getfirst(c, "")+"),"
	   elif columnType == float :
		buildString+=" "+c+"=float("+form.getfirst(c, "")+"),"
	   else :
		buildString+=" "+c+"=\""+form.getfirst(c, "")+"\","

     buildString+=")"
#     print buildString
     o=eval(buildString)
#     print eval("o."+ID),objName+"."+ID

     if pdb.store.find(objType,filter==eval("o."+ID)).count() > 0 :
	print "This object ALREADY exists: CANNOT INSERT"	
     else:
        pdb.store.add(o)
	pdb.store.commit()
	print " Objected added"
  else:     
     print "This object ALREADY exists. You CANNOT INSERT, but you can EDIT ! "

#    s = Sensor()	

#    if (self.isSensorInserted(sensor.SENSOR_ID) == True):
#                 print "ERROR: sensor already inserted", sensor.SENSOR_ID
#                 return None
#           self.store.add(sensor)
#           self.store.commit()
            # log in history
#           self.insertHistory(type="NULL", id=0, target_type="SENSOR", target_id=sensor.SENSOR_ID, operation="INSERT", datee=date.today(), comment="NO COMMENT")
#           return sensor


if action == "Save changes" :
   for c in columns:
	   columnType=type(eval("o."+c))
	   adate=date(2000,1,1)
	   if columnType == type(adate) :
   	        d=form.getfirst(c, getattr(o,c))
	        dd=datetime.strptime(d,"%Y-%m-%d")
	   elif columnType == type(None) :
		setattr(o,c,unicode(form.getfirst(c, getattr(o,c))))
	   else: 
		setattr(o,c,columnType(form.getfirst(c, getattr(o,c))))
   pdb.store.commit()
   print "Saved"

if True :
	print "<table id=example cellspacing=10 >"
	print "<form>"
	print "<input type=hidden name=objName value=\"%s\">" % objName
	print "<thead> <tr>"
	print "<th> Field </th>"
	print "<th> Value </th>"
	print "</thead></tr><tbody>"
	if o :
		print "<input type=hidden name=%s value=\"%s\">" % (ID,objID)
	        print "<tr><td>",ID.lower().capitalize()," (main ID)</td><td><b>%s<b></td></tr>"%(getattr(o,ID))
	else :
                print "<tr><td>",ID.lower().capitalize()," (main ID)</td><td><input type=input name=\"%s\" value=\"%s\">"%(ID,"")

	summary=""
        for c in columns:
          if c != ID :
	   if o :
  		   print "<tr><td>",c.lower().capitalize(),"</td><td><input type=input name=\"%s\" value=\"%s\">"%(c,getattr(o,c))
	   else :
                   print "<tr><td>",c.lower().capitalize(),"</td><td><input type=input name=\"%s\" value=\"%s\">"%(c,"")

	   print "</td></tr>"
	   

	print "</tbody><tfoot></tfoot></table><br>"
	print "<input type=\"submit\" name=\"submit\" value=\"Validate\" />"
	if o : 
 		print "<input type=\"submit\" name=\"submit\" value=\"Save changes\" /></form>"
	else :
 		print "<input type=\"submit\" name=\"submit\" value=\"Insert\" /></form>"

