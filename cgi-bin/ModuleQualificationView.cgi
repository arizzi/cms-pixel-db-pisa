#!/usr/bin/env python
# enable debugging
import sys
import cgitb
from datetime import *
cgitb.enable()

import re
import cgi
from pixelwebui import *


def findMax(o,referencesforMax,analysisToUse,field) :
   tmp = 0
   for r in referencesforMax :
	tmp = max(tmp,eval("o"+r+"."+analysisToUse+"."+field))
   return tmp

def pfn(PFNs) :
  for p in PFNs.split(",") : 
	return p.replace("file:","")+"/TestResult.html"
  return ""   
form = cgi.FieldStorage() # instantiate only once!



objName = form.getfirst('objName', 'empty')
# Avoid script injection escaping the user input
objName = parseObjName(cgi.escape(objName))


print "Content-Type: text/html"
print
print "<html>\n        <head>\n         "      
#                <style type="text/css" title="currentStyle">
#                        @import "../media/css/demo_page.css";
#                        @import "../media/css/jquery.dataTables.css";
#                        @import "../media/css/ColVis.css";
#                </style>

print '''
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

'''
sys.path.append("../PixelDB")

from storm.properties import *
from storm.references import *
from storm import *
from PixelDB import *
import random

moduleid = form.getfirst('ModuleID', 'empty')
summaryid = form.getfirst('SummaryID', 'empty')
# Avoid script injection escaping the user input
moduleid = cgi.escape(moduleid)

pdb = PixelDBInterface(operator="webfrontend",center="cern")
pdb.connectToDB()

referencesforMax = [""]
analysisToUse = "analyses.order_by(\"MACRO_VERSION\").last()"
evals = ["\"%s (<a href=viewdetails.cgi?spec=0&objName=Test_FullModule&TEST_ID=%d>details</a>)\" % (o.TEST_ID,o.TEST_ID)"
        ,"\"%s (<a href=\"%(o.FULLMODULE_ID)+pfn(o."+analysisToUse+".data.PFNs)+\">last analysis results</a>)\""
	,"o.summary.QUALIFICATIONTYPE"
	,"o.session.session.CENTER"
        ,"datetime.fromtimestamp(float(o.TIMESTAMP)).isoformat()","o.TEMPNOMINAL","o."+analysisToUse+".GRADE"
#evals = ["\"%s (<a href=>last analysis results</a>)\"%(o.FULLMODULE_ID)","datetime.fromtimestamp(float(o.TIMESTAMP)).isoformat()","o.TEMPNOMINAL","o."+analysisToUse+".GRADE"
	,"\"%d\"%(o."+analysisToUse+".NOISYPIXELS)"
	,"o."+analysisToUse+".ROCSWORSEPERCENT"
	,"o."+analysisToUse+".PHCAL"
	,"o."+analysisToUse+".TRIMMING"

	]

headers = ["Test ID","Module ID","Qualification","Center","Date","Temperature","Grade","Noisy","ROCs >1%","PhCal","Trimming"]
i =0 
#objName = "Test_FullModule"


objects = None
if summaryid == "empty" :
  module = pdb.store.find(FullModule ,FullModule.FULLMODULE_ID==unicode(moduleid)).one()
  summaryid=module.LASTTEST_FULLMODULE
  titlestring="(last qualification only) "
else:
  titlestring="(only for fullsummary %s) " % summaryid

if summaryid == "all" :
  objects = pdb.store.find(Test_FullModule ,Test_FullModule.FULLMODULE_ID==unicode(moduleid))
  titlestring="(all qualifications) "
else :
  objects = pdb.store.find(Test_FullModule ,Test_FullModule.FULLMODULE_ID==unicode(moduleid) and Test_FullModule.SUMMARY_ID==int(summaryid))
#print "<br> <ul><li> View <a href=viewdetails.cgi?spec=0&objName=FullModule&FULLMODULE_ID="+moduleid+">Module Details</a><br><br>"

print ("<h1>List of FullModule Tests %sfor  <a href=viewdetails.cgi?spec=0&objName=FullModule&FULLMODULE_ID="+moduleid+">"+moduleid+"</b></h1>") % (titlestring) 

print "<table id=example width=\"100%\" class=\"pretty\" >"
print " <thead> <tr>"
for c in headers:
    print "<th>",c.lower().capitalize(),"</th>"
print "</thead></tr><tbody>"


for o in objects : 
   print "<tr>"
   for e in evals:
    print "<td>"+eval(e)+"</td>"
   print "</tr>"

print "</tbody><tfoot></tfoot>"
