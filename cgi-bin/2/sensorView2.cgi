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
<link rel="stylesheet" type="text/css" href="//cdn.datatables.net/colvis/1.1.1/css/dataTables.colVis.css">

<script type="text/javascript" charset="utf8" src="//code.jquery.com/jquery-1.10.2.min.js"></script>
<script type="text/javascript" charset="utf8" src="//cdn.datatables.net/1.10.2/js/jquery.dataTables.js"></script>
<script type="text/javascript" charset="utf8" src="//cdn.datatables.net/colvis/1.1.1/js/dataTables.colVis.min.js"></script>
<script type="text/javascript" src="http://jquery-datatables-column-filter.googlecode.com/svn/trunk/media/js/jquery.dataTables.columnFilter.js"></script>
<script>
                        $(document).ready(function() {
                                $('#example').dataTable( {
					"sDom": 'C<"clear">lfrtip',
			                "iDisplayLength" : 100,
					} );
                        	} ).columnFilter();
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

from storm import *
from PixelDB import *

from pixelwebui import *



pdb = PixelDBInterface(operator="webfrontend",center="cern")
pdb.connectToDB()
toprint = [
#"Sel","'<input type=checkbox name=sel>'"),
#	   ("Sensor id","'%s<input type=checkbox name=sel_sensor%s>'%(s.SENSOR_ID,s.SENSOR_ID)"),
	   ("Sensor ID","s.SENSOR_ID"),
	   ("Status","s.STATUS"),
	   ("Center","tr.RECEIVER"),
	   ("Test date","t.DATE"),
	   ("Type","t.TYPE"),
	   ("Grade","t.GRADE"),
	   ("v1","'%6g'%t.V1"),
	   ("v2","'%6g'%t.V2"),
	   ("i1","'%6g'%t.I1"),
	   ("i2","'%6g'%t.I2"),
	   ("Slope","t.SLOPE"),
	   ("Temp","t.TEMPERATURE"),
           ("i1@20&deg;","'%6g'%corTemp(t.I1,t.TEMPERATURE)"),
           ("i2@20&deg;","'%6g'%corTemp(t.I2,t.TEMPERATURE)"),
#           ("Test id","'%s<input type=checkbox name=sel_sensor%s>'%(t.TEST_ID,t.TEST_ID)"),
           ("Test id","t.TEST_ID"),
           ("Files","'<a href=%s>link</a>'%t.data.PFNs"),
	  ]


objects = pdb.store.find( (Sensor,Test_IV,Transfer), Sensor.SENSOR_ID==Test_IV.SENSOR_ID, Sensor.TRANSFER_ID==Transfer.TRANSFER_ID,Transfer.RECEIVER.like(u'%%%s%%'%form.getfirst("center","")),Test_IV.TYPE.like(u'%%%s%%'%form.getfirst("type","")))
print "<h2> Sensors view </h2>"
print "<form>"
print "Center: <select name=center onchange=\"this.form.submit()\">"
for o in [""]+centers :
	if form.getfirst("center","") == o :
	       print "<option selected>%s</option>" % o
	else:
	       print "<option >%s</option>" % o
print" </select>"

#<input name=center value=%s><br>" % form.getfirst("center","")
print "Type: <input name=type value=\"%s\" onkeydown=\"if (event.keyCode == 13) this.form.submit()\"><br>" % form.getfirst("type","")
#print "<input type=submit value=Apply></form>"
print "<p>"
if False :
 print "<button>Select all sensors</button>"
 print "<button>Unselect all sensors</button>"
 print "<button>Select all tests</button>"
 print "<button>Unselect all tests</button>"
 print " &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <button>Plot all IVs for selected sensors</button> <button>Plot selected IVs</button>"
print "<hr>"
print "<table id=example class=display>"
print " <thead> <tr>"
for (c,e) in toprint :
# print "<th>", c,"<br><input type=\"text\" size=10></th>"
 print "<th>", c,"</th>"
print "</thead></tr><tbody>"

for (s,t,tr) in objects : 
   print "<tr>"
   for (c,e) in toprint :
	print "<td>",eval(e),"</td>"
print "</tbody><tfoot></tfoot>"
