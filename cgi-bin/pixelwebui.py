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
tier0Objects=["InputTar"]
transferObjects=['FullModule','BareModule','Sensor','Roc','Hdi','Tbm','Wafer','Batch','ShippingBox','RocWafer']
centers=['CIS','FACTORY','ETH','PSI','CERN','BARI','CATANIA','PERUGIA','PISA','UNIHH','AACHEN','HELSINKI','DESY','KIT','PADOVA','IZM','Dectris']
legalNames = ["Transfer","Data","Session","Roc","Batch","Wafer","Sensor","BareModule","Hdi","Tbm","FullModule","Test_Logbook","Test_BareModule","Test_FullModuleSession","Test_FullModuleSummary","Test_FullModule","Test_FullModuleAnalysis","Test_Tbm","Test_Hdi_Reception","Test_Hdi_TbmGluing","Test_Hdi_Bonding","Test_Hdi_Electric","Test_Hdi_Validation","Test_Roc","Test_IV","Test_IT","Test_SensorInspection","Test_BareModule_Inspection","Test_BareModule_Chip","Test_CV","History","ShippingBox","Test_DacParameters", "Test_Roc_Setup", "Test_BareModule_QA", "Test_BareModule_Grading","Test_PerformanceParameters","Test_BM_ROC_DacParameters","RocWafer","Test_FullModule_XRay_Vcal_Roc_Analysis","Test_FullModule_XRay_Vcal","Test_FullModule_XRay_Vcal_Module_Analysis","Test_FullModule_XRay_HR_Module","Test_FullModule_XRay_HR_Module_Analysis","Test_FullModule_XRay_HR_Roc","Test_FullModule_XRay_HR_Roc_Analysis"]

userCenters={}
addrCenters={}

sortedCols={}
sortedCols["Test_Hdi_Reception"]=["HDI_ID","RESULT","INSPECTION_FRONT","INSPECTION_BACK" ]
sortedCols["Test_Hdi_TbmGluing"]=["HDI_ID","RESULT","NOTES"] #notes
sortedCols["Test_Hdi_Bonding"]=["HDI_ID","RESULT","TBM_BONDS","HUB_ADDRESS_BONDS","N_TEST_BONDS","AVG_PULL_FORCE_G","NOTES"]
sortedCols["Test_Hdi_Electric"]=["HDI_ID","RESULT","NUM_TBM","DIGITAL_CURRENT_mA","SIGNALS_AND_LVS","HV600_CURRENT_uA","NOTES"]
sortedCols["Test_Hdi_Validation"]=["HDI_ID","RESULT","VISUAL_INSPECTION","NOTES"]
sortedCols["Hdi"]=["HDI_ID","STATUS","TBM1_VERSION","TBM2_VERSION","BATCH_ID","TYPE","COMMENT"]
sortedCols["Test_DacParameters"]=["ROC_POS","VDIG","VANA","VSH","VCOMP","VWLLPR","VWLLSH","VHLDDEL","VTRIM","VTHRCOMP","VIBIAS_BUS","PHOFFSET","VCOMP_ADC","PHSCALE","VICOLOR","CALDEL","CTRLREG","WBC"]
sortedCols["Test_PerformanceParameters"]=["ROC_POS"]
sortedCols["BareModule"]=["BUILTBY","BUILTON","COMMENT"]
sortedCols["RocWafer"]=["ROCWAFER_ID","LOT","TYPE","N_ROC","N_GOOD","YIELD","TEST","PRODCENTER", "NOM_THICKNESS", "COMMENT"]
sortedCols["Test_Roc"]=["SESSION_ID","TEST_ID","ROC_ID","RESULT","COMMENT","DEFECTPIXELS","MASKPIXELS","TRIMPIXELS","ADDRPIXELS","NSIGPIXELS","NOISEPIXELS","IDIGI","IANA","V24","VDCAP","VDREG","VDAC","VANASCAN","VDIGU_VOLTS","VDIGU_ADC","VANAU_VOLTS","VANAU_ADC","VANAR_ADC","VBG_ADC","IANA_MILLIAMPS","IANA_ADC"]

letterToObjName={"B":"BareModule","M":"FullModule","S":"Sensor"}


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

renderStrings={}
renderStrings["BareModule/ROC_ID"]='"<div style=\\\"white-space: nowrap; font-size: 70%% \\\">%s<br>%s</div>"%(o[rn][:100],o[rn][100:])'# "%s"%o["BareModule_ROC_ID"]'
renderStrings["BareModule/COMMENT"]='"<div style=\\\"white-space: nowrap; font-size: 80%% \\\">%s</div>"%(o[rn])'
renderStrings["RocWafer/YIELD"]='"%2.1f"%(o[rn])'
renderStrings["RocWafer/NOM_THICKNESS"]='"%d"%(o[rn])'
renderStrings["Test_BareModule_QA/FAILURES"]=' ("<div title=\\\"%s\\\">%s</div>"%(cgi.escape(o[rn],True),o[rn][:100])+"......") if len(o[rn])>100 else "%s"%(o[rn]) '

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


def printFooter() :
  ff = file("/var/www/html/nav.html")
  print "</main>"
  print ff.read()
  print "</body></html>"

def idlink(x):
  url="<a href=/cgi-bin/id.cgi?id=\\1>\\1</a>"	
#  x=re.sub("([A-Za-z]*[0-9]+-[0-9]+-*[0-9]*)",url,x)
#  x=re.sub("(M[0-9]+)(([^-0-9])+|$)",url+"\\2",x)
#  x=re.sub("([A-Z0-9]+-[0-9][0-9][A-D])",url,x)
  x=re.sub("([A-Z]*[0-9]+[A-Z0-9-]+)",url,x)
	
  return x
 
