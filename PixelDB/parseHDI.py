#!/usr/bin/python
from openpyxl import load_workbook
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
filename="/home/cmsweb/HDI-inventory.csv"
os.path.isfile(filename)
with open(filename, 'rb') as csvfile:
   reader = csv.reader(csvfile, delimiter=',', quotechar='"')
   for row in reader:
	if row[0].isdigit() and  int(row[0]) > 0 :
		HDI_ID=row[0]
		BATCH_ID=row[1]
		CENTER=row[2]
		COMMENT=row[4]
	        t = pdb.insertTransfer(Transfer("FACTORY",CENTER))
		h = pdb.getHdi(unicode(HDI_ID))
		if not h:
	        	  print "HDI %s is new, inserting it..." % HDI_ID
        	          h = Hdi(HDI_ID=HDI_ID, TRANSFER_ID=t.TRANSFER_ID, BATCH_ID=BATCH_ID,COMMENT=COMMENT)  
	                  if pdb.insertHdi(h) :
       		               print "OK<br>"
               		  else :
                        	print "FAILED<br>"
   	   	else :
	               	  print "HDI %s already exists<br>" % HDI_ID

