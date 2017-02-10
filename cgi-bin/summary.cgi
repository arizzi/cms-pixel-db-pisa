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
print "Content-Type: text/html"
print
print "<html>\n        <head>\n         "
print '<link rel="stylesheet" type="text/css" href="/frames.css" />'
print "<body><main>"


from  rawPredefinedViews import *

import json

sys.path.append("../PixelDB")

from storm.properties import *
from storm.references import *
from storm import *
from PixelDB import *
import random
import MySQLdb
db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user=secrets.USER, # your username
                      passwd=secrets.PASSWORD, # your password
                      db="prod_pixel") # name of the data base
cur = db.cursor(MySQLdb.cursors.DictCursor) 
style={
	'USED':"fill:rgb(0,190,0)",
	'MOUNTED':"fill:rgb(0,190,0)",
	'TEST':"fill:rgb(255,190,0)",
	'HIDDEN':"fill:rgb(255,190,100)",
	'BROKEN':"fill:rgb(255,0,0)",
	'INSTOCK':"fill:rgb(0,255,0)",
	'PACTECHLOSTNAM':"fill:rgb(255,255,0)",
	'ASSEMBLED_BARE':"fill:rgb(0,190,0)",
}
inventories=["roc","sensor","hdi","baremodule","fullmodule"]
sortedcats=['USED','MOUNTED','ASSEMBLED_BARE','INSTOCK','BROKEN']
targets={"roc":32000,"sensor":2000,"hdi":2000,"baremodule":2000,"fullmodule":2000}
inv={}


def pretty(x) :
	r=""
	c=sortedcats
        for cat in x:
               if cat not in c :
                        c.append(cat)
        for cat in c :
		if cat in x:
			r+="<svg width=10 height=10><rect width=10 height=10 style=%s></svg>%s:&nbsp;%s<br>  "%(style.get(cat,"fill:rgb(128,128,128)"),cat,x[cat])	
	return r

def builders(table) :
	cur.execute("select BUILTBY from %s where status <> 'TEST' and status <> 'HIDDEN' group by builtby"%table)
	res=[]
	for l in cur.fetchall():
		res.append(l["BUILTBY"])
	return res

def printStock(sWhere="") :
    for i in inventories :
	cur.execute("select COUNT(1),A.STATUS as STATUS from inventory_"+i+" as A left outer join transfers as B on A.TRANSFER_ID = B.TRANSFER_ID  "+sWhere+" group by STATUS")
	inv[i]={}
	for l in cur.fetchall():
		inv[i][l["STATUS"]]=l["COUNT(1)"]
#print inv
    print "<table border=1 cellpadding=0 cellspacing=0 width=900>"

    for i in inventories :
	target=targets[i]
	print "<tr><td>"+i.upper()+"</td><td><svg width=500 height=50>"
	t=0
	c=sortedcats;
	for cat in inv[i] :
		if cat not in c :
			c.append(cat)
	for cat in c :
  	    if cat in inv[i]:
		n=inv[i][cat]
		x=t*300/target
		t+=n
		w=n*300/target
		print "<rect height=30 width=%s x=%s style=%s />"%(w,x,style.get(cat,"fill:rgb(128,128,128)"))
#	print "<img src=aa height=20 width=%s>"%((target-t)*300/target)
	print "<text x=300 y=45 >%s</text>"%(target)
	print "<line x1=300 y1=35 x2=300 y2=0 style='stroke:rgb(0,0,0);stroke-width:2;stroke-dasharray:5,5'/>"
	print "</svg></td><td><font size=2>%s<b>Total in DB: %s</b></td>"%(pretty(inv[i]),t)
    print "</table>"

def drawProd() :
#select grade,timestamp from view10 left join test_fullmodulesummary on FULLMODULESUMMARY_ID=test_id
	cur.execute("select grade,timestamp from view10 left join test_fullmodulesummary on FULLMODULESUMMARY_ID=test_id and STATUS <> 'HIDDEN'")
	for l in cur.fetchall():
		print l	
print "<h1> Stock status </h1>"
print "Dashed line shows needs for 2K modules (no spares, no contingency,etc...) they are not the actual targets.<p>"
printStock()
fmce=builders("inventory_fullmodule")
bmce=builders("inventory_baremodule")
#printStock(" where RECEIVER='PISA' or RECEIVER='BARI' or RECEIVER='CATANIA'")
print "<h1> Module test results </h1>"
print "Grade legend: <font color=green> A(-)</font>"
print "<font color=yellow> B(-)</font>"
print "<font color=red> C</font><p>"
print "<table border=0><tr><td align=center>Bare Modules (x = built on date) </td><td align=center>Full Modules (x = last test date)<br>Series: M1xxx, M2xxx, M3xxx,M4xxx</td><td align=center>FMQ + XRay HR (x = greater of the two test dates)<br>Series: M1xxx, M2xxx, M3xxx,M4xxx</td><</tr>"
print "<tr>"
print "<td align=center> By Center: "
for ce in bmce :
	print "<a href=/cgi-bin/productionPlots.cgi?objName=BareModule&center=%s>%s</a> "%(ce,ce)
print "</td>"
print "<td align=center> By Center: "
for ce in fmce :
	print "<a href=/cgi-bin/productionPlots.cgi?center=%s>%s</a> "%(ce,ce)
print "</td>"
print "<td align=center> By Center: "
for ce in fmce :
	print "<a href=/cgi-bin/productionPlots.cgi?objName=FullModuleWHR&center=%s>%s</a> "%(ce,ce)
print "</td>"

print "</tr>"
print "<tr><td><img src=/cgi-bin/productionPlots.cgi?objName=BareModule>"
print "</td><td><img src=/cgi-bin/productionPlots.cgi></td>"
#https://cmspixelprod.pi.infn.it/cgi-bin/productionPlots.cgi?objName=FullModuleWHR
print "</td><td><img src=/cgi-bin/productionPlots.cgi?objName=FullModuleWHR></td></tr>"
print"</table>"


#printStock()
printFooter()
