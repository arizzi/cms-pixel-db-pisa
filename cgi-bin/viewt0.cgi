#!/usr/bin/env python
# enable debugging
import sys
import cgitb
from datetime import *
cgitb.enable()

import re
import cgi
form = cgi.FieldStorage() # instantiate only once!



objName = form.getfirst('objName', 'empty')
# Avoid script injection escaping the user input
objName = cgi.escape(objName)


print "Content-Type: text/html"
print
print "<html>\n        <head>\n         "      
print '''
                <style type="text/css" title="currentStyle">
                        @import "../media/css/demo_page.css";
                        @import "../media/css/jquery.dataTables.css";
                        @import "../media/css/ColVis.css";
                </style>
                <script type="text/javascript" language="javascript" src="../media/js/jquery.js"></script>
                <script type="text/javascript" language="javascript" src="../media/js/jquery.dataTables.js"></script>
                <script type="text/javascript" language="javascript" src="../media/js/ColVis.min.js"></script>
                <script type="text/javascript" charset="utf-8">
                        $(document).ready(function() {
                                $('#example').dataTable( {
					"sDom": 'C<"clear">lfrtip',
			                "iDisplayLength" : 25,
					} );
                        	} );
			function fnShowHide( iCol )
			{
			    /* Get the DataTables object again - this is not a recreation, just a get of the object */
			    var oTable = $('#example').dataTable();
		     
			    var bVis = oTable.fnSettings().aoColumns[iCol].bVisible;
			    oTable.fnSetColumnVis( iCol, bVis ? false : true );
			}
	                </script>

'''
sys.path.append("../PixelDB")

from storm.properties import *
from storm.references import *
from storm import *
from PixelDB import *
sys.path.append("/home/robot/cms-pixel-db-pisa/Tier0")
from  PixelTier0 import *
import random


pdb = PixelTier0()
#pdb.initProcessing(CONFIG=MACRO_INIT, DEBUG=False)
pdb.connectToDB()




columns = []
refs = []
i =0 
#objName = "Test_FullModule"
objType = eval(objName)
if re.match("test",objName,flags=re.IGNORECASE) : 
  ID="TEST_ID"
elif re.match("INPUTTAR",objName,flags=re.IGNORECASE) :
  ID="TAR_ID"
elif re.match("PROCESSINGRUN",objName,flags=re.IGNORECASE) :
  ID="RUN_ID"
elif re.match("PROCESSEDDIR",objName,flags=re.IGNORECASE) :
  ID="DIR_ID"
else:
  ID=objName+"_ID"
ID=ID.upper()

keys=objType.__dict__.keys()
for attr in keys:
    print attr #,type(eval(objName+"."+attr)).__name__,"<br>"
    if  type(eval(objName+"."+attr)) is properties.PropertyColumn or  type(eval(objName+"."+attr)).__name__ == "date"  or  type(eval(objName+"."+attr)).__name__ == "datetime":
#    if  type(eval(objName+"."+attr)) is properties.PropertyColumn :
         columns.append(attr) 
    if  type(eval(objName+"."+attr)) is references.Reference :
         refs.append(attr)
 
columns.sort()
objects = pdb.store.find(objType) # ,objType.TEST_ID==88)

print "<table id=example width=\"100%\">"

print " <thead> <tr>"
print "<th> ",ID," </th>"
for c in columns:
    print "<th>",c.lower().capitalize(),"</th>"
for r in refs:
    print "<th>", r.lower().capitalize(),"</th>"
print "</thead></tr><tbody>"


for o in objects : 
   print "<tr>"
   print "<td>", getattr(o,ID) ,"(<a href=viewdetailst0.cgi?objName="+objName+"&"+ID+"="+str(getattr(o,ID)),">details</a>)</td>"
   for c in columns:
    v=getattr(o,c)
    if type(v).__name__ == "unicode" : 
      print "<td>",v.encode('utf-8'),"</td>"
    else :
      print "<td>",v,"</td>"
   for r in refs:
    print "<td><a href=\"viewdetailst0.cgi?objName="+objName+"&"+ID+"="+str(getattr(o,ID))+"&ref="+r+"\"> details</a></td>"
#    help(getattr(o,r))
   print "</tr>"

print "</tbody><tfoot></tfoot>"
