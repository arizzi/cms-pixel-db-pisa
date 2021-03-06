#!/usr/bin/env python

# enable debugging
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import cgitb
from datetime import *
cgitb.enable()
import re
import cgi

def printHeaders() :
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
                <script type="text/javascript" language="javascript" src="../media/js/jquery.js"></script>
                <script type="text/javascript" language="javascript" src="../media/js/jquery.dataTables.js"></script>
                <script type="text/javascript" charset="utf-8">
                        $(document).ready(function() {
                                $('#example').dataTable( {
					 "bSort" : false,
					"sDom": 'C<"clear">lfrtip',
               				 "bLengthChange": false,
					  "bPaginate": false,
					 "bStateSave" : false,
				} );
                        } );
function fnShowHide( iCol )
{
    /* Get the DataTables object again - this is not a recreation, just a get of the object */
    var oTable = $('#example2').dataTable();
     
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
from SpecificView import *
from pixelwebui import *

pdb = PixelDBInterface(operator="webfrontend",center="cern")
pdb.connectToDB()


form = cgi.FieldStorage() # instantiate only once!
objName = form.getfirst('objName', 'empty')
# Avoid script injection escaping the user input
objName = cgi.escape(parseObjName(objName))
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
  if objName == "Transfer"  or objName == "Data" or objName == "Session":
    objID = cgi.escape(objID)
    filterValue=int(objID)
  else :
    objID = cgi.escape(objID)
    filterValue=unicode(objID)  

filter=eval(objName+"."+ID)
#ilter=objName+"."+ID
#print "filter ",filter,"=",filterValue, objName,ID
objects = pdb.store.find(objType,filter==filterValue)

#print  "count: ", objects.count()
if objects.count() == 0 : 
  printHeaders()
  print "NOT FOUND"
else :
	if refToShow != "empty":
 	 	   r=getattr(objects[0],refToShow)
		   idn=idField(r.__class__.__name__)
		   newlocation="viewdetails.cgi?objName=%s&%s=%s"%(r.__class__.__name__,idn,getattr(r,idn))
		   print "Location: %s" % newlocation
		   print

  	printHeaders()
	print "<a href=/cgi-bin/writers/edit.cgi?objName=%s&%s=%s>EDIT</a>"%(objName,ID,objID)
	print "<h2> Details for %s  %s </h2>"%(objName,objID) 

	lb = pdb.store.find(Test_Logbook,Test_Logbook.IDS.like(u"%%%s%%"%objID))
	for l in lb:
	    if re.match("(,|^)%s(,|$)"%objID,l.IDS):
		print "<li>Logbook entry about this object <a href=/cgi-bin/viewdetails.cgi?objName=Test_Logbook&TEST_ID=%s>(details)</a>:<br>%s"%(l.TEST_ID,l.COMMENT)
        if cgi.escape(form.getfirst("spec", "1")) == "1" and refToShow=="empty":
	  specificView(objName,form,pdb)
#if reference details were requested, show the details for it rather than the original object
	if refToShow != "empty" :
 	 r=getattr(objects[0],refToShow)
	 if not r:
	  print "NOT FOUND in objtype ", type(objects[0]).__name__, "ref :",refToShow,":<br>"
 	  objects = [] 
	 else:
	 #pprint   "class " , r.__class__.__name__
 	  objects = [] 
  	  objects.append(r)
	  objType=r.__class__
	  objName=r.__class__.__name__
#  specificView(objName,form,pdb)idField(objName) 

	columns = []
	if objName in sortedCols:
        	columns = sortedCols[objName]

	refs = []
	refsets = []
	i =0 
	#type(eval(objName+".FULLMODULE_ID")).__name__
	keys=objType.__dict__.keys()
	for attr in keys:
	#    print attr,type(eval(objName+"."+attr)).__name__,"<br>"
	#    print attr,type(eval(objName+"."+attr)).__name__," || " 
	    if  type(eval(objName+"."+attr)) is properties.PropertyColumn or  type(eval(objName+"."+attr)).__name__ == "date"  or  type(eval(objName+"."+attr)).__name__ == "datetime":
		if attr not in columns :
		        columns.append(attr) 

	    if  type(eval(objName+"."+attr)) is references.ReferenceSet :
                 refsets.append(attr)


	    if  type(eval(objName+"."+attr)) is references.Reference  :
	         refs.append(attr)


	print "<table  id=example width=\"100%\">"

	print " <thead> <tr>"
	print "<th> Field </th>"
	print "<th> Value </th>"
	print "</thead></tr><tbody>"
	summary=""
	for o in objects : 
	   for c in columns:
	    print "<tr><td>",c.lower().capitalize(),"</td><td>",getattr(o,c)
	    res=re.match(".*PIXELDB(.*)",str(getattr(o,c)))
	    if res : 
	     print "(<a href=\"../data/pixels/"+res.group(1)+"\">view</a> | <a href=\"../data/pixels/"+res.group(1)+"\" download>download</a> )"
	#     print res.group(1)," ",res.group(2),res.group(3) 
#	     summary="../data/"+res.group(1)+"/"+res.group(2)+res.group(3)+".gif" 
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
  	     rcolumns = []
             if objRef.__class__.__name__ in sortedCols:
                rcolumns = sortedCols[objRef.__class__.__name__]
             for attr, value in type(objRef).__dict__.iteritems():
                     if attr not in rcolumns :
                               rcolumns.append(attr)
             for attr in rcolumns :
              value=type(objRef).__dict__[attr]
	     #for attr, value in type(objRef).__dict__.iteritems():
	      if  type(eval(objRef.__class__.__name__+"."+attr)) is properties.PropertyColumn :
	       print "<b>",attr,":</b>", getattr(objRef,attr) ,"<BR>"   
	     print "<a href=\"viewdetails.cgi?objName="+objRef.__class__.__name__+"&"+ID1+"="+str(getattr(objRef,ID1))+"\">details</a>"
	    except :
	     print "no info"
	    print "</td></tr>"

           for rs in refsets:
            objRefSet =  getattr(o,rs)
#            print "IIIIIIIIII", objRefSet
            for r in objRefSet:
           
             print "<tr><td>",r.__class__.__name__,"</td>"

             print "<td>"
            #if 1 :
             try :
	      print r
              objRef = r
        #    help(objRef)
              if re.match("test",objRef.__class__.__name__,flags=re.IGNORECASE) :
               ID1="TEST_ID"
              else:
               ID1=objRef.__class__.__name__+"_ID"
               ID1=ID1.upper()
	      rcolumns = []
              if objRef.__class__.__name__ in sortedCols:
                rcolumns = sortedCols[objRef.__class__.__name__]
              for attr, value in type(objRef).__dict__.iteritems():
		     if attr not in columns :
        	               rcolumns.append(attr)
	      for attr in rcolumns :
	       value=type(objRef).__dict__[attr]
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
	printFooter()
