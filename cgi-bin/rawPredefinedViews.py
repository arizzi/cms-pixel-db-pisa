
##################################### Automatic object views ######################################
from pixelwebui import *
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

def fromObjectName(objName):
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
	    if attr == "SESSION_ID" and table!="sessions" :
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
	    cformat.append((c.lower().capitalize(),table+"."+c,renderString(c,objName)))
	for r in refs:
	    cformat.append((r.lower().capitalize(),'','"<a href=\\\"viewdetails.cgi?objName='+objName+'&'+ID+'="+"%s"%(o["'+IDF2+'"])+"&ref='+r+'\\\"> details</a></td>"'))

	     	
	

	# rowkey,cols,query,countquery
	if hasTrans :
		return 	IDF2,cformat,("select %s,Transfer.STATUS as Transfer_STATUS, Transfer.SENDER as Transfer_SENDER from %s left join transfers as Transfer on %s.TRANSFER_ID=Transfer.TRANSFER_ID WHERE  1 "%('%s',table,table)), ("select COUNT(1) from %s"%table)
	elif hasSession :
		cformat.insert(1,("Date","Session.DATE",""))
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
	("HDI ID","Hdi.HDI_ID","'<a href=/cgi-bin/viewdetails.cgi?objName=Hdi&HDI_ID=%s>%s</a>'%(o['Hdi_HDI_ID'],o['Hdi_HDI_ID'])"),
        ("Center","Transfer.RECEIVER","o['Transfer_RECEIVER'] if o['Transfer_STATUS']=='ARRIVED' else  o['Transfer_SENDER'] "),
	("TBM 1","Hdi.TBM1_VERSION",""),
	("TBM 2","Hdi.TBM2_VERSION",""),
#	("Reception","Test_Hdi_Reception.RESULT","coloredResult(o['Test_Hdi_Reception_RESULT']) if o['Test_Hdi_Reception_RESULT'] else '<a href=/cgi-bin/writers/newTest.cgi?objName=Test_Hdi_Reception&HDI_ID=%s>add test</a>'%o['Hdi_HDI_ID']"),

	#("Bonding","Test_Hdi_Bonding.RESULT","o['Test_Hdi_Bonding_RESULT'] if o['Test_Hdi_Bonding_RESULT'] else '<a href=/cgi-bin/writers/newTest.cgi?objName=Test_Hdi_Bonding&HDI_ID=%s>add test</a>'%o['Hdi_HDI_ID']"),
	#("TBM Gluing","Test_Hdi_TbmGluing.RESULT","hdiTbmGlue(o)"),
	#("Electric","Test_Hdi_Electric.RESULT"," '%s (<a href=/cgi-bin/writers/edit.cgi?objName=Test_Hdi_Electric&TEST_ID=%s>edit</a>)'%(o['Test_Hdi_Electric_RESULT'],o['Hdi_LASTTEST_HDI_ELECTRIC']) if o['Test_Hdi_Electric_RESULT'] else '<a href=/cgi-bin/writers/newTest.cgi?objName=Test_Hdi_Electric&HDI_ID=%s>add test</a>'%o['Hdi_HDI_ID']"),
	#("Validation","Test_Hdi_Validation.RESULT","o['Test_Hdi_Validation_RESULT'] if o['Test_Hdi_Validation_RESULT'] else '<a href=/cgi-bin/writers/newTest.cgi?objName=Test_Hdi_Validation&HDI_ID=%s>add test</a>'%o['Hdi_HDI_ID']"),
#
	("Reception","Test_Hdi_Reception.RESULT","testEntry(o,'Test_Hdi_Reception')"),
	("TBM Gluing","Test_Hdi_TbmGluing.RESULT","hdiTbmGlue(o)"),
	("Bonding","Test_Hdi_Bonding.RESULT","testEntry(o,'Test_Hdi_Bonding')"),
#	("Electric","Test_Hdi_Electric.RESULT","testEntry(o,'Test_Hdi_Electric')"),
	("Electric","Test_Hdi_Electric.RESULT","('%s %s(<a href=/cgi-bin/writers/edit.cgi?objName=Test_Hdi_Electric&TEST_ID=%s>edit</a>)%s'%(coloredResult(o['Test_Hdi_Electric_RESULT']),testDetails(o,'Test_Hdi_Electric'),o['Hdi_LASTTEST_HDI_ELECTRIC'],testNotes(o,'Test_Hdi_Electric')) if o['Test_Hdi_Electric_RESULT'] else 'n/a')+' <a href=/cgi-bin/writers/newTest.cgi?objName=Test_Hdi_Electric&HDI_ID=%s><img src=/icons/add.png width=16></a>'%o['Hdi_HDI_ID']"),
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
        ("Pos on wafer","Roc.ROC_POSITION",""),
        ("","Roc.LASTTEST_ROC","NOPRINT"),

])
rowkeys.append("Roc_ROC_ID") #not obvious
queries.append("select %s,Transfer.STATUS as Transfer_STATUS, Transfer.SENDER as Transfer_SENDER from inventory_roc as Roc left outer join transfers as Transfer on Roc.TRANSFER_ID=Transfer.TRANSFER_ID "
                "left outer join test_roc as Test_Roc on Roc.LASTTEST_ROC=Test_Roc.TEST_ID "
                " WHERE 1 ")
countqueries.append("select COUNT(1)  from inventory_roc")

################################################ TestParams View ########################################
header.append('''<h1>Overview of PerformanceParamters</h1>''')
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
c.insert(1,("Full Module","FMT.FULLMODULE_ID",""))
rowkeys.append(i)
queries.append("select %s from test_performanceparameters left outer join test_fullmoduleanalysis as FMA on FMA.TEST_ID=FULLMODULEANALYSISTEST_ID left outer join test_fullmodule as FMT on FMT.TEST_ID=FMA.FULLMODULETEST_ID left join test_fullmodulesession as s1 on s1.TEST_ID=FMT.SESSION_ID left join sessions as Session on s1.SESSION_ID=Session.SESSION_ID WHERE 1")
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
c.insert(1,("Full Module ID","FMT.FULLMODULE_ID",""))
rowkeys.append(i)
queries.append("select %s from test_dacparameters left outer join test_fullmoduleanalysis as FMA on FMA.TEST_ID=FULLMODULEANALYSISTEST_ID left outer join test_fullmodule as FMT on FMT.TEST_ID=FMA.FULLMODULETEST_ID left join test_fullmodulesession as s1 on s1.TEST_ID=FMT.SESSION_ID left join sessions as Session on s1.SESSION_ID=Session.SESSION_ID WHERE 1")
countqueries.append("select COUNT(1)from test_dacparameters left outer join test_fullmoduleanalysis as FMA on FMA.TEST_ID=FULLMODULEANALYSISTEST_ID left outer join test_fullmodule as FMT on FMT.TEST_ID=FMA.FULLMODULETEST_ID  left join test_fullmodulesession as s1 on s1.TEST_ID=FMT.SESSION_ID left join sessions as Session on s1.SESSION_ID=Session.SESSION_ID WHERE 1")
#countqueries.append(cq)
columns.append(c)

################################################ BareModule tests View ########################################

header.append('''<h1>BareModule Tests summary  view</h1>
<img src=/icons/viewmag.png width=16> = view test details <p>
<img src=/icons/add.png width=16> = add new test <p>
''')

def testEntryBM(o,testname,res="_RESULT"):
	 testnameObj=testname
	 typestr=""
	 m=re.match('Test_BareModule_QA_(.*)',testname )
	 if  m :
		testnameObj="Test_BareModule_QA"
		typestr="&TYPE="+m.group(1)	
         ret="n/a"
         if  o[testname+res] :
                ret=(o[testname+res])+testDetails(o,testname)+" "
         ret+=' <a href=/cgi-bin/writers/newTest.cgi?objName='+testnameObj+'&BAREMODULE_ID=%s%s><img src=/icons/add.png width=16></a>'%(o['BareModule_BAREMODULE_ID'],typestr)
         ret+=testNotes(o,testname)
         return ret


columns.append([
	("BARE MODULE  ID","BareModule.BAREMODULE_ID","'<a href=/cgi-bin/viewdetails.cgi?objName=BareModule&BAREMODULE_ID=%s>%s</a>'%(o['BareModule_BAREMODULE_ID'],o['BareModule_BAREMODULE_ID'])"),
        ("Center","Transfer.RECEIVER","o['Transfer_RECEIVER'] if o['Transfer_STATUS']=='ARRIVED' else  o['Transfer_SENDER'] "),
	("Inspection","Test_BareModule_Inspection.RESULT","testEntryBM(o,'Test_BareModule_Inspection')"),
	("BumpBonding Tot failures","Test_BareModule_QA_BumpBonding.TOTAL_FAILURES","testEntryBM(o,'Test_BareModule_QA_BumpBonding','_TOTAL_FAILURES')"),
	("PixelAlive Tot failures","Test_BareModule_QA_PixelAlive.TOTAL_FAILURES","testEntryBM(o,'Test_BareModule_QA_PixelAlive','_TOTAL_FAILURES')"),
	("Global Grade","Test_BareModule_Grading.GLOBAL_GRADING","testEntryBM(o,'Test_BareModule_Grading','_GLOBAL_GRADING')"),
        ("i1","Test_IV.I1","'%6g'%o['Test_IV_I1'] if o['Test_IV_I1'] is not None else 'n/a'"),
        ("i2","Test_IV.I2","'%6g'%o['Test_IV_I2'] if o['Test_IV_I2'] is not None else 'n/a'"),
        ("Slope","Test_IV.SLOPE",''),
        ("i1@CIS","Test_IVCIS.I1","'%6g'%o['Test_IVCIS_I1'] if o['Test_IVCIS_I1'] is not None else 'n/a'"),
        ("i2@CIS","Test_IVCIS.I2","'%6g'%o['Test_IVCIS_I2'] if o['Test_IVCIS_I2'] is not None else 'n/a'"),
        ("Slope@CIS","Test_IVCIS.SLOPE",''),
        ("","Test_BareModule_Inspection.TEST_ID","NOPRINT"),
        ("","Test_BareModule_QA_BumpBonding.TEST_ID","NOPRINT"),
        ("","Test_BareModule_QA_PixelAlive.TEST_ID","NOPRINT"),
        ("","Test_BareModule_Grading.TEST_ID","NOPRINT"),

])
rowkeys.append("BareModule_BAREMODULE_ID") #not obvious
queries.append("select %s,Transfer.STATUS as Transfer_STATUS, Transfer.SENDER as Transfer_SENDER from inventory_baremodule as BareModule join transfers as Transfer on BareModule.TRANSFER_ID=Transfer.TRANSFER_ID "
		"left outer join test_baremodule_qa as Test_BareModule_QA_PixelAlive on BareModule.LASTTEST_BAREMODULE_QA_PIXELALIVE=Test_BareModule_QA_PixelAlive.TEST_ID "
		"left outer join test_baremodule_qa as Test_BareModule_QA_BumpBonding on BareModule.LASTTEST_BAREMODULE_QA_BONDING=Test_BareModule_QA_BumpBonding.TEST_ID "
		"left outer join test_baremodule_grading as Test_BareModule_Grading on BareModule.LASTTEST_BAREMODULE_GRADING=Test_BareModule_Grading.TEST_ID "
		"left outer join test_baremodule_inspection as Test_BareModule_Inspection on BareModule.LASTTEST_BAREMODULE_INSPECTION=Test_BareModule_Inspection.TEST_ID "
		"left outer join test_iv as Test_IVCIS on Test_IVCIS.SENSOR_ID=BareModule.SENSOR_ID and Test_IVCIS.TYPE='CIS' "
		"left outer join test_iv as Test_IV on Test_IV.SENSOR_ID=BareModule.SENSOR_ID and Test_IV.TYPE='BAM' "
		" WHERE 1 ")
countqueries.append("select COUNT(1)  from inventory_hdi")


############################################## tools#####################################################
def coloredResult(res) :
	if res=="OK" :
		return "<font color =green>OK</font>"
	else:
		return "<font color =red>"+res+"</font>"




