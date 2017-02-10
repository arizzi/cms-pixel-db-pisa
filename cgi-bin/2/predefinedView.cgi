#!/usr/bin/env python
# enable debugging
import sys
import cgitb
from datetime import *
cgitb.enable()
from math import *
import re
import cgi
form = cgi.FieldStorage() # instantiate only once!

def corTemp(I,T) :
	kb=1.3806488
	eg=1.2
	return I*(20./T)**2 * exp(-eg/(2*kb)*(1./20.-1./T))

print "Content-Type: text/html"
print
print "<html>\n        <head>\n         "      
print '''
<link rel="stylesheet" type="text/css" href="//cdn.datatables.net/1.10.2/css/jquery.dataTables.css">

<script type="text/javascript" charset="utf8" src="//code.jquery.com/jquery-1.10.2.min.js"></script>
<script type="text/javascript" charset="utf8" src="//cdn.datatables.net/1.10.2/js/jquery.dataTables.js"></script>
<script type="text/javascript" src="http://jquery-datatables-column-filter.googlecode.com/svn/trunk/media/js/jquery.dataTables.columnFilter.js"></script>
<script>
                        $(document).ready(function() {
                                $('#example').dataTable( {
                                        "bStateSave": true,
                                        "iDisplayLength" : 25,
                                        "bProcessing": true,
                                        "bServerSide": true,
                                        "sAjaxSource": "/cgi-bin/predefinedView-backend.cgi",
                                        "fnServerParams": function ( aoData ) {
                                                    aoData.push( { "name" : "viewNumber", "value" : "%s" } );
                                          }
                                        } ).columnFilter();
				});

	                </script>

''' %(0)
sys.path.append("../PixelDB")

from storm import *
from PixelDB import *

from pixelwebui import *



pdb = PixelDBInterface(operator="webfrontend",center="cern")
pdb.connectToDB()

from  predefinedViews import *

toprint = columns[0]


print "<table id=example class=display width=100%>"
print " <thead> <tr>"
for (c,e) in toprint :
 print "<th>", c,"</th>"
print "</thead></tr>"
print " <tfoot> <tr>"
for (c,e) in toprint :
 print "<th>", c,"</th>"
print "</tfoot></tr><tbody></tbody>"

