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
hasTrans=False
for c in columns:
   colNames.append(c)
   if c == "TRANSFER_ID" :
	hasTrans = True 	

if objName == "Transfer" :
  hasTrans = False

for r in refs:
   colNames.append(r)

if sortCol != "empty" :

		sOrder = "ORDER BY  "
	        dosort=0
                cols=int(form.getfirst('iSortingCols'))

		for  i in range (0,cols) :
			sortcol= int(form.getfirst("iSortCol_%d"%i))
			if form.getfirst('bSortable_%d'%sortcol) == "true" :
				if hasTrans:
					sortcol-=1
				if dosort !=0 :
					  sOrder+=" , "
				if form.getfirst("sSortDir_%d"%i) == "asc" :
					dosort=1
					if sortcol > 0 or not hasTrans :
						sOrder += colNames[sortcol]+" asc "
					else:
					   if sortcol == 0 :
						sOrder += "RECEIVER asc"
					   else :
						sOrder += colNames[0]	
				else:
					dosort=1
					if sortcol > 0 or not hasTrans :
						sOrder += colNames[sortcol]+" desc "
					else:
					   if sortcol == 0 :
						sOrder += "RECEIVER desc"
					   else :
						sOrder += colNames[0]+" desc"	
		if dosort ==0 :
			sOrder = ""


import MySQLdb

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user=secrets.USER, # your username
                      passwd=secrets.PASSWORD, # your password
                      db="prod_pixel") # name of the data base
cur = db.cursor(MySQLdb.cursors.DictCursor) 

sLimit = ""

if llast != -1 :
  sLimit = "LIMIT %d,%d" %(first,llast)


sWhere = ""
sSearch = form.getfirst("sSearch","")
escapedSearch = escape_string(sSearch)
if sSearch != "" :
		sWhere = "WHERE (";
		for c in columns :
			if sWhere != "WHERE (":
			   sWhere += " OR "	
			sWhere += "%s LIKE '%%%s%%' " % (table+"."+c,escapedSearch)
		if hasTrans:
			sWhere += "OR (transfers.STATUS='ARRIVED' and RECEIVER like '%%%s%%')"% (escapedSearch)
			sWhere += "OR (transfers.STATUS<>'ARRIVED' and (RECEIVER like '%%%s%%' OR SENDER like '%%%s%%') )"% (escapedSearch,escapedSearch)

		sWhere += ')'
#per column filter
percol=""
for  i in range (0,int(form.getfirst('iColumns'))) :
              searchcol= form.getfirst("sSearch_%d"%i,"")
	      colnum=i
	      if hasTrans:
	    	   if colnum > 0 :
			colnum-=1	
	      colname = colNames[colnum]

	      if searchcol != "" :
		  escapedSearch = escape_string(searchcol)
		  if percol!= "" :
			percol += " AND "
		  if i == 0 or colnum > 0 :
			  percol+="%s like '%%%s%%'" % (table+"."+colname,escapedSearch)		   
		  else :	
                        percol += "( (transfers.STATUS='ARRIVED' and RECEIVER like '%%%s%%')"% (escapedSearch)
                        percol += "OR (transfers.STATUS<>'ARRIVED' and (RECEIVER like '%%%s%%' OR SENDER like '%%%s%%') ) )"% (escapedSearch,escapedSearch)

		 
if sWhere != "":
   sWhere += "AND %s" % percol
elif percol != "" :
  sWhere = "WHERE %s" % percol

#print sWhere
colNames = ",".join(columns)
	
#ur.execute("SELECT SQL_CALC_FOUND_ROWSSELECT COUNT(1) FROM  %s"% (table))
#=cur.fetchone()
#ount = l['COUNT(1)']

cur.execute("SELECT COUNT(1) FROM  %s"% (table))
l=cur.fetchone()
count = l['COUNT(1)']
colNamesFull=[]
for cc in columns :
   colNamesFull.append(table+"."+cc)
colNamesFull=",".join(colNamesFull)
if hasTrans :
# 	print "SELECT %s,transfer.RECEIVER,transfer.SENDER,transfer.STATUS FROM %s left join transfers on TRANSFER_ID=transfers.TRANSFER_ID %s %s %s"% (colNamesFull,table,sWhere,sOrder,sLimit)
 	cur.execute("SELECT %s,transfers.RECEIVER,transfers.SENDER,transfers.STATUS as TSTATUS FROM %s left join transfers on %s.TRANSFER_ID=transfers.TRANSFER_ID %s %s %s"% (colNamesFull,table,table,sWhere,sOrder,sLimit))
else:
        cur.execute("SELECT %s FROM %s %s %s %s"% (colNamesFull,table,sWhere,sOrder,sLimit))

output = {}
output["sEcho"] = form.getfirst('sEcho',1)
output["iTotalRecords"] = count
output["iTotalDisplayRecords"] =  count
output["aaData"] = []


  

for o in cur.fetchall() :
   row = []
#   row.append(o[IDgetattr(o,ID) ,"(<a href=viewdetails.cgi?objName="+objName+"&"+ID+"="+str(getattr(o,ID)),">details</a>|<a href=writers/edit.cgi?objName="+objName+"&"+ID+"="+str(getattr(o,ID)),">edit</a>)</td>"
   row.append( "%s"%(o[ID])+"(<a href=\"viewdetails.cgi?objName="+objName+"&"+ID+"="+"%s"%(o[ID])+"\">details</a>|<a href=\"writers/edit.cgi?objName="+objName+"&"+ID+"="+"%s"%(o[ID])+"\">edit</a>)")
#   row.append( o[ID]+"(<a href=viewdetails.cgi?objName="+objName+"&"+ID+"="+o[ID]+">details</a>)")
   if hasTrans:
#	cur.execute("SELECT RECEIVER,SENDER,STATUS from transfers where TRANSFER_ID = %s"% (o["TRANSFER_ID"]))
#	r=cur.fetchone()
	if o["TSTATUS"] == "ARRIVED" :
		row.append(o["RECEIVER"])
	else:
		row.append("%s to %s"%(o["SENDER"],o["RECEIVER"]))
   for c in columns:
     row.append("%s"%o[c])	
   for r in refs:
     row.append("<a href=\"viewdetails.cgi?objName="+objName+"&"+ID+"="+"%s"%(o[ID])+"&ref="+r+"\"> details</a></td>")
   output["aaData"].append(row)

print json.dumps(output)
