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
table=objType.__storm_table__
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
llast = form.getfirst("iDisplayLength", "-1")
first = int(cgi.escape(first))
llast= int(cgi.escape(llast))


sortCol = form.getfirst("iSortCol_0","empty")

objString = "objects"

colNames=[]
colNames.append(ID)
for c in columns:
   colNames.append(c)
for r in refs:
   colNames.append(r)

if sortCol != "empty" :

		sOrder = "ORDER BY  "
	        dosort=0
                cols=int(form.getfirst('iSortingCols'))

		for  i in range (0,cols) :
			sortcol= int(form.getfirst("iSortCol_%d"%i))
			if form.getfirst('bSortable_%d'%sortcol) == "true" :
				if dosort !=0 :
					  sOrder+=" , "
				if form.getfirst("sSortDir_%d"%i) == "asc" :
					dosort=1
					sOrder += colNames[sortcol]+" asc "
				else:
					dosort=1
					sOrder += colNames[sortcol]+" desc "
		if dosort ==0 :
			sOrder = ""


import MySQLdb

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user=secrets.USER, # your username
                      passwd=secrets.PASSWORD, # your password
                      db="prod_pixel") # name of the data base
cur = db.cursor(MySQLdb.cursors.DictCursor) 

colNames = ",".join(columns)
sLimit = ""

if llast != -1 :
  sLimit = "LIMIT %d,%d" %(first,llast)


sWhere = ""
sSearch = form.getfirst("sSearch","empty")
escapedSearch = escape_string(sSearch)
if sSearch != "empty" :
		sWhere = "WHERE (";
		for c in columns :
			if sWhere != "WHERE (":
			   sWhere += " OR "	
			sWhere += "`%s` LIKE '%%%s%%' " % (c,escapedSearch)
		sWhere += ')'
	
#ur.execute("SELECT SQL_CALC_FOUND_ROWSSELECT COUNT(1) FROM  %s"% (table))
#=cur.fetchone()
#ount = l['COUNT(1)']

cur.execute("SELECT COUNT(1) FROM  %s"% (table))
l=cur.fetchone()
count = l['COUNT(1)']

cur.execute("SELECT %s FROM %s %s %s %s"% (colNames,table,sWhere,sOrder,sLimit))

output = {}
output["sEcho"] = form.getfirst('sEcho',1)
output["iTotalRecords"] = count
output["iTotalDisplayRecords"] =  count
output["aaData"] = []


  

for o in cur.fetchall() :
   row = []
   row.append( o[ID]+"(<a href=viewdetails.cgi?objName="+objName+"&"+ID+"="+o[ID]+">details</a>)")
   for c in columns:
     row.append("%s"%o[c])	
   for r in refs:
     row.append("<a href=\"viewdetails.cgi?objName="+objName+"&"+ID+"="+o[ID]+"&ref="+r+"\"> details</a></td>")
   output["aaData"].append(row)

print json.dumps(output)
