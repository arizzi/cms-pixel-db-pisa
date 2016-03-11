tier0Views=[]
customjs={}
customjs2={}
groupby={}
groupheader={}
customServerSide={}
##################################### Automatic object views ######################################
from pixelwebui import *
import datetime
import sys
sys.path.append("../PixelDB")
from storm.properties import *
from storm.references import *
from storm import *
from PixelDB import *
def renderString(column,objName):
	k="%s/%s" %(objName,column)
	if k in renderStrings :
		return renderStrings[k]
	return ''

def fromObjectName(objName,draw=False):
	cols = []
	if objName in  sortedCols :
		cols = sortedCols[objName]
	refs = []
	i =0
	objType = eval(parseObjName(objName))
	ID=idField(objName)
	table=objType.__storm_table__
	keys=objType.__dict__.keys()
	hasTrans=False
	hasSession=False
	for attr in keys:
	    if attr == "TRANSFER_ID" and table!="transfers" :
                hasTrans=True
	    if attr == "SESSION_ID" and table!="sessions" and table!="test_fullmodule" :
                hasSession=True

	#    print attr #,type(eval(objName+"."+attr)).__name__,"<br>"
	    if  type(eval(objName+"."+attr)) is properties.PropertyColumn or  type(eval(objName+"."+attr)).__name__ == "date"  or  type(eval(objName+"."+attr)).__name__ == "datetime":
	#    if  type(eval(objName+"."+attr)) is properties.PropertyColumn :
		 if attr not in cols :
		         cols.append(attr)
	    if  type(eval(objName+"."+attr)) is references.Reference :
	         refs.append(attr)
	cformat=[]
	IDF=table+"."+ID
	IDF2=table+"_"+ID
	#cformat.append((ID,"",'"%s"%(o[ID])+"(<a href=\"viewdetails.cgi?objName="+objName+"&"+ID+"="+"%s"%(o[ID])+"\">details</a>|<a href=\"writers/edit.cgi?objName="+objName+"&"+ID+"="+"%s"%(o[ID])+"\">edit</a>)'")

	#cformat.append((ID,ID,'"%s"%(o["'+ID+'"])+" (<a href=\\\"viewdetails.cgi?objName='+objName+'&'+ID+'="+"%s"%(o["'+ID+'"])+"\\\">details</a>|<a href=\\\"writers/edit.cgi?objName='+objName+'&'+ID+'="+"%s"%(o["'+ID+'"])+"\\\">edit</a>)"'))
	cformat.append((ID,IDF,'"%s"%(o["'+IDF2+'"])+" (<a href=\\\"viewdetails.cgi?objName='+objName+'&'+ID+'="+"%s"%(o["'+IDF2+'"])+"\\\">details</a>|<a href=\\\"writers/edit.cgi?objName='+objName+'&'+ID+'="+"%s"%(o["'+IDF2+'"])+"\\\">edit</a>)"'))
	if hasTrans:
	    cformat.append(("Center","Transfer.RECEIVER","o['Transfer_RECEIVER'] if o['Transfer_STATUS']=='ARRIVED' else  '%s=>%s'%(o['Transfer_SENDER'],o['Transfer_RECEIVER']) "))
 #       if o["TSTATUS"] == "ARRIVED" :
 #               row.append(o["RECEIVER"])
  #      else:
   #             row.append("%s to %s"%(o["SENDER"],o["RECEIVER"]))

	for c in cols:
	  if c.upper() != ID.upper() :
	    cformat.append((c.lower().capitalize(),table+"."+c,renderString(c,objName) if not draw else '' ))
	for r in refs:
	    cformat.append((r.lower().capitalize(),'','"<a href=\\\"viewdetails.cgi?objName='+objName+'&'+ID+'="+"%s"%(o["'+IDF2+'"])+"&ref='+r+'\\\"> details</a></td>"'))

	     	
	

	# rowkey,cols,query,countquery
	if hasTrans :
		return 	IDF2,cformat,("select %s,Transfer.STATUS as Transfer_STATUS, Transfer.SENDER as Transfer_SENDER from %s left join transfers as Transfer on %s.TRANSFER_ID=Transfer.TRANSFER_ID WHERE  1 "%('%s',table,table)), ("select COUNT(1) from %s"%table)
	elif hasSession :
		cformat.insert(1,("Date","Session.DATE",""))
		cformat.insert(1,("Center","Session.CENTER",""))
		return 	IDF2,cformat,("select %s from %s  left outer join sessions as Session on Session.SESSION_ID=%s.SESSION_ID WHERE 1"%('%s',table,table)), ("select COUNT(1) from %s"%table)
	else:
		return 	IDF2,cformat,("select %s from %s WHERE 1"%('%s',table)), ("select COUNT(1) from %s"%table)


############################################### Sepcific views ############################################
columns=[]
queries=[]
countqueries=[]
rowkeys=[]
header=[]

### Sensor View
header.append("<h1> Sensor View </h1>")
columns.append([
           ("Sensor ID","Sensor.SENSOR_ID",""),#"'<input type=checkbox name=sel_sensor%s>%s'%(o['Sensor_SENSOR_ID'],o['Sensor_SENSOR_ID'])"),
           ("Status","Sensor.STATUS",''),
           ("Center","Transfer.RECEIVER","o['Transfer_RECEIVER'] if o['Transfer_STATUS']=='ARRIVED' else  o['Transfer_SENDER'] "),
           ("Test date","Test_IV.DATE","o['Test_IV_DATE'].strftime('%Y-%m-%d %H:%M:%S')"),
           ("Type","Test_IV.TYPE",''),
           ("Grade","Test_IV.GRADE",''),
           ("v1","Test_IV.V1","'%6g'%o['Test_IV_V1']"),
           ("v2","Test_IV.V2","'%6g'%o['Test_IV_V2']"),
           ("i1","Test_IV.I1","'%6g'%o['Test_IV_I1']"),
           ("i2","Test_IV.I2","'%6g'%o['Test_IV_I2']"),
           ("Slope","Test_IV.SLOPE",''),
           ("Temp","Test_IV.TEMPERATURE",''),
           ("i1@20&deg;","Test_IV.I1","'%6g'%corTemp(o['Test_IV_I1'],o['Test_IV_TEMPERATURE'])"),
           ("i2@20&deg;","Test_IV.I2","'%6g'%corTemp(o['Test_IV_I2'],o['Test_IV_TEMPERATURE'])"),
           ("Test id","Test_IV.TEST_ID",''),
           ("Files","Data.PFNs","'<a href=%s>link</a>'%o['Data_PFNs']"),
          ])
rowkeys.append("Test_IV_TEST_ID");
queries.append("select %s,Transfer.STATUS as Transfer_STATUS, Transfer.SENDER as Transfer_SENDER from inventory_sensor as Sensor, test_iv as Test_IV,transfers as Transfer,test_data as Data where Sensor.SENSOR_ID=Test_IV.SENSOR_ID and  Sensor.TRANSFER_ID=Transfer.TRANSFER_ID and Data.DATA_ID=Test_IV.DATA_ID ")
countqueries.append("select COUNT(1) from inventory_sensor as Sensor, test_iv as Test_IV,transfers as Transfer,test_data as Data where Sensor.SENSOR_ID=Test_IV.SENSOR_ID and  Sensor.TRANSFER_ID=Transfer.TRANSFER_ID and Data.DATA_ID=Test_IV.DATA_ID ")

################################################ HDI Views ########################################
header.append('''<h1>HDI Tests summary  view</h1>
<img src=/icons/viewmag.png width=16> = view test details <p>
<img src=/icons/add.png width=16> = add new test <p>
''')


def testNotes(o,testname) :
         note=""
         nk=testname+'_NOTES'
	 if nk in o :
	    note=o[nk]
	 if "Test_Hdi_Validation_VISUAL_INSPECTION" in o and testname == "Test_Hdi_Validation":
		 note="<i>%s</i><br>%s"% (o["Test_Hdi_Validation_VISUAL_INSPECTION"],note)
	 if note and note != "" :
		return "<br>%s"%note
	 return "" 	
	   
def testDetails(o,testname) :
   testnameObj=testname
   typestr=""
   m=re.match('Test_BareModule_QA_(.*)',testname )
   if  m :
                testnameObj="Test_BareModule_QA"
                typestr="&TYPE="+m.group(1)

   return "&nbsp;<a href=/cgi-bin/viewdetails.cgi?objName="+testnameObj+"&TEST_ID=%s><img src=/icons/viewmag.png width=16></a>"%(o[testname+'_TEST_ID'] )


def hdiTbmGlue(o) :
	 if  o['Test_Hdi_TbmGluing_RESULT'] :
		return coloredResult(o['Test_Hdi_TbmGluing_RESULT'])+ testDetails(o,'Test_Hdi_TbmGluing')+' <a href=/cgi-bin/writers/newTest.cgi?objName=Test_Hdi_TbmGluing&HDI_ID=%s><img src=/icons/add.png width=16></a>'%o['Hdi_HDI_ID']+testNotes(o,'Test_Hdi_TbmGluing')
	 elif o['Hdi_TBM1_VERSION'] == "":
		return '<a href=/cgi-bin/writers/edit.cgi?objName=Hdi&HDI_ID=%s>add TBM to HDI</a>'%o['Hdi_HDI_ID']
	 else :
		return '<a href=/cgi-bin/writers/newTest.cgi?objName=Test_Hdi_TbmGluing&HDI_ID=%s><img src=/icons/add.png width=16></a>'%o['Hdi_HDI_ID']

def testEntry(o,testname):
	 ret="n/a"
	 if  o[testname+'_RESULT'] :
		ret=coloredResult(o[testname+'_RESULT'])+testDetails(o,testname)+" "
#"<a href=/cgi-bin/viewdetails.cgi?objName="+testname+"&TEST_ID=%s>.</a><br>"%(o[testname+'_TEST_ID'] )
#		ret=coloredResult(o[testname+'_RESULT'])+"<br>"
	 ret+=' <a href=/cgi-bin/writers/newTest.cgi?objName='+testname+'&HDI_ID=%s><img src=/icons/add.png width=16></a>'%o['Hdi_HDI_ID']
	 ret+=testNotes(o,testname)
	 return ret
			
columns.append([
	("  HDI ID  ","Hdi.HDI_ID","'<a href=/cgi-bin/viewdetails.cgi?objName=Hdi&HDI_ID=%s>%s</a>'%(o['Hdi_HDI_ID'],o['Hdi_HDI_ID'])"),
        ("Center","Transfer.RECEIVER","o['Transfer_RECEIVER'] if o['Transfer_STATUS']=='ARRIVED' else  o['Transfer_SENDER'] "),
	("TBM 1","Hdi.TBM1_VERSION",""),
	("TBM 2","Hdi.TBM2_VERSION",""),
#	("Reception","Test_Hdi_Reception.RESULT","coloredResult(o['Test_Hdi_Reception_RESULT']) if o['Test_Hdi_Reception_RESULT'] else '<a href=/cgi-bin/writers/newTest.cgi?objName=Test_Hdi_Reception&HDI_ID=%s>add test</a>'%o['Hdi_HDI_ID']"),

	#("Bonding","Test_Hdi_Bonding.RESULT","o['Test_Hdi_Bonding_RESULT'] if o['Test_Hdi_Bonding_RESULT'] else '<a href=/cgi-bin/writers/newTest.cgi?objName=Test_Hdi_Bonding&HDI_ID=%s>add test</a>'%o['Hdi_HDI_ID']"),
	#("TBM Gluing","Test_Hdi_TbmGluing.RESULT","hdiTbmGlue(o)"),
	#("Electric","Test_Hdi_Electric.RESULT"," '%s (<a href=/cgi-bin/writers/edit.cgi?objName=Test_Hdi_Electric&TEST_ID=%s>edit</a>)'%(o['Test_Hdi_Electric_RESULT'],o['Hdi_LASTTEST_HDI_ELECTRIC']) if o['Test_Hdi_Electric_RESULT'] else '<a href=/cgi-bin/writers/newTest.cgi?objName=Test_Hdi_Electric&HDI_ID=%s>add test</a>'%o['Hdi_HDI_ID']"),
	#("Validation","Test_Hdi_Validation.RESULT","o['Test_Hdi_Validation_RESULT'] if o['Test_Hdi_Validation_RESULT'] else '<a href=/cgi-bin/writers/newTest.cgi?objName=Test_Hdi_Validation&HDI_ID=%s>add test</a>'%o['Hdi_HDI_ID']"),
#

	("Reception","Test_Hdi_Reception.RESULT","testEntry(o,'Test_Hdi_Reception')+('<br>%s'%(o['Test_Hdi_Reception_INSPECTION_FRONT']) if o['Test_Hdi_Reception_INSPECTION_FRONT'] is not None else '')"),
	("TBM Gluing","Test_Hdi_TbmGluing.RESULT","hdiTbmGlue(o)"),
	("Bonding","Test_Hdi_Bonding.RESULT","testEntry(o,'Test_Hdi_Bonding')"),
#	("Electric","Test_Hdi_Electric.RESULT","testEntry(o,'Test_Hdi_Electric')"),
	("Electric","Test_Hdi_Electric.RESULT","('%s %s(<a href=/cgi-bin/writers/edit.cgi?objName=Test_Hdi_Electric&TEST_ID=%s>edit</a>)%s'%(coloredResult(o['Test_Hdi_Electric_RESULT']),testDetails(o,'Test_Hdi_Electric'),o['Hdi_LASTTEST_HDI_ELECTRIC'],testNotes(o,'Test_Hdi_Electric')) if o['Test_Hdi_Electric_RESULT'] else 'n/a')+' <a href=/cgi-bin/writers/newTest.cgi?objName=Test_Hdi_Electric&HDI_ID=%s><img src=/icons/add.png width=16></a>'%o['Hdi_HDI_ID']"),
	#("Validation","Test_Hdi_Validation.RESULT","testEntry(o,'Test_Hdi_Validation')+(' <br><i>%s</i>'%(o['Test_Hdi_Validation_VISUAL_INSPECTION']) if o['Test_Hdi_Validation_VISUAL_INSPECTION'] is not None else '')"),
	("Validation","Test_Hdi_Validation.RESULT","testEntry(o,'Test_Hdi_Validation')"),
	("","Hdi.LASTTEST_HDI_ELECTRIC","NOPRINT"),
	("","Hdi.LASTTEST_HDI_BONDING","NOPRINT"),
	("","Hdi.LASTTEST_HDI_TBMGLUING","NOPRINT"),
	("","Hdi.LASTTEST_HDI_VALIDATION","NOPRINT"),
	("","Hdi.LASTTEST_HDI_RECEPTION","NOPRINT"),
	("","Test_Hdi_Reception.TEST_ID","NOPRINT"),
	("","Test_Hdi_Electric.TEST_ID","NOPRINT"),
	("","Test_Hdi_TbmGluing.TEST_ID","NOPRINT"),
	("","Test_Hdi_Validation.TEST_ID","NOPRINT"),
	("","Test_Hdi_Bonding.TEST_ID","NOPRINT"),
	("","Test_Hdi_Electric.NOTES","NOPRINT"),
	("","Test_Hdi_TbmGluing.NOTES","NOPRINT"),
	("","Test_Hdi_Validation.NOTES","NOPRINT"),
	("","Test_Hdi_Bonding.NOTES","NOPRINT"),
	("","Test_Hdi_Validation.VISUAL_INSPECTION","NOPRINT"),
	("","Test_Hdi_Reception.INSPECTION_FRONT","NOPRINT"),

])
rowkeys.append("Hdi_HDI_ID") #not obvious
queries.append("select %s,Transfer.STATUS as Transfer_STATUS, Transfer.SENDER as Transfer_SENDER from inventory_hdi as Hdi join transfers as Transfer on Hdi.TRANSFER_ID=Transfer.TRANSFER_ID "
		"left outer join test_hdi_reception as Test_Hdi_Reception on Hdi.LASTTEST_HDI_RECEPTION=Test_Hdi_Reception.TEST_ID "
		"left outer join test_hdi_bonding as Test_Hdi_Bonding on Hdi.LASTTEST_HDI_BONDING=Test_Hdi_Bonding.TEST_ID "
		"left outer join test_hdi_tbmgluing as Test_Hdi_TbmGluing on Hdi.LASTTEST_HDI_TBMGLUING=Test_Hdi_TbmGluing.TEST_ID "
		"left outer join test_hdi_electric as Test_Hdi_Electric on Hdi.LASTTEST_HDI_ELECTRIC=Test_Hdi_Electric.TEST_ID "
		"left outer join test_hdi_validation as Test_Hdi_Validation on Hdi.LASTTEST_HDI_VALIDATION=Test_Hdi_Validation.TEST_ID "
		" WHERE 1 ")
countqueries.append("select COUNT(1)  from inventory_hdi")

################################################ ROC Views ########################################
header.append('''<h1>Overview of ROCs</h1>''')
#<img src=/icons/viewmag.png width=16> = view test details <p>
#<img src=/icons/add.png width=16> = add new test <p>
#''')

def rocColors(o) :
	res=o['Test_Roc_RESULT']
 	return "%d"% o['Test_Roc_RESULT']

columns.append([
        ("ROC ID","Roc.ROC_ID","'<a href=/cgi-bin/viewdetails.cgi?objName=Roc&ROC_ID=%s>%s</a>'%(o['Roc_ROC_ID'],o['Roc_ROC_ID'])"),
        ("Center","Transfer.RECEIVER","o['Transfer_RECEIVER'] if o['Transfer_STATUS']=='ARRIVED' else  o['Transfer_SENDER'] "),
        ("Status","Roc.STATUS",""),
        ("Grade","Test_Roc.RESULT","rocColors(o)"),
        ("Wafer Type","Roc_Wafer.TYPE",""),
        ("Roc Type","Roc.TYPE",""),
        ("IANA","Test_Roc.IANA",""),
        ("IDIGI","Test_Roc.IDIGI",""),
        ("DEFECTPIXELS","Test_Roc.DEFECTPIXELS",""),
        ("TRIMPIXELS","Test_Roc.TRIMPIXELS",""),
        ("MASKPIXELS","Test_Roc.MASKPIXELS",""),
        ("THRESHOLDPIXELS","Test_Roc.THRESHOLDPIXELS",""),
        ("ADDRPIXELS","Test_Roc.ADDRPIXELS",""),
        ("NSIGPIXELS","Test_Roc.NSIGPIXELS",""),
        ("NOISEPIXELS","Test_Roc.NOISEPIXELS",""),
        ("Pos on wafer","Roc.ROC_POSITION",""),
        ("","Roc.LASTTEST_ROC","NOPRINT"),

])
rowkeys.append("Roc_ROC_ID") #not obvious
queries.append("select %s,Transfer.STATUS as Transfer_STATUS, Transfer.SENDER as Transfer_SENDER from inventory_roc as Roc left outer join transfers as Transfer on Roc.TRANSFER_ID=Transfer.TRANSFER_ID "
                "left outer join test_roc as Test_Roc on Roc.LASTTEST_ROC=Test_Roc.TEST_ID "
                "left outer join inventory_roc_wafer as Roc_Wafer on Roc.WAFER_ID=Roc_Wafer.ROCWAFER_ID "
                " WHERE 1 ")
countqueries.append("select COUNT(1)  from inventory_roc")

################################################ TestParams View ########################################
header.append('''<h1>Overview of PerformanceParameters</h1>''')
(i,c,q,cq)=fromObjectName("Test_PerformanceParameters")
#for i in xrange(0,len(c)):
#    e=c[i]
#    if e[1] != "":
#c[i]=(e[0],"Main.%s"%e[1],e[2])
#print c
c.append(("Macro Version","FMA.MACRO_VERSION",""))
c.insert(2,("Center","Session.CENTER",""))
c.insert(2,("Date","Session.DATE",""))
c.insert(2,("Temperature","FMT.TEMPNOMINAL",""))
c.insert(1,("Status","FM.STATUS",""))
c.insert(1,("Full Module","FMT.FULLMODULE_ID",""))
rowkeys.append(i)
queries.append("select %s from test_performanceparameters left outer join test_fullmoduleanalysis as FMA on FMA.TEST_ID=FULLMODULEANALYSISTEST_ID left outer join test_fullmodule as FMT on FMT.TEST_ID=FMA.FULLMODULETEST_ID left join test_fullmodulesession as s1 on s1.TEST_ID=FMT.SESSION_ID left join sessions as Session on s1.SESSION_ID=Session.SESSION_ID left outer join inventory_fullmodule as FM on FM.FULLMODULE_ID=FMT.FULLMODULE_ID  WHERE 1")
countqueries.append("select COUNT(1)from test_performanceparameters left outer join test_fullmoduleanalysis as FMA on FMA.TEST_ID=FULLMODULEANALYSISTEST_ID left outer join test_fullmodule as FMT on FMT.TEST_ID=FMA.FULLMODULETEST_ID  left join test_fullmodulesession as s1 on s1.TEST_ID=FMT.SESSION_ID left join sessions as Session on s1.SESSION_ID=Session.SESSION_ID WHERE 1")
#countqueries.append(cq)
columns.append(c)

################################################ DacParams View ########################################
header.append('''<h1>Overview of DACParamters</h1>''')
(i,c,q,cq)=fromObjectName("Test_DacParameters")
#for i in xrange(0,len(c)):
#    e=c[i]
#    if e[1] != "":
#c[i]=(e[0],"Main.%s"%e[1],e[2])
#print c
c.append(("Macro Version","FMA.MACRO_VERSION",""))
c.insert(2,("Center","Session.CENTER",""))
c.insert(2,("Date","Session.DATE",""))
c.insert(2,("Temperature","FMT.TEMPNOMINAL",""))
c.insert(1,("Status","FM.STATUS",""))
c.insert(1,("Full Module ID","FMT.FULLMODULE_ID",""))
rowkeys.append(i)
queries.append("select %s from test_dacparameters left outer join test_fullmoduleanalysis as FMA on FMA.TEST_ID=FULLMODULEANALYSISTEST_ID left outer join test_fullmodule as FMT on FMT.TEST_ID=FMA.FULLMODULETEST_ID left join test_fullmodulesession as s1 on s1.TEST_ID=FMT.SESSION_ID left join sessions as Session on s1.SESSION_ID=Session.SESSION_ID left outer join inventory_fullmodule as FM on FM.FULLMODULE_ID=FMT.FULLMODULE_ID WHERE 1")
countqueries.append("select COUNT(1)from test_dacparameters left outer join test_fullmoduleanalysis as FMA on FMA.TEST_ID=FULLMODULEANALYSISTEST_ID left outer join test_fullmodule as FMT on FMT.TEST_ID=FMA.FULLMODULETEST_ID  left join test_fullmodulesession as s1 on s1.TEST_ID=FMT.SESSION_ID left join sessions as Session on s1.SESSION_ID=Session.SESSION_ID WHERE 1")
#countqueries.append(cq)
columns.append(c)

################################################ BareModule tests View ########################################

header.append('''<h1>BareModule Tests summary  view</h1>
<img src=/icons/viewmag.png width=16> = view test details <p>
<img src=/icons/add.png width=16> = add new test <p>
''')

def testEntryBM(o,testname,res="_RESULT",edit=False):
	 testnameObj=testname
	 typestr=""
	 m=re.match('Test_BareModule_QA_(.*)',testname )
	 if  m :
		testnameObj="Test_BareModule_QA"
		typestr="&TYPE="+m.group(1)	
         ret="n/a"
         if  o[testname+res] :
#                ret=(o[testname+res])+testDetails(o,testname)+" "
                ret=viewDetails(o[testname+'_TEST_ID'],testnameObj,o[testname+res]) 
#	 if ret=="n/a" or  not edit :
#           ret+=' <a href=/cgi-bin/writers/newTest.cgi?objName='+testnameObj+'&BAREMODULE_ID=%s%s><img src=/icons/add.png width=16></a>'%(o['BareModule_BAREMODULE_ID'],typestr)
#	 else:
#           ret+=' <a href=/cgi-bin/writers/edit.cgi?objName='+testnameObj+'&TEST_ID=%s>edit</a>'%(o[testnameObj+'_TEST_ID'])
#         ret+=testNotes(o,testname)
         return ret
	
def overrideGrade(o,oo) :
	ret = ""
	if oo is None :
		 ret+=' <a href=/cgi-bin/writers/newTest.cgi?objName=Test_BareModule_Grading&BAREMODULE_ID=%s><img src=/icons/add.png width=16></a>'%(o['BareModule_BAREMODULE_ID'])
	else :
		ret = gradeColor(oo)
		ret+=' <a href=/cgi-bin/writers/edit.cgi?objName=Test_BareModule_Grading&TEST_ID=%s>edit</a>'%(o['Test_BareModule_Grading_TEST_ID'])
	return ret



columns.append([
	("BAREMODULE  ID","BareModule.BAREMODULE_ID","'<a href=/cgi-bin/viewdetails.cgi?objName=BareModule&BAREMODULE_ID=%s>%s</a>'%(o['BareModule_BAREMODULE_ID'],o['BareModule_BAREMODULE_ID'])"),
        ("FullModule","FM.FULLMODULE_ID","oo if oo is not None else ''"),
        ("Center","Transfer.RECEIVER","o['Transfer_RECEIVER'] if o['Transfer_STATUS']=='ARRIVED' else  o['Transfer_SENDER'] "),
        ("Status","BareModule.STATUS",''),
        ("BuiltBy","BareModule.BUILTBY",''),
#	("Inspection","Test_BareModule_Inspection.RESULT","testEntryBM(o,'Test_BareModule_Inspection')"),
	("BB #fail","Test_BareModule_QA_BumpBonding.TOTAL_FAILURES","testEntryBM(o,'Test_BareModule_QA_BumpBonding','_TOTAL_FAILURES')"),
	("PA #fail","Test_BareModule_QA_PixelAlive.TOTAL_FAILURES","testEntryBM(o,'Test_BareModule_QA_PixelAlive','_TOTAL_FAILURES')"),
#	("Global Grade","Test_BareModule_Grading.GLOBAL_GRADING","testEntryBM(o,'Test_BareModule_Grading','_GLOBAL_GRADING',True)"),
	("IV Grade","Test_IV.GRADE",""),
	("#Def for GR","(Test_BareModule_QA_BumpBonding.TOTAL_FAILURES+Test_BareModule_QA_PixelAlive.TOTAL_FAILURES)",""),
	("IDig Grade","idigGrade(BareModule.BAREMODULE_ID)","'<a href=/cgi-bin/view.cgi?objName=Test_BM_ROC_DacParameters&BAREMODULE_ID=%s>%s</a>'%(o['BareModule_BAREMODULE_ID'],oo)"),
        ("#rework","BareModule.TYPE",""),
        ("Final GR","bmGrade(BareModule.BAREMODULE_ID)","gradeColor(oo)"),
        ("Override Grade","Test_BareModule_Grading.GLOBAL_GRADING","overrideGrade(o,oo)"),
        ("i1@20&deg;BAM","Test_IV.I1","'%6g'%corTemp(o['Test_IV_I1'],o['Test_IV_TEMPERATURE']) if oo is not None else 'n/a'"),
        ("i2@20&deg;BAM","Test_IV.I2","'%6g'%corTemp(o['Test_IV_I2'],o['Test_IV_TEMPERATURE']) if oo is not None else 'n/a'"),
#        ("i1@BAM","Test_IV.I1","'%6g'%o['Test_IV_I1'] if o['Test_IV_I1'] is not None else 'n/a'"),
#        ("i2@BAM","Test_IV.I2","'%6g'%o['Test_IV_I2'] if o['Test_IV_I2'] is not None else 'n/a'"),
        ("Slope@BAM","Test_IV.SLOPE",''),
        ("i1@20&deg;CIS","Test_IVCIS.I1","'%6g'%corTemp(o['Test_IVCIS_I1'],o['Test_IVCIS_TEMPERATURE']) if oo is not None else 'n/a'"),
        ("i2@20&deg;CIS","Test_IVCIS.I2","'%6g'%corTemp(o['Test_IVCIS_I2'],o['Test_IVCIS_TEMPERATURE']) if oo is not None else 'n/a'"),
 
#       ("i1@CIS","Test_IVCIS.I1","'%6g'%o['Test_IVCIS_I1'] if o['Test_IVCIS_I1'] is not None else 'n/a'"),
 #       ("i2@CIS","Test_IVCIS.I2","'%6g'%o['Test_IVCIS_I2'] if o['Test_IVCIS_I2'] is not None else 'n/a'"),
        ("Slope@CIS","Test_IVCIS.SLOPE",''),
        ("","Test_IV.TEMPERATURE","NOPRINT"),
        ("","Test_IVCIS.TEMPERATURE","NOPRINT"),
        ("","Test_BareModule_Inspection.TEST_ID","NOPRINT"),
        ("","Test_BareModule_Grading.TEST_ID","NOPRINT"),
        ("","Test_BareModule_QA_BumpBonding.TEST_ID","NOPRINT"),
        ("","Test_BareModule_QA_PixelAlive.TEST_ID","NOPRINT"),
	
#        ("","Test_BareModule_Grading.TEST_ID","NOPRINT"),

])
rowkeys.append("BareModule_BAREMODULE_ID") #not obvious
queries.append("select %s,Transfer.STATUS as Transfer_STATUS, Transfer.SENDER as Transfer_SENDER "
#	        ",(select count(1) from test_bm_roc_dacparameters where test_bm_roc_dacparameters.BAREMODULE_ID = BareModule.BAREMODULE_ID and idig <= 65) as belowDig"
#	        ",(select count(1) from test_bm_roc_dacparameters where test_bm_roc_dacparameters.BAREMODULE_ID = BareModule.BAREMODULE_ID and idig > 65) as aboveDig"
		" from inventory_baremodule as BareModule left outer join transfers as Transfer on BareModule.TRANSFER_ID=Transfer.TRANSFER_ID "
		"left outer join test_baremodule_qa as Test_BareModule_QA_PixelAlive on BareModule.LASTTEST_BAREMODULE_QA_PIXELALIVE=Test_BareModule_QA_PixelAlive.TEST_ID "
		"left outer join test_baremodule_qa as Test_BareModule_QA_BumpBonding on BareModule.LASTTEST_BAREMODULE_QA_BONDING=Test_BareModule_QA_BumpBonding.TEST_ID "
#		"left outer join test_baremodule_grading as Test_BareModule_Grading on BareModule.LASTTEST_BAREMODULE_GRADING=Test_BareModule_Grading.TEST_ID "
		"left outer join test_baremodule_inspection as Test_BareModule_Inspection on BareModule.LASTTEST_BAREMODULE_INSPECTION=Test_BareModule_Inspection.TEST_ID "
		"left outer join test_baremodule_grading as Test_BareModule_Grading on BareModule.BAREMODULE_ID=Test_BareModule_Grading.BAREMODULE_ID "
		"left outer join inventory_fullmodule as FM on BareModule.BAREMODULE_ID = FM.BAREMODULE_ID "
		"left outer join test_iv as Test_IVCIS on Test_IVCIS.SENSOR_ID=BareModule.SENSOR_ID and Test_IVCIS.TYPE='CIS' "
	        "left outer join test_iv as Test_IV on Test_IV.test_id = (select TEST_ID from test_iv where  sensor_id=BareModule.sensor_id and type='BAM' order by TEST_ID desc limit 1)"

#		"left outer join test_iv as Test_IV on Test_IV.SENSOR_ID=BareModule.SENSOR_ID and Test_IV.TYPE='BAM' "
		" WHERE 1 ")
countqueries.append("select COUNT(1)"
                " from inventory_baremodule as BareModule join transfers as Transfer on BareModule.TRANSFER_ID=Transfer.TRANSFER_ID "
                "left outer join test_baremodule_qa as Test_BareModule_QA_PixelAlive on BareModule.LASTTEST_BAREMODULE_QA_PIXELALIVE=Test_BareModule_QA_PixelAlive.TEST_ID "
                "left outer join test_baremodule_qa as Test_BareModule_QA_BumpBonding on BareModule.LASTTEST_BAREMODULE_QA_BONDING=Test_BareModule_QA_BumpBonding.TEST_ID "
#               "left outer join test_baremodule_grading as Test_BareModule_Grading on BareModule.LASTTEST_BAREMODULE_GRADING=Test_BareModule_Grading.TEST_ID "
                "left outer join test_baremodule_inspection as Test_BareModule_Inspection on BareModule.LASTTEST_BAREMODULE_INSPECTION=Test_BareModule_Inspection.TEST_ID "
                "left outer join test_iv as Test_IVCIS on Test_IVCIS.SENSOR_ID=BareModule.SENSOR_ID and Test_IVCIS.TYPE='CIS' "
                "left outer join test_iv as Test_IV on Test_IV.test_id = (select TEST_ID from test_iv where  sensor_id=BareModule.sensor_id and type='BAM' order by TEST_ID desc limit 1)"

#               "left outer join test_iv as Test_IV on Test_IV.SENSOR_ID=BareModule.SENSOR_ID and Test_IV.TYPE='BAM' "
                " WHERE 1 ")

################################################ LogBook View ########################################
header.append('''<h1>Logbook</h1><a href=/cgi-bin/writers/newTest.cgi?objName=Test_Logbook>Add Entry</a><br><p>''')
customjs[6]='"order": [[ 1,"desc" ]],'
(i,c,q,cq)=fromObjectName("Test_Logbook")
c[0]=("Entry #",c[0][1],c[0][2])
c=c[:1]
#for i in xrange(0,len(c)):
#    e=c[i]
#    if e[1] != "":
#c[i]=(e[0],"Main.%s"%e[1],e[2])
#print c
def inlineLinks(x):
	res=""
	if x is not None : 
  	    for l in x.split(",") :	
		url=re.sub("file:","",l)
		n=os.path.split(l)[1]
		n=re.sub("[0-9\.]+__","",n)
		res+="<a href=\"%s\">%s</a>, "%(url,n)
	return res	
c.append(("Date","Session.DATE",""))
c.append(("Center","Session.CENTER",""))
c.append(("Operator","Session.OPERATOR",""))
c.append(("Comment&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;","logbook.COMMENT","idlink(o[rn])"))
c.append(("Files","Data.PFNs",'inlineLinks(o[rn])'))
c.append(("IDs","logbook.IDS",'idlink(o[rn])'))
#c.insert(2,("Date","Session.DATE",""))

rowkeys.append(i)
queries.append("select %s from logbook  left outer join sessions as Session on logbook.SESSION_ID=Session.SESSION_ID left outer join test_data as Data on logbook.DATA_ID=Data.DATA_ID WHERE 1")
countqueries.append("select COUNT(1) from logbook  left outer join sessions as Session on logbook.SESSION_ID=Session.SESSION_ID WHERE 1")
#countqueries.append(cq)
columns.append(c)


################################################ XRay tests View ########################################

header.append('''<h1>XRay Tests summary  view</h1>
''')
def vcalAna(o):
   path=o['DataVcal_PFNs']
   if path is not None:
     m=re.match("file:(/data/pixels.*)",path) 
     if m :
	  return '%s<br><a href=%s/TestResult.html>results</a>'%(o['Test_FullModule_XRay_Vcal_Module_Analysis_TEST_ID'],m.group(1))
   return ""


def hrAna(o):
   path=o['DataHR_PFNs']
   if path is not None :
     m=re.match("file:(/data/pixels.*)",path) 
     if m :
	  return '<a href=%s/TestResult.html>results</a>'%(m.group(1))
   return ""


def rocLink(o) :
   return "<a href=/cgi-bin/rawPredefinedView.cgi?viewNumber=8&exact=1&PROCESSING_ID=%s&FULLMODULETEST_ID=%s>per roc</a>"%(o['Test_FullModule_XRay_Vcal_LAST_PROCESSING_ID'],o['Test_FullModule_XRay_Vcal_TEST_ID'])

columns.append([
        ("FULL MODULE  ID","FullModule.FULLMODULE_ID","'%s<br><a href=/cgi-bin/viewdetails.cgi?objName=FullModule&FULLMODULE_ID=%s>mod details</a> '%(o['FullModule_FULLMODULE_ID'],o['FullModule_FULLMODULE_ID'])"),
        ("Center","Transfer.RECEIVER","o['Transfer_RECEIVER'] if o['Transfer_STATUS']=='ARRIVED' else  o['Transfer_SENDER'] "),
	("Analysis ID","Test_FullModule_XRay_Vcal_Module_Analysis.TEST_ID","vcalAna(o)+' | '+rocLink(o)"),
	("Slope","Test_FullModule_XRay_Vcal_Module_Analysis.SLOPE","'%4.2f'%oo if oo is not None else ''"),
	("Offset","Test_FullModule_XRay_Vcal_Module_Analysis.OFFSET","'%4.2f'%oo if oo is not None else ''"),
	("Grade Vcal","Test_FullModule_XRay_Vcal_Module_Analysis.GRADE",""),
#	("#Pix w/ low eff","GREATEST(Test_FullModule_XRay_HR_Module50_Analysis.N_PIXELS_EFF_BELOW_CUT,Test_FullModule_XRay_HR_Module150_Analysis.N_PIXELS_EFF_BELOW_CUT)",""),

	("HR ID","HRS.TEST_ID","'%s (%s)'%(viewDetails(oo,'Test_FullModule_XRay_HR_Summary') , hrAna(o))"),
	("Eff @50","HRA.INTERP_EFF_50",""),
	("Eff @120","HRA.INTERP_EFF_120",""),
	("#Pix Hot","HRA.N_HOT_PIXELS",""),
	("#Pix NoHit","GREATEST(HRA.N_PIXEL_NO_HIT_50,HRA.N_PIXEL_NO_HIT_150)",""),
	("Grade HR","HRA.GRADE",""),
	("Grade ","GREATEST(Test_FullModule_XRay_Vcal_Module_Analysis.GRADE,HRA.GRADE)",""),
        ("","DataVcal.PFNs","NOPRINT"),

        ("","Test_FullModule_XRay_Vcal.LAST_PROCESSING_ID","NOPRINT"),
        ("","Test_FullModule_XRay_Vcal.TEST_ID","NOPRINT"),
        ("","DataHR.PFNs","NOPRINT"),
      
#        ("Inspection","Test_BareModule_Inspection.RESULT","testEntryBM(o,'Test_BareModule_Inspection')"),
#       ("BumpBonding Tot failures","Test_BareModule_QA_BumpBonding.TOTAL_FAILURES","testEntryBM(o,'Test_BareModule_QA_BumpBonding','_TOTAL_FAILURES')"),
#        ("PixelAlive Tot failures","Test_BareModule_QA_PixelAlive.TOTAL_FAILURES","testEntryBM(o,'Test_BareModule_QA_PixelAlive','_TOTAL_FAILURES')"),
#        ("Global Grade","Test_BareModule_Grading.GLOBAL_GRADING","testEntryBM(o,'Test_BareModule_Grading','_GLOBAL_GRADING')"),
#        ("i1","Test_IV.I1","'%6g'%o['Test_IV_I1'] if o['Test_IV_I1'] is not None else 'n/a'"),
#        ("i2","Test_IV.I2","'%6g'%o['Test_IV_I2'] if o['Test_IV_I2'] is not None else 'n/a'"),
#        ("Slope","Test_IV.SLOPE",''),
#        ("i1@CIS","Test_IVCIS.I1","'%6g'%o['Test_IVCIS_I1'] if o['Test_IVCIS_I1'] is not None else 'n/a'"),
#        ("i2@CIS","Test_IVCIS.I2","'%6g'%o['Test_IVCIS_I2'] if o['Test_IVCIS_I2'] is not None else 'n/a'"),
#        ("Slope@CIS","Test_IVCIS.SLOPE",''),
#        ("","Test_BareModule_Inspection.TEST_ID","NOPRINT"),
#        ("","Test_BareModule_QA_BumpBonding.TEST_ID","NOPRINT"),
#        ("","Test_BareModule_QA_PixelAlive.TEST_ID","NOPRINT"),

])
rowkeys.append("FullModule_FULLMODULE_ID") #not obvious
queries.append("select %s,Transfer.STATUS as Transfer_STATUS, Transfer.SENDER as Transfer_SENDER from inventory_fullmodule as FullModule left outer join transfers as Transfer on FullModule.TRANSFER_ID=Transfer.TRANSFER_ID "
                "left outer join Test_FullModule_XRay_Vcal as Test_FullModule_XRay_Vcal on FullModule.LASTTEST_XRAY_VCAL=Test_FullModule_XRay_Vcal.TEST_ID "
                "left outer join Test_FullModule_XRay_Vcal_Module_Analysis as Test_FullModule_XRay_Vcal_Module_Analysis on Test_FullModule_XRay_Vcal_Module_Analysis.FULLMODULETEST_ID=Test_FullModule_XRay_Vcal.TEST_ID and Test_FullModule_XRay_Vcal_Module_Analysis.PROCESSING_ID=Test_FullModule_XRay_Vcal.LAST_PROCESSING_ID "
		"left outer join test_data as DataVcal on Test_FullModule_XRay_Vcal_Module_Analysis.DATA_ID=DataVcal.DATA_ID "

                "left outer join Test_FullModule_XRay_HR_Summary as HRS on FullModule.LASTTEST_XRAY_HR=HRS.TEST_ID "
                "left outer join Test_FullModule_XRay_HR_Module_Analysis_Summary as HRA on HRA.TEST_XRAY_HR_SUMMARY_ID=HRS.TEST_ID and  HRA.PROCESSING_ID=HRS.LAST_PROCESSING_ID "
                "left outer join Test_FullModule_XRay_HR_Module_Noise as HRN on HRN.TEST_XRAY_HR_SUMMARY_ID=HRS.TEST_ID and  HRN.PROCESSING_ID=HRS.LAST_PROCESSING_ID "
		"left outer join test_data as DataHR on HRA.DATA_ID=DataHR.DATA_ID "
                " WHERE (Test_FullModule_XRay_Vcal.TEST_ID <> 0  OR HRS.TEST_ID <> 0) ")


countqueries.append("select COUNT(1) from inventory_fullmodule as FullModule left outer join transfers as Transfer on FullModule.TRANSFER_ID=Transfer.TRANSFER_ID "
                "left outer join Test_FullModule_XRay_Vcal as Test_FullModule_XRay_Vcal on FullModule.LASTTEST_XRAY_VCAL=Test_FullModule_XRay_Vcal.TEST_ID "
                "left outer join Test_FullModule_XRay_Vcal_Module_Analysis as Test_FullModule_XRay_Vcal_Module_Analysis on Test_FullModule_XRay_Vcal_Module_Analysis.FULLMODULETEST_ID=Test_FullModule_XRay_Vcal.TEST_ID and Test_FullModule_XRay_Vcal_Module_Analysis.PROCESSING_ID=Test_FullModule_XRay_Vcal.LAST_PROCESSING_ID "
                "left outer join test_data as DataVcal on Test_FullModule_XRay_Vcal_Module_Analysis.DATA_ID=DataVcal.DATA_ID "

                "left outer join Test_FullModule_XRay_HR_Summary as HRS on FullModule.LASTTEST_XRAY_HR=HRS.TEST_ID "
                "left outer join Test_FullModule_XRay_HR_Module_Analysis_Summary as HRA on HRA.TEST_XRAY_HR_SUMMARY_ID=HRS.TEST_ID and  HRA.PROCESSING_ID=HRS.LAST_PROCESSING_ID "
                "left outer join Test_FullModule_XRay_HR_Module_Noise as HRN on HRN.TEST_XRAY_HR_SUMMARY_ID=HRS.TEST_ID and  HRN.PROCESSING_ID=HRS.LAST_PROCESSING_ID "
                " WHERE (Test_FullModule_XRay_Vcal.TEST_ID <> 0  OR HRS.TEST_ID <> 0) ")

groupheader[7]="<tr><th  style=\" border-right: 1px solid #111111;\"  nosearch=1 colspan=2>Inventory</th><th  style=\" border-right: 1px solid #111111;\" nosearch=1 colspan=4>VCAL</th><th nosearch=1  style=\" border-right: 1px solid #111111;\" colspan=6>High Rate</th> <th  style=\" border-right: 1px solid #111111;\"  nosearch=1 colspan=1>Final</th></tr>"

################################################ XRay ROC View ########################################
#view8
header.append('''<h1>Overview of XRay ROC results</h1>''')
(i,c,q,cq)=fromObjectName("Test_FullModule_XRay_Vcal_Roc_Analysis")
#for i in xrange(0,len(c)):
#    e=c[i]
#    if e[1] != "":
#c[i]=(e[0],"Main.%s"%e[1],e[2])
#print c
#.append(("Macro Version","FMA.MACRO_VERSION",""))
def rocAna(o):
   path=o['DataVcal_PFNs']
   m=re.match("file:(/data/pixels.*)",path) 
   if m :
	  return '<a href=%s/Chips_Xray/Chip_Xray%s/TestResult.html>results</a>'%(m.group(1),o['Test_FullModule_XRay_Vcal_Roc_Analysis_ROC_POS'])
   return ""

c.insert(2,("Center","Session.CENTER",""))
#c.insert(2,("Date","Session.DATE",""))
c.insert(2,("Temperature","FMT.TEMPNOMINAL",""))
c.insert(1,("Full Module ID","FMT.FULLMODULE_ID",""))
c.insert(5,("Analysis","DataVcal.PFNs","rocAna(o)") )

rowkeys.append(i)
queries.append("select %s from Test_FullModule_XRay_Vcal_Roc_Analysis "
	       "left outer join Test_FullModule_XRay_Vcal as FMT on FMT.TEST_ID=Test_FullModule_XRay_Vcal_Roc_Analysis.FULLMODULETEST_ID "
	       "left outer join Test_FullModule_XRay_Vcal_Module_Analysis as FMA on FMA.TEST_ID=Test_FullModule_XRay_Vcal_Roc_Analysis.TEST_XRAY_VCAL_MODULE_ID "
               "left outer join test_data as DataVcal on FMA.DATA_ID=DataVcal.DATA_ID "
               "left join sessions as Session on FMT.SESSION_ID=Session.SESSION_ID WHERE 1")
countqueries.append("select COUNT(1) from Test_FullModule_XRay_Vcal_Roc_Analysis "
               "left outer join test_fullmodule as FMT on FMT.TEST_ID=Test_FullModule_XRay_Vcal_Roc_Analysis.FULLMODULETEST_ID "
               "left join sessions as Session on FMT.SESSION_ID=Session.SESSION_ID WHERE 1")
#countqueries.append(cq)
columns.append(c)

############################################# Tier0 View #################################################
#view 9
tier0Views.append(9)
customjs[9]='"order": [[ 2,"desc" ],[6,"desc"]],'
header.append("Test Processing")
columns.append([
		("Name","InputTar.NAME",""),
		("InputDate","InputTar.DATE",""),
		("ProcDate","ProcessingRun.DATE",""),
		("Center","InputTar.CENTER",""),
		("Status","InputTar.STATUS",""),
		("TestName","InputTar.TESTNAME",""),
		("Proc ID","ProcessingRun.RUN_ID",""),
		("RunStatus","ProcessingRun.STATUS","procResult(o)"),
		("ExitCode","ProcessingRun.EXIT_CODE",""),
		("Upload","ProcessedDir.UPLOAD_STATUS",""),
		("Macro","ProcessingRun.MACRO_VERSION",""),
		("Log files","ProcessingRun.OUTLOG","logs(o)"),
		("HIDDEN","ProcessingRun.EXIT_CODE","repro(o)"),
		("","ProcessingRun.MACRO_VERSION","NOPRINT"),
		("","ProcessingRun.STATUS","NOPRINT"),
		("","ProcessedDir.UPLOAD_STATUS","NOPRINT"),
])
rowkeys.append("ProcessingRun_RUN_ID")
queries.append("select %s from inputtar as InputTar"
		" left join processingrun as ProcessingRun on InputTar.TAR_ID=ProcessingRun.TAR_ID"
		" left join outputdir as ProcessedDir on ProcessedDir.PROCESSING_RUN_ID=ProcessingRun.RUN_ID"
                "  WHERE 1")
countqueries.append("select COUNT(1) from inputtar as InputTar"
                " left join processingrun as ProcessingRun on InputTar.TAR_ID=ProcessingRun.TAR_ID"
                " left join outputdir as ProcessedDir on ProcessedDir.PROCESSING_RUN_ID=ProcessingRun.RUN_ID"
                "  WHERE 1")
customjs2[9]='''$('#example').dataTable().fnFakeRowspan(0);
               $('#example').dataTable().fnFakeRowspan(1);
              $('#example').dataTable().fnFakeRowspan(2);
              $('#example').dataTable().fnFakeRowspan(3);
'''

def repro(o):
	return "<a href=/cgi-bin/writers/reprocess.cgi?processingrun=%s>reprocess this </a>"  % (o["ProcessingRun_RUN_ID"])


def logs(o):
        last= o["ProcessingRun_OUTLOG"]
        if last is not None :
                a="<a href=%s>log1</a>"%last
                a+="|<a href=%s_upload>log2</a>"%last
                return a
        return "n/a"

def procResult(o):
	macro = o["ProcessingRun_MACRO_VERSION"]
	upload= o["ProcessedDir_UPLOAD_STATUS"]
	exitcode = o["ProcessingRun_EXIT_CODE"]
	status = o["ProcessingRun_STATUS"]
	if exitcode > 0 or (upload is not None and upload != "ok") :
                return "<font color=red>%s</font>"%(status)
	elif exitcode == -1 :
                return "<font color=blue>%s</font>"%(status)
        else:
                return "%s"%(status)


#headers = ["NAME","Date","Center","Status","TestName","LastProcessing(code),macro","logs"]



################################################ Full Module test View ########################################
#view10
header.append('''<h1>Full Module test results (Last test only) </h1>''')
def tempWithPlot(o) :
	t=o["FMT_TEMPNOMINAL"]
#	if t[0] == 'p' :
#		t='+'+t[1:]
#	if t[0] == 'm' :
#		t='-'+t[1:]
#	t=re.sub('_([0-9]+)',' (\\1)',t)
	p=o["Data_PFNs"]
	url='<a href=%s/TestResult.html>%s</a>'%(re.sub('file:','',p),t)
        return url
columns.append([
	("Mod ID","FMS.FULLMODULE_ID",""),
	("STATUS","FM.STATUS",""),
	("Step","FMT.TEMPNOMINAL","tempWithPlot(o)"),
	("T","FMA.TEMPVALUE",""),
#	("Plot","Data.PFNs"," '<a href=%s/TestResult.html>plot</a>'%re.sub('file:','',oo)"),
	("GR","FMA.GRADE","gradeColor(oo)"),
	("IV","IV.GRADE"," gradeColor(oo) if oo !=0 else '-'"),
	("Slope","FMA.IVSLOPE"," viewDetails(o['IV_TEST_ID'],'Test_IV',oo) if o['IV_TEST_ID'] is not None else ( oo if oo !=0 else 'n/a')"),
	("I(uA)","FMA.I150"," '%s'%(float(oo)*1e6) if oo != -1 else 'n/a'"),
	("I@20&deg;","FMA.I150"," '%.2g'%(1e6*corTemp(float(oo),float(o['FMA_TEMPVALUE']))) if oo != -1 else 'n/a'"),
	("#Def","FMA.PIXELDEFECTS",""),
	("ROC>1%","FMA.ROCSWORSEPERCENT",""),
	("PHCAL ID","FMA.PHCAL",""),
	("TRIM","FMA.TRIMMING",""),
	("Comment","FMA.COMMENT",""),
	("Dac|Perf","FMA.TEST_ID","'<a href=http://cmspixelprod.pi.infn.it/cgi-bin/rawPredefinedView.cgi?viewNumber=4&FULLMODULEANALYSISTEST_ID=%s>dac</a>|<a href=http://cmspixelprod.pi.infn.it/cgi-bin/rawPredefinedView.cgi?viewNumber=3&FULLMODULEANALYSISTEST_ID=%s>perf</a>'%(oo,oo)"),
	("DateTest","FMS.TIMESTAMP","datetime.fromtimestamp(int(oo)).strftime('%Y-%m-%d %H:%M:%S')"),
	("DateProc","Session.DATE",""),
	("Center","Session.CENTER",""),
	("Macro Version","FMA.MACRO_VERSION",""),
	("FMS ID","FMS.TEST_ID","'<a href=viewdetails.cgi?objName=Test_FullModuleSummary&TEST_ID=%s>details</a>'%oo"),
	("HIDDEN","Data.PFNs"," '<a href=%s/TestResult.html>plot</a>'%re.sub('file:','',oo) if oo else '' "),
	("HIDDEN","IV.TEST_ID",""),
	("HIDDEN","FMS.QUALIFICATIONTYPE",""),
#	("Slope2","IV.SLOPE"," oo if oo !=0 else 'n/a'"),
#	("FMT ID","FMT.TEST_ID",""),
#	("FMA ID","FMA.TEST_ID",""),
#	("FMSE id","FMSE.TEST_ID",""),
#	("FMSE SE","FMSE.SESSION_ID",""),
	 ])
rowkeys.append("FMS_TEST_ID")
queries.append("select %s from test_fullmodulesummary as FMS "
	       "join inventory_fullmodule as FM on FM.LASTTEST_FULLMODULE = FMS.TEST_ID "	
	       "left join test_fullmodule as FMT on FMS.FULLMODULETEST_IDS like concat('%%',FMT.TEST_ID,'%%') "
	       "left join test_fullmoduleanalysis as FMA on FMA.TEST_ID=(select FMA2.TEST_ID from test_fullmoduleanalysis as FMA2 where FMA2.FULLMODULETEST_ID=FMT.TEST_ID order by TEST_ID DESC limit 1) "
               "left join test_fullmodulesession as FMSE on FMSE.TEST_ID=FMT.SESSION_ID "
               "left join sessions as Session on FMSE.SESSION_ID=Session.SESSION_ID "
               "left join test_data as Data on FMA.DATA_ID=Data.DATA_ID "
               "left join test_iv as IV on IV.REF_ID=FMA.TEST_ID WHERE FM.STATUS <> 'HIDDEN' ")

countqueries.append("select COUNT(1) from test_fullmodulesummary as FMS "
               "join inventory_fullmodule as FM on FM.LASTTEST_FULLMODULE = FMS.TEST_ID "
               "left join test_fullmodule as FMT on FMS.FULLMODULETEST_IDS like concat('%%',FMT.TEST_ID,'%%') "
               "left join test_fullmoduleanalysis as FMA on FMA.TEST_ID=(select FMA2.TEST_ID from test_fullmoduleanalysis as FMA2 where FMA2.FULLMODULETEST_ID=FMT.TEST_ID order by TEST_ID DESC limit 1) "
               "left join test_fullmodulesession as FMSE on FMSE.TEST_ID=FMT.SESSION_ID "
               "left join sessions as Session on FMSE.SESSION_ID=Session.SESSION_ID "
               "left join test_data as Data on FMA.DATA_ID=Data.DATA_ID "
               "left join test_iv as IV on IV.REF_ID=FMA.TEST_ID WHERE FM.STATUS <> 'HIDDEN' ")
#countqueries.append(cq)
customjs2[10]='''$('#example').dataTable().fnFakeRowspan(0);
'''


################################################ Full Module test View ########################################
#view11
header.append('''<h1>Full Module test results (all tests, all analysis, including hidden modules) </h1>''')
columns.append([
	("Mod ID","FMS.FULLMODULE_ID","viewDetails(oo,'FullModule')"),
	("Summary ID","FMS.TEST_ID","viewDetails(oo,'Test_FullModuleSummary')"),
	("Date","Session.DATE",""),
	("Test ID","FMT.TEST_ID","viewDetails(oo,'Test_FullModule')"),
	("Step","FMT.TEMPNOMINAL",""),
	("Macro Version","FMA.MACRO_VERSION",""),
	("Analysis ID","FMA.TEST_ID","viewDetails(oo,'Test_FullModuleAnalysis')+'|<a href=http://cmspixelprod.pi.infn.it/cgi-bin/rawPredefinedView.cgi?viewNumber=4&FULLMODULEANALYSISTEST_ID=%s>dac</a>|<a href=http://cmspixelprod.pi.infn.it/cgi-bin/rawPredefinedView.cgi?viewNumber=3&FULLMODULEANALYSISTEST_ID=%s>perf</a>'%(oo,oo)"),
	#("Plots","Data.PFNs","tempWithPlot(o)"),
	("Plots","Data.PFNs"," '<a href=%s/TestResult.html>plot</a>'%re.sub('file:','',oo) if oo else '' "),
	#("Step","FMT.TEMPNOMINAL","tempWithPlot(o)"),
	("STATUS","FM.STATUS",""),
	("T","FMA.TEMPVALUE",""),
#	("Plot","Data.PFNs"," '<a href=%s/TestResult.html>plot</a>'%re.sub('file:','',oo)"),
	("GR","FMA.GRADE","gradeColor(oo)"),
        ("IV","IV.GRADE"," gradeColor(oo) if oo !=0 else 'n/a'"),
        ("Slope","FMA.IVSLOPE"," viewDetails(o['IV_TEST_ID'],'Test_IV',oo) if o['IV_TEST_ID'] is not None else ( oo if oo !=0 else 'n/a')"),
#	("Slope","FMA.IVSLOPE"," oo if oo !=0 else 'n/a'"),
	("I","FMA.I150"," '%s uA'%oo if oo != -1 else 'n/a'"),
	("#Def","FMA.PIXELDEFECTS",""),
	("ROC>1%","FMA.ROCSWORSEPERCENT",""),
	("PHCAL ID","FMA.PHCAL",""),
	("TRIM","FMA.TRIMMING",""),
	("Comment","FMA.COMMENT",""),
	("Type","FMS.QUALIFICATIONTYPE",""),
	("Center","Session.CENTER",""),
        ("HIDDEN","IV.TEST_ID",""),
 
#	("FMS ID","FMS.TEST_ID","'<a href=viewdetails.cgi?objName=Test_FullModuleSummary&TEST_ID=%s>details</a>'%oo"),
#	("FMSE id","FMSE.TEST_ID",""),
#	("FMSE SE","FMSE.SESSION_ID",""),
	 ])
customjs2[11]='''$('#example').dataTable().fnFakeRowspan(0);
               $('#example').dataTable().fnFakeRowspan(1);
              $('#example').dataTable().fnFakeRowspan(2);
              $('#example').dataTable().fnFakeRowspan(3);
              $('#example').dataTable().fnFakeRowspan(4);
'''
rowkeys.append("FMA_TEST_ID")
queries.append("select %s from test_fullmodule as FMT "
	       "left join test_fullmodulesummary as FMS on FMS.TEST_ID = FMT.SUMMARY_ID "
	       "join inventory_fullmodule as FM on FM.FULLMODULE_ID = FMT.FULLMODULE_ID "	
	       "left join test_fullmoduleanalysis as FMA on FMA.FULLMODULETEST_ID=FMT.TEST_ID "
               "left join test_fullmodulesession as FMSE on FMSE.TEST_ID=FMT.SESSION_ID "
               "left join sessions as Session on FMSE.SESSION_ID=Session.SESSION_ID "
               "left join test_data as Data on FMA.DATA_ID=Data.DATA_ID "
               "left join test_iv as IV on IV.REF_ID=FMA.TEST_ID WHERE FMS.FULLMODULE_ID=FM.FULLMODULE_ID ")

countqueries.append("select COUNT(1)  from test_fullmodule as FMT "
               "left join test_fullmodulesummary as FMS on FMS.TEST_ID = FMT.SUMMARY_ID "
               "join inventory_fullmodule as FM on FM.FULLMODULE_ID = FMT.FULLMODULE_ID " 
               "left join test_fullmoduleanalysis as FMA on FMA.FULLMODULETEST_ID=FMT.TEST_ID "
               "left join test_fullmodulesession as FMSE on FMSE.TEST_ID=FMT.SESSION_ID "
               "left join sessions as Session on FMSE.SESSION_ID=Session.SESSION_ID "
               "left join test_data as Data on FMA.DATA_ID=Data.DATA_ID "
               "left join test_iv as IV on IV.REF_ID=FMA.TEST_ID WHERE 1 ")

#countqueries.append(cq)


################################################ Full Module test View ########################################
#view12
header.append('''<h1>Full Module Overview </h1>''')
'''
        ("Mod ID","FM.FULLMODULE_ID","viewDetails(oo,'FullModule')"),
        ("Built By","FM.BUILTBY",""),
        ("Status","FM.STATUS",""),
	("Center","Transfer.RECEIVER","o['Transfer_RECEIVER'] if o['Transfer_STATUS']=='ARRIVED' else  '%s=>%s'%(o['Transfer_SENDER'],o['Transfer_RECEIVER']) "),
        ("FullQual","MAX(FQ.GRADE)"," '<a href=%s/TestResult.html>%s</a>'%(re.sub('file:','',o['FQ_DATA_ID']),gradeColor(oo)) if oo is not None else '-'"),
        ("#Def","MAX(FQ.Def)",""),
        ("ROC>1%","MAX(FQ.ROCPERCENT)",""),
        ("Reception","MAX(FR.GRADE)"," gradeColor(oo) if oo !=0 else 'n/a'"),
        ("OtherQual","MAX(OQ.GRADE)"," (gradeColor(oo)+' (%s)'%o['OQ_TYPE']) if oo is not None  else 'n/a'"),
        ("VCal","XR.VCALGRADE"," (gradeColor(oo)+' (%2.2f,%2.2f)'%(o['XR_SLOPE'],o['XR_OFFSET']))  if oo is not None  else 'n/a'"),
        ("HR","XR.HRGRADE"," gradeColor(oo) if oo is not None  else 'n/a'"),
        ("GR","XR.GRADE"," gradeColor(oo) if oo is not None  else 'n/a'"),
        ("Grade","bmGrade(IV.BAREMODULE_ID)"," gradeColor(oo) if oo !=0 else 'n/a'"),
        ("CIS","IV.CIS"," '%s'%(viewDetails(o['IV_CIS_ID'],'Test_IV',gradeColor('%1.0f'%float(oo)))) if oo is not None else ''"),
        ("NEW","IV.NEW"," '%s'%(viewDetails(o['IV_NEW_ID'],'Test_IV',gradeColor(oo))) if oo is not None else ''"),
        ("CUT","IV.CUT","'%s'%(viewDetails(o['IV_CUT_ID'],'Test_IV',gradeColor(oo))) if oo is not None else ''"),
        ("BAM","IV.BAM","'%s'%(viewDetails(o['IV_BAM_ID'],'Test_IV',gradeColor(oo))) if oo is not None else ''"),
        ("CYC","IV.CYC","'%s'%(viewDetails(o['IV_CYC_ID'],'Test_IV',gradeColor(oo))) if oo is not None else ''"),
###        ("CYC","IV.CYC","'%s (%s)'%(gradeColor(oo),viewDetails(o['IV_CYC_ID'],'Test_IV','details')) if oo is not None else ''"),
###       ("FMS ID","FMS.TEST_ID","'<a href=viewdetails.cgi?objName=Test_FullModuleSummary&TEST_ID=%s>details</a>'%oo"),
###       ("FMSE id","FMSE.TEST_ID",""),
        ("HIDDEN","OQ.TYPE",""),
        ("HIDDEN","FQ.DATA_ID",""),
        ("HIDDEN","IV.CIS_ID",""),
        ("HIDDEN","IV.NEW_ID",""),
        ("HIDDEN","IV.BAM_ID",""),
        ("HIDDEN","IV.CUT_ID",""),
        ("HIDDEN","IV.CYC_ID",""),
        ("HIDDEN","XR.SLOPE",""),
        ("HIDDEN","XR.OFFSET",""),
        ("HIDDEN","Transfer.SENDER",""),
        ("HIDDEN","Transfer.STATUS",""),
'''
columns.append([
        ("Mod ID","FM_FULLMODULE_ID","viewDetails(oo,'FullModule')"),
        ("Built By","FM_BUILTBY",""),
        ("Status","FM_STATUS",""),
        ("Center","Transfer_RECEIVER","o['Transfer_RECEIVER'] if o['Transfer_STATUS']=='ARRIVED' else  '%s=>%s'%(o['Transfer_SENDER'],o['Transfer_RECEIVER']) "),
        ("Final Gr","GREATEST(MAX_FQ_GRADE,XR_GRADE)","gradeColor(oo) if oo is not None else '-'"),
        ("FullQual","MAX_FQ_GRADE"," '<a href=%s/TestResult.html>%s</a>'%(re.sub('file:','',o['FQ_DATA_ID']),gradeColor(oo)) if oo is not None else '-'"),
        ("#Def","MAX_FQ_Def",""),
        ("ROC>1%","MAX_FQ_ROCPERCENT",""),
        ("Reception","MAX_FR_GRADE"," gradeColor(oo) if oo !=0 else '-'"),
        ("OtherQual","MAX_OQ_GRADE"," (gradeColor(oo)+' (%s)'%o['OQ_TYPE']) if oo is not None  else '-'"),
        ("VCal","XR_VCALGRADE"," (gradeColor(oo)+' (%2.2f,%2.2f)'%(o['XR_SLOPE'],o['XR_OFFSET']))  if oo is not None  else '-'"),
        ("HR","XR_HRGRADE"," gradeColor(oo) if oo is not None  else '-'"),
        ("GR","XR_GRADE"," gradeColor(oo) if oo is not None  else '-'"),
        ("Grade","bmGrade_IV_BAREMODULE_ID"," gradeColor(oo) if oo !=0 else '-'"),
#        ("BM ID","BM.BAREMODULE_ID","viewDetails(oo,'BareModule')"),
        ("CIS","IV_CIS"," '%s'%(viewDetails(o['IV_CIS_ID'],'Test_IV',gradeColor('%1.0f'%float(oo)))) if oo is not None else ''"),
        ("NEW","IV_NEW"," '%s'%(viewDetails(o['IV_NEW_ID'],'Test_IV',gradeColor(oo))) if oo is not None else ''"),
        ("CUT","IV_CUT","'%s'%(viewDetails(o['IV_CUT_ID'],'Test_IV',gradeColor(oo))) if oo is not None else ''"),
        ("BAM","IV_BAM","'%s'%(viewDetails(o['IV_BAM_ID'],'Test_IV',gradeColor(oo))) if oo is not None else ''"),
        ("CYC","IV_CYC","'%s'%(viewDetails(o['IV_CYC_ID'],'Test_IV',gradeColor(oo))) if oo is not None else ''"),
###        ("CYC","IV.CYC","'%s (%s)'%(gradeColor(oo),viewDetails(o['IV_CYC_ID'],'Test_IV','details')) if oo is not None else ''"),
###       ("FMS ID","FMS.TEST_ID","'<a href=viewdetails.cgi?objName=Test_FullModuleSummary&TEST_ID=%s>details</a>'%oo"),
###       ("FMSE id","FMSE.TEST_ID",""),
        ("HIDDEN","OQ_TYPE",""),
        ("HIDDEN","FQ_DATA_ID",""),
        ("HIDDEN","IV_CIS_ID",""),
        ("HIDDEN","IV_NEW_ID",""),
        ("HIDDEN","IV_BAM_ID",""),
        ("HIDDEN","IV_CUT_ID",""),
        ("HIDDEN","IV_CYC_ID",""),
        ("HIDDEN","XR_SLOPE",""),
        ("HIDDEN","XR_OFFSET",""),
        ("HIDDEN","Transfer_SENDER",""),
        ("HIDDEN","Transfer_STATUS",""),

         ])
customServerSide[12]="false"
groupheader[12]="<tr><th  style=\" border-right: 1px solid #111111;\"  nosearch=1 colspan=5>Inventory</th><th  style=\" border-right: 1px solid #111111;\" nosearch=1 colspan=3>Full Qualification</th><th nosearch=1  style=\" border-right: 1px solid #111111;\" colspan=2>More full tests</th> <th  style=\" border-right: 1px solid #111111;\"  nosearch=1 colspan=3>XRay tests</th> <th  style=\" border-right: 1px solid #111111;\"  nosearch=1 colspan=1>BareModule test</th><th nosearch=1 colspan=5 style=\" border-left: 1px solid #111111;\" >IV Tests</th></tr>"
rowkeys.append("FM_FULLMODULE_ID")
groupby[12]="group by FM_FULLMODULE_ID"
queries.append("select %s from view12 where 1 ")
'''
from inventory_fullmodule as FM "
	       "left join transfers as Transfer on FM.TRANSFER_ID=Transfer.TRANSFER_ID "
               "left join viewIV as IV on FM.FULLMODULE_ID=IV.FULLMODULE_ID "
               "left join view10 as FQ on FQ.FULLMODULE_ID=FM.FULLMODULE_ID "
               "left join view10reception as FR on FR.FULLMODULE_ID=FM.FULLMODULE_ID "
               "left join view10other as OQ on OQ.FULLMODULE_ID=FM.FULLMODULE_ID "
	       "left join viewXRay as XR on FM.FULLMODULE_ID=XR.FULLMODULE_ID "
	       " where FM.STATUS<>'HIDDEN' ")
'''
countqueries.append("select COUNT(1) from view12 where 1 ")
'''
,FQ.GRADE,FM.FULLMODULE_ID from inventory_fullmodule as FM "
               "left join transfers as Transfer on FM.TRANSFER_ID=Transfer.TRANSFER_ID "
               "left join viewIV as IV on FM.FULLMODULE_ID=IV.FULLMODULE_ID "
               "left join view10 as FQ on FQ.FULLMODULE_ID=FM.FULLMODULE_ID "
               "left join view10reception as FR on FR.FULLMODULE_ID=FM.FULLMODULE_ID "
               "left join view10other as OQ on OQ.FULLMODULE_ID=FM.FULLMODULE_ID "
               "left join viewXRay as XR on FM.FULLMODULE_ID=XR.FULLMODULE_ID "
               " where FM.STATUS<>'HIDDEN' ")
'''


#view13
################################################ Full Module all xray hr View ########################################

header.append('''<h1>HR XRay Module test results (all tests, all analysis, including hidden modules) </h1>''')
columns.append([
        ("Mod ID","FMS.FULLMODULE_ID","viewDetails(oo,'FullModule')"),
        ("Summary ID","FMS.TEST_ID","'%s '%(viewDetails(oo,'Test_FullModule_XRay_HR_Summary') )"),
        ("Date","Session.DATE",""),
#       ("Step","FMT.TEMPNOMINAL",""),
        ("Proc & Summ. ID","FMA.PROCESSING_ID","'%s (%s)'%(oo,o['FMS_TEST_ID'])"),
        ("Macro Version","FMA.MACRO_VERSION",""),
        ("AnaSummary ID","FMA.TEST_ID","viewDetails(oo,'Test_FullModule_XRay_HR_Module_Analysis_Summary')"),
        #("Plots","Data.PFNs","tempWithPlot(o)"),
        ("Noise ID","FMT.TEST_ID","viewDetails(oo,'Test_FullModule_XRay_HR_Module_Noise')"),
        ("Plots","DataHR.PFNs"," hrAna(o)"),
        #("Step","FMT.TEMPNOMINAL","tempWithPlot(o)"),
        ("STATUS","FM.STATUS",""),
        ("T","FMS.TEMPNOMINAL",""),
#       ("Plot","Data.PFNs"," '<a href=%s/TestResult.html>plot</a>'%re.sub('file:','',oo)"),
        ("GR","FMA.GRADE","gradeColor(oo)"),
#       ("IV","IV.GRADE"," gradeColor(oo) if oo !=0 else 'n/a'"),
#       ("Slope","FMA.IVSLOPE"," viewDetails(o['IV_TEST_ID'],'Test_IV',oo) if o['IV_TEST_ID'] is not None else ( oo if oo !=0 else 'n/a')"),
#       ("Slope","FMA.IVSLOPE"," oo if oo !=0 else 'n/a'"),
#       ("I","FMA.I150"," '%s uA'%oo if oo != -1 else 'n/a'"),
#       ("#Def","FMA.PIXELDEFECTS",""),
#       ("ROC>1%","FMA.ROCSWORSEPERCENT",""),
#       ("PHCAL ID","FMA.PHCAL",""),
#       ("TRIM","FMA.TRIMMING",""),
#       ("Comment","FMA.COMMENT",""),
#      ("Type","FMS.QUALIFICATIONTYPE",""),
        ("Center","Session.CENTER",""),
#       ("HIDDEN","IV.TEST_ID",""),
        ("Eff @50","FMA.INTERP_EFF_50",""),
        ("Eff @120","FMA.INTERP_EFF_120",""),
        ("#Pix Hot","FMA.N_HOT_PIXELS",""),
        ("#Pix NoHit","GREATEST(FMA.N_PIXEL_NO_HIT_50,FMA.N_PIXEL_NO_HIT_150)",""),

#       ("FMS ID","FMS.TEST_ID","'<a href=viewdetails.cgi?objName=Test_FullModuleSummary&TEST_ID=%s>details</a>'%oo"),
#       ("FMSE id","FMSE.TEST_ID",""),
#       ("FMSE SE","FMSE.SESSION_ID",""),
         ])
customjs2[13]='''$('#example').dataTable().fnFakeRowspan(0);
               $('#example').dataTable().fnFakeRowspan(1);
              $('#example').dataTable().fnFakeRowspan(2);
              $('#example').dataTable().fnFakeRowspan(3);
              $('#example').dataTable().fnFakeRowspan(4);
'''
rowkeys.append("FMA_TEST_ID")
queries.append("select %s from Test_FullModule_XRay_HR_Summary as FMS "
               "left join Test_FullModule_XRay_HR_Module_Analysis_Summary as FMA on FMS.TEST_ID=FMA.TEST_XRAY_HR_SUMMARY_ID "
               "left join Test_FullModule_XRay_HR_Module_Noise as FMT on FMS.TEST_ID=FMT.TEST_XRAY_HR_SUMMARY_ID and FMT.PROCESSING_ID=FMA.PROCESSING_ID "
               "join inventory_fullmodule as FM on FM.FULLMODULE_ID = FMS.FULLMODULE_ID "
               "left join sessions as Session on FMA.SESSION_ID=Session.SESSION_ID "
               "left join test_data as DataHR on FMA.DATA_ID=DataHR.DATA_ID WHERE 1 ")

countqueries.append("select COUNT(1) from Test_FullModule_XRay_HR_Summary as FMS "
               "left join Test_FullModule_XRay_HR_Module_Analysis_Summary as FMA on FMS.TEST_ID=FMA.TEST_XRAY_HR_SUMMARY_ID "
               "left join Test_FullModule_XRay_HR_Module_Noise as FMT on FMS.TEST_ID=FMT.TEST_XRAY_HR_SUMMARY_ID and FMT.PROCESSING_ID=FMA.PROCESSING_ID "
               "join inventory_fullmodule as FM on FM.FULLMODULE_ID = FMS.FULLMODULE_ID "
               "left join sessions as Session on FMA.SESSION_ID=Session.SESSION_ID "
               "left join test_data as Data on FMA.DATA_ID=Data.DATA_ID WHERE 1 ")



############################################## tools#####################################################
def coloredResult(res) :
	if res=="OK" :
		return "<font color =green>OK</font>"
	else:
		return "<font color =red>"+res+"</font>"


def viewDetails(oo,objName,text=None) :
  if text is None :
	text=oo
  return '<a href=viewdetails.cgi?objName=%s&%s=%s>%s</a>'%(objName,idField(objName),oo,text)

def gradeColor(oo) :
	if oo == "A" or oo == "A-" or oo=="1":	
		return "<font color=green>%s</font>"%oo
	if oo == "B"  or oo == "B-":	
		return "<font color=blue>%s</font>"%oo
	if oo == "C"  or oo == "C-" or oo == "0":	
		return "<font color=red>%s</font>"%oo
	return oo


