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
print '<link rel="stylesheet" type="text/css" href="/frames.css" />'
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
                //      alert("fail");
                }
                }

        }
        </script>
<body><main>
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
import Cookie

setcookies = Cookie.SimpleCookie()
if 'HTTP_COOKIE' in os.environ:
    cookie_string=os.environ.get('HTTP_COOKIE')
    setcookies.load(cookie_string)


def inputField(objName,column, defVal = "", o=None) :
	config = ConfigParser.ConfigParser()
	config.read('/var/www/cgi-bin/writers/editor.ini')
	#default input string:
	inputString = "<input type=input name=\"%s\" value=\"%s\">" % (column,cgi.escape("%s"%defVal, quote=True))
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
        elif column == "SESSION_ID" and defVal != "" and defVal != 0 and objName!="Session":
		inputString+=" (edit <a href=edit.cgi?objName=Session&SESSION_ID=%s  target=\"_blank\">this session</a> in new window)"%defVal
        elif column == "COMMENT":
                inputString = "<textarea id='%s' name=%s cols='80' rows='10'>%s</textarea>"%(column,column,defVal)
        elif column == "SIGNALS_AND_LVS" and o :
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
				selpass=""
				selfail=""
				val=o.getBit(tests[j],channels[i])
#				print val
				if val == 'FAIL' :	
					selfail='selected'
				if val == 'PASS' :	
					selpass='selected'
                                if lens[i]>j :
                                        inputString+= "<td><select class=sels onchange=update() name=%s><option value=NULL></option><option value=PASS %s>PASS</option><option value=FAIL %s>FAIL</option></select></td>" % ("SIGNALS_AND_LVS_"+channels[i]+"_"+tests[j],selpass,selfail)
                                else:
                                        inputString+= "<td bgcolor=#000000></td>"
                        inputString+= "</tr>"
                inputString+= "</table><p>"
                inputString+= "<button onClick=\"setAllPass();\" type=button> Set all to PASS</button> <button onClick=\"setAllEmpty();\" type=button>Reset all to empty</button>"

	elif column == "DATA_ID" :
	    if defVal != "" and defVal != 0 :
		inputString+=" |  add more files: "
	    inputString+="<input type=\"file\" name=\"DATA_ID_filename\" />"
	elif config.has_section(objName+"/"+column) :
 	    type = config.get(objName+"/"+column,"type")
            if type  == "textarea":
                inputString = "<textarea id='%s' name=%s cols='80' rows='10'>%s</textarea>"%(column,column,defVal)

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
    objID = form.getfirst(ID, '-1')
    objID = cgi.escape(objID)
    filterValue=int(objID)  
  else:
    ID=objName+"_ID"
    ID=ID.upper()
    if objName == "Transfer"  or objName == "Data" or objName == "Session":
      objID = form.getfirst(ID, '-1')
      objID = cgi.escape(objID)
      filterValue=int(objID)
    else :
      objID = form.getfirst(ID, 'empty')
      objID = cgi.escape(objID)
      filterValue=unicode(objID)  

  filter = eval(objName+"."+ID)

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
#       print "found"	
       o = objects[0]	
       aux = None	
if action == "Validate" :
   print "to be implemented"

columns.sort()
columns=onlyColumns(objName)

if action == "Insert" :
  if  aux or first :
     buildString=objName+"("
     buildDict={}	
     for c in columns:
#           columnType=type(eval("aux."+c))
           adate=date(2000,1,1)
           columnType2=type(eval(objName+"."+c+".variable_factory()"))
	   SIGNALS_AND_LVS=None
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
			 buildDict["DATA_ID"]=0
		    else:
			 buildString+="DATA_ID=%s,"%insertedData.DATA_ID
                         buildDict["DATA_ID"]=insertedData.DATA_ID
	   elif c == "TRANSFER_ID" and (form.getfirst(c, "empty") == "empty" or form.getfirst(c, "empty") == "" ):
		print "Creating transfer"
	        t = pdb.insertTransfer(Transfer(SENDER=form.getfirst("TRANSFER_ID_sender"), RECEIVER=form.getfirst("TRANSFER_ID_receiver"), ISSUED_DATE=datetime.now(), RECEIVED_DATE=datetime.now(), STATUS="ARRIVED", COMMENT="autogen at creation"))
		pdb.store.commit()
		buildString+=" "+c+"=int(\"%s\")," % (t.TRANSFER_ID)
                buildDict[c]=int(t.TRANSFER_ID)
           elif columnType2 == DateVariable :
                d=form.getfirst(c, "")
		try: 
		        dd=datetime.strptime(d,"%Y-%m-%d")
		except:
			print "Cannot parse the date, using today, was (#%s#)"%d
                        dd=date.today()
		buildString+=" "+c+"=dd,"
                buildDict[c]=dd
           elif columnType2 == DateTimeVariable :
                d=form.getfirst(c, "")
                try:
                        dd=datetime.strptime(d,"%Y-%m-%d")
                except :
			print "using date and time<br>"
			try : 
			 	dd=datetime.strptime(d,"%Y-%m-%d %H:%M:%S")
		        except:
				print "Cannot parse the datetime, using today, was (#%s#)"%d
				dd=datetime.now()
                buildString+=" "+c+"=dd,"
                buildDict[c]=dd
           elif columnType2 == UnicodeVariable : 
		buildString+=" "+c+"=\""+form.getfirst(c, "")+"\","
                buildDict[c]=form.getfirst(c, "")
	   elif columnType2 == IntVariable :
		if form.getfirst(c, "") != "" :
                        buildDict[c]=int(form.getfirst(c, "0"))
		else:
			buildDict[c]=int()
		buildString+=" "+c+"=int("+form.getfirst(c, "")+"),"
	   elif columnType2 == FloatVariable :
                if form.getfirst(c, "") != "" :
                        buildDict[c]=float(form.getfirst(c, ""))
		else:
                        buildDict[c]=float()
		buildString+=" "+c+"=float("+form.getfirst(c, "")+"),"
	   else :
		buildString+=" "+c+"=\""+form.getfirst(c, "")+"\","
		buildDict[c]=form.getfirst(c, "")
	
     buildString+=")"
     o=objType(**buildDict)
#     print buildString
#     o=eval(buildString)
#     print buildString	 
#     print eval("o."+ID),objName+"."+ID

     if pdb.store.find(objType,filter==getattr(o,ID)).count() > 0 :
	print "This object ALREADY exists: CANNOT INSERT"	
     else:
	try:
	   print "<br>"
	   ret= eval("pdb.insert%s(o)"%objName)
	except:
	    print "Cannot use Insert function, inserting with no checks"
	    pdb.store.add(o)
	    pdb.store.commit()
 	    pdb.insertHistory(type=0,id=0, target_id=getattr(o,ID), target_type=objName, operation="INSERT", datee=datetime.now(), comment="")
	    ret=o	
	if ret is not None:
	        print "<br>"
		print " Objected added"
	else :
  		print "<br>"
		print "<h3> Cannot INSERT! Please fix the errors and try again</h3>"

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


if action == "Save changes" or  action == "Save and Close":
   for c in columns:
	   field =  getattr(o,c)
	   list = form.getlist(c)
	   if len(list) > 0 :
		field = list[-1] 
	   columnType=type(eval("o."+c))
           columnType2=type(eval(objName+"."+c+".variable_factory()"))
#	   print c, field, columnType, columnType2
	   adate=date(2000,1,1)
           if c == "DATA_ID" and form['DATA_ID_filename'].filename :
                    fileitem = form['DATA_ID_filename']
                    fn = objID+"__"+os.path.basename(fileitem.filename)
                    open('/data/pixels/uploads/'+objName+'/' + fn, 'wb').write(fileitem.file.read())
                    pfn='file:/data/pixels/uploads/'+objName+'/' + fn
		    if field == '0' :
	                   data = Data(PFNs=pfn)
        	           insertedData = pdb.insertData(data)
	                   if (insertedData is None):
        	                print"<br>Error inserting data"
                        	o.DATA_ID=0
	                   else:
				print insertedData.DATA_ID
                	        setattr(o,c,insertedData.DATA_ID)
		    else :
			   d=pdb.getData(int(field))
			   d.PFNs+=","+pfn
	   elif columnType == type(adate) or columnType2 == DateVariable:
		if field == "None":
			field = "1970-01-01" 
   	        d=field #form.getfirst(c, getattr(o,c))
	        dd=datetime.strptime(d,"%Y-%m-%d")
		setattr(o,c,dd)
	   elif columnType2 ==  DateTimeVariable :
                if field == "None":
                        field = "1970-01-01 00:00:00"   
                d=field #form.getfirst(c, getattr(o,c))
           	try:
		     dd=datetime.strptime(d,"%Y-%m-%d %H:%M:%S")
               	     setattr(o,c,dd)
		except :
		     print "Cannot parse date %s<br>"%d
	   elif c == "SIGNALS_AND_LVS" :
		salstr =  form.getfirst("SIGNALS_AND_LVS","")	
		print salstr
		if salstr != "" :
			print "USING PASSED STRING INSTEAD OF TABLE", salstr
			o.SIGNALS_AND_LVS=salstr
		else :
                   for f in form :
                        m=re.match('SIGNALS_AND_LVS_(.*)_(.*)',f)
                        if m :
                                o.setBit(m.group(2),m.group(1),form[f].value)
           elif columnType2 == IntVariable :
		if form.getfirst(c, "0") == 'None' :
			 setattr(o,c,0)
		else:
	                 setattr(o,c,int(form.getfirst(c, "0")))
           elif columnType2 == FloatVariable :
		if form.getfirst(c, "0") == 'None' :
                         setattr(o,c,0)
                else: 
	                 setattr(o,c,float(form.getfirst(c, "0")))
	   elif columnType == type(None) :
#		setattr(o,c,unicode(form.getfirst(c, getattr(o,c))))
		setattr(o,c,unicode(field))
	   else: 
#		setattr(o,c,columnType(form.getfirst(c, getattr(o,c))))
		setattr(o,c,columnType(field))
   pdb.store.commit()
   pdb.insertHistory(type=0,id=0, target_id=getattr(o,ID), target_type=objName, operation="WEBEDIT", datee=datetime.now(), comment=" from %s "%(os.environ["REMOTE_ADDR"]))

   print "<b>Saved!!!!!!</b>"

if action != "Save and Close" :
        print "<H1>Editing %s %s </H1>" %(objName,objID)
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
                print inputField(objName,ID,getattr(o,ID),o)
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
		   print inputField(objName,c,getattr(o,c),o)
	   else :
                   print "<tr><td>",c.lower().capitalize(),"</td><td>"
#<input type=input name=\"%s\" value=\"%s\">"%(c,"")
		   print inputField(objName,c)

	   print "</td></tr>"
	   

	print "</tbody><tfoot></tfoot></table><br>"
#	print "<input type=\"submit\" name=\"submit\" value=\"Validate\" />"
	if o : 
 		print "<input type=\"submit\" name=\"submit\" value=\"Save changes\" />"
 		print "<input type=\"submit\" name=\"submit\" value=\"Save and Close\" /></form>"
#	print "<br><br><a href=/> Back to DB home page</a>"
	else :
 		print "<input type=\"submit\" name=\"submit\" value=\"Insert\" /></form>"
print "<br> <a href=/>back home</a> | <a href=%s>back to last list view </a>" % (setcookies["lastview"].value if "lastview" in setcookies else "")
printFooter()
