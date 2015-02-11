from math import *
import sys
sys.path.append("../PixelDB")
from storm.properties import *
from storm.references import *
from storm.variables import (
    Variable, VariableFactory, BoolVariable, IntVariable, FloatVariable,
    DecimalVariable, RawStrVariable, UnicodeVariable, DateTimeVariable,
    DateVariable, TimeVariable, TimeDeltaVariable, PickleVariable,
    ListVariable, EnumVariable)

from storm import *

from PixelDB import *
import re
import cgi
import os
transferObjects=['FullModule','BareModule','Sensor','Roc','Hdi','Tbm','Wafer','Batch','ShippingBox']
centers=['CIS','FACTORY','ETH','PSI','CERN','BARI','CATANIA','PERUGIA','PISA','HAMBURG','AACHEN','HELSINKI','DESY','KIT']
legalNames = ["Transfer","Data","Session","Roc","Batch","Wafer","Sensor","BareModule","Hdi","Tbm","FullModule","Logbook","Test_BareModule","Test_FullModuleSession","Test_FullModuleSummary","Test_FullModule","Test_FullModuleAnalysis","Test_Tbm","Test_Hdi_Reception","Test_Hdi_TbmGluing","Test_Hdi_Bonding","Test_Hdi_Electric","Test_Hdi_Validation","Test_Roc","Test_IV","Test_IT","Test_SensorInspection","Test_BareModule_Inspection","Test_BareModule_Chip","Test_CV","History","ShippingBox","Test_DacParameters", "Test_Roc_Setup", "Test_BareModule_QA", "Test_BareModule_Grading","Test_PerformanceParameters","Test_BM_ROC_DacParameters","RocWafer","Test_FullModule_XRay_Vcal_Roc_Analysis","Test_FullModule_XRay_Vcal","Test_FullModule_XRay_Vcal_Module_Analysis"]
userCenters={}
addrCenters={}

sortedCols={}
sortedCols["Test_Hdi_Reception"]=["HDI_ID","RESULT","INSPECTION_FRONT","INSPECTION_BACK" ]
sortedCols["Test_Hdi_TbmGluing"]=["HDI_ID","RESULT","NOTES"] #notes
sortedCols["Test_Hdi_Bonding"]=["HDI_ID","RESULT","TBM_BONDS","HUB_ADDRESS_BONDS","N_TEST_BONDS","AVG_PULL_FORCE_G","NOTES"]
sortedCols["Test_Hdi_Electric"]=["HDI_ID","RESULT","NUM_TBM","DIGITAL_CURRENT_mA","SIGNALS_AND_LVS","HV600_CURRENT_uA","NOTES"]
sortedCols["Test_Hdi_Validation"]=["HDI_ID","RESULT","VISUAL_INSPECTION","NOTES"]
sortedCols["Hdi"]=["HDI_ID","STATUS","TBM1_VERSION","TBM2_VERSION","BATCH_ID","TYPE","COMMENT"]
sortedCols["Test_DacParameters"]=["ROC_POS","VDIG","VANA","VSH","VCOMP","VWLLPR","VWLLSH","VHLDDEL","VTRIM","VTHRCOMP","VIBIAS_BUS","PHOFFSET","VCOMP_ADC","PHSCALE","VICOLOR","VCAL","CALDEL","CTRLREG","WBC"]
sortedCols["Test_PerformanceParameters"]=["ROC_POS"]
# HDI_ID > center > status (assumendo questo sara' lo stato globale
# dell' oggetto: OK or BAD o missing tests) >  TBM1_version > TBM2_Version >
# Lasttest_hdi_Reception > Lasttest_hdi_TBM Gluing > Lasttest_hdi_Bonding >
# Lasttest_hdi_Electric > Lasttest_hdi_Validation > Transfer (o Transfer_Id
# clickabile) > Batch_id (o Lot_id se rinominata)> Type )o Version se
# rinominata) > Comment
#* nella Gluing table input I/F: Reorder more logically:
#Test_id > HDI_id > Session_id > Notes > Data_id > Result (currently Notes is at the end)

#* nella Inventory overview: Reorder more logically the test-related columns:
#Lasttest_hdi_Reception > Lasttest_hdi_TBM Gluing > Lasttest_hdi_Bonding > Lasttest_hdi_Electric > Lasttest_hdi_Validation 

sortedInputCols={}
sortedInputCols["Test_Hdi_Reception"]=["TEST_ID","HDI_ID","SESSION_ID","INSPECTION_FRONT","INSPECTION_BACK","DATA_ID","RESULT"]
sortedInputCols["Test_Hdi_TbmGluing"]=["TEST_ID","HDI_ID","SESSION_ID","NOTES","DATA_ID","RESULT"]
sortedInputCols["Test_Hdi_Bonding"]=["TEST_ID","HDI_ID","SESSION_ID","TBM_BONDS","HUB_ADDRESS_BONDS","N_TEST_BONDS","AVG_PULL_FORCE_G","NOTES","DATA_ID","RESULT"]
sortedInputCols["Test_Hdi_Electric"]=["TEST_ID","HDI_ID","SESSION_ID","NUM_TBM","DIGITAL_CURRENT_mA","SIGNALS_AND_LVS","HV600_CURRENT_uA","NOTES","DATA_ID","RESULT"]
sortedInputCols["Test_Hdi_Validation"]=["TEST_ID","HDI_ID","SESSION_ID","VISUAL_INSPECTION","NOTES","DATA_ID","RESULT"]
sortedInputCols["Hdi"]=sortedCols["Hdi"]

def defaultCenter() :
	user=os.environ['REMOTE_USER']
	host=os.environ['REMOTE_ADDR']
	if user.upper() in centers :
		return user.upper()
	if user in userCenters.keys() :
		return userCenters[user]
	if host in addrCenters.keys() :
		return addrCenters[user]
	return ""

def parseObjName(objName) :
    for name in legalNames:
     if objName == name :
       return name
    return "empty"


def idField(objName):
  if re.match("test",objName,flags=re.IGNORECASE) :
    ID="TEST_ID"
  else:
    ID=objName+"_ID"
    ID=ID.upper()
  return ID

def idFieldTypedValue(objName,objID):
  if re.match("test",objName,flags=re.IGNORECASE) :
    objID = cgi.escape(objID)
    filterValue=int(objID)
  else:
    ID=objName+"_ID"
    ID=ID.upper()
    if objName == "Transfer"  or objName == "Data" or objName == "Session":
      objID = cgi.escape(objID)
      filterValue=int(objID)
    else :
      objID = cgi.escape(objID)
      filterValue=unicode(objID)
  return filterValue 

def allColumns(objName):
 objType = eval(parseObjName(objName))
 columns=[]
 keys=objType.__dict__.keys()
 hasTrans=False
 for attr in keys:
  if  type(eval(objName+"."+attr)) is properties.PropertyColumn or  type(eval(objName+"."+attr)).__name__ == "date"  or  type(eval(objName+"."+attr)).__name__ == "datetime":
         columns.append(attr) 
         if attr == "TRANSFER_ID" :
                hasTrans=True
  if  type(eval(objName+"."+attr)) is references.Reference :
         refs.append(attr)
  columns.sort()
  results=[]
  for c in columns :
     results.append((c,c))
  for r in refs :
     results.append((r,r))
 return results

def onlyColumns(objName):
 objType = eval(parseObjName(objName))
 keys=objType.__dict__.keys()
 columns=[]
 if objName in sortedInputCols:
	columns = sortedInputCols[objName]
 for attr in keys:
  if  type(eval(objName+"."+attr)) is properties.PropertyColumn or  type(eval(objName+"."+attr)).__name__ == "date"  or  type(eval(objName+"."+attr)).__name__ == "datetime":
	if attr not in columns :
	         columns.append(attr)
 # columns.sort()
 return columns


def corTemp(I,T) :
        kb=1.3806488e-23
        eg=1.2e-19
	T+=273.
        return I*(293.15/T)**2 * exp(-eg/(2*kb)*(1./293.15-1./T))

 
