#!/usr/bin/env python
# enable debugging
import sys
import cgitb
from datetime import *
cgitb.enable()

import re
import cgi
from pixelwebui import *

def defaultHidden(cols) :
	i=0
	s=""	
	for c in cols:
		i+=1
		if re.match("LASTTEST",c) or c == "TRANSFER_ID" or re.match("transfer",c) :  
			 s+="{ \"bVisible\": false, \"aTargets\": [ %s ] }, // %s\n" % (i+1,c)
	return s 

form = cgi.FieldStorage() # instantiate only once!



objName = form.getfirst('objName', 'empty')
# Avoid script injection escaping the user input
objName = parseObjName(cgi.escape(objName))

sys.path.append("../PixelDB")

from storm.properties import *
from storm.references import *
from storm import *
from PixelDB import *
import random


pdb = PixelDBInterface(operator="webfrontend",center="cern")
pdb.connectToDB()


columns = []
refs = []
i =0 
#objName = "Test_FullModule"
objType = eval(objName)
if re.match("test",objName,flags=re.IGNORECASE) : 
  ID="TEST_ID"
else:
  ID=objName+"_ID"
ID=ID.upper()

keys=objType.__dict__.keys()
hasTrans=False
for attr in keys:
    #print attr #,type(eval(objName+"."+attr)).__name__,"<br>"
    if  type(eval(objName+"."+attr)) is properties.PropertyColumn or  type(eval(objName+"."+attr)).__name__ == "date"  or  type(eval(objName+"."+attr)).__name__ == "datetime":
#    if  type(eval(objName+"."+attr)) is properties.PropertyColumn :
         columns.append(attr) 
	 if attr == "TRANSFER_ID" :
		hasTrans=True
    if  type(eval(objName+"."+attr)) is references.Reference :
         refs.append(attr)
    
columns.sort()
hide=defaultHidden(columns+refs)
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
					"bStateSave": true,
					"sDom": 'C<"clear">lfrtip',
					"aoColumnDefs": [%s],
			                "iDisplayLength" : 25,
					"bProcessing": true,
					"bServerSide": true,
					"sAjaxSource": "/cgi-bin/view-backend.cgi",
        				"fnServerParams": function ( aoData ) {
					            aoData.push( { "name" : "objName", "value" : "%s" } );
					  }
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

'''%(hide,objName)

objects = pdb.store.find(objType) # ,objType.TEST_ID==88)

print "<table id=example width=\"100%\">"

print " <thead> <tr>"
print "<th> ",ID," </th>"
if hasTrans :
	print "<th> Location </th>"
for c in columns:
    print "<th>",c.lower().capitalize(),"</th>"
for r in refs:
    print "<th>", r.lower().capitalize(),"</th>"
print "</thead></tr><tbody>"



print "</tbody><tfoot></tfoot>"
