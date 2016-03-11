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


from  rawPredefinedViews import *

objName = form.getfirst('objName', 'empty')
ss=True
if objName == 'empty' :
        viewNumber = int(form.getfirst('viewNumber', '0'))
        if viewNumber >= len(columns) :
                exit(0)
        else:
		cols=columns[viewNumber]
		query=queries[viewNumber]
		countquery=countqueries[viewNumber]
		rowkey=rowkeys[viewNumber]
		sGroup=groupby.get(viewNumber,' ')
		ss=(customServerSide.get(viewNumber,"true") == "true" )
else:
	viewNumber=-1
        objName = parseObjName(cgi.escape(objName))
	draw= (form.getfirst('draw', '0') == '1')
        rowkey,cols,query,countquery = fromObjectName(objName,draw)
	sGroup=groupby.get(objName,' ')

dbname="prod_pixel"
if objName in tier0Objects  or viewNumber in tier0Views :
	dbname="test_tier0"
exactSearch = form.getfirst('exact',0)


import json

sys.path.append("../PixelDB")

from storm.properties import *
from storm.references import *
from storm import *
from PixelDB import *
import random



debug = form.getfirst("debug", "0")
#debug="1"
if debug == "1" :
	print ss
all = form.getfirst("all", "0")
first = form.getfirst("iDisplayStart", "0")
llast = form.getfirst("iDisplayLength", "-1")
first = int(cgi.escape(first))
llast= int(cgi.escape(llast))
if all == "1" :
	first = 0
	llast = -1

sortCol = form.getfirst("iSortCol_0","empty")
colNames=[]
for c in cols :
	colNames.append(c[1])

if debug == "1":
	print cols
	print "COLNAMESSSSSSSSSSSSSSS",colNames

sOrder = ""
if sortCol != "empty" :
		sOrder = "ORDER BY  "
	        dosort=0
                ncols=int(form.getfirst('iSortingCols',0))
		for  i in range (0,ncols) :
			sortcol= int(form.getfirst("iSortCol_%d"%i))
			if form.getfirst('bSortable_%d'%sortcol,"true") == "true" :
				if dosort !=0 :
					  sOrder+=" , "
				if form.getfirst("sSortDir_%d"%i,"asc") == "asc" :
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
                      db=dbname) # name of the data base
cur = db.cursor(MySQLdb.cursors.DictCursor) 

sLimit = ""

if llast != -1 :
  sLimit = "LIMIT %d,%d" %(first,llast)

sWhere = ""
sSearch = form.getfirst("sSearch","")
escapedSearch = escape_string(sSearch)
if sSearch != "" :
                sWhere = "AND (";
                for c in colNames :
		     if c != "" and c is not None :
                        if sWhere != "AND (":
                           sWhere += " OR "
                        sWhere += "%s LIKE '%%%s%%' " % (c,escapedSearch)
#                if hasTrans:
 #                       sWhere += "OR (transfers.STATUS='ARRIVED' and RECEIVER like '%%%s%%')"% (escapedSearch)
 #                       sWhere += "OR (transfers.STATUS<>'ARRIVED' and (RECEIVER like '%%%s%%' OR SENDER like '%%%s%%') )"% (escapedSearch,escapedSearch)

                sWhere += ')'
percol=""
for  i in range (0,int(form.getfirst('iColumns',0))) :
              searchcol= form.getfirst("sSearch_%d"%i,"")
              colnum=i
              colname = colNames[colnum]

              if searchcol != "" :
                  escapedSearch = escape_string(searchcol)
                  if percol!= "" :
                        percol += " AND "
		  if exactSearch == "1":
	                 percol+="%s like '%s'" % (colname,escapedSearch)                   
		  else:
	                 percol+="%s like '%%%s%%'" % (colname,escapedSearch)                   

                 
if sWhere != "" and percol!= "":
   sWhere += "AND %s" % percol
elif percol != "" :
  sWhere = " AND %s" % percol
if debug == "1" :
	print countquery

count = -1
if ss :
  cur.execute(countquery)
  l=cur.fetchone()
  count = l['COUNT(1)']
colString=""
for c in colNames :
     if c!= '' :
	if colString !="" :
		colString+=","
	cc=re.sub('\.','_',c)
	cc=re.sub('\(','_',cc)
	cc=re.sub(',','_',cc)
	cc=re.sub('\)','_',cc)
	cc=re.sub('\+','_',cc)
	colString+="%s as %s"%( c,cc)

if debug == "1" :
	print "COUNTSTRING: %s %s %s %s"% ((query%" count(1) "),sWhere,sGroup,sOrder)

countdisplay=-1
if ss :
  try :
    countdisplay=cur.execute("%s %s %s %s "% ((query%" count(1) "),sWhere,sGroup,sOrder))
  except :
    countdisplay=cur.execute("%s "% (query%"count(1)"))

if countdisplay == 1 :
	totdis =  cur.fetchone()['count(1)']
elif countdisplay > 1:
	totdis= countdisplay
else: 
	totdis = 0

if debug == "1" :
	print "QUERY:%s %s %s %s %s"% ((query%colString),sWhere,sGroup,sOrder,sLimit)
cc=cur.execute("%s %s %s %s %s"% ((query%colString),sWhere,sGroup,sOrder,sLimit))

if count==-1 : 
	if debug == "1" :
		print "COUNTTTTTT " , cc,count,totdis
	totdis=cc
	count=cc
	

output = {}
output["sEcho"] = form.getfirst('sEcho',1)
output["iTotalRecords"] = count
#output["iTotalDisplayRecords"] =  countdisplay
output["iTotalDisplayRecords"] = totdis
output["aaData"] = []
for i,(c,rn,ev) in enumerate(cols) :
            rn=re.sub('\.','_',rn)
            rn=re.sub('\(','_',rn)
            rn=re.sub(',','_',rn)
            rn=re.sub('\)','_',rn)
            rn=re.sub('\+','_',rn)
            cols[i]=(c,rn,ev)

for o in cur.fetchall() :
   i=0
   row = {}
   for c,rn,ev in cols :
      if ev != "NOPRINT":
#       rn=re.sub('\.','_',rn)
#       rn=re.sub('\(','_',rn)
#       rn=re.sub(',','_',rn)
#       rn=re.sub('\)','_',rn)
#rn=re.sub('\+','_',rn)

	oo=o[rn] if rn in o else None
	if ev == '' :
		row[i]="%s"%o[rn]
	else :
                if debug=="1":
                  print "EEEEEEEVVVVVVV   ",ev
                row[i]=eval(ev)
                if debug=="1":
                   print "AFTER"
	i+=1
   row["DT_RowId"]=o[rowkey]
   output["aaData"].append(row)

print json.dumps(output)
