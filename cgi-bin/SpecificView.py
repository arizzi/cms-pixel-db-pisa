from time import *
import sys
sys.path.append("../PixelDB")

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
  
