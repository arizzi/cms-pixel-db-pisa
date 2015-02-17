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
filename="test.json"
os.path.isfile(filename)
t= None
i=0
import json
with open(filename, 'rb') as f:
   i+=1
   for row in f :
	 wj=json.loads(row	)
	 if True :
		CENTER=wj["TEST_CENTER"]
                dd=datetime.strptime(wj["TEST_DATE"],"%Y-%m-%d %H:%M:%S")
                s = pdb.insertSession(Session(OPERATOR="n/a", CENTER=CENTER, DATE=dd, TYPE="ROCTEST",  COMMENT=wj["COMMENT"]))
		rocid=wj["ROC_ID"]	
		h = pdb.getRoc(unicode(rocid))
		if not h:
			  fields=re.split("-",rocid)
			  waferid=fields[0]
			  position=fields[1]
	        	  print "Roc %s is new, inserting it...with waferid %s" % (rocid,waferid)
			  t = pdb.insertTransfer(Transfer("FACTORY",CENTER.upper()))
	   	          h = Roc(WAFER_ID=waferid, TRANSFER_ID=t.TRANSFER_ID, COMMENT=wj["COMMENT"],ROC_POSITION=position,ROC_ID=rocid,STATUS="INSTOCK")  
	                  if  pdb.insertRoc(h) :
       		               print "OK<br>"
               		  else :
                        	print "FAILED<br>"
	       
	        if h :
			wg=wj
			te=Test_Roc(SESSION_ID=s.SESSION_ID, ROC_ID=rocid, RESULT=wj["RESULT"],  V24=wj["V24"], IANA=wg["IANA"], IDIGI=wg["IDIGI"], 
		VDAC=-1, DEFECTPIXELS=wg["DEFECTPIXELS"], ADDRPIXELS=wg["ADDRPIX"], TRIMPIXELS=wg["TRIMPIXELS"], MASKPIXELS=wg["MASKPIXELS"], NSIGPIXELS=wg["NSIGPIXELS"],NOISEPIXELS=wg["NOISEPIXELS"], 
		THRESHOLDPIXELS=wg["THRESHOLDPIXELS"], PHFAIL=-1, VDCAP=wg["VDCAP"],VDIGU_ADC=wg["VDIGU_ADC"],VANAU_ADC=wg["VANAU_ADC"],VANAR_ADC=wg["VANAR_ADC"],VBG_ADC=wg["VBG_ADC"],IANA_ADC=wg["IANA_ADC"],
		VDIGU_VOLTS=wg["VDIGU_VOLTS"],VANAU_VOLTS=wg["VANAU_VOLTS"],IANA_MILLIAMPS=wg["IANA_MILLIAMPS"],VANASCAN=json.dumps(wg["VANASCAN"]),COMMENT=wj["COMMENT"],DATA_ID=0)
			tt = pdb.insertRocTest(te)
			if tt is None :
				print "RocTest insertion failed"
			else :
				print "Inserted"
#   if i > 2 : 
#	exit(1) 
