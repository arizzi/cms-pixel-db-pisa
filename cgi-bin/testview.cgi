#!/usr/bin/env python

# enable debugging
import cgitb
from datetime import *
cgitb.enable()

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
		"sDom": 'C<"clear">lfrtip'
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
for attr, value in Test_FullModule.__dict__.iteritems():
    if  type(eval("Test_FullModule."+attr)) is properties.PropertyColumn :
         columns.append(attr) 


    if  type(eval("Test_FullModule."+attr)) is references.Reference :
         refs.append(attr)
 
objects = pdb.store.find(Test_FullModule)

print "<table id=example width=\"100%\">"

print " <thead> <tr>"
for c in columns:
    print "<th>",c.lower().capitalize(),"</th>"
for r in refs:
    print "<th>", r.lower().capitalize(),"</th>"
print "</thead></tr><tbody>"


for o in objects : 
   print "<tr>"
   for c in columns:
    print "<td>",getattr(o,c),"</td>"
   for r in refs:
    print "<td><a href=ref>", r,"</a></td>"

   print "</tr>"

print "</tbody><tfoot></tfoot>"
