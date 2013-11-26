#!/usr/bin/env python
import sys
# enable debugging
import cgitb
from datetime import *
cgitb.enable()
import re
import cgi
sys.path.append("../PixelDB")

from PixelDB import *
from storm.properties import *
from storm.references import *
from storm import *

legalNames = ["Transfer","Data","Session","Roc","Batch","Wafer","Sensor","BareModule","Hdi","Tbm","FullModule","Logbook","Test_BareModule","Test_FullModuleSession","Test_FullModuleSummary","Test_FullModule","Test_FullModuleAnalysis","Test_Tbm","Test_Hdi","Test_Roc","Test_IV","Test_IT","Test_SensorInspection","Test_BareModuleInspection","Test_BareModule_Chip","Test_CV","History"]
def parseObjName(objName) :
    for name in legalNames:
     if objName == name :
       return name
    return "empty"

def getAllPrintableFields(objName) : 
	columns = []
	refs = []
	refsets = []
        objType = eval(parseObjName(objName))
	i =0 
	#type(eval(objName+".FULLMODULE_ID")).__name__
	keys=objType.__dict__.keys()
	for attr in keys:
	#    print attr,type(eval(objName+"."+attr)).__name__,"<br>"
	#    print attr,type(eval(objName+"."+attr)).__name__," || " 
	    if  type(eval(objName+"."+attr)) is properties.PropertyColumn or  type(eval(objName+"."+attr)).__name__ == "date"  or  type(eval(objName+"."+attr)).__name__ == "datetime":
	        columns.append(attr) 

	    if  type(eval(objName+"."+attr)) is references.ReferenceSet :
                 refsets.append(attr)

	    if  type(eval(objName+"."+attr)) is references.Reference  :
	         refs.append(attr)
        return (columns,refs,refsets)   

def printTableHeader(ID,columns,refs,tableid,options="") :       
    print "<table id=\"%s\" width=\"100%%\" %s>" % (tableid,options)
    print " <thead> <tr>"
    print "<th> ",ID," </th>"
    for c in columns:
      print "<th>",c.lower().capitalize(),"</th>"
    for r in refs:
      print "<th>", r.lower().capitalize(),"</th>"
    print "</thead></tr><tbody>"

def printObject(o,ID,columns,refs,objName):
   print "<tr>"
   print "<td>", getattr(o,ID) ,"(<a href=viewdetails.cgi?objName="+objName+"&"+ID+"="+str(getattr(o,ID)),">details</a>)</td>"
   for c in columns:
    v=getattr(o,c)
    if type(v).__name__ == "unicode" : 
      print "<td>",unicode(v),"</td>"
    else :
      print "<td>",v,"</td>"
   for r in refs:
    print "<td><a href=\"viewdetails.cgi?objName="+objName+"&"+ID+"="+str(getattr(o,ID))+"&ref="+r+"\"> details</a></td>"
#    help(getattr(o,r))
   print "</tr>"

def printTableFooter():
    print "</tbody><tfoot></tfoot></table>"


def printTable(objects,objName,ID,tableid,options=""):
   columns,refs,refset = getAllPrintableFields(objName)
   printTableHeader(ID,columns,refs,tableid,options)
   for o in objects :
     printObject(o,ID,columns,refs,objName)
   printTableFooter()

