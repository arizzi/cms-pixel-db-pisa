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
sys.path.append("..")

from storm.properties import *
from storm.references import *
from storm.variables import (
    Variable, VariableFactory, BoolVariable, IntVariable, FloatVariable,
    DecimalVariable, RawStrVariable, UnicodeVariable, DateTimeVariable,
    DateVariable, TimeVariable, TimeDeltaVariable, PickleVariable,
    ListVariable, EnumVariable)

from storm import *
from PixelDB import *
import random
import ConfigParser
from pixelwebui import *

def inputField(objName,column, defVal = "") :
	config = ConfigParser.ConfigParser()
	config.read('/var/www/cgi-bin/writers/editor.ini')
	#default input string:
	inputString = "<input type=input name=\"%s\" value=\"%s\">" % (column,defVal)
	if column == "DATA_ID" :
	    if defVal == "" :
	 	inputString="<input type=\"file\" name=\"DATA_ID_filename\" />"
	elif config.has_section(objName+"/"+column) :
 	    type = config.get(objName+"/"+column,"type")
 	    if type == "select" :
		   options = re.split(',',config.get(objName+"/"+column,"options"))
		   inputString="<select name=\"%s\">" % column
		   for o in options :
			if o== defVal :
			    selected = "SELECTED"
			else :
			    selected = ""
			inputString+="<option value=\"%s\" %s>%s</option>" % (o,selected,o)

		   inputString+="</select>"
  	    if config.has_option(objName+"/"+column,"comment") :
		inputString+="&nbsp;&nbsp;&nbsp;(<i>"+config.get(objName+"/"+column,"comment")+"</i>)"
	return inputString	

pdb = PixelDBInterface(operator="webfrontend",center="cern")
pdb.connectToDB()


form = cgi.FieldStorage() # instantiate only once!
action = form.getfirst('submit', 'empty')
force = form.getfirst('force', False)
action = cgi.escape(action)
objName = form.getfirst('objName', 'empty')
if objName == "empty" :
    exit()
if objName != "" :
# Avoid script injection escaping the user input
  objName = parseObjName(cgi.escape(objName))
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
  first=objects.count()==0
  if objects.count() != 1 : 
      aux=pdb.store.find(objType).any()
#       o =eval(objName+"()")
      print "<h1> Create new %s </h1>" % objName 
  else :
       print "found"	
       o = objects[0]	
       aux = None	
if action == "Validate" :
   print "to be implemented"

if action == "Insert" :
  if  aux or first :
     buildString=objName+"("
     for c in columns:
#           columnType=type(eval("aux."+c))
           adate=date(2000,1,1)
           columnType2=type(eval(objName+"."+c+".variable_factory()"))
	   if c == "DATA_ID" and form['DATA_ID_filename'].filename :
  		    fileitem = form['DATA_ID_filename']
         	    fn = objID+"__"+os.path.basename(fileitem.filename)
                    open('/data/pixels/inventory/'+objName+'/' + fn, 'wb').write(fileitem.file.read())
		    pfn='file:/data/pixels/inventory/'+objName+'/' + fn
 	            data = Data(PFNs=pfn)
	            insertedData = pdb.insertData(data)
 		    if (insertedData is None):
	                 print"<br>Error inserting data"
			 buildString+="DATA_ID=0"
		    else:
			 buildString+="DATA_ID=%s,"%insertedData.DATA_ID
           elif columnType2 == DateVariable :
                d=form.getfirst(c, "")
		try: 
		        dd=datetime.strptime(d,"%Y-%m-%d")
		except:
                        dd=date.today()
		buildString+=" "+c+"=dd,"
           elif columnType2 == DateTimeVariable :
                d=form.getfirst(c, "")
                try:
                        dd=datetime.strptime(d,"%Y-%m-%d")
                except:
			dd=datetime.now()
                buildString+=" "+c+"=dd,"
           elif columnType2 == UnicodeVariable : 
		buildString+=" "+c+"=\""+form.getfirst(c, "")+"\","
	   elif columnType2 == IntVariable :
		buildString+=" "+c+"=int("+form.getfirst(c, "")+"),"
	   elif columnType2 == FloatVariable :
		buildString+=" "+c+"=float("+form.getfirst(c, "")+"),"
	   else :
		buildString+=" "+c+"=\""+form.getfirst(c, "")+"\","

     buildString+=")"
#     print buildString
     o=eval(buildString)
#     print buildString	 
#     print eval("o."+ID),objName+"."+ID

     if pdb.store.find(objType,filter==eval("o."+ID)).count() > 0 :
	print "This object ALREADY exists: CANNOT INSERT"	
     else:
        pdb.store.add(o)
	pdb.store.commit()
	print " Objected added"
	pdb.insertHistory(type=0,id=0, target_id=eval("o."+ID), target_type=objName, operation="INSERT", datee=datetime.now(), comment="")

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
	   field =  getattr(o,c)
	   list = form.getlist(c)
	   if len(list) > 0 :
		field = list[-1] 
	   columnType=type(eval("o."+c))
           columnType2=type(eval(objName+"."+c+".variable_factory()"))
	   print c, field, columnType, columnType2
	   adate=date(2000,1,1)
	   if columnType == type(adate) or columnType2 == DateVariable:
		if field == "None":
			field = "1970-01-01" 
   	        d=field #form.getfirst(c, getattr(o,c))
	        dd=datetime.strptime(d,"%Y-%m-%d")
		setattr(o,c,dd)
	   if columnType2 ==  DateTimeVariable :
                if field == "None":
                        field = "1970-01-01 00:00:00"   
                d=field #form.getfirst(c, getattr(o,c))
                dd=datetime.strptime(d,"%Y-%m-%d %H:%M:%S")
                setattr(o,c,dd)
	   elif columnType == type(None) :
#		setattr(o,c,unicode(form.getfirst(c, getattr(o,c))))
		setattr(o,c,unicode(field))
	   else: 
#		setattr(o,c,columnType(form.getfirst(c, getattr(o,c))))
		setattr(o,c,columnType(field))
   pdb.store.commit()
   print "Saved"

if True :
	print "<table id=example cellspacing=10 >"
	print "<form enctype=\"multipart/form-data\" method=\"post\" action=edit.cgi>"
	print "<input type=hidden name=objName value=\"%s\">" % objName
	print "<thead> <tr>"
	print "<th align=left> Field: </th>"
	print "<th align=left> Value: </th>"
	print "</thead></tr><tbody>"
	if o :
	    if force != "1" :
		print "<input type=hidden name=%s value=\"%s\">" % (ID,objID)
	        print "<tr><td>",ID.lower().capitalize()," (main ID)</td><td><b>%s<b></td></tr>"%(getattr(o,ID))
	    else : 	
		print "<input type=hidden name=%s value=\"%s\">" % (ID,objID)
                print "<tr><td>",ID.lower().capitalize()," (main ID)</td><td>"
                print inputField(objName,ID,getattr(o,ID))
	else :
                print "<tr><td>",ID.lower().capitalize()," (main ID)</td><td>"
                print inputField(objName,ID)

#<input type=input name=\"%s\" value=\"%s\">"%(ID,"")

	summary=""
        for c in columns:
          if c != ID : #or force:
	   if o :
  		   print "<tr><td>",c.lower().capitalize(),"</td><td>"
#d><input type=input name=\"%s\" value=\"%s\">"%(c,getattr(o,c))
		   print inputField(objName,c,getattr(o,c))
	   else :
                   print "<tr><td>",c.lower().capitalize(),"</td><td>"
#<input type=input name=\"%s\" value=\"%s\">"%(c,"")
		   print inputField(objName,c)

	   print "</td></tr>"
	   

	print "</tbody><tfoot></tfoot></table><br>"
	print "<input type=\"submit\" name=\"submit\" value=\"Validate\" />"
	if o : 
 		print "<input type=\"submit\" name=\"submit\" value=\"Save changes\" /></form>"
	else :
 		print "<input type=\"submit\" name=\"submit\" value=\"Insert\" /></form>"

