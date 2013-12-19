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
    def __init__(self, SENDER,RECEIVER, ISSUED_DATE=datetime(1970,1,1), RECEIVED_DATE=datetime.now(), STATUS="ARRIVED", COMMENT=""):
        self.SENDER=unicode(SENDER)
        self.RECEIVER=unicode(RECEIVER)
        self.ISSUED_DATE=ISSUED_DATE
        self.RECEIVED_DATE=RECEIVED_DATE
        self.STATUS=unicode(STATUS)
        self.COMMENT=unicode(COMMENT)

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
        self.TYPE=unicode(type)
        self.COMMENT=unicode(COMMENT)
    
#
# inventory
#
class Roc(object):
  __storm_table__ = "inventory_roc"
  ROC_ID = Unicode(primary=True)
  WAFER_ID = Unicode()
  ROC_POSITION = Unicode()
  GRADING_CLASS = Unicode()
  CURRENT_D = Unicode()
  CURRENT_A = Unicode()
  VANA  = Unicode()
  DEFECTS =  Unicode()
  TRANSFER_ID = Int()
  transfer = Reference(TRANSFER_ID, Transfer.TRANSFER_ID)
  COMMENT = Unicode()
  STATUS=Unicode()
  LASTTEST_ROC=Int()
  def __init__(self,ROC_ID, TRANSFER_ID, COMMENT="",LASTTEST_ROC=0, STATUS="",WAFER_ID="",ROC_POSITION="",GRADING_CLASS="",CURRENT_D="",CURRENT_A="",VANA="",DEFECTS=""):
      self.ROC_ID=unicode(ROC_ID)
      self.TRANSFER_ID=(TRANSFER_ID)
      self.COMMENT=unicode(COMMENT)
      self.LASTTEST_ROC = LASTTEST_ROC
      self.STATUS=unicode(STATUS)
      self.WAFER_ID=unicode(WAFER_ID)
      self.ROC_POSITION=unicode(ROC_POSITION)
      self.GRADING_CLASS=unicode(GRADING_CLASS)
      self.CURRENT_D=unicode(CURRENT_D)
      self.CURRENT_A=unicode(CURRENT_A)
      self.VANA=unicode(VANA)
      self.DEFECTS=unicode(DEFECTS)

class Batch(object):
    __storm_table__ = "inventory_batch"
    BATCH_ID = Unicode(primary=True)
    TRANSFER_ID=Int()
    transfer = Reference(TRANSFER_ID, Transfer.TRANSFER_ID)
    PRODCENTER = Unicode()
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
    CV = Unicode()
    OPTICAL_INSPECTION=Unicode()
    OPTICAL_INSPECTION_RESULT=Unicode()
    COMMENT = Unicode()
    DATA_ID=Int()
    data=Reference(DATA_ID,Data.DATA_ID)
    NUMBEROFGOODSENSORS=Int()
    RESULT=Unicode()

    def __init__(self,WAFER_ID,BATCH_ID, TRANSFER_ID, METALIZATION="", PASSIVATION="", UNDER_BUMP_METALIZATION="", SIZE_OF_OPENING="", CV="", OPTICAL_INSPECTION="", OPTICAL_INSPECTION_RESULT="", COMMENT="",DATA_ID=0, NUMBEROFGOODSENSORS=0, RESULT=""):
        self.BATCH_ID=unicode(BATCH_ID)
        self.WAFER_ID=unicode(WAFER_ID)
        self.TRANSFER_ID=TRANSFER_ID
        self.COMMENT=unicode(COMMENT)
        self.METALIZATION= unicode(METALIZATION )       
        self.PASSIVATION= unicode(PASSIVATION )       
        self.UNDER_BUMP_METALIZATION= unicode(UNDER_BUMP_METALIZATION )       
        self.SIZE_OF_OPENING= unicode(SIZE_OF_OPENING )       
        self.CV= unicode(CV )       
        self.OPTICAL_INSPECTION= unicode(OPTICAL_INSPECTION)       
        self.OPTICAL_INSPECTION_RESULT= unicode(OPTICAL_INSPECTION_RESULT)       
        self.RESULT=unicode(RESULT)
        self.NUMBEROFGOODSENSORS=NUMBEROFGOODSENSORS
        self.DATA_ID=DATA_ID

    


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
  def __init__(self,SENSOR_ID,TRANSFER_ID, TYPE, PRODCENTER,COMMENT="", 
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
  BUILTBY = Unicode()
  COMMENT = Unicode()
  LABEL2D = Unicode()
  POWERCABLE=Unicode()
  SIGNALCABLE=Unicode()
  TYPE=Unicode()
  LASTTEST_BAREMODULE_INSPECTION =Int()
  LASTTEST_CHIPS = Unicode()
  def getRoc(self,i):
      #
      # parse ROC_IDs to extract field # N
      #
      result =(self.ROC_ID.split(","))[i]
      return result
  def getChipTest(self,i):
      result =(self.LASTTEST_CHIPS.split(","))[i]
      return int(result)
  def __init__(self,BAREMODULE_ID,ROC_ID,SENSOR_ID,TRANSFER_ID,  BUILTBY, BUILTON=datetime.now(),COMMENT="", LASTTEST_CHIPS = "",LASTTEST_BAREMODULE_INSPECTION=0, STATUS="",LABEL2D="",POWERCABLE="", SIGNALCABLE="", TYPE="" ):
      self.BAREMODULE_ID=unicode(BAREMODULE_ID)
      self.ROC_ID=unicode(ROC_ID)
      self.SENSOR_ID=unicode(SENSOR_ID)
      self.TRANSFER_ID=TRANSFER_ID
      self.BUILTON=BUILTON
      self.BUILTBY=unicode(BUILTBY)
      self.COMMENT=unicode(COMMENT)
      self.LASTTEST_BAREMODULE_INSPECTION=LASTTEST_BAREMODULE_INSPECTION
      self.LASTTEST_CHIPS=unicode(LASTTEST_CHIPS)
      self.STATUS=unicode(STATUS)
      self.LABEL2D=unicode(LABEL2D)
      self.POWERCABLE=unicode(POWERCABLE)
      self.SIGNALCABLE=unicode(SIGNALCABLE)
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
  TBM1_ID=Unicode()
  TBM2_ID=Unicode()
  tbm1 = Reference(TBM1_ID, Tbm.TBM_ID)
  tbm2 = Reference(TBM2_ID, Tbm.TBM_ID)
  COMMENT = Unicode()
  TYPE = Unicode()
  STATUS=Unicode()
  LASTTEST_HDI=Int()
  def __init__(self,HDI_ID, TRANSFER_ID, COMMENT="", LASTTEST_HDI=0, STATUS="",TYPE="", TBM1_ID="", TBM2_ID=""):
    self.HDI_ID=unicode(HDI_ID)
    self.TRANSFER_ID=TRANSFER_ID
    self.COMMENT=unicode(COMMENT)
    self.LASTTEST_HDI=LASTTEST_HDI
    self.STATUS=unicode(STATUS)
    self.TYPE=unicode(TYPE)
    self.TBM1_ID=unicode(TBM1_ID)
    self.TBM2_ID=unicode(TBM2_ID)

          
class FullModule(object):
  __storm_table__ = "inventory_fullmodule"
  FULLMODULE_ID = Unicode(primary=True)
  BAREMODULE_ID =  Unicode()
  HDI_ID =  Unicode()
  TBM_ID =  Unicode()
  STATUS=Unicode()    
  TRANSFER_ID = Int()
  transfer = Reference(TRANSFER_ID, Transfer.TRANSFER_ID)
  tbm = Reference(TBM_ID, Tbm.TBM_ID)
  baremodule = Reference(BAREMODULE_ID, BareModule.BAREMODULE_ID)
  hdi = Reference(HDI_ID, Hdi.HDI_ID)
  BUILTON = DateTime()
  BUILTBY = Unicode()
  COMMENT = Unicode()
  LASTTEST_FULLMODULE=Int()

  def __init__(self,FULLMODULE_ID, BAREMODULE_ID, HDI_ID, TBM_ID, TRANSFER_ID, BUILTBY, BUILTON=datetime.now(), COMMENT="", STATUS="",LASTTEST_FULLMODULE=0):
      self.TBM_ID=unicode(TBM_ID)
      self.HDI_ID=unicode(HDI_ID)
      self.BAREMODULE_ID=unicode(BAREMODULE_ID)
      self.FULLMODULE_ID=unicode(FULLMODULE_ID)
      self.TRANSFER_ID=TRANSFER_ID
      self.COMMENT=unicode(COMMENT)
      self.BUILTON=BUILTON
      self.BUILTBY=unicode(BUILTBY)
      self.STATUS=unicode(STATUS)
      self.LASTTEST_FULLMODULE=LASTTEST_FULLMODULE        

#
# logbook
#
class Logbook(object):
      __storm_table__ = "logbook"
      ENTRY_ID = Int(primary=True)
      SESSION_ID=Int()
      session = Reference(SESSION_ID, Session.SESSION_ID)
      TEST_ROCS = Unicode()
      TEST_WAFERS = Unicode()      
      TEST_BATCHES = Unicode()
      TEST_TBMS = Unicode()
      TEST_HDIS = Unicode()
      TEST_SENSORS = Unicode()
      TEST_BAREMODULES = Unicode()
      TEST_FULLMODULES = Unicode()
      COMMENT=Unicode()
      ADDDATA_ID = Int()

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



class Test_Hdi(object):
      __storm_table__ = "test_hdi"
      TEST_ID = Int(primary=True)
      SESSION_ID=Int()
      session = Reference (SESSION_ID,Session.SESSION_ID)
      HDI_ID =  Unicode()
      hdi=Reference(HDI_ID, Hdi.HDI_ID)
      RESULT=Float()
      DATA_ID=Int()
      data=Reference(DATA_ID,Data.DATA_ID)
      def __init__(self,SESSION_ID,HDI_ID,RESULT,DATA_ID):
          self.SESSION_ID=SESSION_ID
          self.HDI_ID=unicode(HDI_ID)
          self.RESULT=float(RESULT)
          self.DATA_ID=DATA_ID


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
      V24 = Float()
      PHFAIL = Int()
      
      COMMENT = Unicode()
      def __init__(self,SESSION_ID, ROC_ID, RESULT, DATA_ID, V24, IANA, IDIGI, VDAC, DEFECTPIXELS, ADDRPIXELS, TRIMPIXELS, MASKPIXELS, NSIGPIXELS, NOISEPIXELS, THRESHOLDPIXELS, PHFAIL, COMMENT=""):
          self.SESSION_ID=SESSION_ID 
          self.ROC_ID=unicode(ROC_ID)
          self.RESULT=int(RESULT)
          self.DATA_ID=DATA_ID
          self.DEFECTPIXELS=int(DEFECTPIXELS)
          self.VDAC = float(VDAC)
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
      DATE = Int()
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
          self.DATE = int(DATE)
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
      DATE = Int()
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
          self.DATE = int(DATE)
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
      DATE = Int()
      COMMENT = Unicode()
      data=Reference(DATA_ID,Data.DATA_ID)
      def __init__(self,SESSION_ID,SENSOR_ID,RESULT,DATA_ID,DATE,TYPE="", COMMENT=""):
          self.SESSION_ID=SESSION_ID
          self.SENSOR_ID=unicode(SENSOR_ID)
          self.TYPE=unicode(TYPE)
          self.GRADE=unicode(GRADE)
          self.DATA_ID=DATA_ID
          self.DATE = int(DATE)
          self.RESULT=unicode(RESULT)
          self.COMMENT=unicode(COMMENT)
          self.DATE = int(DATE)

class Test_BareModuleInspection(object):
      __storm_table__ = "test_baremodule_inspection"
      TEST_ID = Int(primary=True)
      SESSION_ID=Int()
      session = Reference (SESSION_ID,Session.SESSION_ID)
      BAREMODULE_ID =  Unicode()
      baremodule=Reference(BAREMODULE_ID, BareModule.BAREMODULE_ID)
      RESULT = Unicode()
      DATA_ID=Int()
      DATE = Int()
      COMMENT = Unicode()
      data=Reference(DATA_ID,Data.DATA_ID)
      def __init__(self,SESSION_ID,BAREMODULE_ID,RESULT,DATA_ID,DATE,TYPE="", COMMENT=""):
          self.SESSION_ID=SESSION_ID
          self.BAREMODULE_ID=unicode(BAREMODULE_ID)
          self.TYPE=unicode(TYPE)
          self.GRADE=unicode(GRADE)
          self.DATA_ID=DATA_ID
          self.DATE = int(DATE)
          self.RESULT=unicode(RESULT)
          self.COMMENT=unicode(COMMENT)
          self.DATE = int(DATE)

class Test_BareModule_Chip(object):
      __storm_table__ = "test_baremodule_chip"
      TEST_ID = Int(primary=True)
      SESSION_ID=Int()
      session = Reference (SESSION_ID,Session.SESSION_ID)
      BAREMODULE_ID =  Unicode()
      CHIP_N = Int()
      DATE = Int()
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
      DATE = Int()
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
          self.DATE = int(DATE)
          self.SLOPE= float(SLOPE)
          self.TEMPERATURE = TEMPERATURE
          

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

BareModule.lasttest_baremodule_inspection = Reference(  BareModule.LASTTEST_BAREMODULE_INSPECTION, Test_BareModuleInspection.TEST_ID)
Hdi.lasttest_hdi = Reference(  Hdi.LASTTEST_HDI, Test_Hdi.TEST_ID)
Tbm.lasttest_tbm = Reference(  Tbm.LASTTEST_TBM, Test_Tbm.TEST_ID)
#FullModule.lasttest_fullmodule = Reference(  FullModule.LASTTEST_FULLMODULE, Test_FullModule.TEST_ID)

Logbook.adddata = Reference(Logbook.ADDDATA_ID,Data.DATA_ID)

#
# ne mancano ...
#
#Test_FullModuleSummary.fullmoduletest_t1 = Reference(Test_FullModuleSummary.FULLMODULETEST_T1,Test_FullModule.TEST_ID)
#Test_FullModuleSummary.fullmoduletest_t2 = Reference(Test_FullModuleSummary.FULLMODULETEST_T2,Test_FullModule.TEST_ID)
#Test_FullModuleSummary.fullmoduletest_t3 = Reference(Test_FullModuleSummary.FULLMODULETEST_T3,Test_FullModule.TEST_ID)

Test_FullModuleSummary.fullmoduletests =  ReferenceSet(Test_FullModuleSummary.TEST_ID,Test_FullModule.SUMMARY_ID)

FullModule.lasttest = Reference(FullModule.LASTTEST_FULLMODULE, Test_FullModuleSummary.TEST_ID)
FullModule.summaries = ReferenceSet(FullModule.FULLMODULE_ID, Test_FullModuleSummary.FULLMODULE_ID)
FullModule.tests = ReferenceSet(FullModule.FULLMODULE_ID, Test_FullModule.FULLMODULE_ID)
Test_FullModule.analyses = ReferenceSet(Test_FullModule.TEST_ID, Test_FullModuleAnalysis.FULLMODULETEST_ID
)
