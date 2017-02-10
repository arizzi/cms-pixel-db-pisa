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
filename="benedikt.csv"
os.path.isfile(filename)
t= None
i=0
with open(filename, 'rb') as csvfile:
   i+=1
   reader = csv.reader(csvfile, delimiter=',', quotechar='"')
   for row in reader:
	#if row[0].isdigit() and  int(row[0]) > 0 :
                print "ROW",row
		HDI_ID=row[0]
#		BATCH_ID=row[1]
		CENTER="UNIHH"
		TYPEtemp=re.split("-",HDI_ID)[0]
                if (TYPEtemp == '549'):
                   TYPE='547'
                elif (TYPEtemp=='737'):
                   TYPE='813'
                TYPE=row[1]
		COMMENT=''
                STATUS="INSTOCK"
                print "INSERTING", HDI_ID, TYPE, " to ", CENTER
                if True:
		 if not t or t.RECEIVER != CENTER.upper() :
			print "New transfer to " , CENTER
		        t = pdb.insertTransfer(Transfer("FACTORY",CENTER.upper()))
		 h = pdb.getHdi(unicode(HDI_ID))
		 if not h:
	        	  print "HDI %s is new, inserting it..." % HDI_ID
        	          h = Hdi(HDI_ID=HDI_ID, TRANSFER_ID=t.TRANSFER_ID, COMMENT=COMMENT, TYPE=TYPE,STATUS=STATUS)  
	                  if  pdb.insertHdi(h) :
       		               print "OK<br>"
               		  else :
                        	print "FAILED<br>"
   	   	 else :
	               	  print "HDI %s already exists<br>" % HDI_ID

