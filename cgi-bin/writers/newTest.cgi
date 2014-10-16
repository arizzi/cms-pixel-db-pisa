#!/usr/bin/env python

# enable debugging
import sys
import cgitb
from datetime import *
cgitb.enable()
import re
import cgi

sys.path.append("../../PixelDB")
sys.path.append("..")
#import os
#print os.environ['REMOTE_ADDR']
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
import Cookie
import ConfigParser
from pixelwebui import *
#print defaultCenter()
import time

def printHeaders(setcookies):
	print "Content-Type: text/html"
	print setcookies
	print
	print "<html>\n        <head>\n         "      
	print '''
	<script>
	function setAllPass(){
		var val = "PASS";
		var sels = document.getElementsByClassName("sels");
		for (var i = sels.length - 1; i >= 0; i--)
		{
		sel=sels[i];
		var opts = sel.options;
		for(var opt, j = 0; opt = opts[j]; j++) {
			if(opt.value == val) {
				sel.selectedIndex = j;
				break;
			}
		}
		}
	}
        function setAllEmpty(){
                var sels = document.getElementsByClassName("sels");
                for (var i = sels.length - 1; i >= 0; i--)
                {
                sel=sels[i];
                var opts = sel.options;
                sel.selectedIndex = 0;
                }
        }
	function update(){
                var sels = document.getElementsByClassName("sels");
                for (var i = sels.length - 1; i >= 0; i--)
                {
                sel=sels[i];
                var opts = sel.options;
		console.log(opts[sel.selectedIndex]);
		if(opts[sel.selectedIndex].value == "FAIL") {
			document.getElementById("RESULT").value="FAIL";
			document.getElementById("RESULT").style.backgroundColor = "yellow";
		//	alert("fail");
		}
                }

	}
	</script>

	'''

def inputField(objName,column, cookies, defVal = "") :
	config = ConfigParser.ConfigParser()
	config.read('/var/www/cgi-bin/writers/editor.ini')
	#default input string:
	inputString = "<input id=%s type=input name=\"%s\" value=\"%s\">" % (column,column,defVal)
	if column == "TRANSFER_ID" and defVal == "":
		inputString+=" <b>or</b> create transfer..."
# FROM: <input type=\"input\" name=\"TRANSFER_ID_from\" /> TO: <input type=\"input\" name=\"TRANSFER_ID_to\" /> "
		inputString+=" Sender:   <select name=TRANSFER_ID_sender>"
		cents=[""]
		cents+=centers
		for o in cents :
		        inputString+="<option>%s</option>" % o
		inputString+=" </select>"
		inputString+=" Receiver:   <select name=TRANSFER_ID_receiver>"
		for o in cents :
	        	inputString+="<option>%s</option>" % o
	   	inputString+=" </select><p>"
	elif column == "OSCILLOSCOPE_CHANNELS" :
		channels = ["CH1","CH2","CH3","CH4","LV"]
		tests = ["CLK0","CLK1","CLK2","CLK3","CTR0","CTR1","CTR2","CTR3","SDA0","SDA1","SDA2","SDA3"]
		lens = [12,12,8,12,4]
		inputString= "<table cellpadding=0 cellspacing=2 bgcolor=#000000><tr bgcolor=#FFFFFF><td>Test</td>"
		for c in channels :
			inputString+= "<td>%s</td>" % c
		inputString+= "</tr>"
		for j in xrange(0,len(tests)) :
			inputString+= "<tr bgcolor=#FFFFFF><td>%s</td>"%tests[j]
			for i in xrange(0,5) :
				if lens[i]>j :	
					inputString+= "<td><select class=sels onClick=update()><option value=undef></option><option value=PASS>PASS</option><option value=FAIL>FAIL</option></select></td>"
				else:
					inputString+= "<td bgcolor=#000000></td>"
			inputString+= "</tr>"	
		inputString+= "</table><p>"
		inputString+= "<button onClick=\"setAllPass();\" type=button> Set all to PASS</button> <button onClick=\"setAllEmpty();\" type=button>Reset all to empty</button>"

	elif column == "DATA_ID" :
	    if defVal == "" :
	 	inputString="<input type=\"file\" name=\"DATA_ID_filename\" />"
	elif column == "TEST_ID" :
	    if defVal == "" :
                inputString="Automatic <input type=\"hidden\" name=\"TEST_ID\" value=AUTOGEN />"
        elif column == "SESSION_ID" :
            if defVal == "" :  
		if "center" in cookies :
			inputString=" Operator: <input type=input  name=\"SESSION_OPERATOR\" value=\"%s\"/>" % cookies["center"].value
		else :
			inputString=" Operator: <input type=input  name=\"SESSION_OPERATOR\" />" 

		if "operator" in cookies :
			inputString+=" Center: <input type=input  name=\"SESSION_CENTER\" value=\"%s\"/>" % cookies["operator"].value
		else:
			inputString+=" Center: <input type=input  name=\"SESSION_CENTER\" />" 
		inputString+=" Comment: <input type=input  name=\"SESSION_COMMENT\"/>" 
	elif config.has_section(objName+"/"+column) :
 	    type = config.get(objName+"/"+column,"type")
 	    if defVal == "" and config.has_option(objName+"/"+column,"default"):
		    defVal = config.get(objName+"/"+column,"default")
            if type == "select" :
                   options = re.split(',',config.get(objName+"/"+column,"options"))
                   inputString="<select name=\"%s\">" % (column)
                   for o in options :
                        if o== defVal :
                            selected = "SELECTED"
                        else :
                            selected = ""
                        inputString+="<option value=\"%s\" %s>%s</option>" % (o,selected,o)

                   inputString+="</select>"
 	    if type == "selectedit" :
		   options = re.split(',',config.get(objName+"/"+column,"options"))

		   inputString="<input list=%s_list name=\"%s\" value=%s>" % (column,column,defVal)
		   inputString+="<datalist id=%s_list>" % (column)
		   for o in options :
			if o== defVal :
			    selected = "SELECTED"
			else :
			    selected = ""
			inputString+="<option value=\"%s\" %s>%s</option>" % (o,selected,o)

#		   inputString+="</select>"
		   inputString+="</datalist>"
  	    if config.has_option(objName+"/"+column,"comment") :
		inputString+="&nbsp;&nbsp;&nbsp;(<i>"+config.get(objName+"/"+column,"comment")+"</i>)"
	return inputString	

pdb = PixelDBInterface(operator="webfrontend",center="cern")
pdb.connectToDB()

setcookies = Cookie.SimpleCookie()
if 'HTTP_COOKIE' in os.environ:
    cookie_string=os.environ.get('HTTP_COOKIE')
    setcookies.load(cookie_string)


form = cgi.FieldStorage() # instantiate only once!
action = form.getfirst('submit', 'empty')
force = form.getfirst('force', False)
action = cgi.escape(action)
objName = form.getfirst('objName', 'empty')

if objName == "empty" :
    printHeaders()
    exit()

if objName != "" :
  columns = onlyColumns(objName)
  objName = parseObjName(cgi.escape(objName))
  objType = eval(objName)
  ID=idField(objName)

if action == "Insert" :
     setcookies["center"]=form.getfirst("SESSION_CENTER","")
     setcookies["operator"]=form.getfirst("SESSION_OPERATOR","")
     printHeaders(setcookies)

     buildString=objName+"("
     for c in columns:
#           columnType=type(eval("aux."+c))
           adate=date(2000,1,1)
           columnType2=type(eval(objName+"."+c+".variable_factory()"))
	   objID="%s"%time.time()	
	   if c == ID :
		 if form.getfirst(c, "") != 'AUTOGEN' :
			print "Call Houston"	
#                buildString+=" "+c+"=int("+form.getfirst(c, "")+"),"
	   elif c == "DATA_ID" and form['DATA_ID_filename'].filename :
  		    fileitem = form['DATA_ID_filename']
         	    fn = objID+"__"+os.path.basename(fileitem.filename)
                    open('/data/pixels/uploads/'+objName+'/' + fn, 'wb').write(fileitem.file.read())
		    pfn='file:/data/pixels/uploads/'+objName+'/' + fn
 	            data = Data(PFNs=pfn)
	            insertedData = pdb.insertData(data)
 		    if (insertedData is None):
	                 print"<br>Error inserting data"
			 buildString+="DATA_ID=0"
		    else:
			 buildString+="DATA_ID=%s,"%insertedData.DATA_ID
	   elif c == "TRANSFER_ID" and (form.getfirst(c, "empty") == "empty" or form.getfirst(c, "empty") == "" ):
		print "Creating transfer"
	        t = pdb.insertTransfer(Transfer(SENDER=form.getfirst("TRANSFER_ID_sender"), RECEIVER=form.getfirst("TRANSFER_ID_receiver"), ISSUED_DATE=datetime.now(), RECEIVED_DATE=datetime.now(), STATUS="ARRIVED", COMMENT="autogen at creation"))
		pdb.store.commit()
		buildString+=" "+c+"=int(\"%s\")," % (t.TRANSFER_ID)
	   elif c == "SESSION_ID" :
		t = pdb.insertSession(Session(OPERATOR=form.getfirst("SESSION_OPERATOR"), CENTER=form.getfirst("SESSION_CENTER"), DATE=datetime.now(), TYPE=objName,  COMMENT=form.getfirst("SESSION_COMMENT")))
                pdb.store.commit()
                buildString+=" "+c+"=int(\"%s\")," % (t.SESSION_ID)
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
	print " <a href=/>back home</a>" 

#    s = Sensor()	

#    if (self.isSensorInserted(sensor.SENSOR_ID) == True):
#                 print "ERROR: sensor already inserted", sensor.SENSOR_ID
#                 return None
#           self.store.add(sensor)
#           self.store.commit()
            # log in history
#           self.insertHistory(type="NULL", id=0, target_type="SENSOR", target_id=sensor.SENSOR_ID, operation="INSERT", datee=date.today(), comment="NO COMMENT")
#           return sensor


else :
        printHeaders(setcookies)
	print "<table id=example cellspacing=10 >"
	print "<form enctype=\"multipart/form-data\" method=\"post\" action=newTest.cgi>"
	print "<input type=hidden name=objName value=\"%s\">" % objName
	print "<thead> <tr>"
	print "<th align=left> Field: </th>"
	print "<th align=left> Value: </th>"
	print "</thead></tr><tbody>"
        print "<tr><td>",ID.lower().capitalize()," (main ID)</td><td>"
	print inputField(objName,ID,setcookies)

	summary=""
        for c in columns:
          if c != ID : #or force:
                   print "<tr><td>",c.lower().capitalize(),"</td><td>"
		   defVal =  form.getfirst(c,'')
		   print inputField(objName,c,setcookies,defVal)
		   print "</td></tr>"
	   

	print "</tbody><tfoot></tfoot></table><br>"
	print "<input type=\"submit\" name=\"submit\" value=\"Insert\" /></form>"

