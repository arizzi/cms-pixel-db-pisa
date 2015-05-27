#!/usr/bin/env python

# enable debugging
#import cgitb
from datetime import *
#cgitb.enable()

from MySQLdb import *
from storm.locals import *


#
# transfer
#
class Transfer (object):
    __storm_table__ = "transfers"
    TRANSFER_ID=Int(primary=True)
    SENDER=Unicode()
    RECEIVER=Unicode()
    ISSUED_DATE=DateTime()
    RECEIVED_DATE=DateTime() 
    STATUS=Unicode()
    COMMENT=Unicode()
    TRACKING=Unicode()
    def __init__(self, SENDER,RECEIVER, ISSUED_DATE=datetime.now(), RECEIVED_DATE=datetime.now(), STATUS="ARRIVED", COMMENT="", TRACKING=""):
        self.SENDER=unicode(SENDER)
        self.RECEIVER=unicode(RECEIVER)
        self.ISSUED_DATE=ISSUED_DATE
        self.RECEIVED_DATE=RECEIVED_DATE
        self.STATUS=unicode(STATUS)
        self.COMMENT=unicode(COMMENT)
        self.TRACKING=unicode(TRACKING)

class Data(object):
      __storm_table__ = "test_data"
      DATA_ID = Int(primary=True)
      URLs = Unicode()
      PFNs=Unicode()
      COMMENT=Unicode()
      def __init__(self,URLs="", PFNs="", COMMENT=""):
            self.URLs=unicode(URLs)
            self.PFNs=unicode(PFNs)
            self.COMMENT=unicode(COMMENT)


#
# Session
#
class Session (object):
    __storm_table__ = "sessions"
    SESSION_ID=Int(primary=True)
    CENTER=Unicode()
    OPERATOR=Unicode()
    DATE=DateTime()
    TYPE=Unicode()
    COMMENT=Unicode()
    def __init__(self,CENTER, OPERATOR,TYPE="TESTSESSION",DATE=datetime.now(), COMMENT=""):
        self.CENTER=unicode(CENTER)
        self.OPERATOR=unicode(OPERATOR)
        self.DATE=DATE
        self.TYPE=unicode(TYPE)
        self.COMMENT=unicode(COMMENT)
    
#
# inventory
#

class BaseStripBatch(object):
    __storm_table__ = "inventory_basestripbatch"
    BSBATCH_ID = Unicode()
    LENGTH = Float()
    COMMENT = Unicode()
    TYPE = Unicode()
    NDELIVERED = Int()
    def __init__ (self, BSBATCH_ID, LENGTH, NDELIVERED,COMMENT="", TYPE=""):
        self.BSBATCH_ID = unicode(BSBATCH_ID)
        self.LENGTH = float(LNGTH)
        self.NDELIVERED = int(NDELIVERED)
        self.COMMENT = unicode(COMMENT)
        self.TYPE = unicode(TYPE)

class CableBatch(object):
    __storm_table__ = "inventory_cablebatch"
    CABLEBATCH_ID = Unicode()
    LENGTH = Float()
    COMMENT = Unicode()
    NDELIVERED = Int()
    TYPE=Unicode()
    def __init__ (self, CABLEBATCH_ID, LENGTH, NDELIVERED,TYPE="",COMMENT=""):
        self.BSBATCH_ID = unicode(BSBATCH_ID)
        self.LENGTH = float(LNGTH)
        self.NDELIVERED = int(NDELIVERED)
        self.COMMENT = unicode(COMMENT)
        self.TYPE = unicode(TYPE)

class Roc(object):
  __storm_table__ = "inventory_roc"
  ROC_ID = Unicode(primary=True)
  WAFER_ID = Unicode()
  ROC_POSITION = Unicode()
  GRADING_CLASS = Unicode()
  TRANSFER_ID = Int()
  transfer = Reference(TRANSFER_ID, Transfer.TRANSFER_ID)
  COMMENT = Unicode()
  STATUS=Unicode()
  LASTTEST_ROC=Int()
  TYPE=Unicode()
  def __init__(self,ROC_ID, TRANSFER_ID, COMMENT="",LASTTEST_ROC=0, STATUS="",WAFER_ID="",ROC_POSITION="",GRADING_CLASS="",TYPE=""):
      self.ROC_ID=unicode(ROC_ID)
      self.TRANSFER_ID=(TRANSFER_ID)
      self.COMMENT=unicode(COMMENT)
      self.LASTTEST_ROC = LASTTEST_ROC
      self.STATUS=unicode(STATUS)
      self.WAFER_ID=unicode(WAFER_ID)
      self.ROC_POSITION=unicode(ROC_POSITION)
      self.GRADING_CLASS=unicode(GRADING_CLASS)
      self.TYPE=unicode(TYPE)
    

class RocWafer (object):
    __storm_table__ = "inventory_roc_wafer"
    ROCWAFER_ID = Unicode(primary=True)
    TRANSFER_ID=Int()
    transfer = Reference(TRANSFER_ID, Transfer.TRANSFER_ID)
    PRODCENTER = Unicode()
    COMMENT = Unicode()
    DATA_ID=Int()
    data=Reference(DATA_ID,Data.DATA_ID)
    NOM_THICKNESS= Float()
    N_GOOD=Int()
    N_ROC=Int()
    YIELD = Float()
    TYPE = Unicode() 
    TEST = Unicode() 
    LOT = Unicode() 
    def __init__(self,ROCWAFER_ID, TRANSFER_ID, PRODCENTER, NOM_THICKNESS, YIELD, TYPE, N_GOOD, DATA_ID, N_ROC,LOT,TEST,COMMENT=""):
         self.ROCWAFER_ID=unicode(ROCWAFER_ID)
         self.TRANSFER_ID=TRANSFER_ID
         self.PRODCENTER=unicode(PRODCENTER)
         self.COMMENT=unicode(COMMENT)
         self.TYPE=unicode(TYPE)
         self.TEST=unicode(TEST)
         self.LOT=unicode(LOT)
         self.DATA_ID=DATA_ID
         self.NOM_THICKNESS=float(NOM_THICKNESS)
         self.YIELD=float(YIELD)
         self.N_GOOD=int(N_GOOD)
         self.N_ROC=int(N_ROC)

class Batch(object):
     __storm_table__ = "inventory_batch"
     BATCH_ID = Unicode(primary=True)
     TRANSFER_ID=Int()
     transfer = Reference(TRANSFER_ID, Transfer.TRANSFER_ID)
     COMMENT = Unicode()
     DATA_ID=Int()
     data=Reference(DATA_ID,Data.DATA_ID)
     RESULT=Unicode()   
     def __init__(self,BATCH_ID,TRANSFER_ID,  PRODCENTER="N/A", COMMENT="", DATA_ID=0, RESULT=""):
         self.BATCH_ID=unicode(BATCH_ID)
         self.TRANSFER_ID=TRANSFER_ID
         self.PRODCENTER=unicode(PRODCENTER)
         self.COMMENT=unicode(COMMENT)
         self.RESULT=unicode(RESULT)
         self.DATA_ID=DATA_ID

class Wafer(object):
    __storm_table__ = "inventory_wafer"
    WAFER_ID = Unicode(primary=True)
    BATCH_ID=Unicode()
    batch = Reference(BATCH_ID, Batch.BATCH_ID)
    TRANSFER_ID=Int()
    transfer = Reference(TRANSFER_ID, Transfer.TRANSFER_ID)
    METALIZATION=Unicode()
    PASSIVATION=Unicode()
    UNDER_BUMP_METALIZATION=Unicode()
    SIZE_OF_OPENING=Unicode()
    VDEPL = Unicode()
    OPTICAL_INSPECTION=Unicode()
    OPTICAL_INSPECTION_RESULT=Unicode()
    COMMENT = Unicode()
    DATA_ID=Int()
    data=Reference(DATA_ID,Data.DATA_ID)
    NUMBEROFGOODSENSORS=Int()
    RESULT=Unicode()

    def __init__(self,WAFER_ID,BATCH_ID, TRANSFER_ID, METALIZATION="", PASSIVATION="", UNDER_BUMP_METALIZATION="", SIZE_OF_OPENING="", VDEPL="", OPTICAL_INSPECTION="", OPTICAL_INSPECTION_RESULT="", COMMENT="",DATA_ID=0, NUMBEROFGOODSENSORS=0, RESULT=""):
        self.BATCH_ID=unicode(BATCH_ID)
        self.WAFER_ID=unicode(WAFER_ID)
        self.TRANSFER_ID=TRANSFER_ID
        self.COMMENT=unicode(COMMENT)
        self.METALIZATION= unicode(METALIZATION )       
        self.PASSIVATION= unicode(PASSIVATION )       
        self.UNDER_BUMP_METALIZATION= unicode(UNDER_BUMP_METALIZATION )       
        self.SIZE_OF_OPENING= unicode(SIZE_OF_OPENING )       
        self.OPTICAL_INSPECTION= unicode(OPTICAL_INSPECTION)       
        self.OPTICAL_INSPECTION_RESULT= unicode(OPTICAL_INSPECTION_RESULT)       
        self.RESULT=unicode(RESULT)
        self.NUMBEROFGOODSENSORS=NUMBEROFGOODSENSORS
        self.DATA_ID=DATA_ID
	self.VDEPL=unicode(VDEPL)
    


class Sensor(object):
  __storm_table__ = "inventory_sensor"
  SENSOR_ID = Unicode(primary=True)
  TRANSFER_ID = Int()
  WAFER_ID = Unicode()
  wafer = Reference(WAFER_ID, Wafer.WAFER_ID)
  transfer = Reference(TRANSFER_ID, Transfer.TRANSFER_ID)
  COMMENT = Unicode()
  TYPE= Unicode()
  STATUS=Unicode()
  LASTTEST_SENSOR_IV =Int()
  LASTTEST_SENSOR_IT =Int()
  LASTTEST_SENSOR_CV =Int()
  LASTTEST_SENSOR_INSPECTION =Int()
  def __init__(self,SENSOR_ID,TRANSFER_ID, TYPE, COMMENT="", 
               LASTTEST_SENSOR_IV=0,LASTTEST_SENSOR_CV=0,LASTTEST_SENSOR_IT=0,LASTTEST_SENSOR_INSPECTION=0,STATUS="", WAFER_ID=""):
      self.SENSOR_ID=unicode(SENSOR_ID)
      self.TRANSFER_ID=(TRANSFER_ID)
      self.TYPE=unicode(TYPE)
      self.WAFER_ID=unicode(WAFER_ID)
      self.COMMENT=unicode(COMMENT)
      self.LASTTEST_SENSOR_IV         = LASTTEST_SENSOR_IV
      self.LASTTEST_SENSOR_CV         = LASTTEST_SENSOR_CV
      self.LASTTEST_SENSOR_IT         = LASTTEST_SENSOR_IT
      self.LASTTEST_SENSOR_INSPECTION = LASTTEST_SENSOR_INSPECTION
      self.STATUS=unicode(STATUS)
      

class BareModule(object):
  __storm_table__ = "inventory_baremodule"
  BAREMODULE_ID = Unicode(primary=True)
  ROC_ID =  Unicode() # comma separated list
  SENSOR_ID = Unicode()
  STATUS=Unicode()
  TRANSFER_ID = Int()
  def roc(self,i):
      internal=self.getRoc(i)
      rocc=Reference(internal, Roc.ROC_ID)
      return rocc
  sensor = Reference(SENSOR_ID, Sensor.SENSOR_ID)
  transfer = Reference(TRANSFER_ID, Transfer.TRANSFER_ID)
  BUILTON = DateTime()
  N_REWORKED_ROC = Int()
  BUILTBY = Unicode()
  COMMENT = Unicode()
  LABEL = Unicode()
  TYPE=Unicode()
  LASTTEST_BAREMODULE_INSPECTION =Int()
  LASTTEST_CHIPS = Unicode()
  LASTTEST_BAREMODULE_QA_BONDING = Int()
  LASTTEST_BAREMODULE_QA_PIXELALIVE = Int()
  LASTTEST_BAREMODULE_GRADING = Int()
  def getRoc(self,i):
      #
      # parse ROC_IDs to extract field # N
      #
      result =(self.ROC_ID.split(","))[i]
      return result
  def checkChip(self):
      if self.LASTTEST_CHIPS is None or self.LASTTEST_CHIPS == "" :
          for i in range(15):
              self.LASTTEST_CHIPS = self.LASTTEST_CHIPS + ","
      results = (self.LASTTEST_CHIPS.split(","))
      if len(results) != 16:
          print " ERROR : LASTTEST_CHIPS has wrong format: ", self.LASTTEST_CHIPS
          return None
  
  def setChipTest(self, test,number):
      self.checkChip()
      results = (self.LASTTEST_CHIPS.split(","))
      results[test.CHIP_N] = test.TEST_ID
      self.LASTTEST_CHIPS = ",".join(results )

  def getChipTest(self,i):
      self.checkChip()
      result =(self.LASTTEST_CHIPS.split(","))[i]
      return int(result)
  
  def __init__(self,BAREMODULE_ID,ROC_ID,SENSOR_ID,TRANSFER_ID,  BUILTBY, BUILTON=datetime.now(),COMMENT="", LASTTEST_CHIPS = "",LASTTEST_BAREMODULE_INSPECTION=0, LASTTEST_BAREMODULE_QA_PIXELALIVE = 0,LASTTEST_BAREMODULE_QA_BONDING = 0, LASTTEST_BAREMODULE_GRADING=0,  STATUS="",LABEL="", TYPE="",N_REWORKED_ROC=0 ):
      self.BAREMODULE_ID=unicode(BAREMODULE_ID)
      self.ROC_ID=unicode(ROC_ID)
      self.SENSOR_ID=unicode(SENSOR_ID)
      self.TRANSFER_ID=TRANSFER_ID
      self.BUILTON=BUILTON
      self.N_REWORKED_ROC=int(N_REWORKED_ROC)
      self.BUILTBY=unicode(BUILTBY)
      self.COMMENT=unicode(COMMENT)
      self.LASTTEST_BAREMODULE_INSPECTION=int(LASTTEST_BAREMODULE_INSPECTION)
      self.LASTTEST_BAREMODULE_GRADING=int(LASTTEST_BAREMODULE_GRADING)
      self.LASTTEST_BAREMODULE_QA_BONDING=int(LASTTEST_BAREMODULE_QA_BONDING)
      self.LASTTEST_BAREMODULE_QA_PIXELALIVE=int(LASTTEST_BAREMODULE_QA_PIXELALIVE)
      self.LASTTEST_CHIPS=unicode(LASTTEST_CHIPS)
      self.STATUS=unicode(STATUS)
      self.LABEL=unicode(LABEL)
      self.TYPE=unicode(TYPE)

      
class Tbm(object):
  __storm_table__ = "inventory_tbm"
  TBM_ID = Unicode(primary=True)
  TRANSFER_ID = Int()
  transfer = Reference(TRANSFER_ID, Transfer.TRANSFER_ID)
  COMMENT = Unicode()
  TYPE=Unicode()
  STATUS=Unicode()
  LASTTEST_TBM=Int()
  def __init__(self,TBM_ID, TRANSFER_ID, COMMENT="", LASTTEST_TBM=0, STATUS="", TYPE=""):
      self.TBM_ID=unicode(TBM_ID)
      self.TRANSFER_ID=TRANSFER_ID
      self.COMMENT=unicode(COMMENT)
      self.LASTTEST_TBM=LASTTEST_TBM
      self.STATUS=unicode(STATUS)
      self.TYPE=unicode(TYPE)
  
  
class Hdi(object):
  __storm_table__ = "inventory_hdi"
  HDI_ID = Unicode(primary=True)
  TRANSFER_ID = Int()
  transfer = Reference(TRANSFER_ID, Transfer.TRANSFER_ID)
  BATCH_ID=Unicode()
  TBM1_VERSION=Unicode()
  TBM2_VERSION=Unicode()
  COMMENT = Unicode()
  TYPE = Unicode()
  STATUS=Unicode()
  LASTTEST_HDI_RECEPTION=Int()
  LASTTEST_HDI_TBMGLUING=Int()
  LASTTEST_HDI_BONDING=Int()
  LASTTEST_HDI_ELECTRIC=Int()
  LASTTEST_HDI_VALIDATION=Int()

  def __init__(self,HDI_ID, TRANSFER_ID, COMMENT="", LASTTEST_HDI_RECEPTION=0,LASTTEST_HDI_TBMGLUING=0,LASTTEST_HDI_BONDING=0,LASTTEST_HDI_ELECTRIC=0, LASTTEST_HDI_VALIDATION=0, STATUS="",TYPE="", TBM1_VERSION="", TBM2_VERSION="",BATCH_ID=""):
    self.HDI_ID=unicode(HDI_ID)
    self.TRANSFER_ID=TRANSFER_ID
    self.COMMENT=unicode(COMMENT)
    self.STATUS=unicode(STATUS)
    self.TYPE=unicode(TYPE)
    self.TBM1_VERSION=unicode(TBM1_VERSION)
    self.TBM2_VERSION=unicode(TBM2_VERSION)
    self.BATCH_ID=unicode(BATCH_ID)
    self.LASTTEST_HDI_RECEPTION=LASTTEST_HDI_RECEPTION
    self.LASTTEST_HDI_TBMGLUING=LASTTEST_HDI_TBMGLUING
    self.LASTTEST_HDI_BONDING=LASTTEST_HDI_BONDING
    self.LASTTEST_HDI_ELECTRIC=LASTTEST_HDI_ELECTRIC
    self.LASTTEST_HDI_VALIDATION=LASTTEST_HDI_VALIDATION


          
class FullModule(object):
  __storm_table__ = "inventory_fullmodule"
  FULLMODULE_ID = Unicode(primary=True)
  BAREMODULE_ID =  Unicode()
  HDI_ID =  Unicode()
  TBM_ID =  Unicode()
  STATUS=Unicode()    
  CABLEBATCH_ID = Unicode()
  BSBATCH_ID = Unicode()
  TRANSFER_ID = Int()
  transfer = Reference(TRANSFER_ID, Transfer.TRANSFER_ID)
  bsbatch = Reference(BSBATCH_ID, BaseStripBatch.BSBATCH_ID)
  cablebatch = Reference(CABLEBATCH_ID, CableBatch.CABLEBATCH_ID)
  tbm = Reference(TBM_ID, Tbm.TBM_ID)
  baremodule = Reference(BAREMODULE_ID, BareModule.BAREMODULE_ID)
  hdi = Reference(HDI_ID, Hdi.HDI_ID)
  BUILTON = DateTime()
  BUILTBY = Unicode()
  COMMENT = Unicode()
  LASTTEST_FULLMODULE=Int()
  LASTTEST_XRAY_HR150=Int()
  LASTTEST_XRAY_HR50=Int()
  LASTTEST_XRAY_VCAL=Int()

  def __init__(self,FULLMODULE_ID, BAREMODULE_ID, HDI_ID, TBM_ID, TRANSFER_ID, BUILTBY, BUILTON=datetime.now(), COMMENT="", STATUS="",LASTTEST_FULLMODULE=0, LASTTEST_XRAY_VCAL=0, LASTTEST_XRAY_HR50=0,LASTTEST_XRAY_HR150=0  , CABLEBATCH_ID="", BSBATCH_ID=""):
      self.TBM_ID=unicode(TBM_ID)
      self.HDI_ID=unicode(HDI_ID)
      self.BAREMODULE_ID=unicode(BAREMODULE_ID)
      self.FULLMODULE_ID=unicode(FULLMODULE_ID)
      self.TRANSFER_ID=TRANSFER_ID
      self.COMMENT=unicode(COMMENT)
      self.CABLEBATCH_ID=unicode(CABLEBATCH_ID)
      self.BSBATCH_ID=unicode(BSBATCH_ID)
      self.BUILTON=BUILTON
      self.BUILTBY=unicode(BUILTBY)
      self.STATUS=unicode(STATUS)
      self.LASTTEST_FULLMODULE=int(LASTTEST_FULLMODULE        )
      self.LASTTEST_XRAY_VCAL=int(LASTTEST_XRAY_VCAL)
      self.LASTTEST_XRAY_HR150=int(LASTTEST_XRAY_HR50)
      self.LASTTEST_XRAY_HR150=int(LASTTEST_XRAY_HR50)

class ShippingBox(object):
    __storm_table__ = "inventory_shippingbox"
    SHIPPINGBOX_ID = Unicode(primary=True)
    TRANSFER_ID = Int()
    transfer = Reference(TRANSFER_ID, Transfer.TRANSFER_ID)
    COMMENT = Unicode()
    TYPE = Unicode()
    MANUFACTURER = Unicode()
    def __init__(self,SHIPPINGBOX_ID, TRANSFER_ID, MANUFACTURER, TYPE, COMMENT=""):
        self.SHIPPINGBOX_ID = unicode(SHIPPINGBOX_ID)
        self.TRANSFER_ID = TRANSFER_ID
        self.COMMENT=unicode(COMMENT)
        self.TYPE=unicode(TYPE)
        self.MANUFACTURER=unicode(MANUFACTURER)
        






#
# logbook
#
class Test_Logbook(object):
      __storm_table__ = "logbook"
      TEST_ID = Int(primary=True)
      SESSION_ID=Int()
      session = Reference(SESSION_ID, Session.SESSION_ID)
      IDS = Unicode()
      COMMENT=Unicode()
      DATA_ID = Int()
      def __init__ (self,SESSION_ID, IDS,COMMENT,DATA_ID) :
		self.SESSION_ID=int(SESSION_ID)
		self.IDS=unicode(IDS)
		self.COMMENT=unicode(COMMENT)
		self.DATA_ID=int(DATA_ID)
#
# Data


#"Bulk Import"||
# tests
#
class Test_BareModule(object):
      __storm_table__ = "test_baremodule"
      TEST_ID = Int(primary=True)
      SESSION_ID=Int()
      session = Reference (SESSION_ID,Session.SESSION_ID)
      BAREMODULE_ID =  Unicode()
      baremodule=Reference(BAREMODULE_ID, BareModule.BAREMODULE_ID)
      RESULT=Float()
      DATA_ID=Int()
      data=Reference(DATA_ID,Data.DATA_ID)

class Test_BareModule_QA (object):
      __storm_table__ = "test_baremodule_qa"
      TEST_ID = Int(primary=True)
      SESSION_ID=Int()
      session = Reference (SESSION_ID,Session.SESSION_ID)
      BAREMODULE_ID =  Unicode()
      baremodule=Reference(BAREMODULE_ID, BareModule.BAREMODULE_ID)
      DATA_ID=Int()
      data=Reference(DATA_ID,Data.DATA_ID)
      TYPE = Unicode()
      TOTAL_FAILURES = Unicode()
      TEMPERATURE = Float()
      HUMIDITY = Float()
#
# supposed to be a JSON of the form '{"ROC1": [[2, 3], [4, 5]]}'
#
      FAILURES = Unicode()
      def __init__ (self,DATA_ID,SESSION_ID,BAREMODULE_ID, TYPE, TEMPERATURE, HUMIDITY, TOTAL_FAILURES, FAILURES="" ):
         self.DATA_ID = DATA_ID
         self.SESSION_ID= SESSION_ID
         self.TYPE= unicode(TYPE)
         self.TEMPERATURE = TEMPERATURE
         self.HUMIDITY   =  HUMIDITY
         self.FAILURES= unicode(FAILURES)
         self.BAREMODULE_ID= unicode(BAREMODULE_ID)
         self.TOTAL_FAILURES = unicode(TOTAL_FAILURES)
      def splitObjects(self,pippo, i):
          result =((unicode(pippo)).split(","))[i]
          return result
      def joinObjects(self, arrayofrocids):
            if len (arrayofrocids) !=6 :
                return None
            return unicode(string.join(arrayofrocids,","))

'''
      def dictToString(self, dictionary):
          returnString=""
          for i in dictionary:
            roc = i
            listOfFailures=dictionary[i]
            for j in listOfFailures:
               row = j[0]
               column = j[1]
               returnString+=str(","+roc+",",row+",'+column)
           return returnString

      def stringToDict(self, aString):
          myDict={}
          result =((unicode(aString)).split(","))
          number = len(result)/3
          index=0
          for i in range(number):
             roc = result[i*3]
             row = result[i*3+1]
             column = result[i*3+2]
             pairTemp = [row,column]
             myDict[roc].append(pairTemp)
          return myDict
            
'''


class Test_BareModule_Grading(object):
      __storm_table__ = "test_baremodule_grading"
      TEST_ID = Int(primary=True)
      SESSION_ID=Int()
      session = Reference (SESSION_ID,Session.SESSION_ID)
      BAREMODULE_ID =  Unicode()
      baremodule=Reference(BAREMODULE_ID, BareModule.BAREMODULE_ID)
      DATA_ID=Int()
      data=Reference(DATA_ID,Data.DATA_ID)

      GLOBAL_GRADING = Unicode()
      GLOBAL_GRADING_1 = Unicode()
      GLOBAL_GRADING_2 = Unicode()
      GLOBAL_GRADING_3 = Unicode()
      GLOBAL_GRADING_4 = Unicode()
      GLOBAL_GRADING_5 = Unicode()
      GLOBAL_GRADING_6 = Unicode()
      GLOBAL_GRADING_7 = Unicode()
      GLOBAL_GRADING_8 = Unicode()
      GLOBAL_GRADING_9 = Unicode()
      GLOBAL_GRADING_10 = Unicode()

      def __init__ (self, SESSION_ID, BAREMODULE_ID , DATA_ID , GLOBAL_GRADING, 
          GLOBAL_GRADING_1, 
          GLOBAL_GRADING_2, 
          GLOBAL_GRADING_3, 
          GLOBAL_GRADING_4,   
          GLOBAL_GRADING_5, 
          GLOBAL_GRADING_6, 
          GLOBAL_GRADING_7, 
          GLOBAL_GRADING_8, 
          GLOBAL_GRADING_9, 
          GLOBAL_GRADING_10):
          
          self.DATA_ID = DATA_ID
          self.SESSION_ID= SESSION_ID
          self.BAREMODULE_ID= unicode(BAREMODULE_ID)
          self.GLOBAL_GRADING  = unicode(GLOBAL_GRADING)
          self.GLOBAL_GRADING_1 = unicode (GLOBAL_GRADING_1 )
          self.GLOBAL_GRADING_2 = unicode (GLOBAL_GRADING_2 )
          self.GLOBAL_GRADING_3 = unicode (GLOBAL_GRADING_3 )
          self.GLOBAL_GRADING_4 = unicode (GLOBAL_GRADING_4 )
          self.GLOBAL_GRADING_5 = unicode (GLOBAL_GRADING_5 )
          self.GLOBAL_GRADING_6 = unicode (GLOBAL_GRADING_6 )
          self.GLOBAL_GRADING_7 = unicode (GLOBAL_GRADING_7 )
          self.GLOBAL_GRADING_8 = unicode (GLOBAL_GRADING_8 )
          self.GLOBAL_GRADING_9 = unicode (GLOBAL_GRADING_9 )
          self.GLOBAL_GRADING_10 = unicode (GLOBAL_GRADING_10 )



'''

class Test_BareModule_DaqParameters(object):
      __storm_table__ = "test_baremodule_grading"
      TEST_ID = Int(primary=True)
      SESSION_ID=Int()
      session = Reference (SESSION_ID,Session.SESSION_ID)
      BAREMODULE_ID =  Unicode()
      baremodule=Reference(BAREMODULE_ID, BareModule.BAREMODULE_ID)
      DATA_ID=Int()
      data=Reference(DATA_ID,Data.DATA_ID)



'''


class Test_FullModuleSession(object):
      __storm_table__ = "test_fullmodulesession"
      TEST_ID = Int(primary=True)
      DATA_ID=Int()
      data=Reference(DATA_ID,Data.DATA_ID)
      SESSION_ID=Int()
      session = Reference (SESSION_ID,Session.SESSION_ID)
      FULLMODULE_ID =  Unicode()
      fullmodule=Reference(FULLMODULE_ID, FullModule.FULLMODULE_ID)
      def __init__(self,DATA_ID,SESSION_ID,FULLMODULE_ID):
          self.DATA_ID=DATA_ID
          self.SESSION_ID=SESSION_ID
          self.FULLMODULE_ID=FULLMODULE_ID


class Test_FullModuleSummary(object):
      __storm_table__ = "test_fullmodulesummary"
      TEST_ID=Int(primary=True)
      FULLMODULE_ID = Unicode()
      fullmodule=Reference(FULLMODULE_ID, FullModule.FULLMODULE_ID)
      FULLMODULETEST_NAMES = Unicode()
      FULLMODULETEST_TYPES = Unicode()
      FULLMODULETEST_IDS = Unicode()
      DATA_ID = Int()
      data=Reference(DATA_ID,Data.DATA_ID)
      QUALIFICATIONTYPE=Unicode()
      FULLTESTGRADE=Unicode()
      SHORTTESTGRADE=Unicode()
      TIMESTAMP=Unicode()
      def splitObjects(self,pippo, i):
          result =((unicode(pippo)).split(","))[i]
          return result
      def joinObjects(self, arrayofrocids):
            return unicode(string.join(arrayofrocids,","))
      def findObjectFromCommaSeparatedList(self, stringcommaseparated,name):
          temp = unicode(name)
          lista =((unicode(stringcommaseparated)).split(","))
          if temp  in lista:
              return lista.index(temp)
          else:
              return None
          
          
      def __init__(self, FULLMODULE_ID,DATA_ID, FULLMODULETEST_NAMES="", FULLMODULETEST_TYPES="", FULLMODULETEST_IDS="", FULLTESTGRADE="", SHORTTESTGRADE="",QUALIFICATIONTYPE="",TIMESTAMP=""):
          self.FULLMODULE_ID=    unicode(      FULLMODULE_ID)
          self.DATA_ID=DATA_ID
          self.QUALIFICATIONTYPE=unicode(QUALIFICATIONTYPE)
          self.FULLMODULETEST_NAMES=unicode(FULLMODULETEST_NAMES)
          self.FULLMODULETEST_TYPES=unicode(FULLMODULETEST_TYPES)
          self.FULLMODULETEST_IDS=unicode(FULLMODULETEST_IDS)
          self.FULLTESTGRADE=unicode(FULLTESTGRADE)
          self.SHORTTESTGRADE =unicode(SHORTTESTGRADE )
	  self.TIMESTAMP=unicode(TIMESTAMP)

class Test_FullModule(object):
      __storm_table__ = "test_fullmodule"
      TEST_ID = Int(primary=True)
      SESSION_ID=Int()
      session = Reference (SESSION_ID,Test_FullModuleSession.TEST_ID)
      FULLMODULE_ID =  Unicode()
      fullmodule=Reference(FULLMODULE_ID, FullModule.FULLMODULE_ID)
      RESULT=Unicode()
      TEMPNOMINAL = Unicode()
      DATA_ID=Int()
      SUMMARY_ID = Int() 
      TYPE=Unicode()
      summary=Reference(SUMMARY_ID, Test_FullModuleSummary.TEST_ID)
      data=Reference(DATA_ID,Data.DATA_ID)
      CKSUM=Unicode()
      TIMESTAMP=Unicode()
      COLDBOX=Unicode()
      COLDBOX_SLOT=Unicode()
      def __init__(self,SESSION_ID,FULLMODULE_ID,RESULT,TEMPNOMINAL,DATA_ID,COLDBOX,COLDBOX_SLOT, CKSUM,TIMESTAMP,TYPE):

       self.SESSION_ID=SESSION_ID
       self.FULLMODULE_ID=unicode(FULLMODULE_ID)
       self.RESULT=unicode(RESULT)
       self.TEMPNOMINAL=unicode(TEMPNOMINAL)
       self.DATA_ID=DATA_ID
       self.COLDBOX=unicode(COLDBOX)
       self.COLDBOX_SLOT=unicode(COLDBOX_SLOT)
       self.CKSUM=unicode(CKSUM)
       self.TYPE = unicode(TYPE)
       self.TIMESTAMP=unicode(TIMESTAMP)

class Test_FullModuleAnalysis(object):
      __storm_table__ = "test_fullmoduleanalysis"
      TEST_ID=Int(primary=True)
      FULLMODULETEST_ID= Int()
      fullmoduletest=Reference(FULLMODULETEST_ID, Test_FullModule.TEST_ID)
      DATA_ID=Int()
      HOSTNAME=Unicode()
      COMMENT=Unicode()
      PIXELDEFECTS=Int()
      GRADE=Unicode()
      MACRO_VERSION=Unicode()
      data=Reference(DATA_ID,Data.DATA_ID)
      DEADPIXELS      =Int()
      MASKEDPIXELS      =Int()
      BUMPDEFPIXELS    =Int()
      TRIMDEFPIXELS     =Int()
      ADDRESSDEFPIXELS  =Int()
      NOISYPIXELS  =Int()
      THRESHDEFPIXELS   =Int()
      GAINDEFPIXELS    =Int()
      PEDESTALDEFPIXELS =Int()
      PAR1DEFPIXELS      =Int()
      ROCSWORSEPERCENT=Unicode()
      I150 = Float()
      I150_2 = Float()
      CURRENT = Float()
      CURRENT_2 = Float()
      TRIMMING =Unicode()
      PHCAL = Unicode()
      IVSLOPE  = Float()
      TEMPVALUE = Float() 
      TEMPERROR = Float()
      CYCLING= Unicode()
      TCYCLHIGH = Float()
      TCYCLLOW = Float()
      def __init__(self,FULLMODULE_ID, DATA_ID,FULLMODULETEST_ID,
                   GRADE="",HOSTNAME="",
                   DEADPIXELS=-1,MASKEDPIXELS=-1,BUMPDEFPIXELS=-1,TRIMDEFPIXELS=-1,ADDRESSDEFPIXELS=-1,NOISYPIXELS=-1,THRESHDEFPIXELS=-1,
                   GAINDEFPIXELS=-1,PEDESTALDEFPIXELS=-1,PAR1DEFPIXELS=-1,ROCSWORSEPERCENT="",MACRO_VERSION="",
                   I150=0,I150_2=0,CURRENT=0,CURRENT_2=0,TRIMMING="",PHCAL="",IVSLOPE=0,TEMPVALUE=0,TEMPERROR=0,CYCLING=0,TCYCLHIGH=0,TCYCLLOW=0, PIXELDEFECTS=0, COMMENT=""):

          self.DATA_ID=DATA_ID
          self.FULLMODULETEST_ID=(FULLMODULETEST_ID)
          self.FULLMODULE_ID=unicode(FULLMODULE_ID)
          self.GRADE=unicode(GRADE)
          self.ROCSWORSEPERCENT=unicode(ROCSWORSEPERCENT)
          self.COMMENT=unicode(COMMENT)
          self.PIXELDEFECTS=int(PIXELDEFECTS)
          self.TRIMMING=unicode(TRIMMING)
          self.PHCAL=unicode(PHCAL)
          self.IVSLOPE=float(IVSLOPE)
          self.TEMPVALUE=float(TEMPVALUE)
          self.TEMPERROR=float(TEMPERROR)
          self.TCYCLHIGH=float(TCYCLHIGH)
          self.TCYCLLOW=float(TCYCLLOW)
          self.DEADPIXELS = float(DEADPIXELS)
          self.MASKEDPIXELS=float(MASKEDPIXELS)
          self.BUMPDEFPIXELS=float(BUMPDEFPIXELS)
          self.TRIMDEFPIXELS=float(TRIMDEFPIXELS)
          self.ADDRESSDEFPIXELS=float(ADDRESSDEFPIXELS)
          self.NOISYPIXELS=float(NOISYPIXELS)
          self.THRESHDEFPIXELS=float(THRESHDEFPIXELS)
          self.GAINDEFPIXELS=float(GAINDEFPIXELS)
          self.PEDESTALDEFPIXELS=float(PEDESTALDEFPIXELS)
          self.PAR1DEFPIXELS=float(PAR1DEFPIXELS)
          self.I150=float(I150)
          self.I150_2=float(I150_2)
          self.CURRENT=float(CURRENT)
          self.CURRENT_2=float(CURRENT_2)
          self.CYCLING=unicode(CYCLING)
          self.HOSTNAME=unicode(HOSTNAME)
          self.MACRO_VERSION=unicode(MACRO_VERSION)



#
# xray tests
#


class Test_FullModule_XRay_Vcal(object):
    __storm_table__ = "Test_FullModule_XRay_Vcal"
    TEST_ID = Int(primary=True)
    SESSION_ID=Int()
    session = Reference (SESSION_ID,Session.SESSION_ID)
    FULLMODULE_ID =  Unicode()
    fullmodule=Reference(FULLMODULE_ID, FullModule.FULLMODULE_ID)
    DATA_ID=Int()
    data=Reference(DATA_ID,Data.DATA_ID)
    LAST_PROCESSING_ID = Int()
    RESULT = Unicode()
    XRAY_SLOT = Int()
    HITRATENOMINAL = Float()
    TEMPNOMINAL = Float()
    TIMESTAMP = Unicode()
    COMMENT = Unicode()
    def __init__(self,SESSION_ID, TARGET, DATA_ID, LAST_PROCESSING_ID,  FULLMODULE_ID, XRAY_SLOT,HITRATENOMINAL, TEMPNOMINAL, TIMESTAMP,
                 RESULT="", COMMENT=""):
        self.SESSION_ID = int(SESSION_ID)
        self.TARGET = unicode(TARGET)
        self.DATA_ID = int(DATA_ID)
        self.LAST_PROCESSING_ID  = int(LAST_PROCESSING_ID )
        self.RESULT = unicode(RESULT)
        self.XRAY_SLOT = int(XRAY_SLOT)
        self.HITRATENOMINAL = float(HITRATENOMINAL)
        self.TEMPNOMINAL = float(TEMPNOMINAL)
        self.TIMESTAMP = unicode(TIMESTAMP)
        self.COMMENT = unicode(COMMENT)
        self.FULLMODULE_ID = unicode(FULLMODULE_ID)
        
class Test_FullModule_XRay_Vcal_Module_Analysis(object):
    __storm_table__ = "Test_FullModule_XRay_Vcal_Module_Analysis"
    TEST_ID = Int(primary=True)
    SESSION_ID=Int()
    session = Reference (SESSION_ID,Session.SESSION_ID)
    FULLMODULETEST_ID =  Int()
    xrayvcaltest=Reference(FULLMODULETEST_ID, Test_FullModule_XRay_Vcal.TEST_ID)
    SESSION_ID=Int()
    session = Reference (SESSION_ID,Session.SESSION_ID)
    DATA_ID=Int()
    data=Reference(DATA_ID,Data.DATA_ID)
    TARGET = Unicode()
    PROCESSING_ID = Int()
    MACRO_VERSION = Unicode()
    SLOPE  =Float()
    OFFSET = Float()
    TARGET_HIT_RATE = Float()
    GRADE = Unicode()
    def __init__(self, SESSION_ID, FULLMODULETEST_ID, DATA_ID, TARGET, PROCESSING_ID, MACRO_VERSION, SLOPE, OFFSET,  TARGET_HIT_RATE, GRADE):
        self.SESSION_ID = int(SESSION_ID)
        self.FULLMODULETEST_ID = int(FULLMODULETEST_ID)
        self.DATA_ID = int(DATA_ID)
        self.TARGET = unicode(TARGET)
        self.PROCESSING_ID  = int(PROCESSING_ID )
        self.MACRO_VERSION = unicode(MACRO_VERSION)
        self.SLOPE = float(SLOPE)
        self.OFFSET = float(OFFSET)
        self.TARGET_HIT_RATE = float(TARGET_HIT_RATE)
        self.GRADE = unicode(GRADE)




class  Test_FullModule_XRay_Vcal_Roc_Analysis (object):
    __storm_table__ = "Test_FullModule_XRay_Vcal_Roc_Analysis"
    TEST_ID = Int(primary=True)
    ROC_POS = Int()
    TEST_XRAY_VCAL_MODULE_ID = Int()
    xrayvcalanalysis = Reference(TEST_XRAY_VCAL_MODULE_ID, Test_FullModule_XRay_Vcal_Module_Analysis.TEST_ID)
    FULLMODULETEST_ID = Int()
    xrayvcaltest=Reference(FULLMODULETEST_ID, Test_FullModule_XRay_Vcal.TEST_ID)
    SESSION_ID=Int()
    session = Reference (SESSION_ID,Session.SESSION_ID)
    DATA_ID=Int()
    data=Reference(DATA_ID,Data.DATA_ID)
    MACRO_VERSION = Unicode()
    PROCESSING_ID = Int()
    TARGET = Unicode()
    SLOPE  =Float()
    OFFSET = Float()
    CHI2NDF  = Float()
    TARGET_HIT_RATE = Float()
    TARGET_PEAK_ENERGY = Float()
    GRADE = Unicode()
    COMMENT = Unicode()
    def __init__(self, SESSION_ID, FULLMODULETEST_ID, DATA_ID, TARGET, PROCESSING_ID, MACRO_VERSION, SLOPE, OFFSET, CHi2NDF, TARGET_HIT_RATE, TARGET_PEAK_ENERGY, 
                 TEST_XRAY_VCAL_MODULE_ID, ROC_POS, GRADE, COMMENT=""  ):
        self.SESSION_ID = int(SESSION_ID)
        self.TARGET = unicode(TARGET)
        self.DATA_ID = int(DATA_ID)
        self.PROCESSING_ID  = int(PROCESSING_ID )
        self.TARGET_HIT_RATE = float(TARGET_HIT_RATE)
        self.MACRO_VERSION = unicode(MACRO_VERSION)
        self.FULLMODULETEST_ID = int(FULLMODULETEST_ID)
        self.GRADE = unicode(GRADE)
        self.ROC_POS = int(ROC_POS)
        self.TARGET_PEAK_ENERGY = float(TARGET_PEAK_ENERGY)
        self.TEST_XRAY_VCAL_MODULE_ID = int(TEST_XRAY_VCAL_MODULE_ID)
        self.COMMENT = unicode(COMMENT)




class Test_Tbm(object):
      __storm_table__ = "test_tbm"
      TEST_ID = Int(primary=True)
      SESSION_ID=Int()
      session = Reference (SESSION_ID,Session.SESSION_ID)
      TBM_ID =  Unicode()
      tbm=Reference(TBM_ID, Tbm.TBM_ID)
      RESULT=Float()
      DATA_ID=Int()
      GAIN = Float()
      BL_A = Float()
      BL_B = Float()
      data=Reference(DATA_ID,Data.DATA_ID)
      def __init__(self,SESSION_ID,TBM_ID,RESULT,DATA_ID, GAIN, BL_A, BL_B):
          self.SESSION_ID=SESSION_ID
          self.TBM_ID=unicode(TBM_ID)
          self.RESULT=float(RESULT)
          self.DATA_ID=DATA_ID
          self.GAIN=GAIN
          self.BL_A=BL_A
          self.BL_B=BL_B



class Test_Hdi_Reception(object):
      __storm_table__ = "test_hdi_reception"
      TEST_ID = Int(primary=True)
      SESSION_ID=Int()
      session = Reference (SESSION_ID,Session.SESSION_ID)
      HDI_ID =  Unicode()
      hdi=Reference(HDI_ID, Hdi.HDI_ID)
      RESULT=Unicode()
      DATA_ID=Int()
      INSPECTION_BACK=Unicode()
      INSPECTION_FRONT=Unicode()
      data=Reference(DATA_ID,Data.DATA_ID)
      def __init__(self,SESSION_ID,HDI_ID,RESULT,DATA_ID,INSPECTION_BACK,INSPECTION_FRONT):
          self.SESSION_ID=SESSION_ID
          self.HDI_ID=unicode(HDI_ID)
          self.RESULT=unicode(RESULT)
          self.DATA_ID=DATA_ID
          self.INSPECTION_BACK=unicode(INSPECTION_BACK)
          self.INSPECTION_FRONT=unicode(INSPECTION_FRONT)

class Test_Hdi_TbmGluing(object):
      __storm_table__ = "test_hdi_tbmgluing"
      TEST_ID = Int(primary=True)
      SESSION_ID=Int()
      session = Reference (SESSION_ID,Session.SESSION_ID)
      HDI_ID =  Unicode()
      hdi=Reference(HDI_ID, Hdi.HDI_ID)
      RESULT=Unicode()
      NOTES=Unicode()
      DATA_ID=Int()
      data=Reference(DATA_ID,Data.DATA_ID)
      def __init__(self,SESSION_ID,HDI_ID,RESULT,DATA_ID, NOTES):
          self.SESSION_ID=SESSION_ID
          self.HDI_ID=unicode(HDI_ID)
          self.RESULT=unicode(RESULT)
          self.DATA_ID=DATA_ID
          self.NOTES=unicode(NOTES)


class Test_Hdi_Bonding(object):
      __storm_table__ = "test_hdi_bonding"
      TEST_ID = Int(primary=True)
      SESSION_ID=Int()
      session = Reference (SESSION_ID,Session.SESSION_ID)
      HDI_ID =  Unicode()
      hdi=Reference(HDI_ID, Hdi.HDI_ID)
      RESULT=Unicode()
      DATA_ID=Int()
      TBM_BONDS = Unicode()
      HUB_ADDRESS_BONDS = Unicode()
      N_TEST_BONDS=Int()
      AVG_PULL_FORCE_G=Float()
      NOTES = Unicode()
      data=Reference(DATA_ID,Data.DATA_ID)
      def __init__(self,SESSION_ID,HDI_ID,RESULT,DATA_ID,TBM_BONDS,HUB_ADDRESS_BONDS, N_TEST_BONDS, AVG_PULL_FORCE_G, NOTES ):
          self.SESSION_ID=SESSION_ID
          self.HDI_ID=unicode(HDI_ID)
          self.RESULT=unicode(RESULT)
          self.DATA_ID=DATA_ID
          self.TBM_BONDS = unicode(TBM_BONDS)
          self.HUB_ADDRESS_BONDS=unicode(HUB_ADDRESS_BONDS)
          self.N_TEST_BONDS=N_TEST_BONDS
          self.AVG_PULL_FORCE_G=float(AVG_PULL_FORCE_G)
	  self.NOTES=unicode(NOTES)


class Test_Hdi_Electric(object):
      __storm_table__ = "test_hdi_electric"
      TEST_ID = Int(primary=True)
      SESSION_ID=Int()
      session = Reference (SESSION_ID,Session.SESSION_ID)
      HDI_ID =  Unicode()
      hdi=Reference(HDI_ID, Hdi.HDI_ID)
      RESULT=Unicode()
      DATA_ID=Int()
      data=Reference(DATA_ID,Data.DATA_ID)
      SIGNALS_AND_LVS=Unicode()
      HV600_CURRENT_uA=Float()
      DIGITAL_CURRENT_mA=Float()
      NUM_TBM=Int()
      TEST_MAP={}
      CHANNEL_MAP={}
      VALUE_MAP = {}
      TOT_SIZE = 0
      NOTES=Unicode()
      def init_maps(self):
          self.TEST_MAP={'CLK0' : 0,'CLK1' : 1,'CLK2' : 2,'CLK3' : 3,'CTR0' : 4,'CTR1' : 5,'CTR2' : 6,'CTR3' : 7,'SDA0' : 8,'SDA1' : 9,'SDA2' : 10,'SDA3' : 11}
          self.CHANNEL_MAP={'CH1' : 0,'CH2' : 1,'CH3' : 2,'CH4' : 3,'LV' : 4}
          self.VALUE_MAP = {'NULL' : 0, 'PASS' : 1, 'FAIL' : 2}
          self.TOT_SIZE = len(self.TEST_MAP)*len(self.CHANNEL_MAP)

      def __init__(self,SESSION_ID,HDI_ID,RESULT,DATA_ID,  HV600_CURRENT_uA, DIGITAL_CURRENT_mA, NUM_TBM, SIGNALS_AND_LVS="",NOTES=""):
	  self.init_maps()
          nullOsc = "0"*(self.TOT_SIZE)

          self.SESSION_ID=SESSION_ID
          self.HDI_ID=unicode(HDI_ID)
          self.RESULT=unicode(RESULT)
          self.DATA_ID=DATA_ID
          if (SIGNALS_AND_LVS == ""):
              self.SIGNALS_AND_LVS = unicode(nullOsc)
          else:
              self.SIGNALS_AND_LVS =unicode(SIGNALS_AND_LVS)
          self.HV600_CURRENT_uA =   HV600_CURRENT_uA
          self.DIGITAL_CURRENT_mA =DIGITAL_CURRENT_mA   
          self.NUM_TBM = NUM_TBM  
#
# I define inside the object the accessors for oscilloscope
#
      def setBit(self,test, channel, value):
          self.init_maps()
          if not test in self.TEST_MAP:
              return None
          if not channel in self.CHANNEL_MAP:
              return None
          if len(self.SIGNALS_AND_LVS) != self.TOT_SIZE:
              return None
          if not value in self.VALUE_MAP:
              return None
          v = self.VALUE_MAP[value]
          t = self.TEST_MAP[test]          
          c = self.CHANNEL_MAP[channel]
          offset = t*len(self.CHANNEL_MAP)+c
          s = list(self.SIGNALS_AND_LVS)
          s[offset] = "%s"%v
          self.SIGNALS_AND_LVS = "".join(s)
          return self.SIGNALS_AND_LVS
      def getBit(self,test, channel):
          self.init_maps()
          if not test in self.TEST_MAP:
              return None
          if not channel in self.CHANNEL_MAP:
              return None
          if len(self.SIGNALS_AND_LVS) != self.TOT_SIZE:
              return None
          t = self.TEST_MAP[test]          
          c = self.CHANNEL_MAP[channel]
          offset = t*len(self.CHANNEL_MAP)+c
          inv = dict(map(reversed, self.VALUE_MAP.iteritems()))
          return inv[int((self.SIGNALS_AND_LVS.encode('utf8'))[offset])]


class Test_Hdi_Validation(object):
      __storm_table__ = "test_hdi_validation"
      TEST_ID = Int(primary=True)
      SESSION_ID=Int()
      session = Reference (SESSION_ID,Session.SESSION_ID)
      HDI_ID =  Unicode()
      hdi=Reference(HDI_ID, Hdi.HDI_ID)
      RESULT=Unicode()
      DATA_ID=Int()
      data=Reference(DATA_ID,Data.DATA_ID)
      VISUAL_INSPECTION=Unicode()
      NOTES=Unicode()
      def __init__(self,SESSION_ID,HDI_ID,RESULT,DATA_ID,VISUAL_INSPECTION, NOTES="" ):
          self.SESSION_ID=SESSION_ID
          self.HDI_ID=unicode(HDI_ID)
          self.RESULT=unicode(RESULT)
          self.DATA_ID=DATA_ID
          self.VISUAL_INSPECTION = unicode(VISUAL_INSPECTION)
          self.NOTES=unicode(NOTES)


class Test_Roc(object):
      __storm_table__ = "test_roc"
      TEST_ID = Int(primary=True)
      SESSION_ID=Int()
      session = Reference (SESSION_ID,Session.SESSION_ID)
      ROC_ID =  Unicode()
      roc=Reference(ROC_ID, Roc.ROC_ID)
      RESULT= Int()
      DATA_ID=Int()
      data=Reference(DATA_ID,Data.DATA_ID)
      DEFECTPIXELS = Int()
      ADDRPIXELS = Int()
      TRIMPIXELS = Int()
      MASKPIXELS = Int()
      NSIGPIXELS = Int()
      NOISEPIXELS = Int()
      THRESHOLDPIXELS = Int()
      IANA = Float()
      IDIGI = Float()
      VDAC = Float()
      VDREG = Float()
      V24 = Float()
      PHFAIL = Int()
      VDCAP = Float()
      VDIGU_ADC = Int()
      VANAU_ADC = Int()
      VANAR_ADC = Int()
      VBG_ADC = Int()
      IANA_ADC = Int()
      VDIGU_VOLTS = Float()
      VANAU_VOLTS = Float()
      IANA_MILLIAMPS = Float()
      VANASCAN = Unicode()	

       
      COMMENT = Unicode()
      def __init__(self,SESSION_ID, ROC_ID, RESULT,  V24, IANA, IDIGI, VDAC, DEFECTPIXELS, ADDRPIXELS, TRIMPIXELS, MASKPIXELS, NSIGPIXELS, NOISEPIXELS, THRESHOLDPIXELS, PHFAIL, 
			VDCAP,VDIGU_ADC,VANAU_ADC,VANAR_ADC,VBG_ADC,IANA_ADC,VDIGU_VOLTS,VANAU_VOLTS,IANA_MILLIAMPS,VANASCAN,VDREG=0,COMMENT="",DATA_ID=0):
          self.SESSION_ID=SESSION_ID 
          self.ROC_ID=unicode(ROC_ID)
          self.RESULT=int(RESULT)
          self.DATA_ID=DATA_ID
          self.DEFECTPIXELS=int(DEFECTPIXELS)
          self.VDAC = float(VDAC)
          self.VDREG = float(VDREG)
          self.IANA= float(IANA)
          self.V24 = float(V24)
          self.IDIGI=float(IDIGI)
          self.ADDRPIXELS=int(ADDRPIXELS)
          self.TRIMPIXELS=int(TRIMPIXELS)
          self.MASKPIXELS=int(MASKPIXELS)
          self.NSIGPIXELS=int(NSIGPIXELS)
          self.NOISEPIXELS=int(NOISEPIXELS)
          self.THRESHOLDPIXELS=int(THRESHOLDPIXELS)
          self.PHFAIL=int(PHFAIL)
          self.COMMENT=unicode(COMMENT)
	  self.VDCAP = float(VDCAP)
          self.VDIGU_ADC = int(VDIGU_ADC)
          self.VANAU_ADC = int(VANAU_ADC)
          self.VANAR_ADC = int(VANAR_ADC)
          self.VBG_ADC = int(VBG_ADC)
          self.IANA_ADC = int(IANA_ADC)
          self.VDIGU_VOLTS = float(VDIGU_VOLTS)
          self.VANAU_VOLTS = float(VANAU_VOLTS)
          self.IANA_MILLIAMPS = float(IANA_MILLIAMPS)
          self.VANASCAN = unicode(VANASCAN)



class Test_Roc_Setup(object):
    __storm_table__ = "test_roc_setup"
    TEST_ID = Int(primary=True)
    SESSION_ID=Int()
    session = Reference (SESSION_ID,Session.SESSION_ID)
    ROC_ID =  Unicode()
    roc=Reference(ROC_ID, Roc.ROC_ID)
    DATA_ID=Int()
    data=Reference(DATA_ID,Data.DATA_ID)

    TEMPERATURE =Float()
    HUMIDITY =Float()
    IDIG  = Int()
    CLK   = Int()
    DESER   = Int()
    VDIG  = Int()
    VANA  = Int()
    VSH  = Int()
    VCOMP  = Int()
    VWLLPR  = Int()
    VWLLSH  = Int()
    VHLDDEL  = Int()
    VTRIM  = Int()
    VTHRCOMP  = Int()
    VIBIAS_BUS  = Int()
    VBIAS_SF  = Int()
    VOFFSETOP  = Int()
    PHOFFSET  = Int()
    VION  = Int()
    VCOMP_ADC  = Int()
    PHSCALE  = Int()
    VICOLOR  = Int() 
    VCAL  = Int()
    CALDEL  = Int()
    VD  = Int()	
    VA  = Int()
    CTRLREG  = Int()
    WBC  = Int()
    RBREG  = Int()
     
    def __init__(self, SESSION_ID, DATA_ID, ROC_ID,
                 TEMPERATURE, 
                 HUMIDITY,
                 IDIG,	
                 CLK,
                 DESER  ,
                 VDIG ,
                 VANA ,
                 VSH ,
                 VCOMP ,
                 VWLLPR ,
                 VWLLSH ,
                 VHLDDEL ,
                 VTRIM ,
                 VTHRCOMP ,
                 VIBIAS_BUS ,
                 VBIAS_SF ,
                 VOFFSETOP ,
                 PHOFFSET ,
                 VION ,
                 VCOMP_ADC ,
                 PHSCALE ,
                 VICOLOR , 
                 VCAL ,
                 CALDEL ,
                 VD ,	
                 VA ,
                 CTRLREG ,
		 WBC ,
                 RBREG):
        
       self.TEMPERATURE = float(TEMPERATURE)
       self.HUMIDITY = float(HUMIDITY)
       self.IDIG=int(           IDIG )	    	
       self.CLK =int( 		 CLK  )	    
       self.DESER =int( 	 DESER  )   
       self.VDIG =int( 	 VDIG )	    
       self.VANA =int( 	 VANA )	    
       self.VSH =int( 		 VSH )	    
       self.VCOMP =int( 	 VCOMP )    
       self.VWLLPR =int( 	 VWLLPR )   
       self.VWLLSH =int( 	 VWLLSH )   
       self.VHLDDEL =int( 	 VHLDDEL )  
       self.VTRIM =int( 	 VTRIM )    
       self.VTHRCOMP =int( 	 VTHRCOMP ) 
       self.VIBIAS_BUS =int( 	 VIBIAS_BUS )
       self.VBIAS_SF =int(VBIAS_SF)
       self.VOFFSETOP =int( 	 VOFFSETOP )
       self.PHOFFSET =int( 	 PHOFFSET ) 
       self.VION =int( 	 VION )	    
       self.VCOMP_ADC =int( 	 VCOMP_ADC )
       self.PHSCALE =int( 	 PHSCALE )  
       self.VICOLOR =int( 	 VICOLOR )  
       self.VCAL =int( 	 VCAL )	    
       self.CALDEL =int( 	 CALDEL )   
       self.VD =int( 		 VD )	    
       self.VA =int( 		 VA )	    
       self.CTRLREG =int( 	 CTRLREG )  
       self.WBC =int(		 WBC )	    
       self.RBREG =int(	 RBREG )    
       

          


class Test_IV(object): # e' il vecchio test_sensor
      __storm_table__ = "test_iv"
      TEST_ID = Int(primary=True)
      SESSION_ID=Int()
      session = Reference (SESSION_ID,Session.SESSION_ID)
      SENSOR_ID =  Unicode()
      sensor=Reference(SENSOR_ID, Sensor.SENSOR_ID)
      GRADE = Unicode()
      DATA_ID=Int()
      V1 = Float()
      I1= Float()
      COMMENT=Unicode()
      V2 = Float()
      I2= Float()
      DATE = DateTime()
      SLOPE = Float()
      TEMPERATURE= Float()
      TYPE = Unicode()
      data=Reference(DATA_ID,Data.DATA_ID)
      def __init__(self,SESSION_ID,SENSOR_ID,GRADE,DATA_ID,V1,I1,V2,I2,SLOPE, DATE,TYPE="", COMMENT="", TEMPERATURE=0):
          self.SESSION_ID=SESSION_ID
          self.SENSOR_ID=unicode(SENSOR_ID)
          self.TYPE=unicode(TYPE)
          self.GRADE=unicode(GRADE)
          self.DATA_ID=DATA_ID
	  self.V1=float(V1)
          self.GRADE=unicode(GRADE)
          self.COMMENT=unicode(COMMENT)
          self.V2=float(V2)
          self.I1=float(I1)
          self.I2=float(I2)
          self.DATE = DATE
          self.SLOPE= float(SLOPE)
          self.TEMPERATURE = TEMPERATURE


class Test_IT(object):
      __storm_table__ = "test_it"
      TEST_ID = Int(primary=True)
      SESSION_ID=Int()
      session = Reference (SESSION_ID,Session.SESSION_ID)
      SENSOR_ID =  Unicode()
      sensor=Reference(SENSOR_ID, Sensor.SENSOR_ID)
      TIMELENGTH = Float()
      GRADE = Unicode()
      DATA_ID=Int()
      AVG_I = Float()
      MAX_I = Float()
      MIN_I = Float()
      RMS_I = Float()
      COMMENT=Unicode()
      DATE = DateTime()
      SLOPE = Float()
      TEMPERATURE = Float()
      TYPE = Unicode()
      data=Reference(DATA_ID,Data.DATA_ID)
      def __init__(self,SESSION_ID,SENSOR_ID,GRADE,DATA_ID,  TIMELENGTH, AVG_I, RMS_I,MAX_I, MIN_I , SLOPE  , TEMPERATURE, DATE,TYPE="", COMMENT=""):
          self.SESSION_ID=SESSION_ID
          self.SENSOR_ID=unicode(SENSOR_ID)
          self.TYPE=unicode(TYPE)
          self.GRADE=unicode(GRADE)
          self.DATA_ID=DATA_ID
          self.GRADE=unicode(GRADE)
          self.COMMENT=unicode(COMMENT)
          self.DATE = (DATE)
          self.SLOPE= float(SLOPE)
          self.TIMELENGTH= float(TIMELENGTH)
          self.MAX_I= float(MAX_I)
          self.MIN_I= float(MIN_I)
          self.RMS_I= float(RMS_I)
          self.AVG_I= float(AVG_I)
          self.TEMPERATURE = TEMPERATURE

class Test_SensorInspection(object):
      __storm_table__ = "test_sensor_inspection"
      TEST_ID = Int(primary=True)
      SESSION_ID=Int()
      session = Reference (SESSION_ID,Session.SESSION_ID)
      SENSOR_ID =  Unicode()
      sensor=Reference(SENSOR_ID, Sensor.SENSOR_ID)
      RESULT = Unicode()
      DATA_ID=Int()
      DATE = DateTime()
      COMMENT = Unicode()
      data=Reference(DATA_ID,Data.DATA_ID)
      def __init__(self,SESSION_ID,SENSOR_ID,RESULT,DATA_ID,DATE,TYPE="", COMMENT=""):
          self.SESSION_ID=SESSION_ID
          self.SENSOR_ID=unicode(SENSOR_ID)
          self.TYPE=unicode(TYPE)
          self.GRADE=unicode(GRADE)
          self.DATA_ID=DATA_ID
          self.DATE = (DATE)
          self.RESULT=unicode(RESULT)
          self.COMMENT=unicode(COMMENT)

class Test_BareModule_Inspection(object):
      __storm_table__ = "test_baremodule_inspection"
      TEST_ID = Int(primary=True)
      SESSION_ID=Int()
      session = Reference (SESSION_ID,Session.SESSION_ID)
      BAREMODULE_ID =  Unicode()
      baremodule=Reference(BAREMODULE_ID, BareModule.BAREMODULE_ID)
      RESULT = Unicode()
      DATA_ID=Int()
      DATE = DateTime()
      COMMENT = Unicode()
      data=Reference(DATA_ID,Data.DATA_ID)
      def __init__(self,SESSION_ID,BAREMODULE_ID,RESULT,DATA_ID,DATE,TYPE="", COMMENT=""):
          self.SESSION_ID=SESSION_ID
          self.BAREMODULE_ID=unicode(BAREMODULE_ID)
          self.TYPE=unicode(TYPE)
  #        self.GRADE=unicode(GRADE)
          self.DATA_ID=DATA_ID
          self.DATE = (DATE)
          self.RESULT=unicode(RESULT)
          self.COMMENT=unicode(COMMENT)

class Test_BareModule_Chip(object):
      __storm_table__ = "test_baremodule_chip"
      TEST_ID = Int(primary=True)
      SESSION_ID=Int()
      session = Reference (SESSION_ID,Session.SESSION_ID)
      BAREMODULE_ID =  Unicode()
      CHIP_N = Int()
      DATE = DateTime()
      baremodule=Reference(BAREMODULE_ID, BareModule.BAREMODULE_ID)
      GRADE = Unicode()
      DATA_ID=Int()
      COMMENT=Unicode()
      def __init__(self,SESSION_ID,BAREMODULE_ID,GRADE,DATA_ID,V1,CHIP_N,DATE,TYPE="", COMMENT=""):
          self.SESSION_ID=SESSION_ID
          self.BAREMODULE_ID=unicode(BAREMODULE_ID)
          self.TYPE=unicode(TYPE)
          self.GRADE=unicode(GRADE)
          self.DATA_ID=DATA_ID
          self.COMMENT=unicode(COMMENT)
          self.CHIP_N = int(CHIP_N)

class Test_CV(object):
      __storm_table__ = "test_cv"
      TEST_ID = Int(primary=True)
      SESSION_ID=Int()
      session = Reference (SESSION_ID,Session.SESSION_ID)
      SENSOR_ID =  Unicode()
      sensor=Reference(SENSOR_ID, Sensor.SENSOR_ID)
      GRADE = Unicode()
      DATA_ID=Int()
      VDEPL = Float()
      C= Float()
      COMMENT=Unicode()
      R = Float()
      SLOPE_BEFORE_DEPLETION = Float()
      DATE = DateTime()
      TEMPERATURE = Float()
      TYPE = Unicode()
      data=Reference(DATA_ID,Data.DATA_ID)
      def __init__(self,SESSION_ID,SENSOR_ID,GRADE,DATA_ID,V1,C1,V2,C2,SLOPE, TEMPERATURE, R,DATE,TYPE="", COMMENT=""):
          self.SESSION_ID=SESSION_ID
          self.SENSOR_ID=unicode(SENSOR_ID)
          self.TYPE=unicode(TYPE)
          self.GRADE=unicode(GRADE)
          self.DATA_ID=DATA_ID
          self.V1=float(V1)
          self.GRADE=unicode(GRADE)
          self.COMMENT=unicode(COMMENT)
          self.R = float(R)
          self.V2=float(V2)
          self.C1=float(C1)
          self.C2=float(C2)
          self.DATE = (DATE)
          self.SLOPE= float(SLOPE)
          self.TEMPERATURE = TEMPERATURE

class Test_PerformanceParameters(object):
    __storm_table__ = "test_performanceparameters"
    TEST_ID = Int(primary=True)
    ROC_POS = Int()
    FULLMODULEANALYSISTEST_ID = Int()
    Total = Int()
    nDeadPixel  = Int()
    nMaskDefect  = Int()
    nDeadBumps  = Int()
    nDeadTrimbits  = Int()
    nAddressProblems  = Int()
    nNoisy1Pixel  = Int()
    nNoisy2Pixel  = Int()
    nThrDefect  = Int()
    nGainDefect  = Int()
    nPedDefect  = Int()
    nPar1Defect  = Int()
    PixelDefectsGrade  = Int()
    SCurveWidth_mu= Float()
    SCurveWidth_sigma= Float()
    ThresholdTrimmed_mu= Float()
    ThresholdTrimmed_sigma= Float()
    BumpBonding_mu= Float()
    BumpBonding_sigma= Float()
    BumpBonding_threshold= Float()
    PHCalibrationGain_mu= Float()
    PHCalibrationGain_sigma= Float()
    PHCalibrationPar1_mu= Float()
    PHCalibrationPar1_sigma= Float()
    PHCalibrationPedestal_mu= Float()
    PHCalibrationPedestal_sigma= Float()
    TrimBits_mu= Float()
    TrimBits_sigma= Float()
    def __init__( self, 
                  ROC_POS,
                  FULLMODULEANALYSISTEST_ID,
                  Total , 
                  nDeadPixel  ,
                  nMaskDefect  ,
                  nDeadBumps  ,
                  nDeadTrimbits  ,
                  nAddressProblems  ,
                  nNoisy1Pixel  ,
                  nNoisy2Pixel  ,
                  nThrDefect  ,
                  nGainDefect  ,
                  nPedDefect  ,
                  nPar1Defect  ,
                  PixelDefectsGrade  ,
                  SCurveWidth_mu , 
                  SCurveWidth_sigma,
                  ThresholdTrimmed_mu,
                  ThresholdTrimmed_sigma,
                  BumpBonding_mu,
                  BumpBonding_sigma,
                  BumpBonding_threshold,
                  PHCalibrationGain_mu,
                  PHCalibrationGain_sigma,
                  PHCalibrationPar1_mu,
                  PHCalibrationPar1_sigma,
                  PHCalibrationPedestal_mu,
                  PHCalibrationPedestal_sigma,
                  TrimBits_mu,
                  TrimBits_sigma):  
        self.FULLMODULEANALYSISTEST_ID  = FULLMODULEANALYSISTEST_ID
        self.ROC_POS =                   int(      ROC_POS )
        self.Total =                        int(      Total  )                        
        self.nDeadPixel  =                     int(   nDeadPixel )                    
        self.nMaskDefect  =                     int(  nMaskDefect  )                  
        self.nDeadBumps  =                      int(  nDeadBumps     )                
        self.nDeadTrimbits  =                   int(  nDeadTrimbits    )              
        self.nAddressProblems  =                int(  nAddressProblems   )            
        self.nNoisy1Pixel  =                    int(  nNoisy1Pixel         )          
        self.nNoisy2Pixel  =                    int(  nNoisy2Pixel           )        
        self.nThrDefect  =                      int(  nThrDefect               )      
        self.nGainDefect  =                      int( nGainDefect                )    
        self.nPedDefect  =                  int(      nPedDefect                   )  
        self.nPar1Defect  =                    int(   nPar1Defect                    )
        self.PixelDefectsGrade  =               int(  PixelDefectsGrade              )
        self.SCurveWidth_mu =                  float( SCurveWidth_mu                  )
        self.SCurveWidth_sigma=                float( SCurveWidth_sigma              )
        self.ThresholdTrimmed_mu=              float( ThresholdTrimmed_mu            )
        self.ThresholdTrimmed_sigma=            float(ThresholdTrimmed_sigma         )
        self.BumpBonding_mu=                    float(BumpBonding_mu                 )
        self.BumpBonding_sigma=                 float(BumpBonding_sigma             )
        self.BumpBonding_threshold=             float(BumpBonding_threshold          )
        self.PHCalibrationGain_mu=              float(PHCalibrationGain_mu           )
        self.PHCalibrationGain_sigma=           float(PHCalibrationGain_sigma        )
        self.PHCalibrationPar1_mu=              float(PHCalibrationPar1_mu           )
        self.PHCalibrationPar1_sigma=           float(PHCalibrationPar1_sigma        )
        self.PHCalibrationPedestal_mu=          float(PHCalibrationPedestal_mu       )
        self.PHCalibrationPedestal_sigma=       float(PHCalibrationPedestal_sigma    )
        self.TrimBits_mu=                       float(TrimBits_mu                    )
        self.TrimBits_sigma=                    float(TrimBits_sigma)


class Test_DacParameters(object):
      __storm_table__ = "test_dacparameters"
      TEST_ID = Int(primary=True)
      TRIM_VALUE = Unicode()
      ROC_POS = Int()
      FULLMODULEANALYSISTEST_ID = Int()
      VDIG=Int()
      VANA=Int()
      VCAL=Int()
      VSH=Int()
      VCOMP=Int()
      VWLLPR=Int()
      VWLLSH=Int()
      VTRIM=Int()
      VTHRCOMP=Int()
      VHLDDEL=Int()
      VIBIAS_BUS=Int()
      PHOFFSET=Int()
      VCOMP_ADC=Int()
      PHSCALE=Int()
      VICOLOR=Int()
      CALDEL=Int()
      CTRLREG=Int()
      WBC=Int()
      def __init__(self, 
                   ROC_POS,
                   TRIM_VALUE,
                   FULLMODULEANALYSISTEST_ID,
                   VDIG,
                   VANA,
                   VSH,
                   VCAL,
                   VCOMP,
                   VWLLPR,
                   VWLLSH,
                   VTRIM,
                   VTHRCOMP,
                   VHLDDEL,
                   VIBIAS_BUS,
		   PHOFFSET,
                   VCOMP_ADC,
                   PHSCALE,
#                   VOFFSET_R0,
#                   VIBIAS_PH,
#                   VIREF_ADC,
                   VICOLOR,
                   CALDEL,
                   CTRLREG,
                   WBC):       
           self.TRIM_VALUE = unicode(TRIM_VALUE)
           self.ROC_POS=int(ROC_POS)
           self.FULLMODULEANALYSISTEST_ID=int(  FULLMODULEANALYSISTEST_ID)
           self.VDIG=int(                VDIG)     
           self.VANA=int(                VANA)       
           self.VSH=int(                 VSH)        
           self.VCOMP=int(               VCOMP)      
           self.VWLLPR=int(              VWLLPR)     
           self.VWLLSH=int(              VWLLSH)     
           self.VTRIM=int(               VTRIM)      
           self.VTHRCOMP=int(            VTHRCOMP)   
           self.VHLDDEL=int(             VHLDDEL)    
           self.VIBIAS_BUS=int(          VIBIAS_BUS) 
           self.PHOFFSET=int(          PHOFFSET) 
           self.VCOMP_ADC=int(           VCOMP_ADC)  
           self.VCAL=int(           VCAL)  
           self.PHSCALE=int(           PHSCALE)  
           self.VICOLOR=int(             VICOLOR)    
           self.CALDEL=int(              CALDEL)     
           self.CTRLREG=int(             CTRLREG   )
           self.WBC=int(                 WBC)
      
    
class Test_BM_ROC_DacParameters(object):
      __storm_table__ = "test_bm_roc_dacparameters"
      TEST_ID = Int(primary=True)
      QATEST_ID = Int()
      qatest = Reference(QATEST_ID, Test_BareModule_QA.TEST_ID)
      ROC_POS = Int()
      BAREMODULE_ID = Unicode()
      baremodule = Reference(BAREMODULE_ID, BareModule.BAREMODULE_ID)
      DATA_ID=Int()
      data=Reference(DATA_ID,Data.DATA_ID)
      SESSION_ID = Int()
      IDIG  = Int() 
      CLK  = Int() 
      DESER  = Int() 
      VDIG  = Int() 
      VANA  = Int() 
      VSH  = Int()
      VCOMP  = Int() 
      VWLLPR  = Int() 
      VWLLSH  = Int() 
      VHLDDEL  = Int() 
      VTRIM  = Int() 
      VTHRCOMP  = Int() 
      VIBIAS_BUS  = Int() 
      VIBIAS_SF  = Int() 
      VOFFSETOP  = Int() 
      PHOFFSET  = Int()
      VION  = Int()
      VCOMP_ADC  = Int()
      PHSCALE  = Int()
      VICOLOR  = Int() 
      VCAL  = Int() 
      CALDEL  = Int() 
      VD  = Int() 
      VA  = Int() 
      CTRLREG  = Int() 
      WBC  = Int() 
      RBREG  = Int() 
      TEMPERATURE = Float()
      HUMIDITY= Float()
      def __init__(self, 
                   ROC_POS,
                   BAREMODULE_ID,
                   DATA_ID ,
                   IDIG  ,
                   CLK  ,
                   DESER , 
                   VDIG  ,
                   VANA  ,
                   VSH,
                   VCOMP,  
                   VWLLPR , 
                   VWLLSH  ,
                   VHLDDEL  ,
                   VTRIM  ,
                   VTHRCOMP , 
                   VIBIAS_BUS,  
                   VIBIAS_SF  ,
                   VOFFSETOP  ,
                   PHOFFSET ,
                   VION ,
                   VCOMP_ADC ,
                   PHSCALE ,
                   VICOLOR ,
                   VCAL  ,
                   CALDEL , 
                   VD  ,
                   VA  ,
                   CTRLREG,  
                   WBC  ,
                   RBREG  ,
                   SESSION_ID,
                   TEMPERATURE,
		   QATEST_ID,
                   HUMIDITY                   ):
          self.ROC_POS = int(ROC_POS)      
          self.BAREMODULE_ID= unicode(BAREMODULE_ID)
          self.SESSION_ID = int(  SESSION_ID)   
          self.DATA_ID = int(    DATA_ID)
          self.IDIG  = int(       IDIG )        
          self.CLK  = int(        CLK )         
          self.DESER  = int(      DESER )       
          self.VDIG  = int(       VDIG )        
          self.VANA  = int(       VANA )        
          self.VSH  = int(        VSH )         
          self.VCOMP  = int(      VCOMP )       
          self.VWLLPR  = int(     VWLLPR )      
          self.VWLLSH  = int(     VWLLSH )      
          self.VHLDDEL  = int(    VHLDDEL )     
          self.VTRIM  = int(      VTRIM )       
          self.VTHRCOMP  = int(   VTHRCOMP )    
          self.VIBIAS_BUS  = int( VIBIAS_BUS )  
          self.VIBIAS_SF  = int(  VIBIAS_SF )   
          self.VOFFSETOP  = int(  VOFFSETOP )    
          self.PHOFFSET  = int(   PHOFFSET )    
          self.VION  = int(       VION )        
          self.VCOMP_ADC  = int(  VCOMP_ADC )   
          self.PHSCALE  = int(    PHSCALE )     
          self.VICOLOR  = int(    VICOLOR )     
          self.VCAL  = int(       VCAL )        
          self.CALDEL  = int(     CALDEL )      
          self.VD  = int(         VD )          
          self.VA  = int(         VA )          
          self.CTRLREG  = int(    CTRLREG )     
          self.WBC  = int(        WBC )         
          self.RBREG = int(       RBREG)
          self.TEMPERATURE = float(TEMPERATURE)
          self.QATEST_ID = int(QATEST_ID)
          self.HUMIDITY = float(HUMIDITY)

class Test_FullModule_XRay_HR_Module(object):
    __storm_table__ = "Test_FullModule_XRay_HR_Module"
    TEST_ID = Int(primary=True)
    SESSION_ID=Int()
    session = Reference (SESSION_ID,Session.SESSION_ID)
    FULLMODULE_ID =  Unicode()
    fullmodule=Reference(FULLMODULE_ID, FullModule.FULLMODULE_ID)
    DATA_ID=Int()
    data=Reference(DATA_ID,Data.DATA_ID)
    LAST_PROCESSING_ID = Int()
    RESULT = Unicode()
    XRAY_SLOT = Int()
    HITRATENOMINAL = Float()
    TEMPNOMINAL = Float()
    TIMESTAMP = Unicode()
    COMMENT = Unicode()
    
    
    MEASURED_EFFICIENCY = Float() 
    MEASURED_HITRATE_EFF = Float() 
    N_PIXEL_NO_HIT  = Int() 
    MEASURED_HITRATE = Float() 
    MEAN_NOISE_ALLPIXELS = Float() 
    WIDTH_NOISE_ALLPIXELS = Float() 
    MEASURED_HITRATE_NOISE = Float() 
    
    XRAY_SLOT  = Int() 
    HITRATENOMINAL = Float() 
    TEMPNOMINAL = Float() 
    TIMESTAMP =Unicode() 
    COMMENT = Unicode()
    MACRO_VERSION = Unicode()

    def __init__(self, SESSION_ID,  FULLMODULE_ID ,  DATA_ID,   LAST_PROCESSING_ID , RESULT, HITRATENOMINAL, TEMPNOMINAL, TIMESTAMP, MEASURED_EFFICIENCY, MEASURED_HITRATE_EFF, N_PIXEL_NO_HIT  ,
                 MEASURED_HITRATE,
                 MEAN_NOISE_ALLPIXELS ,
                 WIDTH_NOISE_ALLPIXELS,
                 MEASURED_HITRATE_NOISE,                 
                 XRAY_SLOT,
                 MACRO_VERSION,
                 COMMENT ):
        self.SESSION_ID = int(SESSION_ID)
        self.MEASURED_HITRATE_EFF = float(MEASURED_HITRATE_EFF)
        self.FULLMODULE_ID = unicode(FULLMODULE_ID)
        self.DATA_ID = int(DATA_ID)
        self.MEASURED_EFFICIENCY = float(MEASURED_EFFICIENCY)
        self.RESULT = unicode(RESULT)
        self.LAST_PROCESSING_ID = int(LAST_PROCESSING_ID)
        self.TEMPNOMINAL = float(TEMPNOMINAL)
        self.MACRO_VERSION = unicode(MACRO_VERSION)
        self.XRAY_SLOT = int(XRAY_SLOT)
        self.HITRATENOMINAL = float(HITRATENOMINAL)
        self.TIMESTAMP = unicode(TIMESTAMP)
        self.N_PIXEL_NO_HIT = int(N_PIXEL_NO_HIT)
        self.MEASURED_HITRATE = float(MEASURED_HITRATE)
        self.MEAN_NOISE_ALLPIXELS = float(MEAN_NOISE_ALLPIXELS)
        self.COMMENT = unicode(COMMENT)
        self.WIDTH_NOISE_ALLPIXELS = float(WIDTH_NOISE_ALLPIXELS)
        self.MEASURED_HITRATE_NOISE = float(MEASURED_HITRATE_NOISE)
        self.HITRATENOMINAL = float(HITRATENOMINAL)
        self.TEMPNOMINAL = float(TEMPNOMINAL)
        self.TIMESTAMP = unicode(TIMESTAMP)

class Test_FullModule_XRay_HR_Module_Analysis(object):
    __storm_table__ = "Test_FullModule_XRay_HR_Module_Analysis"
    TEST_ID = Int(primary=True)
    SESSION_ID=Int()
    session = Reference (SESSION_ID,Session.SESSION_ID)
#    FULLMODULE_ID =  Unicode()
#    fullmodule=Reference(FULLMODULE_ID, FullModule.FULLMODULE_ID)
    DATA_ID=Int()
    data=Reference(DATA_ID,Data.DATA_ID)
    PROCESSING_ID = Int()
    RESULT = Unicode()
    FULLMODULETEST_ID  = Int()
    fullmoduletest=Reference(FULLMODULETEST_ID,Test_FullModule_XRay_HR_Module.TEST_ID )
    MACRO_VERSION = Unicode()
    GRADE = Unicode()
    N_PIXELS_EFF_BELOW_CUT = Int() 
    INTERP_EFF_TESTPOINT = Float() 
    N_HOT_PIXELS = Int() 
    N_COL_NONUNIFORM = Int() 
    N_COL_BELOW_CUT = Int() 
    N_PIXELS_NOISE_ABOVETH = Int() 
    

    def __init__(self, SESSION_ID, 
#		 FULLMODULE_ID , 
		 DATA_ID, 
                 PROCESSING_ID , GRADE,RESULT, MACRO_VERSION, FULLMODULETEST_ID,     
                 N_PIXELS_EFF_BELOW_CUT,    INTERP_EFF_TESTPOINT,    N_HOT_PIXELS,    
                 N_COL_NONUNIFORM,     N_COL_BELOW_CUT,     N_PIXELS_NOISE_ABOVETH, COMMENT=""):
        self.SESSION_ID = int(SESSION_ID)
        self.DATA_ID = int(DATA_ID)
        self.PROCESSING_ID = int(PROCESSING_ID)
        self.FULLMODULETEST_ID = int(FULLMODULETEST_ID)
        self.N_PIXELS_EFF_BELOW_CUT = int(N_PIXELS_EFF_BELOW_CUT)
        self.N_HOT_PIXELS = int(    N_HOT_PIXELS)
        self.N_COL_NONUNIFORM = int(N_COL_NONUNIFORM)
        self.N_COL_BELOW_CUT = int(N_COL_BELOW_CUT)
        self.N_PIXELS_NOISE_ABOVETH = int(N_PIXELS_NOISE_ABOVETH)
        self.INTERP_EFF_TESTPOINT = float(INTERP_EFF_TESTPOINT)
 #       self.FULLMODULE_ID = unicode(FULLMODULE_ID)
        self.GRADE = unicode(GRADE)
        self.RESULT = unicode(RESULT)
        self.MACRO_VERSION = unicode(MACRO_VERSION)
        self.COMMENT = unicode(COMMENT)
        

    
class Test_FullModule_XRay_HR_Roc(object):
    __storm_table__ = "Test_FullModule_XRay_HR_Roc"
    TEST_ID = Int(primary=True)
    ROC_POS = Int()
    SESSION_ID=Int()
    session = Reference (SESSION_ID,Session.SESSION_ID)
    TEST_XRAY_HR_MODULE_ID= Int()
    fullmodule=Reference(TEST_XRAY_HR_MODULE_ID, Test_FullModule_XRay_HR_Module.TEST_ID)
    DATA_ID=Int()
    data=Reference(DATA_ID,Data.DATA_ID)
    LAST_PROCESSING_ID = Int()
    COMMENT = Unicode()    
    
    MEASURED_EFFICIENCY = Float() 
    MEASURED_HITRATE_EFF = Float() 
    N_PIXEL_NO_HIT  = Int() 
    MEASURED_HITRATE = Float() 
    MEAN_NOISE_ALLPIXELS = Float() 
    WIDTH_NOISE_ALLPIXELS = Float() 
    MEASURED_HITRATE_NOISE = Float() 
    
    GRADE = Unicode()
    MACRO_VERSION= Unicode()


    def __init__(self,  ROC_POS,
                 SESSION_ID,
                 TEST_XRAY_HR_MODULE_ID,
                 DATA_ID,
                 LAST_PROCESSING_ID,MACRO_VERSION,
                 MEASURED_EFFICIENCY ,
                 MEASURED_HITRATE_EFF,
                 N_PIXEL_NO_HIT,
                 MEASURED_HITRATE,
                 MEAN_NOISE_ALLPIXELS, 
                 WIDTH_NOISE_ALLPIXELS,
                 MEASURED_HITRATE_NOISE,
                 GRADE,
                 COMMENT = ""):
        self.TEST_XRAY_HR_MODULE_ID =                  int(TEST_XRAY_HR_MODULE_ID)
        self.SESSION_ID = int(SESSION_ID)
        self.MEASURED_HITRATE_EFF = float(MEASURED_HITRATE_EFF)
        self.DATA_ID = int(DATA_ID)
        self.MEASURED_EFFICIENCY = float(MEASURED_EFFICIENCY)
        self.LAST_PROCESSING_ID = int(LAST_PROCESSING_ID)
        self.MACRO_VERSION = unicode(MACRO_VERSION)
        self.N_PIXEL_NO_HIT = int(N_PIXEL_NO_HIT)
        self.MEASURED_HITRATE = float(MEASURED_HITRATE)
        self.MEAN_NOISE_ALLPIXELS = float(MEAN_NOISE_ALLPIXELS)
        self.COMMENT = unicode(COMMENT)
        self.WIDTH_NOISE_ALLPIXELS = float(WIDTH_NOISE_ALLPIXELS)
        self.MEASURED_HITRATE_NOISE = float(MEASURED_HITRATE_NOISE)





class Test_FullModule_XRay_HR_Roc_Analysis(object):
    __storm_table__ = "Test_FullModule_XRay_HR_Roc_Analysis"
    TEST_ID = Int(primary=True)
    SESSION_ID=Int()
    session = Reference (SESSION_ID,Session.SESSION_ID)
    DATA_ID=Int()
    data=Reference(DATA_ID,Data.DATA_ID)
    PROCESSING_ID = Int()
    RESULT = Unicode()
    TEST_XRAY_HR_ROC_ID = Int()
    test_xray_hr_roc=Reference(TEST_XRAY_HR_ROC_ID,Test_FullModule_XRay_HR_Roc.TEST_ID )
    MACRO_VERSION = Unicode()
    GRADE = Unicode()
    N_PIXELS_EFF_BELOW_CUT = Int() 
    N_HOT_PIXELS = Int() 
    N_COL_BELOW_CUT = Int() 
    ADDR_PIXELS_BAD = Unicode()
    INTERP_EFF_TESTPOINT = Float()
    ADDR_PIXELS_HOT = Unicode()
    N_COL_NONUNIFORM = Int()
    N_BINS_LOWHIGH = Int()
    N_COL_LOWEFF = Int()
    N_EVENTS_LOWEFF_COL = Int()
    N_PIXELS_NOISE = Int()
    ADDR_PIXELS_NOISE = Unicode()
    COMMENT = Unicode()
    

    def __init__(self,  SESSION_ID,
                 DATA_ID,
                 PROCESSING_ID,
                 TEST_XRAY_HR_ROC_ID,
                 MACRO_VERSION,
                 GRADE,
                 N_PIXELS_EFF_BELOW_CUT,
                 N_HOT_PIXELS,
                 N_COL_BELOW_CUT,
                 ADDR_PIXELS_BAD,
                 INTERP_EFF_TESTPOINT,
                 ADDR_PIXELS_HOT,
                 N_COL_NONUNIFORM,
                 N_BINS_LOWHIGH,
                 N_COL_LOWEFF,
                 N_EVENTS_LOWEFF_COL,
                 N_PIXELS_NOISE,
                 ADDR_PIXELS_NOISE,
                 COMMENT=""):



        self.SESSION_ID = int(SESSION_ID)
        self.DATA_ID = int(DATA_ID)
        self.PROCESSING_ID = int(PROCESSING_ID)
        self.TEST_XRAY_HR_ROC_ID = int(TEST_XRAY_HR_ROC_ID)
        self.MACRO_VERSION = unicode(MACRO_VERSION)
        self.GRADE = unicode(GRADE)
        self.N_PIXELS_EFF_BELOW_CUT = int(N_PIXELS_EFF_BELOW_CUT)
        self.N_COL_NONUNIFORM = int(N_COL_NONUNIFORM)
        self.N_HOT_PIXELS = int(    N_HOT_PIXELS)
        self.ADDR_PIXELS_HOT = unicode(                 ADDR_PIXELS_HOT)
        self.ADDR_PIXELS_NOISE = unicode(                 ADDR_PIXELS_NOISE)
        self.ADDR_PIXELS_BAD = unicode(                 ADDR_PIXELS_BAD)
        self.N_BINS_LOWHIGH = int(                 N_BINS_LOWHIGH)
        self.N_COL_LOWEFF = int(N_COL_LOWEFF)
        self.N_EVENTS_LOWEFF_COL = int(N_EVENTS_LOWEFF_COL)
        self.N_PIXELS_NOISE= int(N_PIXELS_NOISE)
        self.N_COL_BELOW_CUT = int(N_COL_BELOW_CUT)
        self.N_PIXELS_NOISE_ABOVETH = int(N_PIXELS_NOISE_ABOVETH)
        self.INTERP_EFF_TESTPOINT = float(INTERP_EFF_TESTPOINT)
        self.COMMENT = unicode(COMMENT)


#history
 
class History(object):
    __storm_table__ = "history"    
    HISTORY_ID = Int(primary=True)
    TYPE=Unicode()
    ID=Unicode()
    TARGET_TYPE=Unicode()
    TARGET_ID=Unicode()
    OPERATION=Unicode()
    DATE=DateTime()
    COMMENT=Unicode()
    def __init__(self, TYPE, ID, TARGET_TYPE, TARGET_ID, OPERATION, DATE=datetime.now(), COMMENT=""):
        self.TYPE=unicode(TYPE)
        self.ID=unicode(ID)
        self.TARGET_TYPE=unicode(TARGET_TYPE)
        self.TARGET_ID=unicode(TARGET_ID)
        self.OPERATION=unicode(OPERATION)
        self.DATE=DATE
        self.COMMENT=unicode(COMMENT)
    
# References
Roc.lasttest_roc = Reference(  Roc.LASTTEST_ROC, Test_Roc.TEST_ID)

Sensor.lasttest_sensor_iv          = Reference(  Sensor.LASTTEST_SENSOR_IV, Test_IV.TEST_ID)
Sensor.lasttest_sensor_cv          = Reference(  Sensor.LASTTEST_SENSOR_CV, Test_CV.TEST_ID)
Sensor.lasttest_sensor_it          = Reference(  Sensor.LASTTEST_SENSOR_IT, Test_IT.TEST_ID)
Sensor.lasttest_sensor_inspection  = Reference(  Sensor.LASTTEST_SENSOR_INSPECTION, Test_SensorInspection.TEST_ID)

BareModule.lasttest_baremodule_inspection = Reference(  BareModule.LASTTEST_BAREMODULE_INSPECTION, Test_BareModule_Inspection.TEST_ID)
Hdi.lasttest_hdi_reception = Reference(  Hdi.LASTTEST_HDI_RECEPTION, Test_Hdi_Reception.TEST_ID)
Hdi.lasttest_hdi_tbmgluing = Reference(  Hdi.LASTTEST_HDI_TBMGLUING, Test_Hdi_TbmGluing.TEST_ID)
Hdi.lasttest_hdi_bonding = Reference(  Hdi.LASTTEST_HDI_BONDING, Test_Hdi_Bonding.TEST_ID)
Hdi.lasttest_hdi_electric = Reference(  Hdi.LASTTEST_HDI_ELECTRIC, Test_Hdi_Electric.TEST_ID)
Hdi.lasttest_hdi_validation = Reference(  Hdi.LASTTEST_HDI_VALIDATION, Test_Hdi_Validation.TEST_ID)


Tbm.lasttest_tbm = Reference(  Tbm.LASTTEST_TBM, Test_Tbm.TEST_ID)
#FullModule.lasttest_fullmodule = Reference(  FullModule.LASTTEST_FULLMODULE, Test_FullModule.TEST_ID)

Test_Logbook.adddata = Reference(Test_Logbook.DATA_ID,Data.DATA_ID)

Test_DacParameters.fullmoduleanalysistest = Reference(  Test_DacParameters.FULLMODULEANALYSISTEST_ID,Test_FullModuleAnalysis.TEST_ID)
Test_PerformanceParameters.fullmoduleanalysistest = Reference(  Test_PerformanceParameters.FULLMODULEANALYSISTEST_ID,Test_FullModuleAnalysis.TEST_ID)


#
# ne mancano ...
#
#Test_FullModuleSummary.fullmoduletest_t1 = Reference(Test_FullModuleSummary.FULLMODULETEST_T1,Test_FullModule.TEST_ID)
#Test_FullModuleSummary.fullmoduletest_t2 = Reference(Test_FullModuleSummary.FULLMODULETEST_T2,Test_FullModule.TEST_ID)
#Test_FullModuleSummary.fullmoduletest_t3 = Reference(Test_FullModuleSummary.FULLMODULETEST_T3,Test_FullModule.TEST_ID)

Test_FullModuleSummary.fullmoduletests =  ReferenceSet(Test_FullModuleSummary.TEST_ID,Test_FullModule.SUMMARY_ID)

FullModule.lasttest = Reference(FullModule.LASTTEST_FULLMODULE, Test_FullModuleSummary.TEST_ID)

FullModule.lasttest_xray_vcal = Reference(FullModule.LASTTEST_XRAY_VCAL, Test_FullModule_XRay_Vcal.TEST_ID)


FullModule.summaries = ReferenceSet(FullModule.FULLMODULE_ID, Test_FullModuleSummary.FULLMODULE_ID)
FullModule.tests = ReferenceSet(FullModule.FULLMODULE_ID, Test_FullModule.FULLMODULE_ID)
Test_FullModule.analyses = ReferenceSet(Test_FullModule.TEST_ID, Test_FullModuleAnalysis.FULLMODULETEST_ID
)

BareModule.test_inspection =  Reference(BareModule.LASTTEST_BAREMODULE_INSPECTION, Test_BareModule_Inspection.TEST_ID )
BareModule.test_qa_bonding =  Reference(BareModule.LASTTEST_BAREMODULE_QA_BONDING, Test_BareModule_QA.TEST_ID )
BareModule.test_qa_pixelalive =  Reference(BareModule.LASTTEST_BAREMODULE_QA_PIXELALIVE, Test_BareModule_QA.TEST_ID )
BareModule.test_grading =  Reference(BareModule.LASTTEST_BAREMODULE_GRADING, Test_BareModule_Grading.TEST_ID )
Roc.wafer = Reference(Roc.WAFER_ID, RocWafer.ROCWAFER_ID)
