from time import *
import sys
sys.path.append("../PixelDB")
import operator

from PixelDB import *
import cgi
import re
from GenericView import *


def specificView(objName,form,pdb) :
   if objName == "BareModule" :
     bm = pdb.getBareModule(cgi.escape(form.getfirst('BAREMODULE_ID', 'empty')))
     if bm : 
       print "<H1> BareModule %s </h1>" % cgi.escape(form.getfirst('BAREMODULE_ID', 'empty'))
       print "ROCS:<br>"	 
       print "<table border=1 cellpadding=2>"
#       for i in range(0,16) : 
       rocs= bm.ROC_ID.split(",")
       for roc in rocs :
  	  columns = defaultSortedColumns("Roc")
	  print "<tr>"
          for c,r in columns:
            v=roc
	    if v == "" : 
		v=  "n/a"
           # help(roc) #getattr(roc,c)
	    if type(v).__name__ == "unicode" : 
     	        st = v.encode('utf-8')
    	    else :
      		st = v

   	    if r :
     		 print "<td><a href=\"viewdetails.cgi?objName=Roc&ROC_ID="+str(getattr(o,ID))+"&ref="+r+"\">%s</a></td>" % (st)
            else :
                 print "<td>%s</td>" % (st)
            
       print "</table>"		

   if objName == "Data" :
	 dataID=cgi.escape(form.getfirst('DATA_ID', 'empty'))
	 data = pdb.getData(int(dataID))
	 m=re.match("file:/home/(.*)/dropbox/(.*)",data.PFNs)
	 if m :
		print "<h1> Input file %s </h1>" % m.group(2)
		print "<a href=/data/pixels/centerinputs/%s/%s>Download file </a>" %(m.group(1),m.group(2))
         else: 
		files=re.split(",",data.PFNs)
		for f in files:
   		 	m=re.match("file:(/data/pixels/.*(jpg|png|gif|bmp))",f)
			if m :
			     print f+"<br><img src=%s><hr>" % m.group(1)	
			
			
   if objName == "Sensor" :
         sensorid=cgi.escape(form.getfirst('SENSOR_ID', 'empty'))
         tl = ""
         if sensorid != "empty" :
                  tests = pdb.store.find(Test_IV,Test_IV.SENSOR_ID==unicode(sensorid))
                  for t in tests :
                    tl+="test=%s&" % t.TEST_ID
         if tl != "" :
                print "<img src=iv.cgi?%s>" %tl
                print "<img src=iv.cgi?%slog=0&fixrange=1><br>" %tl

   if objName == "Wafer" :
	 waferid=cgi.escape(form.getfirst('WAFER_ID', 'empty'))
         tl = ""
       	 if waferid != "empty" : 
	    sensors = pdb.store.find(Sensor,Sensor.WAFER_ID==unicode(waferid))
	    for s in sensors:
		  tests = pdb.store.find(Test_IV,Test_IV.SENSOR_ID==s.SENSOR_ID)
		  for t in tests :
		    tl+="test=%s&" % t.TEST_ID
	 if tl != "" :
	        print "<img src=iv.cgi?%s><br>" %tl
   if objName == "Test_IV" :
	 testid=cgi.escape(form.getfirst('TEST_ID', 'empty'))
       	 if testid != "empty" : 
            print "<img src=iv.cgi?test=%s><br>" % testid

   if objName == "FullModule" :
	  moduleID=cgi.escape(form.getfirst('FULLMODULE_ID', 'empty'))
          fm = pdb.getFullModule(unicode(moduleID))
            
          print "<H1>Module ID: %s</h1>" % moduleID
          printTable([fm],"FullModule","FULLMODULE_ID","details","cellspacing=0 cellpadding=2 border=1")
          tests = fm.tests
#  summaries = fm.summaries
          for test in tests : 
             print "<h2> Test at %s on %s</h2>" % (test.TEMPNOMINAL,strftime("%d/%m/%Y %H:%M", localtime(float(test.TIMESTAMP))))
             columns,refs,refset = getAllPrintableFields("Test_FullModuleAnalysis")
             print "<!-- %s -->" % columns
	     printTableHeader("Test_FullModuleAnalysis",columns,refs,("table_%s" % test.TEMPNOMINAL),"cellspacing=0 cellpadding=2 border=1")
             for ana in test.analyses :
	       printObject(ana,"TEST_ID",columns,refs,"Test_FullModuleAnalysis")
	     printTableFooter()
#	     print "<img src=%s%s%s.gif><br>" % (re.sub("\n","",re.sub("file:","",ana.data.PFNs)),moduleID,test.TEMPNOMINAL) #file:/data/OUT/M0289/1.1/T+17a/ M0289T+17a.gif
	     print "<iframe width=900 height=600 src=\"%s/TestResult.html\" ></iframe>" % (re.sub("\n","",re.sub("file:","",ana.data.PFNs))) #file:/data/OUT/M0289/1.1/T+17a/ M0289T+17a.gif
               
#             print "Grade: %s" % ana.GRADE 	
#	     print test.CKSUM
#	     print "oo",test.data.URLs
#	     print "aa",test.analyses
#          for summary in summaries : 
#	     print "ii",summary.data.PFNs

   if objName == "Test_FullModuleAnalysis" :
          ana = pdb.store.find(Test_FullModuleAnalysis, Test_FullModuleAnalysis.TEST_ID==int(cgi.escape(form.getfirst('TEST_ID', 'empty')))).one()
	  path=re.sub("file:","",ana.data.PFNs)
          print "<a href=%s>output results</a>" % path
          #>M0178T-10a.gif"


   if objName == "Test_Hdi_Electric" :
	 ele =  pdb.store.find(Test_Hdi_Electric,Test_Hdi_Electric.TEST_ID==int(cgi.escape(form.getfirst('TEST_ID', 'empty')))).one()
         if ele :
		ele.init_maps()
		print "<table border=1><tr><td></td>"
		for ch,i in sorted(ele.CHANNEL_MAP.items(), key=operator.itemgetter(1),reverse=True) :
			print "<td>%s</td>" % ch
		print "</tr>"
		for test,i in sorted(ele.TEST_MAP.items(), key=operator.itemgetter(1)) :
			print "<tr><td>%s</td>"%(test)
			for ch,j in sorted(ele.CHANNEL_MAP.items(), key=operator.itemgetter(1)):
				if ele.getBit(test,ch) == 'NULL' :
					print "<td bgcolor=yellow>n/a</td>"
				if ele.getBit(test,ch) == 'PASS' :
					print "<td bgcolor=green>OK</td>"
				if ele.getBit(test,ch) == 'FAIL' :
					print "<td bgcolor=red>FAIL</td>"
				
			print "</tr>"



   return 0


def defaultSortedColumns(objName) :
    if objName == "FullModule" :
       return [("BAREMODULE_ID","baremodule"),("STATUS",0),("BUILTON",0),("HDI_ID","hdi")]
    if objName == "BareModule" :
       return [("SENSOR_ID","sensor"),("STATUS",0),("BUILTON",0)]
    if objName == "Roc" :
       return [("ROC_ID",0)]
#    if objName == "FullModuleAnalysis" :
#       return  ['THRESHDEFPIXELS', 'MACRO_VERSION', 'PHCAL', 'I150', 'BUMPDEFPIXELS', 'CYCLING', 'PEDESTALDEFPIXELS', 'PAR1DEFPIXELS', 'DATA_ID', 'FULLMODULETEST_ID', 'TEMPERROR', 'TCYCLVALUE', 'I150_2', 'DEADPIXELS', 'TRIMDEFPIXELS', 'ROCSWORSEPERCENT', 'NOISYPIXELS', 'IVSLOPE', 'CURRENT', 'TEST_ID', 'ADDRESSDEFPIXELS', 'GRADE', 'HOSTNAME', 'TCYCLERROR', 'TEMPVALUE', 'CURRENT_2', 'GAINDEFPIXELS', 'TRIMMING', 'MASKEDPIXELS'] 
  
