#!/usr/bin/env python
# enable debugging
import sys
import cgitb
from datetime import *
cgitb.enable()
from pixelwebui import *

import re
import cgi

def findMax(o,analysisToUse,field) :
   tmp = 0
   for r in o.fullmoduletests :
	one = eval("r."+analysisToUse+"."+field)
	try: 
  	 if float(one) > float(tmp) :
  	    tmp = one
        except ValueError:
	   tmp = max(tmp,eval("r."+analysisToUse+"."+field))
   return tmp
  
def concat(o,analysisToUse,field) :
   tmp = ""
   for r in o.fullmoduletests :
        one = eval("r."+analysisToUse+"."+field)
#   for r in referencesforMax :
#        one = eval("o"+r+"."+analysisToUse+"."+field)
	if one != "" :
	   tmp+=" / "+one
   return tmp

 
form = cgi.FieldStorage() # instantiate only once!



objName = form.getfirst('objName', 'empty')
# Avoid script injection escaping the user input
objName = parseObjName(cgi.escape(objName))


print "Content-Type: text/html"
print
print "<html>\n        <head>\n         "      
print '<link rel="stylesheet" type="text/css" href="/frames.css" />'
print '''
                <style type="text/css" title="currentStyle">
                        @import "../media/css/demo_page.css";
                        @import "../media/css/jquery.dataTables.css";
                        @import "../media/css/ColVis.css";
                </style>
                <link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/3.3.0/build/cssreset/reset-min.css">
                <link rel="stylesheet" type="text/css" href="/complete.css">

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
<body><main>
'''
sys.path.append("../PixelDB")

from storm.properties import *
from storm.references import *
from storm import *
from PixelDB import *
import random


pdb = PixelDBInterface(operator="webfrontend",center="cern")
pdb.connectToDB()

analysisToUse = "analyses.order_by(\"MACRO_VERSION\").last()"
evals = ["\"<a href=ModuleQualificationView.cgi?ModuleID=%s&SummaryID=all>%s</a>\"%( o.FULLMODULE_ID,o.FULLMODULE_ID)"
	,"\"<a href=ModuleQualificationView.cgi?ModuleID=%s&SummaryID=%s>%s</a>\"%( o.FULLMODULE_ID,o.TEST_ID,o.TEST_ID)"
	,"o.fullmoduletests.any().session.session.CENTER"
#	,"\"%d\" %o.fullmoduletests.count()"
	,"datetime.fromtimestamp(float(o.fullmoduletests.any().TIMESTAMP)).isoformat()","o.QUALIFICATIONTYPE","findMax(o,analysisToUse,\"GRADE\")"
	,"\"%d\"%(findMax(o,analysisToUse,\"PIXELDEFECTS\"))"
	,"\"%s\"%(findMax(o,analysisToUse,\"ROCSWORSEPERCENT\"))"
	,"\"%d\"%(findMax(o,analysisToUse,\"PHCAL\"))"
	,"str(findMax(o,analysisToUse,\"TRIMMING\"))"
	,"(concat(o,analysisToUse,\"COMMENT\"))"

	]

headers = ["Module ID","Summary ID","Center","Date","Qualification Type","Grade","Pixel Defects","ROCs >1%","PhCal","Trimming","Comments"]
i =0 
#objName = "Test_FullModule"

 
objects = pdb.store.find(Test_FullModuleSummary) # ,objType.TEST_ID==88)

print "<table id=example width=\"100%\" class=\"pretty\">"

print " <thead> <tr>"
for c in headers:
    print "<th>",c.lower().capitalize(),"</th>"
print "</thead></tr><tbody>"


for o in objects :
 if o.fullmoduletests.count() > 0 : 
   print "<tr>"
   for e in evals:
    print "<td>"+eval(e)+"</td>"
   print "</tr>"

print "</tbody><tfoot></tfoot></table>"
printFooter()
