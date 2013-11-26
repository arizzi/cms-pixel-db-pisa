import re
import cgi

legalNames = ["Transfer","Data","Session","Roc","Batch","Wafer","Sensor","BareModule","Hdi","Tbm","FullModule","Logbook","Test_BareModule","Test_FullModuleSession","Test_FullModuleSummary","Test_FullModule","Test_FullModuleAnalysis","Test_Tbm","Test_Hdi","Test_Roc","Test_IV","Test_IT","Test_SensorInspection","Test_BareModuleInspection","Test_BareModule_Chip","Test_CV","History"]

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
