
columns=[]
queries=[]
countqueries=[]
rowkeys=[]
columns.append([
#"Sel","'<input type=checkbox name=sel>'"),
#          ("Sensor id","'%s<input type=checkbox name=sel_sensor%s>%s'%(o[0].SENSOR_ID,o[0].SENSOR_ID)"),
           ("Sensor ID","Sensor.SENSOR_ID",""),#"'<input type=checkbox name=sel_sensor%s>%s'%(o['Sensor_SENSOR_ID'],o['Sensor_SENSOR_ID'])"),
           ("Status","Sensor.STATUS",''),
           ("Center","Transfer.RECEIVER","o['Transfer_RECEIVER'] if o['Transfer_STATUS']=='ARRIVED' else  o['Transfer_SENDER'] "),
 #"if o['Transfer_STATUS']=='NEW' : print  o['Transfer_SENDER']; else :  print  o['Transfer_RECEIVER'];"),
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
#           ("Test id","'%s<input type=checkbox name=sel_sensor%s>'%(o[1].TEST_ID,o[1].TEST_ID)"),
#          ("Test id","Test_IV.TEST_ID",""'<input type=checkbox name=sel_sensor%s>%s'%(o['Test_IV.TEST_ID'],o['Test_IV.TEST_ID']"),
           ("Test id","Test_IV.TEST_ID",''),
           ("Files","Data.PFNs","'<a href=%s>link</a>'%o['Data_PFNs']"),
          ])
rowkeys.append("Test_IV_TEST_ID");
queries.append("select %s,Transfer.STATUS as Transfer_STATUS, Transfer.SENDER as Transfer_SENDER from inventory_sensor as Sensor, test_iv as Test_IV,transfers as Transfer,test_data as Data where Sensor.SENSOR_ID=Test_IV.SENSOR_ID and  Sensor.TRANSFER_ID=Transfer.TRANSFER_ID and Data.DATA_ID=Test_IV.DATA_ID ")
countqueries.append("select COUNT(1) from inventory_sensor as Sensor, test_iv as Test_IV,transfers as Transfer,test_data as Data where Sensor.SENSOR_ID=Test_IV.SENSOR_ID and  Sensor.TRANSFER_ID=Transfer.TRANSFER_ID and Data.DATA_ID=Test_IV.DATA_ID ")

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

	cformat.append((ID,ID,'"%s"%(o["'+ID+'"])+"(<a href=\\\"viewdetails.cgi?objName='+objName+'&'+ID+'="+"%s"%(o["'+ID+'"])+"\\\">details</a>|<a href=\\\"writers/edit.cgi?objName='+objName+'&'+ID+'="+"%s"%(o["'+ID+'"])+"\\\">edit</a>)"'))
	if hasTrans:
	    cformat.append(("Center","Transfer.RECEIVER","o['Transfer_RECEIVER'] if o['Transfer_STATUS']=='ARRIVED' else  o['Transfer_SENDER'] "))
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

