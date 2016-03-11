#!/usr/bin/env python
# enable debugging
import tempfile
import sys
import cgitb
from datetime import *
import time as tt
cgitb.enable()
from pixelwebui import *
import re
import cgi
form = cgi.FieldStorage() # instantiate only once!


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


import ROOT
t0=1388534400+50*7*86400
t1=1388534400+156*7*86400
t2=(int(tt.time()/(7*86400))+2)*7*86400
gradeA=ROOT.TH1F("A","Grade A",106,t0,t1)
gradeB=ROOT.TH1F("B","Grade B",106,t0,t1)
gradeC=ROOT.TH1F("C","Grade C",106,t0,t1)

o=form.getfirst('objName','FullModule')
center=form.getfirst('center','')
if o == 'FullModule' :
	r=cur.execute("select MAX(GRADE)as GRADE,MAX(TIMESTAMP) as TIMESTAMP from view10 left join test_fullmodulesummary on FULLMODULESUMMARY_ID=test_id left join inventory_fullmodule on view10.FULLMODULE_ID=inventory_fullmodule.FULLMODULE_ID where GRADE is not NULL and view10.STATUS <> 'HIDDEN' and (view10.FULLMODULE_ID like 'M1%' or view10.FULLMODULE_ID like 'M2%' or view10.FULLMODULE_ID like 'M3%' or view10.FULLMODULE_ID like 'M4%' )and BUILTBY like '%"+center+"%' group by view10.FULLMODULE_ID")
elif o == 'BareModule' :
	r=cur.execute("select bmGrade(BAREMODULE_ID) as GRADE,UNIX_TIMESTAMP(BUILTON) as TIMESTAMP from inventory_baremodule where  BUILTBY like '%"+center+"%' ")
elif o == 'FullModuleWHR' :
    r=cur.execute("select MAX(GREATEST(view10.GRADE,A.GRADE))as GRADE,GREATEST(test_fullmodulesummary.TIMESTAMP,S.TIMESTAMP) as TIMESTAMP from view10 left join test_fullmodulesummary on FULLMODULESUMMARY_ID=test_id left join inventory_fullmodule on view10.FULLMODULE_ID=inventory_fullmodule.FULLMODULE_ID left join Test_FullModule_XRay_HR_Summary as S on S.TEST_ID=inventory_fullmodule.LASTTEST_XRAY_HR left join Test_FullModule_XRay_HR_Module_Analysis_Summary as A on S.TEST_ID=A.TEST_XRAY_HR_SUMMARY_ID and S.LAST_PROCESSING_ID=A.PROCESSING_ID where view10.STATUS <> 'HIDDEN' and (view10.FULLMODULE_ID like 'M1%' or view10.FULLMODULE_ID like 'M2%' or view10.FULLMODULE_ID like 'M3%' or view10.FULLMODULE_ID like 'M4%' )and BUILTBY like '%"+center+"%' and GREATEST(view10.GRADE,A.GRADE) is not NULL group by view10.FULLMODULE_ID;")

#r=cur.execute("select GREATEST(MAX_FQ_GRADE,XR_HRGRADE)as GRADE,MAX(TIMESTAMP) as TIMESTAMP from view12 where FM_STATUS <> 'HIDDEN' and (FM_FULLMODULE_ID like 'M1%' or view10.FM_FULLMODULE_ID like 'M2%' or view10.FM_FULLMODULE_ID like 'M3%' or FM_FULLMODULE_ID like 'M4%' )and FM_BUILTBY like '%"+center+"%' group by FM_FULLMODULE_ID")


#print "Content-Type: text/plain"
#print
for x in cur.fetchall() :
#	print x
	gr=x["GRADE"]
	t=int(x["TIMESTAMP"])
	if gr[:1] in ['A','B','C'] :
#	    for i in xrange(t,t1,7*86400) :
	    for i in xrange(int(t/(7*86400))*(7*86400),t2,7*86400) :
		histo=eval("grade"+gr[:1])
		histo.Fill(i)

out = tempfile.NamedTemporaryFile(suffix=".png",delete=False)
ROOT.gStyle.SetPadRightMargin(0.1)
canvas= ROOT.TCanvas("plot","plot",400,300)
#stack
gradeB+=gradeA
gradeC+=gradeB
gradeA.SetFillColor(ROOT.kGreen)
gradeB.SetFillColor(ROOT.kYellow)
gradeC.SetFillColor(ROOT.kRed)
gradeA.SetFillStyle(ROOT.kSolid)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)
gradeC.Draw()
#ROOT.gStyle.SetTimeOffset(ROOT.TDatime(1970,01,01,00,00,00).Convert())
#gradeC.GetYaxis().SetRangeUser(0,2000)
gradeC.GetXaxis().SetTimeDisplay(1)
gradeC.GetXaxis().SetTimeFormat("%m-%Y%F1970-01-01 00:00:01")
gradeB.Draw("same")
gradeA.Draw("same")
canvas.SaveAs(out.name)


f = open(out.name, 'r')
print "Content-Type: image/png"
print
print f.read()
os.unlink(out.name)

