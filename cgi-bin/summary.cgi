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
	'TEST':"fill:rgb(255,190,0)",
	'HIDDEN':"fill:rgb(255,190,100)",
	'BROKEN':"fill:rgb(255,0,0)",
	'INSTOCK':"fill:rgb(0,255,0)",
	'PACTECHLOSTNAM':"fill:rgb(255,255,0)",
	'ASSEMBLED_BARE':"fill:rgb(0,190,0)",
}
inventories=["roc","sensor","hdi","baremodule","fullmodule"]
sortedcats=['USED','ASSEMBLED_BARE','INSTOCK','BROKEN']
targets={"roc":40000,"sensor":2000,"hdi":2000,"baremodule":2000,"fullmodule":2000}
inv={}


def pretty(x) :
	r=""
	c=sortedcats
        for cat in x:
               if cat not in c :
                        c.append(cat)
        for cat in c :
		if cat in x:
			r+="<svg width=30 height=15><rect width=30 height=15 style=%s></svg>%s: %s , "%(style.get(cat,"fill:rgb(128,128,128)"),cat,x[cat])	
	return r


def printStock(sWhere="") :
    for i in inventories :
	cur.execute("select COUNT(1),A.STATUS as STATUS from inventory_"+i+" as A left outer join transfers as B on A.TRANSFER_ID = B.TRANSFER_ID  "+sWhere+" group by STATUS")
	inv[i]={}
	for l in cur.fetchall():
		inv[i][l["STATUS"]]=l["COUNT(1)"]
#print inv
    print "<table border=0>"

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
	print "</svg></td><td>%s Total in DB: %s</td>"%(pretty(inv[i]),t)
    print "</table>"

print "<h1> Stock status </h1>"
printStock()
#printStock(" where RECEIVER='PISA' or RECEIVER='BARI' or RECEIVER='CATANIA'")
