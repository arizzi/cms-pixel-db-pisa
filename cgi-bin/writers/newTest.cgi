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
	 <link rel="stylesheet" href="//code.jquery.com/ui/1.11.2/themes/smoothness/jquery-ui.css">
	 <script src="//code.jquery.com/jquery-1.10.2.js"></script>
	 <script src="//code.jquery.com/ui/1.11.2/jquery-ui.js"></script>
	 <link rel="stylesheet" href="/resources/demos/style.css">
	 <script>
	 $(function() {
	    $( "#datepicker" ).datepicker({ dateFormat: "dd/mm/yy" });
	  });
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
			document.getElementById("RESULT").value="BAD";
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
	inputString = "<input size=40 id=%s type=input name=\"%s\" value=\"%s\">" % (column,column,defVal)
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
	elif column == "SIGNALS_AND_LVS" :
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
					inputString+= "<td><select class=sels onchange=update() name=%s><option value=NULL></option><option value=PASS>PASS</option><option value=FAIL>FAIL</option></select></td>" % ("SIGNALS_AND_LVS_"+channels[i]+"_"+tests[j])
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
			inputString=" Operator: <input type=input  name=\"SESSION_OPERATOR\" value=\"%s\"/>" % cookies["operator"].value
		else :
			inputString=" Operator: <input type=input  name=\"SESSION_OPERATOR\" />" 

		if "operator" in cookies :
			inputString+=" Center: <input type=input  name=\"SESSION_CENTER\" value=\"%s\"/>" % cookies["center"].value
		else:
			inputString+=" Center: <input type=input  name=\"SESSION_CENTER\" />" 
		inputString+=" Comment: <input type=input  name=\"SESSION_COMMENT\"/>" 
		inputString+=" Date: <input type=text id=\"datepicker\"  name=\"SESSION_DATE\" value=today />" 
	elif config.has_section(objName+"/"+column) :
 	    type = config.get(objName+"/"+column,"type")
 	    if defVal == "" and config.has_option(objName+"/"+column,"default"):
		    defVal = config.get(objName+"/"+column,"default")
	            inputString = "<input id=%s type=input name=\"%s\" value=\"%s\">" % (column,column,defVal)
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

if objName == "empty" or not re.match('Test',objName) :
    printHeaders(setcookies)
    exit()

if objName != "" :
  columns = onlyColumns(objName)
  objName = parseObjName(cgi.escape(objName))
  objType = eval(objName)
  ID=idField(objName)
  m=re.match("Test_([A-Za-z]+)(_*.*)",objName)
  insertFunction = getattr(pdb,"insert%sTest%s"%(m.group(1),m.group(2)))

if action == "Insert" :
     setcookies["center"]=form.getfirst("SESSION_CENTER","")
     setcookies["operator"]=form.getfirst("SESSION_OPERATOR","")
     printHeaders(setcookies)
     buildDict={}
     SIGNALS_AND_LVS = None
     for c in columns:
           adate=date(2000,1,1)
           columnType2=type(eval(objName+"."+c+".variable_factory()"))
	   objID="%s"%time.time()	
	   if c == ID :
		 if form.getfirst(c, "") != 'AUTOGEN' :
			print "Call Houston"	
	   elif c == "DATA_ID" and form['DATA_ID_filename'].filename :
  		    fileitem = form['DATA_ID_filename']
         	    fn = objID+"__"+os.path.basename(fileitem.filename)
                    open('/data/pixels/uploads/'+objName+'/' + fn, 'wb').write(fileitem.file.read())
		    pfn='file:/data/pixels/uploads/'+objName+'/' + fn
 	            data = Data(PFNs=pfn)
	            insertedData = pdb.insertData(data)
 		    if (insertedData is None):
	                 print"<br>Error inserting data"
			 buildDict["DATA_ID"]=0
		    else:
			 buildDict["DATA_ID"]=insertedData.DATA_ID
	   elif c == "SIGNALS_AND_LVS" :
		SIGNALS_AND_LVS={}
		for f in form :
			m=re.match('SIGNALS_AND_LVS_(.*)_(.*)',f) 
			if m :
#				print m.group(1),m.group(2)
				if not m.group(1) in SIGNALS_AND_LVS :
					SIGNALS_AND_LVS[m.group(1)]={}
				SIGNALS_AND_LVS[m.group(1)][m.group(2)]=form[f]
#		print  form,form.getlist("SIGNALS_AND_LVS[]")
	   elif c == "TRANSFER_ID" and (form.getfirst(c, "empty") == "empty" or form.getfirst(c, "empty") == "" ):
		print "Creating transfer"
	        t = pdb.insertTransfer(Transfer(SENDER=form.getfirst("TRANSFER_ID_sender"), RECEIVER=form.getfirst("TRANSFER_ID_receiver"), ISSUED_DATE=datetime.now(), RECEIVED_DATE=datetime.now(), STATUS="ARRIVED", COMMENT="autogen at creation"))
		pdb.store.commit()
		buildDict[c]=int(t.TRANSFER_ID)
	   elif c == "SESSION_ID" :
		dd=datetime.now()
		if form.getfirst("SESSION_DATE") and form.getfirst("SESSION_DATE") != "today" :
			dd=datetime.strptime(form.getfirst("SESSION_DATE"),"%d/%m/%Y")
		t = pdb.insertSession(Session(OPERATOR=form.getfirst("SESSION_OPERATOR"), CENTER=form.getfirst("SESSION_CENTER"), DATE=dd, TYPE=objName,  COMMENT=form.getfirst("SESSION_COMMENT")))
                pdb.store.commit()
		buildDict[c]=int(t.SESSION_ID)
           elif columnType2 == DateVariable :
                d=form.getfirst(c, "")
		try: 
		        dd=datetime.strptime(d,"%Y-%m-%d")
		except:
                        dd=date.today()
		buildDict[c]=dd
           elif columnType2 == DateTimeVariable :
                d=form.getfirst(c, "")
                try:
                        dd=datetime.strptime(d,"%Y-%m-%d")
                except:
			dd=datetime.now()
		buildDict[c]=dd
           elif columnType2 == UnicodeVariable : 
		buildDict[c]=form.getfirst(c, "")
	   elif columnType2 == IntVariable :
                if form.getfirst(c, "") != "" :
			buildDict[c]=int(form.getfirst(c, "0"))
		else:
	                buildDict[c]=int()

	   elif columnType2 == FloatVariable :
		if form.getfirst(c, "") != "" :
	                buildDict[c]=float(form.getfirst(c, ""))
		else :	
			buildDict[c]=float()
	   else :
		buildDict[c]=form.getfirst(c, "")

#    print "DICT: ",buildDict
     o=objType(**buildDict)
     if SIGNALS_AND_LVS  :
		channels = SIGNALS_AND_LVS
		for ch in channels :
			for t in channels[ch] :
				o.setBit(t,ch,channels[ch][t].value)	
#     print eval("o."+ID),objName+"."+ID

     if pdb.store.find(objType,filter==eval("o."+ID)).count() > 0 :
	print "This object ALREADY exists: CANNOT INSERT"	
#	pdb.insertHistory(type=0,id=0, target_id=eval("o."+ID), target_type=objName, operation="INSERT", datee=datetime.now(), comment="")
     else:
	insertFunction(o)
	print " Objected added"
	print " <a href=/>back home</a> | <a href=%s>back to last list view </a>" % (setcookies["lastview"].value if "lastview" in setcookies else "")



else :
        printHeaders(setcookies)
        print "<H1>Inserting %s </H1>" %(objName)	
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

