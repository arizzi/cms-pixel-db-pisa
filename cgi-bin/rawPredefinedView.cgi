#!/usr/bin/env python
# enable debugging
import sys
import cgitb
from datetime import *
cgitb.enable()
from math import *
import re
import cgi
from  rawPredefinedViews import *
print "Content-Type: text/html"
print
form = cgi.FieldStorage() # instantiate only once!
toprint=[]


objName = form.getfirst('objName', 'empty')
if objName == 'empty' :
	viewNumber = int(form.getfirst('viewNumber', '0'))
	if viewNumber >= len(columns) :
		exit(0)
	else:
		toprint = columns[viewNumber]
		topush='"name" : "viewNumber", "value" : "%s"' % viewNumber
else:
	objName = parseObjName(cgi.escape(objName))
	id,toprint,query,count = fromObjectName(objName)
	topush='"name" : "objName", "value" : "%s"' % objName

print "<html>\n        <head>\n         "      
print '''
<link rel="stylesheet" type="text/css" href="//cdn.datatables.net/1.10.2/css/jquery.dataTables.css">

<script type="text/javascript" charset="utf8" src="//code.jquery.com/jquery-1.10.2.min.js"></script>
<script type="text/javascript" charset="utf8" src="//cdn.datatables.net/1.10.2/js/jquery.dataTables.js"></script>
<script type="text/javascript" src="http://jquery-datatables-column-filter.googlecode.com/svn/trunk/media/js/jquery.dataTables.columnFilter.js"></script>
<script>
$(document).ready(function() {
		$('#example tbody').on( 'click', 'tr', function () {
		        $(this).toggleClass('selected');
		} );
		$('#example thead th').each( function () {
			var title = $('#example thead th').eq( $(this).index() ).text();
			$(this).html(title+'<br><input size=10 type="text" onclick="event.stopPropagation();"/>' );
			} );

		var table =          $('#example').DataTable( {
			"bStateSave": false,
			"iDisplayLength" : 25,
			"bProcessing": true,
			"bServerSide": true,
			"sAjaxSource": "/cgi-bin/rawPredefinedView-backend.cgi",
			"fnServerParams": function ( aoData ) {
			aoData.push( { %s } );
			}
			} );
		// Apply the search
		table.columns().eq( 0 ).each( function ( colIdx ) {
			$( 'input', table.column( colIdx ).header() ).on( 'keyup change', function () {
				table
				.column( colIdx )
                .search( this.value )
                .draw();
        } );
    } );

//.columnFilter({ sPlaceHolder: "filterPH"});
				});

	                </script>

''' %(topush)
sys.path.append("../PixelDB")

from storm import *
from PixelDB import *

from pixelwebui import *



pdb = PixelDBInterface(operator="webfrontend",center="cern")
pdb.connectToDB()


print "<p id=filterPH></p>"

print "<table id=example class=display width=100%>"
print " <thead> <tr>"
for (c,s,e) in toprint :
 print "<th>", c,"</th>"
print "</thead></tr>"
print " <tfoot> <tr>"
for (c,s,e) in toprint :
 print "<th>", c,"</th>"
print "</tfoot></tr><tbody></tbody>"

