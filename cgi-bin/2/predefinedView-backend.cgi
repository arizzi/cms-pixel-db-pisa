#!/usr/bin/env python
# enable debugging
import sys
import cgitb
from datetime import *
cgitb.enable()
from pixelwebui import *
import re
import cgi
import json
sys.path.append("../PixelDB")
#from storm.properties import *
#from storm.references import *
#from storm import *
from PixelDB import *
#import random
from operator import itemgetter, attrgetter

form = cgi.FieldStorage() # instantiate only once!
print "Content-Type: text/plain"
print

from  predefinedViews import *
viewNumber = int(form.getfirst('viewNumber', '0'))
if viewNumber >= len(columns) :
  exit(1)

col=columns[viewNumber]
tab=tables[viewNumber]
join=joins[viewNumber]

pdb = PixelDBInterface(operator="webfrontend",center="cern")
pdb.connectToDB()

allresults = pdb.store.find( eval(tab), eval(join))

first = form.getfirst("iDisplayStart", "0")
llast = form.getfirst("iDisplayLength", "-1")
first = int(cgi.escape(first))
llast= int(cgi.escape(llast))


sortCol = form.getfirst("iSortCol_0","empty")
results=[]
for o in allresults :
	match = True
	r=[]
	for  i in range (0,int(form.getfirst('iColumns'))) :
          searchcol= form.getfirst("sSearch_%d"%i,"")
          c,e = col[i]		   
	  if searchcol : 
              escapedSearch = escape_string(searchcol)
	      if not re.match(escapedSearch,eval(e)) :	
		match = False
	  r.append(eval(e))
	if match :
		results.append(r)

output = {}
output["sEcho"] = form.getfirst('sEcho',1)
output["iTotalRecords"] = allresults.count()
output["iTotalDisplayRecords"] =  len(results)
output["aaData"] = []
i=0
if sortCol != 'empty' :
 thesort=int(sortCol)
 results.sort(key=itemgetter(thesort)) 
	
for o in results :
  if i >= first and i <first+llast :
#     row = []
#     for (c,e) in col :
#	   row.append(eval(e))
     output["aaData"].append(o)
  i+=1

print json.dumps(output)




