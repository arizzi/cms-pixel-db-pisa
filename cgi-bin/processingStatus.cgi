#!/usr/bin/env python
# enable debugging
import sys
import cgitb
from datetime import *
cgitb.enable()

import re
import cgi
from pixelwebui import *

print "Content-Type: text/html"
print

print "<html>\n        <head>\n         "      
print '<link rel="stylesheet" type="text/css" href="/frames.css" />'
print '''
<link rel="stylesheet" type="text/css" href="//cdn.datatables.net/1.10.2/css/jquery.dataTables.css">

<script type="text/javascript" charset="utf8" src="//code.jquery.com/jquery-1.10.2.min.js"></script>
<script type="text/javascript" charset="utf8" src="//cdn.datatables.net/1.10.2/js/jquery.dataTables.js"></script>
<script type="text/javascript" src="http://jquery-datatables-column-filter.googlecode.com/svn/trunk/media/js/jquery.dataTables.columnFilter.js"></script>
<script>
                var selected = [];

$(document).ready(function() {
                $('#example tbody').on( 'click', 'tr', function () {
                                        var id = $(this).attr('id');
                                        var index = $.inArray(id, selected);
                                        if ( index === -1 ) {
                                        selected.push( id );
                                        } else {
                                        selected.splice( index, 1 );
                                        }
                                        $(this).toggleClass('selected');
                                        update();
                } );
                $('#example thead th').each( function () {
                        var title = $('#example thead th').eq( $(this).index() ).text();
                        $(this).html(title);
                        } );

                var table =          $('#example').DataTable( {
                        "bStateSave": true,
                         "aLengthMenu": [   [25, 50, 100, 200, -1],
                                        [25, 50, 100, 200, "All"]],
                        "iDisplayLength" : 25,
                        "bProcessing": true,
			 "order": [[ 1,"desc" ]]
                        } );
        } );

                        </script>
<body>
<main>
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

def logs(x):
        last= o.processes.order_by("RUN_ID").last()
        if last is not None :
	    if last.OUTLOG is not None:
		a="<a href=%s>log1</a>"%last.OUTLOG
		a+="|<a href=%s_upload>log2</a>"%last.OUTLOG
		return a
	return "n/a"

def lastProc(x):
	last= o.processes.order_by("RUN_ID").last()
	if last is not None :
	      if last.EXIT_CODE > 0 or (last.processed_dir_id is not None and last.processed_dir_id.UPLOAD_STATUS != None and last.processed_dir_id.UPLOAD_STATUS != "ok") :
		return "<font color=red>%s(%s), %s, %s</font>"%(last.STATUS,last.EXIT_CODE,last.MACRO_VERSION,last.processed_dir_id.UPLOAD_STATUS)
	      elif last.EXIT_CODE == -1 :
		return "<font color=blue>%s(%s), %s</font>"%(last.STATUS,last.EXIT_CODE,last.MACRO_VERSION)
	      else:
		return "%s(%s), %s, %s"%(last.STATUS,last.EXIT_CODE,last.MACRO_VERSION,last.processed_dir_id.UPLOAD_STATUS)
	 
	return "n/a"	

evals = ["o.NAME","\"%s\"%o.DATE","o.CENTER","o.STATUS","o.TESTNAME","lastProc(o.processes)","logs(o.processes)"]

a=["\"<a href=ModuleQualificationView.cgi?ModuleID=%s>%s</a>\"%( o.FULLMODULE_ID,o.FULLMODULE_ID)"
	,"o.fullmoduletests.any().session.session.CENTER"
#	,"\"%d\" %o.fullmoduletests.count()"
	,"datetime.fromtimestamp(float(o.fullmoduletests.any().TIMESTAMP)).isoformat()","o.QUALIFICATIONTYPE","findMax(o,analysisToUse,\"GRADE\")"
	,"\"%d\"%(findMax(o,analysisToUse,\"PIXELDEFECTS\"))"
	,"\"%d\"%(findMax(o,analysisToUse,\"ROCSWORSEPERCENT\"))"
	,"\"%d\"%(findMax(o,analysisToUse,\"PHCAL\"))"
	,"str(findMax(o,analysisToUse,\"TRIMMING\"))"
	,"(concat(o,analysisToUse,\"COMMENT\"))"

	]

headers = ["NAME","Date","Center","Status","TestName","LastProcessing(code),macro","logs"]
i =0 
#objName = "Test_FullModule"

 
objects = pdb.store.find(InputTar) # ,objType.TEST_ID==88)

print "<table id=example width=\"100%\" class=\"display\">"

print " <thead> <tr>"
for c in headers:
    print "<th>",c.lower().capitalize(),"</th>"
print "</thead></tr><tbody>"


for o in objects :
   print "<tr>"
   for e in evals:
    print "<td>"+eval(e)+"</td>"
   print "</tr>"

print "</tbody><tfoot></tfoot></table>"
printFooter()
