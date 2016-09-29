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
#filename="/home/cmsweb/First_batch_KIT_Oct14.csv"
#filename="/home/cmsweb/HDIsfromHH-2015-09-09.csv"
#filename="/home/cmsweb/Hi1530-box1-68.csv"
filename="/home/cmsweb/2016-04-21-1208.csv"
os.path.isfile(filename)
t= None
i=0
with open(filename, 'rb') as csvfile:
   i+=1
   reader = csv.reader(csvfile, delimiter=',', quotechar='"')
   for row in reader:
	#if row[0].isdigit() and  int(row[0]) > 0 :
		HDI_ID=row[0]
		BATCH_ID=row[1]
		CENTER=row[2]
		TYPE=row[3]
		COMMENT=row[4]
		if not t or t.RECEIVER != CENTER.upper() :
			print "New transfer to " , CENTER
		        t = pdb.insertTransfer(Transfer("FACTORY",CENTER.upper()))
		h = pdb.getHdi(unicode(HDI_ID))
		if not h:
	        	  print "HDI %s is new, inserting it..." % HDI_ID
        	          h = Hdi(HDI_ID=HDI_ID, TRANSFER_ID=t.TRANSFER_ID, BATCH_ID=BATCH_ID,COMMENT=COMMENT, TYPE=TYPE,STATUS='INSTOCK')  
	                  if  pdb.insertHdi(h) :
       		               print "OK<br>"
               		  else :
                        	print "FAILED<br>"
   	   	else :
	               	  print "HDI %s already exists<br>" % HDI_ID

#   if i > 2 : 
#	exit(1) 
