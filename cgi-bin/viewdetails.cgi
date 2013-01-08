#!/usr/bin/env python

# enable debugging
import cgitb
from datetime import *
cgitb.enable()
import re
import cgi


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
               				 "bLengthChange": false,
					  "bPaginate": false,
					"bStateSave": true
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



form = cgi.FieldStorage() # instantiate only once!
objName = form.getfirst('objName', 'empty')
# Avoid script injection escaping the user input
objName = cgi.escape(objName)
objType = eval(objName)
refToShow = form.getfirst("ref", 'empty')

if re.match("test",objName,flags=re.IGNORECASE) : 
  ID="TEST_ID"
  objID = form.getfirst(ID, 'empty')
  objID = cgi.escape(objID)
  filterValue=int(objID)  
else:
  ID=objName+"_ID"
  ID=ID.upper()
  objID = form.getfirst(ID, 'empty')
  if objName == "Transfer"  or objName == "Data":
    objID = cgi.escape(objID)
    filterValue=int(objID)
  else :
    objID = cgi.escape(objID)
    filterValue=unicode(objID)  

filter=eval(objName+"."+ID)
objects = pdb.store.find(objType,filter==filterValue)

#if reference details were requested, show the details for it rather than the original object
if refToShow != "empty" :
 r=getattr(objects[0],refToShow)
 objects = [] 
 objects.append(r)
 objType=r.__class__
 objName=r.__class__.__name__
  
columns = []
refs = []
i =0 
for attr, value in objType.__dict__.iteritems():
#    print attr,type(eval(objName+"."+attr)).__name__," || " 
    if  type(eval(objName+"."+attr)) is properties.PropertyColumn or  type(eval(objName+"."+attr)).__name__ == "date"  or  type(eval(objName+"."+attr)).__name__ == "datetime":
        columns.append(attr) 


    if  type(eval(objName+"."+attr)) is references.Reference :
         refs.append(attr)

 

print "<table id=example width=\"100%\">"

print " <thead> <tr>"
print "<th> Field </th>"
print "<th> Value </th>"
print "</thead></tr><tbody>"
summary=""
for o in objects : 
   for c in columns:
    print "<tr><td>",c.lower().capitalize(),"</td><td>",getattr(o,c)
    res=re.match("file:(.*/(M.*)/(T.*)/)",str(getattr(o,c)))
    if res : 
     print "(<a href=\"../data/"+res.group(1)+"\">view</a>)"
#     print res.group(1)," ",res.group(2),res.group(3) 
     summary="../data/"+res.group(1)+"/"+res.group(2)+res.group(3)+".gif" 
   print "</td></tr>"
   
   for r in refs:
    print "<tr><td>",r.lower().capitalize(),"</td>"
    
    print "<td>"
    #if 1 :
    try :
     objRef = getattr(o,r)
#    help(objRef)
     if re.match("test",objRef.__class__.__name__,flags=re.IGNORECASE) :
      ID1="TEST_ID"
     else:
      ID1=objRef.__class__.__name__+"_ID"
      ID1=ID1.upper()
     for attr, value in type(objRef).__dict__.iteritems():
      if  type(eval(objRef.__class__.__name__+"."+attr)) is properties.PropertyColumn :
       print "<b>",attr,":</b>", getattr(objRef,attr) ,"<BR>"   
     print "<a href=\"viewdetails.cgi?objName="+objRef.__class__.__name__+"&"+ID1+"="+str(getattr(objRef,ID1))+"\">details</a>"
    except :
     print "no info"
    print "</td></tr>"
#    print "<td><a href=ref>", r,"</a></td>"
#    help(getattr(o,r))


print "</tbody><tfoot></tfoot></table><br>"
if summary != "" :
   print "<img src="+summary+">"
