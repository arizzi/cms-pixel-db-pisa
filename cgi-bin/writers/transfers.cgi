#!/usr/bin/env python

# enable debugging
import sys
sys.path.append("../../PixelDB")
sys.path.append("..")
import cgitb
from datetime import *
cgitb.enable()
import re
import cgi
from pixelwebui import *

print "Content-Type: text/html"
print
print "<html>\n        <head>\n         "
print '''
                <style type="text/css" title="currentStyle">
                        @import "../../media/css/demo_page.css";
                        @import "../../media/css/jquery.dataTables.css";
                </style>
                <script type="text/javascript" language="javascript" src="../../media/js/jquery.js"></script>
                <script type="text/javascript" language="javascript" src="../../media/js/jquery.dataTables.js"></script>
		<script type="text/javascript" src="../../media/js/jquery-barcode.js"></script>  

                <script type="text/javascript" charset="utf-8">
                        $(document).ready(function() {

                                $('#transfers').dataTable( {
                                        "sDom": 'C<"clear">lfrtip',
                                        "iDisplayLength" : 50,
                                        } );
                                } );

function verify(a)
{
var s=prompt("Please scan the barcode of the transfer\\n"+a,"");
if(s!=a) alert("Wrong barcode!!");
return (s==a);
}
                        </script>

'''

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

#transferObjects=['FullModule','BareModule','Sensor','Roc','Hdi','Tbm','Wafer','Batch']
#centers=['CIS','FACTORY','ETH','PSI','CERN','BARI','CATANIA','PERUGIA','PISA','HAMBURG','AACHEN','HELSINKI','DESY','KIT']


pdb = PixelDBInterface(operator="webfrontend",center="cern")
pdb.connectToDB()

def checkCenter(objName,id,sender) :
    value=idFieldTypedValue(objName,id)
    ID=idField(objName)
    filter=eval(objName+"."+ID)
    objType = eval(objName)
    o=pdb.store.find(objType,filter==value).one()
    if o :
      if o.TRANSFER_ID!=0 and o.transfer and (o.transfer.RECEIVER.lower() != sender.lower() or o.transfer.STATUS == "SENT") and sender != "any" :
         return False
      else :
	 return True
    return False

def getChildren(objName,ids,sender) :
   objects = []
   notAtRightcenter = []
   objName  = parseObjName(form.getfirst('type', 'empty'))
   if objName == "Batch" :
        for id in ids:
		value=idFieldTypedValue(objName,id)
		if not checkCenter(objName,id,sender) :
                       	notAtRightcenter.append((objName,id))
		else :
		        objects.append((objName,id))
                wafers = pdb.store.find(Wafer,Wafer.BATCH_ID==value)
                for w in wafers :
	             if not  checkCenter("Wafer",w.WAFER_ID,sender) :
	                   notAtRightcenter.append(("Wafer",w.WAFER_ID))
        	     else :
                           objects.append(("Wafer",w.WAFER_ID))
                     sensors = pdb.store.find(Sensor,Sensor.WAFER_ID==w.WAFER_ID)         
                     for s in sensors :
	                  if not checkCenter("Sensor",s.SENSOR_ID,sender) :
		                  notAtRightcenter.append(("Sensor",s.SENSOR_ID))
                          else :
             	                  objects.append(("Sensor",s.SENSOR_ID))
   elif objName == "Wafer" :
        for id in ids:
                value=idFieldTypedValue(objName,id)
		if not checkCenter("Wafer",value,sender) :
			notAtRightcenter.append(("Wafer",value))
                else :
			objects.append(("Wafer",value))
                sensors = pdb.store.find(Sensor,Sensor.WAFER_ID==value)
                for s in sensors :
                  if not checkCenter("Sensor",s.SENSOR_ID,sender) :
                       notAtRightcenter.append(("Sensor",s.SENSOR_ID))
                  else :
                       objects.append(("Sensor",s.SENSOR_ID))
   elif objName == "RocWafer" :
        for id in ids:
                value=idFieldTypedValue(objName,id)
                if not checkCenter("RocWafer",value,sender) :
                        notAtRightcenter.append(("RocWafer",value))
                else :
                        objects.append(("RocWafer",value))
                rocs = pdb.store.find(Roc,Roc.WAFER_ID==value)
                for s in rocs :
                  if not checkCenter("Roc",s.ROC_ID,sender) :
                       notAtRightcenter.append(("Roc",s.ROC_ID))
                  else :
                       objects.append(("Roc",s.ROC_ID))

   else:
	print "Transfer with children not yet implemented for this type. please use normal transfer"
   return (objects,notAtRightcenter)


def getTransferList(objName,ids,sender,children) :
   objects = []
   notAtRightcenter = []
   objName  = parseObjName(form.getfirst('type', 'empty'))
   if children :
	return getChildren(objName,ids,sender)
   else :
	objects = []
	notAtRightcenter = []
        for id in ids:
	     if id != "" :	
                value=idFieldTypedValue(objName,id)
                if not checkCenter(objName,id,sender) :
                        notAtRightcenter.append((objName,id))
                else :
                        objects.append((objName,id))
	return (objects,notAtRightcenter)



form = cgi.FieldStorage() # instantiate only once!
action = form.getfirst('submit', 'empty')
action = cgi.escape(action)
children=False
if action == "Transfer with children":
    children = True

if action == "Transfer with children" or action == "Transfer" :
    objName  = parseObjName(form.getfirst('type', 'empty'))
    idsString  = form.getfirst('ids', '')
    sender = form.getfirst('sender', 'empty')
    receiver = form.getfirst('receiver', 'empty')
    comment  = form.getfirst('comment', '')
    ids=re.split("\s",idsString)
    center=sender #"any"
    (objs,errors) = getTransferList(objName,ids,center,children)
    if len(errors) > 0 :
	   print "Not Found at Center %s:<br><table border=1><tr><td>Type</td><td>Id</td></tr>" % center
	   for i in errors : 
		print "<tr><td>%s</td><td>%s</td></tr>" % (i[0],i[1])		
	   print "</table>"
    if len(objs) > 0 :
	    print "You are going to transfer:<br><table border=1><tr><td>Type</td><td>Id</td></tr>"
	    print "<form>"
	    for i in objs : 
		print "<tr><td>%s</td><td>%s</td></tr>" % (i[0],i[1])		
		print "<input type=\"hidden\" name=\"object[]\" value=\"%s,%s\" >" % (i[0],i[1])		
	    print "</table>"
	    print "<input type=\"hidden\" name=\"sender\" value=\"%s\" >" % sender
	    print "<input type=\"hidden\" name=\"receiver\" value=\"%s\" >" % receiver
	    print "<input type=\"hidden\" name=\"comment\" value=\"%s\" >" % comment
            print "<p><input type=\"submit\" name=\"submit\" value=\"Confirm this transfer\" /></p></form>"

    else:
	    print "None of the specified objects have been found at center %s!!" % (center)
 

if action == "Confirm this transfer" :
  sender = form.getfirst('sender', 'empty')
  receiver = form.getfirst('receiver', 'empty')
  comment  = form.getfirst('comment', '')
  nonempty=False
  objects = form.getlist('object[]')
  for ob in objects :
      (objName,id) = re.split(",",ob)
      if checkCenter(objName,id,sender):
	 nonempty=True
	 break
  if nonempty  :
   t = pdb.insertTransfer(Transfer(SENDER=sender, RECEIVER=receiver, ISSUED_DATE=datetime.now(), RECEIVED_DATE=datetime(1970,1,1), STATUS="SENT", COMMENT=comment))
   print "<p>Inserted transfer %s, received date %s, issued date %s<p>" % (t.TRANSFER_ID, t.RECEIVED_DATE, t.ISSUED_DATE)
#  tt=pdb.store.find(Transfer,Transfer.TRANSFER_ID==t.TRANSFER_ID).one()
#  print "<p>Inserted transfer %s, received date %s, issued date %s<p>" % (tt.TRANSFER_ID, tt.RECEIVED_DATE, tt.ISSUED_DATE)
   pdb.store.commit()
#  (objs,errors) = getTransferList(objName,ids,center,children)
#   if len(errors) > 0 :

   for ob in objects :
        (objName,id) = re.split(",",ob)
	print "<p>Inserting", objName,id,"<br>"
        objType = eval(objName)
	ID=idField(objName)
        filter=eval(objName+"."+ID)
        value=idFieldTypedValue(objName,id)
        o=pdb.store.find(objType,filter==value).one()
        if o :
           print "OLD Transfer ID", o.TRANSFER_ID
	   pdb.insertHistory("TRANSFER", t.TRANSFER_ID , objName, id, "SEND", datee=datetime.now(), comment="OLDTRANS=%s"%o.TRANSFER_ID)
           o.TRANSFER_ID=t.TRANSFER_ID
           pdb.store.commit()
        else :
           print "<p><b>cannot find %s with %s = %s</b>" %(objName,ID,id)
   print "<a href=transfers.cgi?submit=details&TRANSFER_ID=%s>Details and transfer sheet</a><br>" % t.TRANSFER_ID
  else :
	   print "wrong center or empty transfer, did you hit reload or back button on your browser?<br>"
     
#$("#barcodeTarget").html("").show().barcode(
#   print'''<div  id="bcTarget" style="height: 50px; width: 250px"></div><button onclick='$("#bcTarget").barcode("123","ean13",{barWidth:2, barHeight:30});'>Barcode</button>'''
  print "<a href=transfers.cgi>Back to list of transfers</a>"



if action == "receive" :
   #mark transfer as received
   #TODO: check receiver center
   transfer = pdb.store.find(Transfer,Transfer.TRANSFER_ID==int(form.getfirst('TRANSFER_ID', 'empty'))).one()
   pdb.insertHistory("TRANSFER", transfer.TRANSFER_ID ,"" , 0 , "RECEIVE", datee=datetime.now(), comment="")
   transfer.STATUS=unicode("ARRIVED")
   transfer.RECEIVED_DATE=datetime.now()
   #TODO: insert in history
   print "RECEIVED!"
   pdb.store.commit()
   action="empty"

if action == "cancel" :
   #mark transfer as received
   #TODO: check receiver center
   transfer = pdb.store.find(Transfer,Transfer.TRANSFER_ID==int(form.getfirst('TRANSFER_ID', 'empty'))).one()
   pdb.insertHistory("TRANSFER", transfer.TRANSFER_ID ,"" , 0 , "CANCEL", datee=datetime.now(), comment="")
   transfer.STATUS=unicode("ARRIVED")
   transfer.RECEIVER=transfer.SENDER
   transfer.RECEIVED_DATE=datetime.now()
   #TODO: insert in history
   print "CANCELLED (receiver set back to sender)"
   pdb.store.commit()
   action="empty"

if action == "details" :
   tid=int(form.getfirst('TRANSFER_ID', 'empty'))
   t = pdb.store.find(Transfer,Transfer.TRANSFER_ID==int(form.getfirst('TRANSFER_ID', 'empty'))).one()

   print "<h1>Transfer ID %s (%s => %s)</h1>"%(tid,t.SENDER,t.RECEIVER)
   print "Created on date: <b>%s</b> <br>" % (t.ISSUED_DATE)
   print "Notes: %s <br>" % (t.COMMENT)
   print "<h2>Content of the transfer</h2>"
   for objName in transferObjects :
        objType = eval(objName)
	objs = pdb.store.find(objType,objType.TRANSFER_ID==int(form.getfirst('TRANSFER_ID', 'empty')))
	first = True
	for o in objs :
		if first:
		       print "<h3>The following %s(s)</h2>"%(objName)
		       first = False
		print getattr(o,idField(objName)),"<BR>"
   print "<br><br>"
   print "<h2>Barcode for fast reception: (to be implemented)</h2>"
   print "<a href=transfers.cgi>Back to list of transfers</a>"
   		
if action == "empty" :
   print "<h1> Pixel upgrade Transfer Interface</h1>" 
   print "<img src=/Truck.png width=200><br>"
   print "<a href=transfers.cgi?submit=newTransferForm> <button>Add NEW transfer</button> </a>"
   print "<h2> List of active transfers </h2><p>"

   #show list of open transfers
   transfers = pdb.store.find(Transfer,Transfer.STATUS!=unicode("ARRIVED"))
   print "<table id=transfers width=\"100%\">"
   print " <thead> <tr>"
   print "<th>Sender</th><th>Receiver</th><th>Comment</th><th>Status</th><th>Date sent</th><th>Actions</th>"
   print "</thead></tr><tbody>"
   for o in transfers :
     print "<tr>"
     print "<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td><a href=transfers.cgi?submit=receive&TRANSFER_ID=%s onClick=\"return verify(%s);\" >receive</a> | <a href=transfers.cgi?submit=cancel&TRANSFER_ID=%s onClick=\"return verify(%s);\" >cancel</a> |  <a href=transfers.cgi?submit=details&TRANSFER_ID=%s >details</a> " %(o.SENDER,o.RECEIVER,o.COMMENT,o.STATUS,o.ISSUED_DATE, o.TRANSFER_ID,o.TRANSFER_ID,o.TRANSFER_ID,o.TRANSFER_ID,o.TRANSFER_ID)
   print "</tbody><tfoot></tfoot>"

   if False:
    print "<h2> List of received transfers </h2><p>"
    transfers = pdb.store.find(Transfer,Transfer.STATUS==unicode("ARRIVED"))
    print "<table id=transfers2 width=\"100%\">"
    print " <thead> <tr>"
    print "<th>Sender</th><th>Receiver</th><th>Comment</th><th>Status</th><th>Date sent</th>"
    print "</thead></tr><tbody>"
    for o in transfers :
      print "<tr>"
      print "<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>" %(o.SENDER,o.RECEIVER,o.COMMENT,o.STATUS,o.ISSUED_DATE )
    print "</tbody><tfoot></tfoot>"
  
 
if action == "newTransferForm" :
   #show form for new transfers
   print '''<html>
<body>
   <form >
'''
   print "<p>Sender:   <select name=sender>"
   for o in centers+["any"] :
        print "<option>%s</option>" % o
   print" </select><p>"
   print "<p>Receiver:   <select name=receiver>"
   for o in centers :
        print "<option>%s</option>" % o
   print" </select><p>"

   print '''
   <p>Comment:   <input type="text" name="comment" />
   <p> Type of transferred objects:<select name=type>
'''
   for o in transferObjects :
     print "<option>%s</option>" % o
   print '''   </select><p>
   List of IDs (space or new line separated):<p> 
<textarea rows="4" cols="50" name=ids>
</textarea>

   <p>
   <p><input type="submit" name="submit" value="Transfer" /> 
   <input type="submit" name="submit" value="Transfer with children" /></p>

   </form>
</body>
</html> 
'''
