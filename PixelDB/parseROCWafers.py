#!/usr/bin/python
import re
import datetime
import os
import glob
import sys
sys.path.append("/home/cmsweb/cms-pixel-db-pisa/PixelDB")
from storm import *
from PixelDB import *
import csv
pdb = PixelDBInterface(operator="webfrontend",center="cern")
pdb.connectToDB()
#filename="/home/cmsweb/First_batch_KIT_Oct14.csv"
filename="wafers.json"
os.path.isfile(filename)
t= None
i=0
import json
with open(filename, 'rb') as f:
   i+=1
   for row in f :
	 wj=json.loads(row	)
	 if True :
		CENTER=wj["PRODCENTER"]
		if not t or t.RECEIVER != CENTER.upper() :
			print "New transfer to " , CENTER
		        t = pdb.insertTransfer(Transfer("FACTORY",CENTER.upper()))
		waferid=wj["WAFERID"]	
		h = pdb.getRocWafer(unicode(waferid))
		if not h:
	        	  print "RocWafer %s is new, inserting it..." % waferid
			  dest="/data/pixels/uploads/RocWafers/%s_wmap_fail.ps" % waferid
			  origin="wafermaps/%s_wmap_fail.ps" %waferid
			  os.system("cp %s %s"%(origin,dest))
		          data = Data(PFNs=dest)
                          pdb.insertData(data)
			  if wj["THICKNESS"] == "" :
				wj["THICKNESS"]=0
        	          h = RocWafer(ROCWAFER_ID=waferid, TRANSFER_ID=t.TRANSFER_ID, COMMENT=wj["COMMENT"],NOM_THICKNESS=wj["THICKNESS"],PRODCENTER=wj["PRODCENTER"], YIELD=wj["YIELD"],N_GOOD=wj["GOOD"],TYPE=wj["ROCTYPE"],DATA_ID=data.DATA_ID,LOT=wj["LOT"],N_ROC=wj["ROCS"],TEST=wj["TEST"])  
	                  if  pdb.insertRocWafer(h) :
       		               print "OK<br>"
               		  else :
                        	print "FAILED<br>"
   	   	else :
	               	  print "ROCWafer %s already exists<br>" % waferid

#   if i > 2 : 
#	exit(1) 
