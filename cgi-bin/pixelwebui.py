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
legalNames = ["Transfer","Data","Session","Roc","Batch","Wafer","Sensor","BareModule","Hdi","Tbm","FullModule","Logbook","Test_BareModule","Test_FullModuleSession","Test_FullModuleSummary","Test_FullModule","Test_FullModuleAnalysis","Test_Tbm","Test_Hdi_Reception","Test_Hdi_TbmGluing","Test_Hdi_Bonding","Test_Hdi_Electric","Test_Hdi_Validation","Test_Roc","Test_IV","Test_IT","Test_SensorInspection","Test_BareModuleInspection","Test_BareModule_Chip","Test_CV","History","ShippingBox"]
userCenters={}
userCenters["andrea"]="PISA"
userCenters["andrei"]="ETH"
addrCenters={}
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
 for attr in keys:
  if  type(eval(objName+"."+attr)) is properties.PropertyColumn or  type(eval(objName+"."+attr)).__name__ == "date"  or  type(eval(objName+"."+attr)).__name__ == "datetime":
         columns.append(attr)
 # columns.sort()
 return columns


def corTemp(I,T) :
        kb=1.3806488e-23
        eg=1.2e-19
	T+=273.
        return I*(293.15/T)**2 * exp(-eg/(2*kb)*(1./293.15-1./T))

 
