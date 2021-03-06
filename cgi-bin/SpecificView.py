from time import *
import sys
sys.path.append("../PixelDB")
import operator

from PixelDB import *
import cgi
import re
from GenericView import *
colorRoc={}
#colorRoc[1]="#00AA00"
#colorRoc[2]="#00FF00"
#colorRoc[3]="#008800"
#colorRoc[4]="#0000FF"
#colorRoc[5]="#FF0000"
colorRoc[1]="#00FF00"
colorRoc[2]="#0000FF"
colorRoc[3]="#AA00AA"
colorRoc[4]="#FFFF00"
colorRoc[5]="#FF0000"

def specificView(objName,form,pdb) :
   rocMap=[[7,6,5,4,3,2,1,0],[8,9,10,11,12,13,14,15]]
   if objName == "BareModule" :
     bm = pdb.getBareModule(cgi.escape(form.getfirst('BAREMODULE_ID', 'empty')))
     if bm : 
       print "<H1> BareModule %s </h1>" % cgi.escape(form.getfirst('BAREMODULE_ID', 'empty'))
       print "ROCS:<br>"	 
       print "<table border=1 cellpadding=2>"
#       for i in range(0,16) : 
       rocs= bm.ROC_ID.split(",")
       for row in rocMap :
	 print "<tr>"
	 for col in row :
	    if  len(rocs) > col : 
               roc=rocs[col]      
	    else :
		roc="n/a"
	    if roc == "" :
		roc="n/a"
		
            print "<td><a href=\"viewdetails.cgi?objName=Roc&ROC_ID=%s\">%s</a>"%(roc,roc)
	 print "<td>cables here</td></tr>"
            
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
   		 	m=re.match("file:(/+data/pixels/.*(jpg|png|gif|bmp))",f)
			if m :
			     print f+"<br><img src=%s><hr>" % m.group(1)	
			else:
   		 	     m=re.match("file:(/+data/pixels/.*)",f)
			     if m :
		 		     print "<a href=%s>%s </a><br>" %(m.group(1),f)
			     else: 
		 		     print "<a href=%s>%s </a><br>" %(f,f)

		
			
			
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

   if objName == "Test_BareModule_QA" :
          ana = pdb.store.find(Test_BareModule_QA, Test_BareModule_QA.TEST_ID==int(cgi.escape(form.getfirst('TEST_ID', 'empty')))).one()
          path=re.sub(",","",ana.data.PFNs)
          print "<img src=%s/bareModuleQA.png>" % path
          #>M0178T-10a.gif"

   if objName == "RocWafer" :
          rocs = pdb.store.find(Roc, Roc.WAFER_ID==unicode(cgi.escape(form.getfirst('ROCWAFER_ID', 'empty'))))
	  r={}
	  for roc in rocs :
			r[roc.ROC_POSITION]=roc
	  print "<table align=center border=1 cellspacing=0 cellpadding=0>"
	  lettermap=['A','C','B','D'] 
	  print "<tr><td></td>"
	  for yy in xrange (0,10) :
		print "<td colspan=1>Y%s" % yy
	  for x in xrange(0,8) :
#	    x=xx/2
	    print "<tr><td> %sX" %(x)
	    for y in xrange(0,10) :
#	      y=yy/2
	     print "<td><table  width=100% border=0>"
	     for xx in xrange(0,2) :
	      print "<tr>"
	      for yy in xrange(0,2) :
	        i=xx%2+yy%2*2
	        p=lettermap[i]
	        key="%s%s%s"%(x,y,p)
		if x==0 and y==0 :
                     print "<td bgcolor=#CCCCCC><font size=+2>"
                     print "%s"%p

	        if key in r :
			if r[key].LASTTEST_ROC :
  	      			print "<td bgcolor=%s><font size=+2>"%(colorRoc[r[key].lasttest_roc.RESULT])
				print "&nbsp;%s&nbsp;"%r[key].lasttest_roc.RESULT
			else : 
				print "<td>X"
	        else:
			print "<td>&nbsp;"
	     print "</table>"
	  print "</table>"
#          path=re.sub(",","",ana.data.PFNs)
#          print "<img src=%s/bareModuleQA.png>" % path
	

   if objName == "Test_Hdi_Electric" :
	 ele =  pdb.store.find(Test_Hdi_Electric,Test_Hdi_Electric.TEST_ID==int(cgi.escape(form.getfirst('TEST_ID', 'empty')))).one()
         if ele :
		ele.init_maps()
		print "<table border=1><tr><td></td>"
		for ch,i in sorted(ele.CHANNEL_MAP.items(), key=operator.itemgetter(1)) :
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
  
