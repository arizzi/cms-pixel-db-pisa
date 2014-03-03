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
var s=prompt("Please scan the barcode of the transfer","");
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


pdb = PixelDBInterface(operator="webfrontend",center="cern")
pdb.connectToDB()

form = cgi.FieldStorage() # instantiate only once!
action = form.getfirst('submit', 'empty')
action = cgi.escape(action)
if action == "Transfer with children" :
   objName  = parseObjName(form.getfirst('type', 'empty'))
   if objName == "Batch" :
        sender = form.getfirst('sender', 'empty')
        receiver = form.getfirst('receiver', 'empty')
        comment  = form.getfirst('comment', '')
        t = pdb.insertTransfer(Transfer(SENDER=sender, RECEIVER=receiver, ISSUED_DATE=datetime.now(), RECEIVED_DATE=datetime(1970,1,1), STATUS="NEW", COMMENT=comment))
        print "<p>Inserted transfer %s, received date %s, issued date %s<p>" % (t.TRANSFER_ID, t.RECEIVED_DATE, t.ISSUED_DATE)
        tt=pdb.store.find(Transfer,Transfer.TRANSFER_ID==t.TRANSFER_ID).one()
        print "<p>Inserted transfer %s, received date %s, issued date %s<p>" % (tt.TRANSFER_ID, tt.RECEIVED_DATE, tt.ISSUED_DATE)
        pdb.store.commit()
        idsString  = form.getfirst('ids', '')
        objName  = parseObjName(form.getfirst('type', 'empty'))
        objType = eval(objName)
        ID=idField(objName)
        filter=eval(objName+"."+ID)
        ids=re.split("\s",idsString)
        for id in ids:
                value=idFieldTypedValue(objName,id)
                o=pdb.store.find(objType,filter==value).one()
                if o :
                        print "OLD ID", o.TRANSFER_ID
                        o.TRANSFER_ID=t.TRANSFER_ID
                        print "Children Wafers:"
		        wafers = pdb.store.find(Wafer,Wafer.BATCH_ID==value)
			for w in wafers :
                  	      	sensors = pdb.store.find(Sensor,Sensor.WAFER_ID==w.WAFER_ID)         
                               	print "- OLD ID", w.TRANSFER_ID
                               	w.TRANSFER_ID=t.TRANSFER_ID
                        	for s in sensors :
                                	print "+ OLD ID", s.TRANSFER_ID
                                	s.TRANSFER_ID=t.TRANSFER_ID
                        pdb.store.commit()
                else :
                        print "<p><b>cannot find %s with %s = %s</b>" %(objName,ID,id)

#$("#barcodeTarget").html("").show().barcode(
        print'''<div  id="bcTarget" style="height: 50px; width: 250px"></div><button onclick='$("#bcTarget").barcode("123","ean13",{barWidth:2, barHeight:30});'>Barcode</button>'''
        print "<a href=transfers.cgi>Back to list of transfers</a>"
   elif objName == "Wafer" :
        sender = form.getfirst('sender', 'empty')
   	receiver = form.getfirst('receiver', 'empty')
   	comment  = form.getfirst('comment', '')
   	t = pdb.insertTransfer(Transfer(SENDER=sender, RECEIVER=receiver, ISSUED_DATE=datetime.now(), RECEIVED_DATE=datetime(1970,1,1), STATUS="NEW", COMMENT=comment))
   	print "<p>Inserted transfer %s, received date %s, issued date %s<p>" % (t.TRANSFER_ID, t.RECEIVED_DATE, t.ISSUED_DATE)
   	tt=pdb.store.find(Transfer,Transfer.TRANSFER_ID==t.TRANSFER_ID).one()
   	print "<p>Inserted transfer %s, received date %s, issued date %s<p>" % (tt.TRANSFER_ID, tt.RECEIVED_DATE, tt.ISSUED_DATE)
   	pdb.store.commit()
   	idsString  = form.getfirst('ids', '')
   	objName  = parseObjName(form.getfirst('type', 'empty'))
   	objType = eval(objName)
   	ID=idField(objName)
   	filter=eval(objName+"."+ID)
   	ids=re.split("\s",idsString)
   	for id in ids:
        	value=idFieldTypedValue(objName,id)
        	o=pdb.store.find(objType,filter==value).one()
        	if o :
           		print "OLD ID", o.TRANSFER_ID
           		o.TRANSFER_ID=t.TRANSFER_ID
	   		print "Children Sensors:"
	   		sensors = pdb.store.find(Sensor,Sensor.WAFER_ID==value)		
	   		for s in sensors :
		 		print "- OLD ID", s.TRANSFER_ID
           	 		s.TRANSFER_ID=t.TRANSFER_ID
           		pdb.store.commit()
        	else :
           		print "<p><b>cannot find %s with %s = %s</b>" %(objName,ID,id)

#$("#barcodeTarget").html("").show().barcode(
   	print'''<div  id="bcTarget" style="height: 50px; width: 250px"></div><button onclick='$("#bcTarget").barcode("123","ean13",{barWidth:2, barHeight:30});'>Barcode</button>'''
   	print "<a href=transfers.cgi>Back to list of transfers</a>"
   else:
     print "Transfer with Children not available for ",objName," making simple transfer"
 	
if action == "Transfer" :
#   print "<pre>%s</pre>", form
   #insert new transfer
   sender = form.getfirst('sender', 'empty')
   receiver = form.getfirst('receiver', 'empty')
   comment  = form.getfirst('comment', '')
   t = pdb.insertTransfer(Transfer(SENDER=sender, RECEIVER=receiver, ISSUED_DATE=datetime.now(), RECEIVED_DATE=datetime(1970,1,1), STATUS="NEW", COMMENT=comment))
   print "<p>Inserted transfer %s, received date %s, issued date %s<p>" % (t.TRANSFER_ID, t.RECEIVED_DATE, t.ISSUED_DATE)
   tt=pdb.store.find(Transfer,Transfer.TRANSFER_ID==t.TRANSFER_ID).one()
   print "<p>Inserted transfer %s, received date %s, issued date %s<p>" % (tt.TRANSFER_ID, tt.RECEIVED_DATE, tt.ISSUED_DATE)
   pdb.store.commit()
   idsString  = form.getfirst('ids', '')
   objName  = parseObjName(form.getfirst('type', 'empty'))
   objType = eval(objName)
   ID=idField(objName)
   filter=eval(objName+"."+ID)
 
   ids=re.split("\s",idsString)
   for id in ids:
        value=idFieldTypedValue(objName,id)
	o=pdb.store.find(objType,filter==value).one()
        if o :
	   print "OLD ID", o.TRANSFER_ID
  	   o.TRANSFER_ID=t.TRANSFER_ID
	   pdb.store.commit()
        else :
	   print "<p><b>cannot find %s with %s = %s</b>" %(objName,ID,id)

#$("#barcodeTarget").html("").show().barcode(
   print'''<div  id="bcTarget" style="height: 50px; width: 250px"></div><button onclick='$("#bcTarget").barcode("123","ean13",{barWidth:2, barHeight:30});'>Barcode</button>'''
   print "<a href=transfers.cgi>Back to list of transfers</a>"


if action == "receive" :
   #mark transfer as received
   #TODO: check receiver center
   transfer = pdb.store.find(Transfer,Transfer.TRANSFER_ID==int(form.getfirst('TRANSFER_ID', 'empty'))).one()
   transfer.STATUS=unicode("ARRIVED")
   transfer.RECEIVED_DATE=datetime.now()
   #TODO: insert in history
   print "RECEIVED!"
   pdb.store.commit()
   action="empty"

if action == "empty" :
   print "<h2> Actions </h2><p>"
   print "<a href=transfers.cgi?submit=newTransferForm> <button>Add new transfer</button> </a>"
   print "<h2> Active transfers </h2><p>"

   #show list of open transfers
   transfers = pdb.store.find(Transfer,Transfer.STATUS!=unicode("ARRIVED"))
   print "<table id=transfers width=\"100%\">"
   print " <thead> <tr>"
   print "<th>Sender</th><th>Receiver</th><th>Comment</th><th>Status</th><th>Date sent</th><th>Actions</th>"
   print "</thead></tr><tbody>"
   for o in transfers :
     print "<tr>"
     print "<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td><a href=transfers.cgi?submit=receive&TRANSFER_ID=%s onClick=\"return verify(%s);\" >receive</a>" %(o.SENDER,o.RECEIVER,o.COMMENT,o.STATUS,o.ISSUED_DATE, o.TRANSFER_ID,o.TRANSFER_ID)
   print "</tbody><tfoot></tfoot>"

   
if action == "newTransferForm" :
   #show form for new transfers
   print '''<html>
<body>
   <form >
   <p>Sender:   <input type="text" name="sender" />
   <p>Receiver:   <input type="text" name="receiver" />
   <p>Comment:   <input type="text" name="comment" />
   <p> Type of transferred objects:<select name=type>
   <option>FullModule</option>
   <option>BareModule</option>
   <option>Sensor</option>
   <option>Roc</option>
   <option>HDI</option>
   <option>TBM</option>
   <option>Wafer</option>
   <option>Batch</option>
   </select><p>
   List of IDs:<p> 
<textarea rows="4" cols="50" name=ids>
</textarea>

   <p>
   <p><input type="submit" name="submit" value="Transfer" /></p>
   <p><input type="submit" name="submit" value="Transfer with children" /></p>

   </form>
</body>
</html> 
'''
