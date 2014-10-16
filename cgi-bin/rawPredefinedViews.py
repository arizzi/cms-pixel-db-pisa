
columns=[]
queries=[]
countqueries=[]
rowkeys=[]

### Sensor View
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

### HDI Views


columns.append([
	("HDI ID","Hdi.HDI_ID",""),
        ("Center","Transfer.RECEIVER","o['Transfer_RECEIVER'] if o['Transfer_STATUS']=='ARRIVED' else  o['Transfer_SENDER'] "),
	("Reception","Test_Hdi_Reception.RESULT","coloredResult(o['Test_Hdi_Reception_RESULT']) if o['Test_Hdi_Reception_RESULT'] else '<a href=newhdireception>add test</a>'"),
	("Bonding","Test_Hdi_Bonding.RESULT","o['Test_Hdi_Bonding_RESULT'] if o['Test_Hdi_Bonding_RESULT'] else '<a href=/cgi-bin/writers/newTest.cgi?objName=Test_Hdi_Bonding&HDI_ID=%s>add test</a>'%o['Hdi_HDI_ID']"),
	("TBM Gluing","Test_Hdi_TbmGluing.RESULT","o['Test_Hdi_TbmGluing_RESULT'] if o['Test_Hdi_TbmGluing_RESULT'] else '<a href=newhdibonding>add test</a>'"),
	("Electric","Test_Hdi_Electric.RESULT","o['Test_Hdi_Electric_RESULT'] if o['Test_Hdi_Electric_RESULT'] else '<a href=newhdibonding>add test</a>'"),
	("Validation","Test_Hdi_Validation.RESULT","o['Test_Hdi_Validation_RESULT'] if o['Test_Hdi_Validation_RESULT'] else '<a href=newhdibonding>add test</a>'"),
])
rowkeys.append("Hdi_HDI_ID") #not obvious
queries.append("select %s,Transfer.STATUS as Transfer_STATUS, Transfer.SENDER as Transfer_SENDER from inventory_hdi as Hdi join transfers as Transfer on Hdi.TRANSFER_ID=Transfer.TRANSFER_ID "
		"left outer join test_hdi_reception as Test_Hdi_Reception on Hdi.HDI_ID=Test_Hdi_Reception.HDI_ID "
		"left outer join test_hdi_bonding as Test_Hdi_Bonding on Hdi.HDI_ID=Test_Hdi_Bonding.HDI_ID "
		"left outer join test_hdi_tbmgluing as Test_Hdi_TbmGluing on Hdi.HDI_ID=Test_Hdi_TbmGluing.HDI_ID "
		"left outer join test_hdi_electric as Test_Hdi_Electric on Hdi.HDI_ID=Test_Hdi_Electric.HDI_ID "
		"left outer join test_hdi_validation as Test_Hdi_Validation on Hdi.HDI_ID=Test_Hdi_Validation.HDI_ID "
		" WHERE 1 ")
countqueries.append("select COUNT(1)  from inventory_hdi")



### tools
def coloredResult(res) :
	if res=="OK" :
		return "<font color =green>OK</font>"
	else:
 	   return res

### Automatic object views
from pixelwebui import *
import sys
sys.path.append("../PixelDB")
from storm.properties import *
from storm.references import *
from storm import *
from PixelDB import *

def fromObjectName(objName):
	cols = []
	refs = []
	i =0
	objType = eval(parseObjName(objName))
	ID=idField(objName)
	table=objType.__storm_table__
	keys=objType.__dict__.keys()
	hasTrans=False
	for attr in keys:
	    if attr == "TRANSFER_ID" and table!="transfers" :
                hasTrans=True

	#    print attr #,type(eval(objName+"."+attr)).__name__,"<br>"
	    if  type(eval(objName+"."+attr)) is properties.PropertyColumn or  type(eval(objName+"."+attr)).__name__ == "date"  or  type(eval(objName+"."+attr)).__name__ == "datetime":
	#    if  type(eval(objName+"."+attr)) is properties.PropertyColumn :
	         cols.append(attr)
	    if  type(eval(objName+"."+attr)) is references.Reference :
	         refs.append(attr)
	cols.sort()
	cformat=[]
	#cformat.append((ID,"",'"%s"%(o[ID])+"(<a href=\"viewdetails.cgi?objName="+objName+"&"+ID+"="+"%s"%(o[ID])+"\">details</a>|<a href=\"writers/edit.cgi?objName="+objName+"&"+ID+"="+"%s"%(o[ID])+"\">edit</a>)'")

	cformat.append((ID,ID,'"%s"%(o["'+ID+'"])+" (<a href=\\\"viewdetails.cgi?objName='+objName+'&'+ID+'="+"%s"%(o["'+ID+'"])+"\\\">details</a>|<a href=\\\"writers/edit.cgi?objName='+objName+'&'+ID+'="+"%s"%(o["'+ID+'"])+"\\\">edit</a>)"'))
	if hasTrans:
	    cformat.append(("Center","Transfer.RECEIVER","o['Transfer_RECEIVER'] if o['Transfer_STATUS']=='ARRIVED' else  '%s=>%s'%(o['Transfer_SENDER'],o['Transfer_RECEIVER']) "))
 #       if o["TSTATUS"] == "ARRIVED" :
 #               row.append(o["RECEIVER"])
  #      else:
   #             row.append("%s to %s"%(o["SENDER"],o["RECEIVER"]))

	for c in cols:
	    cformat.append((c.lower().capitalize(),table+"."+c,''))
	for r in refs:
	    cformat.append((r.lower().capitalize(),'','"<a href=\\\"viewdetails.cgi?objName='+objName+'&'+ID+'="+"%s"%(o["'+ID+'"])+"&ref='+r+'\\\"> details</a></td>"'))
	# rowkey,cols,query,countquery
	if hasTrans :
		return 	ID,cformat,("select %s,Transfer.STATUS as Transfer_STATUS, Transfer.SENDER as Transfer_SENDER from %s left join transfers as Transfer on %s.TRANSFER_ID=Transfer.TRANSFER_ID WHERE  1 "%('%s',table,table)), ("select COUNT(1) from %s"%table)
	else:
		return 	ID,cformat,("select %s from %s WHERE 1"%('%s',table)), ("select COUNT(1) from %s"%table)

