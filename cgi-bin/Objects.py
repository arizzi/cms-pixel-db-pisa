#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
from datetime import *
cgitb.enable()

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
    ISSUED_DATE=datetime(1970,1,1)
    RECEIVED_DATE=date.today()
    STATUS=Unicode()
    COMMENT=Unicode()
    def __init__(self, SENDER,RECEIVER, ISSUED_DATE=datetime(1970,1,1), RECEIVED_DATE=date.today(), STATUS="ARRIVED", COMMENT=""):
        self.SENDER=unicode(SENDER)
        self.RECEIVER=unicode(RECEIVER)
        self.ISSUED_DATE=ISSUED_DATE
        self.RECEIVED_DATE=RECEIVED_DATE
        self.STATUS=unicode(STATUS)
        self.COMMENT=unicode(COMMENT)

#
# Session
#
class Session (object):
    __storm_table__ = "sessions"
    SESSION_ID=Int(primary=True)
    CENTER=Unicode()
    OPERATOR=Unicode()
    DATE=date.today()
    TYPE=Unicode()
    COMMENT=Unicode()
    def __init__(self,CENTER, OPERATOR,TYPE="TESTSESSION",DATE=date.today(), COMMENT=""):
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
  TRANSFER_ID = Int()
  transfer = Reference(TRANSFER_ID, Transfer.TRANSFER_ID)
  COMMENT = Unicode()
  STATUS=Unicode()
  LASTTEST_ROC=Int()
  def __init__(self,ROC_ID, TRANSFER_ID, COMMENT="",LASTTEST_ROC=0, STATUS=""):
      self.ROC_ID=unicode(ROC_ID)
      self.TRANSFER_ID=(TRANSFER_ID)
      self.COMMENT=unicode(COMMENT)
      self.LASTTEST_ROC = LASTTEST_ROC
      self.STATUS=unicode(STATUS)


class Sensor(object):
  __storm_table__ = "inventory_sensor"
  SENSOR_ID = Unicode(primary=True)
  TRANSFER_ID = Int()
  transfer = Reference(TRANSFER_ID, Transfer.TRANSFER_ID)
  COMMENT = Unicode()
  STATUS=Unicode()
  LASTTEST_SENSOR =Int()
  def __init__(self,SENSOR_ID,TRANSFER_ID, COMMENT="", LASTTEST_SENSOR=0, STATUS=""):
      self.SENSOR_ID=unicode(SENSOR_ID)
      self.TRANSFER_ID=(TRANSFER_ID)
      self.COMMENT=unicode(COMMENT)
      self.LASTTEST_SENSOR = LASTTEST_SENSOR
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
      print "III",internal
      rocc=Reference(internal, Roc.ROC_ID)
      return rocc
  sensor = Reference(SENSOR_ID, Sensor.SENSOR_ID)
  transfer = Reference(TRANSFER_ID, Transfer.TRANSFER_ID)
  BUILTON = date.today()
  BUILTBY = Unicode()
  COMMENT = Unicode()
  LASTTEST_BAREMODULE =Int()
  def getRoc(self,i):
      #
      # parse ROC_IDs to extract field # N
      #
      result =(self.ROC_ID.split(","))[i]
      return result
  def __init__(self,BAREMODULE_ID,ROC_ID,SENSOR_ID,TRANSFER_ID,  BUILTBY, BUILTON=date.today(),COMMENT="", LASTTEST_BAREMODULE=0, STATUS=""):
      self.BAREMODULE_ID=unicode(BAREMODULE_ID)
      self.ROC_ID=unicode(ROC_ID)
      self.SENSOR_ID=unicode(SENSOR_ID)
      self.TRANSFER_ID=TRANSFER_ID
      self.BUILTON=BUILTON
      self.BUILTBY=unicode(BUILTBY)
      self.COMMENT=unicode(COMMENT)
      self.LASTTEST_BAREMODULE=LASTTEST_BAREMODULE
      self.STATUS=unicode(STATUS)

      
  
  
class Hdi(object):
  __storm_table__ = "inventory_hdi"
  HDI_ID = Unicode(primary=True)
  TRANSFER_ID = Int()
  transfer = Reference(TRANSFER_ID, Transfer.TRANSFER_ID)
  COMMENT = Unicode()
  STATUS=Unicode()
  LASTTEST_HDI=Int()
  def __init__(self,HDI_ID, TRANSFER_ID, COMMENT="", LASTTEST_HDI=0, STATUS=""):
    self.HDI_ID=unicode(HDI_ID)
    self.TRANSFER_ID=TRANSFER_ID
    self.COMMENT=unicode(COMMENT)
    self.LASTTEST_HDI=LASTTEST_HDI
    self.STATUS=unicode(STATUS)

class Tbm(object):
  __storm_table__ = "inventory_tbm"
  TBM_ID = Unicode(primary=True)
  TRANSFER_ID = Int()
  transfer = Reference(TRANSFER_ID, Transfer.TRANSFER_ID)
  COMMENT = Unicode()
  STATUS=Unicode()
  LASTTEST_TBM=Int()
  def __init__(self,TBM_ID, TRANSFER_ID, COMMENT="", LASTTEST_TBM=0, STATUS=""):
      self.TBM_ID=unicode(TBM_ID)
      self.TRANSFER_ID=TRANSFER_ID
      self.COMMENT=unicode(COMMENT)
      self.LASTTEST_TBM=LASTTEST_TBM
      self.STATUS=unicode(STATUS)
          

     
class FullModule(object):
  __storm_table__ = "inventory_fullmodule"
  FULLMODULE_ID = Unicode(primary=True)
  BAREMODULE_ID =  Unicode()
  HDI_ID =  Unicode()
  TBM_ID =  Unicode()
  STATUS=Unicode()    
  TRANSFER_ID = Int()
  tbm = Reference(TBM_ID, Tbm.TBM_ID)
  baremodule = Reference(BAREMODULE_ID, BareModule.BAREMODULE_ID)
  hdi = Reference(HDI_ID, HDI_ID)
  BUILTON = date.today()
  BUILTBY = Unicode()
  COMMENT = Unicode()
  LASTTEST_FULLMODULE=Int()
  def __init__(self,FULLMODULE_ID, BAREMODULE_ID, HDI_ID, TBM_ID, TRANSFER_ID, BUILTBY, BUILTON=date.today(), COMMENT="", LASTTEST_FULLMODULE=0, STATUS=""):
      self.TBM_ID=unicode(TBM_ID)
      self.HDI_ID=unicode(HDI_ID)
      self.BAREMODULE_ID=unicode(BAREMODULE_ID)
      self.FULLMODULE_ID=unicode(FULLMODULE_ID)
      self.TRANSFER_ID=TRANSFER_ID
      self.COMMENT=unicode(COMMENT)
      self.LASTTEST_FULLMODULE=LASTTEST_FULLMODULE
      self.BUILTON=BUILTON
      self.BUILTBY=unicode(BUILTBY)
      self.STATUS=unicode(STATUS)
        

#
# logbook
#
class Logbook(object):
      __storm_table__ = "logbook"
      ENTRY_ID = Int(primary=True)
      SESSION_ID=Int()
      session = Reference(SESSION_ID, Session.SESSION_ID)
      TEST_ROCS = Unicode()
      TEST_TBMS = Unicode()
      TEST_HDIS = Unicode()
      TEST_SENSORS = Unicode()
      TEST_BAREMODULES = Unicode()
      TEST_FULLMODULES = Unicode()
      COMMENT=Unicode()
      ADDDATA_ID = Int()

#
# Data


class Data(object):
      __storm_table__ = "test_data"
      DATA_ID = Int(primary=True)
      URLs = Unicode()
      PFNs=Unicode()
      COMMENT=Unicode()

#
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

class Test_FullModule(object):
      __storm_table__ = "test_fullmodule"
      TEST_ID = Int(primary=True)
      SESSION_ID=Int()
      session = Reference (SESSION_ID,Session.SESSION_ID)
      FULLMODULE_ID =  Unicode()
      fullmodule=Reference(FULLMODULE_ID, FullModule.FULLMODULE_ID)
      RESULT=Float()
      DATA_ID=Int()
      data=Reference(DATA_ID,Data.DATA_ID)
      ROCSWORSEPERCENT=Float()
      NOISE=Unicode()
      TRIMMING =Unicode()
      PHCAL = Unicode()
      CURRENT1UA = Float()
      CURRENT2UA  = Float()
      CURRENT1501UA = Float() 
      CURRENT1502UA = Float()
      IVSLOPE  = Float()
      TEMPVALUE = Float() 
      TEMPERROR = Float()
      TCYCLVALUE = Float()
      TCYCLERROR = Float()
      COMMENT= Unicode()
      def __init__(self,FULLMODULE_ID,SESSION_ID,RESULT,DATA_ID,ROCSWORSEPERCENT,NOISE,TRIMMING,PHCAL,CURRENT1UA,CURRENT2UA,CURRENT1501UA,CURRENT1502UA,IVSLOPE,TEMPVALUE,TEMPERROR,TCYCLVALUE,TCYCLERROR,COMMENT):
            self.DATA_ID=DATA_ID
            self.SESSION_ID=SESSION_ID
            self.FULLMODULE_ID=unicode(FULLMODULE_ID)
            self.RESULT=RESULT
            self.ROCSWORSEPERCENT=ROCSWORSEPERCENT
            self.NOISE=unicode(NOISE)
            self.TRIMMING=unicode(TRIMMING)
            self.PHCAL=unicode(PHCAL)
            self.CURRENT1UA=CURRENT1UA
            self.CURRENT2UA=CURRENT2UA
            self.CURRENT1501UA=CURRENT1501UA
            self.CURRENT1502UA=CURRENT1502UA
            self.IVSLOPE=IVSLOPE
            self.TEMPVALUE=TEMPVALUE
            self.TEMPERROR=TEMPERROR
            self.TCYCLVALUE=TCYCLVALUE
            self.TCYCLERROR=TCYCLERROR
            self.COMMENT=unicode(COMMENT)





class Test_Tbm(object):
      __storm_table__ = "test_tmb"
      TEST_ID = Int(primary=True)
      SESSION_ID=Int()
      session = Reference (SESSION_ID,Session.SESSION_ID)
      TBM_ID =  Unicode()
      tbm=Reference(TBM_ID, Tbm.TBM_ID)
      RESULT=Float()
      DATA_ID=Int()
      data=Reference(DATA_ID,Data.DATA_ID)


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

class Test_Roc(object):
      __storm_table__ = "test_roc"
      TEST_ID = Int(primary=True)
      SESSION_ID=Int()
      session = Reference (SESSION_ID,Session.SESSION_ID)
      ROC_ID =  Unicode()
      roc=Reference(ROC_ID, Roc.ROC_ID)
      RESULT=Float()
      DATA_ID=Int()
      data=Reference(DATA_ID,Data.DATA_ID)


class Test_Sensor(object):
      __storm_table__ = "test_sensor"
      TEST_ID = Int(primary=True)
      SESSION_ID=Int()
      session = Reference (SESSION_ID,Session.SESSION_ID)
      SENSOR_ID =  Unicode()
      sensor=Reference(SENSOR_ID, Sensor.SENSOR_ID)
      RESULT=Float()
      DATA_ID=Int()
      data=Reference(DATA_ID,Data.DATA_ID)

#history
 
class History(object):
    __storm_table__ = "history"    
    HISTORY_ID = Int(primary=True)
    TYPE=Unicode()
    ID=Unicode()
    TARGET_TYPE=Unicode()
    TARGET_ID=Unicode()
    OPERATION=Unicode()
    DATE=date.today()
    COMMENT=Unicode()
    def __init__(self, TYPE, ID, TARGET_TYPE, TARGET_ID, OPERATION, DATE=date.today(), COMMENT=""):
        self.TYPE=unicode(TYPE)
        self.ID=unicode(ID)
        self.TARGET_TYPE=unicode(TARGET_TYPE)
        self.TARGET_ID=unicode(TARGET_ID)
        self.OPERATION=unicode(OPERATION)
        self.DATE=DATE
        self.COMMENT=unicode(COMMENT)
    
# References
Roc.lasttest_roc = Reference(  Roc.LASTTEST_ROC, Test_Roc.TEST_ID)
Sensor.lasttest_sensor = Reference(  Sensor.LASTTEST_SENSOR, Test_Sensor.TEST_ID)
BareModule.lasttest_baremodule = Reference(  BareModule.LASTTEST_BAREMODULE, Test_BareModule.TEST_ID)
Hdi.lasttest_hdi = Reference(  Hdi.LASTTEST_HDI, Test_Hdi.TEST_ID)
Tbm.lasttest_tbm = Reference(  Tbm.LASTTEST_TBM, Test_Tbm.TEST_ID)
FullModule.lasttest_fullmodule = Reference(  FullModule.LASTTEST_FULLMODULE, Test_FullModule.TEST_ID)
Logbook.adddata = Reference(Logbook.ADDDATA_ID,Data.DATA_ID)







 

 
