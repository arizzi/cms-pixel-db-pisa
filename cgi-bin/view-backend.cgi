#!/usr/bin/env python
# enable debugging
import sys
import cgitb
from datetime import *
cgitb.enable()
from pixelwebui import *
import re
import cgi
form = cgi.FieldStorage() # instantiate only once!
print "Content-Type: text/plain"
print



objName = form.getfirst('objName', 'empty')
# Avoid script injection escaping the user input
objName = parseObjName(cgi.escape(objName))
import json

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
for attr in keys:
#    print attr #,type(eval(objName+"."+attr)).__name__,"<br>"
    if  type(eval(objName+"."+attr)) is properties.PropertyColumn or  type(eval(objName+"."+attr)).__name__ == "date"  or  type(eval(objName+"."+attr)).__name__ == "datetime":
#    if  type(eval(objName+"."+attr)) is properties.PropertyColumn :
         columns.append(attr) 
    if  type(eval(objName+"."+attr)) is references.Reference :
         refs.append(attr)
 
columns.sort()
first = form.getfirst("iDisplayStart", "0")
last = form.getfirst("iDisplayLength", "-1")
first = int(cgi.escape(first))
last= int(cgi.escape(last))

last += first

#if last == -1 : 
#        ob = "objects[%d:]"%first
#else :
#        ob = "objects[%d:%d]"%(first,last)

objects = pdb.store.find(objType) # ,objType.TEST_ID==88)

sortCol = form.getfirst("iSortCol_0","empty")

objString = "objects"

colNames=[]
colNames.append(ID)
for c in columns:
   colNames.append(c)
for r in refs:
   colNames.append(r)

if sortCol != "empty" :
               cols=int(form.getfirst('iSortingCols'))
               if cols > 0 : 
                       sortcol= int(form.getfirst("iSortCol_0"))
                       if form.getfirst('bSortable_%d'%sortcol) == "true" :
                              if form.getfirst("sSortDir_%d"%i) == "asc" :
			          objString = "objects.order_by(%s.%s)"	% (objName,colNames[sortcol])	
			      else:	
			          objString = "objects.order_by(Desc(%s.%s))"	% (objName,colNames[sortcol])	
#		sOrder = "ORDER BY  "
#	        dosort=0
#		for  i in range (0,cols-1) :
#			sortcol= int(form.getfirst("iSortCol_%d"%i))
#			if form.getfirst('bSortable_%d'%sortcol) == "true" :
#				if dosort !=0 :
#					  sOrder+=" , "
#				if form.getfirst("sSortDir_%d"%i) == "asc" :
#					dosort=1
#					sOrder += column[sortcol]+" asc "
#				else:
#					dosort=1
#					sOrder += column[sortcol]+" desc "
#		if dosort ==0 :
#			sOrder = ""
#print objString
if last == -1 : 
        ob = objString+"[%d:]"%first
else :
        ob = objString+"[%d:%d]"%(first,last)

output = {}
output["sEcho"] = form.getfirst('sEcho',1)
output["iTotalRecords"] = objects.count()
output["iTotalDisplayRecords"] =  objects.count()
output["aaData"] = []


for o in eval(ob) : 
   row = []
   row.append( getattr(o,ID)+"(<a href=viewdetails.cgi?objName="+objName+"&"+ID+"="+str(getattr(o,ID))+">details</a>)")
   for c in columns:
    v=getattr(o,c)
    if type(v).__name__ == "unicode" : 
       row.append(v.encode('utf-8'))
    else :
       row.append(v)
   for r in refs:
    row.append("<a href=\"viewdetails.cgi?objName="+objName+"&"+ID+"="+str(getattr(o,ID))+"&ref="+r+"\"> details</a></td>")
   output["aaData"].append(row)

print json.dumps(output)
