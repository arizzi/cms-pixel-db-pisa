from Objects import *
from MySQLdb import *
from storm.locals import *
import commands
import string
import subprocess
import os.path
import re

class PixelDBInterface(object) :

      def __init__(self, operator, center, datee =date.today() ) :
            self.operator = operator
            self.center =  center
            self.date = datee
            
      def connectToDB(self) :
            self.database = create_database("mysql://tester:pixels@cmspixel.pi.infn.it/prod_pixel")
            self.store = Store(self.database)
            
      def insertTransfer(self,transfer):
            self.store.add(transfer)
            self.store.commit()
            return transfer

      def insertData(self,transfer):
            self.store.add(transfer)
            self.store.commit()
            return transfer


      def insertSession(self,session):
            self.store.add(session)
            self.store.commit()
            return session
    
      def insertSensor(self,sensor) :
            if (self.isSensorInserted(sensor.SENSOR_ID) == True):
                  print "ERROR: sensor already inserted", sensor.SENSOR_ID
                  return None
            self.store.add(sensor)
            self.store.commit()
            # log in history
            self.insertHistory(type="NULL", id=0, target_type="SENSOR", target_id=sensor.SENSOR_ID, operation="INSERT", datee=date.today(), comment="NO COMMENT")
            return sensor
      
      def insertRoc (self, roc):
            if (self.isRocInserted(roc.ROC_ID) == True):
                  print "ERROR: roc already inserted", roc.ROC_ID
                  return None
            self.store.add(roc)
            self.store.commit()
            # log in history
            self.insertHistory(type="NULL", id=0, target_type="ROC", target_id=roc.ROC_ID, operation="INSERT", datee=date.today(), comment="NO COMMENT")
            return roc

      def insertTbm (self, tbm):
            if (self.isTbmInserted(tbm.TBM_ID) == True):
                  print "ERROR: tbm already inserted", tbm.TBM_ID
                  return None
            self.store.add(tbm)
            self.store.commit()
            # log in history
            self.insertHistory(type="NULL", id=0, target_type="TBM", target_id=tbm.TBM_ID, operation="INSERT", datee=date.today(), comment="NO COMMENT")
            return tbm

      def insertHdi (self, hdi):
            if (self.isHdiInserted(hdi.HDI_ID) == True):
                  print "ERROR: hdi already inserted", hdi.HDI_ID
                  return None
            self.store.add(hdi)
            self.store.commit()
            # log in history
            self.insertHistory(type="NULL", id=0, target_type="HDI", target_id=hdi.HDI_ID, operation="INSERT", datee=date.today(), comment="NO COMMENT")
            return hdi      
      

      def insertBatch (self, batch):
            if (self.isBatchInserted(batch.BATCH_ID) == True):
                  print "ERROR: batch already inserted", batch.BATCH_ID
                  return None
            self.store.add(batch)
            self.store.commit()
            # log in history
            self.insertHistory(type="NULL", id=0, target_type="BATCH", target_id=batch.BATCH_ID, operation="INSERT", datee=date.today(), comment="NO COMMENT")
            return batch      

      def insertWafer (self, wafer):
            if (self.isWaferInserted(wafer.WAFER_ID) == True):
                  print "ERROR: wafer already inserted", wafer.WAFER_ID
                  return None
            self.store.add(wafer)
            self.store.commit()
            # log in history
            self.insertHistory(type="NULL", id=0, target_type="WAFER", target_id=wafer.WAFER_ID, operation="INSERT", datee=date.today(), comment="NO COMMENT")
            return wafer      

      


      def joinObjects(self, arrayofrocids):
            return string.join(arrayofrocids,",")
      def splitObjects(self, pp):
            return string.split(pp,",")
#
#
#
      def insertBareModule(self, bm):
            #
            # to be used directly
            #
            #
            # check if all the objects are already in DB
            #
            if (self.canSensorBeUsed(bm.SENSOR_ID) == False):
                  print "ERROR: sensor not available", bm.SENSOR_ID
                  return None
            
            for i in self.splitObjects(bm.ROC_ID):
                  if (self.canRocBeUsed(i) == False):
                        print "ERROR: roc not available", i
                        return None
            #            
            self.setSensorStatus(bm.SENSOR_ID,"USED")
            for i in self.splitObjects(bm.ROC_ID):
                  self.setRocStatus(i,"USED")
            self.store.add(bm)
            self.store.commit()
            # log in history sensor
            self.insertHistory(type="SENSOR", id=bm.SENSOR_ID, target_type="BAREMODULE", target_id=bm.BAREMODULE_ID, operation="ASSEMBLE", datee=date.today(), comment="NO COMMENT")
            # log in history rocs
            for i in self.splitObjects(bm.ROC_ID):
                  self.insertHistory(type="ROC", id=i, target_type="BAREMODULE", target_id=bm.BAREMODULE_ID, operation="ASSEMBLE", datee=date.today(), comment="NO COMMENT")
            
            return bm

            
      def assembleBareModule(self, baremodule_id, roc_ids,  sensor_id, builtby, transfer_id,COMMENT="", LASTTEST_BAREMODULE=0, STATUS="",LABEL2D="",POWERCABLE="", SIGNALCABLE="", TYPE=""):
            newbm = BareModule(BAREMODULE_ID=baremodule_id, ROC_ID=self.joinObjects(roc_ids), SENSOR_ID=sensor_id, TRANSFER_ID=transfer_id,BUILTBY=builtby, COMMENT=COMMENT, LASTTEST_BAREMODULE=LASTTEST_BAREMODULE, STATUS=STATUS,LABEL2D=LABEL2D,POWERCABLE=POWERCABLE, SIGNALCABLE=SIGNALCABLE, TYPE=TYPE)
            bm = self.insertBareModule(newbm)
            if (bm is None):
                 print"<br>Error inserting BAREMODULE"
            return bm
            
            
      def insertHistory(self, type, id, target_type, target_id, operation, datee=date.today(), comment=""):
            newHist=History(type, id, target_type, target_id, operation, datee, comment)
            self.store.add(newHist)
            self.store.commit()            
            return newHist


      def insertFullModule(self,fm):
            #
            # check if all the objects are already in DB
            #
            if (self.canBareModuleBeUsed(fm.BAREMODULE_ID) == False):
                  print "ERROR: baremodule not available", fm.BAREMODULE_ID
                  return None
	    if (self.canTbmBeUsed(fm.TBM_ID) == False):
                  print "ERROR: tbm not available",fm.TBM_ID
                  return None
	    if (self.canHdiBeUsed(unicode(fm.HDI_ID)) == False):
                  print "ERROR: hdi not available",fm.HDI_ID
                  return None

            #
            self.setBareModuleStatus(fm.BAREMODULE_ID,"USED")
            self.setHdiStatus(fm.TBM_ID,"USED")
            self.setTbmStatus(fm.HDI_ID,"USED")
            self.store.add(fm)
            self.store.commit()
            # log in history 
            self.insertHistory(type="BAREMODULE", id=fm.BAREMODULE_ID, target_type="FULLMODULE", target_id=fm.FULLMODULE_ID, operation="ASSEMBLE", datee=date.today(), comment="NO COMMENT")
            self.insertHistory(type="HDI", id=fm.HDI_ID, target_type="FULLMODULE", target_id=fm.FULLMODULE_ID, operation="ASSEMBLE", datee=date.today(), comment="NO COMMENT")
            self.insertHistory(type="TBM", id=fm.TBM_ID, target_type="FULLMODULE", target_id=fm.FULLMODULE_ID, operation="ASSEMBLE", datee=date.today(), comment="NO COMMENT")
            return fm

            


      def assembleFullModule(self, fullmodule_id, baremodule_id, tbm_id, hdi_id,  builtby, transfer_id,builton=date.today(),comment=""):
            newfm = FullModule(FULLMODULE_ID=fullmodule_id, BAREMODULE_ID=baremodule_id, HDI_ID=hdi_id, TBM_ID=tbm_id,TRANSFER_ID=transfer_id, BUILTBY=builtby, BUILTON=builton, COMMENT=comment)
            self.insertFullModule(newfm)
            return newfm
            
#
# check methods 
#
      def isSensorInserted(self, sensor_id):
            temp=unicode(sensor_id)
            aa = self.store.find(Sensor, Sensor.SENSOR_ID==unicode(temp)).one()
            return aa is not None

      def isBatchInserted(self, batch_id):
            temp=unicode(batch_id)
            aa = self.store.find(Batch, Batch.BATCH_ID==unicode(temp)).one()
            return aa is not None

      def isWaferInserted(self, wafer_id):
            temp=unicode(wafer_id)
            aa = self.store.find(Wafer, Wafer.WAFER_ID==unicode(temp)).one()
            return aa is not None




      def isRocInserted(self, roc_id):
            temp=unicode(roc_id)
            aa = self.store.find(Roc, Roc.ROC_ID==temp).one()
            return aa is not None

      def isTbmInserted(self, tbm_id):
            temp=unicode(tbm_id)
            aa = self.store.find(Tbm, Tbm.TBM_ID==temp).one()
            return aa is not None

      def isHdiInserted(self, hdi_id):
            aa = self.store.find(Hdi, Hdi.HDI_ID==hdi_id).one()
            return aa is not None

      def isBareModuleInserted(self, BareModule_id):
            temp=unicode(BareModule_id)
            aa = self.store.find(BareModule, BareModule.BAREMODULE_ID==temp).one()
            return aa is not None

      def isFullModuleInserted(self, FullModule_id):
            aa = self.store.find(FullModule, FullModule.FULLMODULE_ID==FullModule_id).one()
            return aa is not None

      def searchFullModuleTestSummaryByDirName(self, dirname):
            temp=unicode('file:'+dirname)
            result = self.store.find((Test_FullModuleSummary, Data),
                                Test_FullModuleSummary.DATA_ID == Data.DATA_ID,
                                Data.PFNs.like(temp))

            aa=[(session) for session,data in result]

#            print "AAAA ",aa[0].TEST_ID
            if (len(aa) == 0):
                      return None
            else:
                      return aa[0]


#
# check if already used
#
      def canSensorBeUsed(self, sensor_id):
            if (self.isSensorInserted(sensor_id) == False):
                  return False
            if ((self.getSensor(sensor_id)).STATUS == "USED" ):
                  return False
            if (((self.getSensor(sensor_id)).transfer).STATUS != "ARRIVED"):
                  return False
            return True
            
      def canRocBeUsed(self, roc_id):
            if (roc_id == ''):
                  return True
            if (self.isRocInserted(roc_id) == False):
                  return False
            print "ROC IDDDDDDD",roc_id 
            if ((self.getRoc(roc_id)).STATUS == "USED" ):
                  return False
            if (((self.getRoc(roc_id)).transfer).STATUS != "ARRIVED"):
                  return False
            return True

      def canBareModuleBeUsed(self, baremodule_id):
            if (self.isBareModuleInserted(baremodule_id) == False):
                  return False
            if ((self.getBareModule(baremodule_id)).STATUS == "USED" ):
                  return False
            if (((self.getBareModule(baremodule_id)).transfer).STATUS != "ARRIVED"):
                  return False
            return True

      def canFullModuleBeUsed(self, fullmodule_id):
            if (self.isFullModuleInserted(fullmodule_id) == False):
                  return False
            if ((self.getFullModule(fullmodule_id)).STATUS == "USED" ):
                  return False
            if (((self.getFullModule(fullmodule_id)).transfer).STATUS != "ARRIVED"):
                  return False
            return True

      def canHdiBeUsed(self, hdi_id):
            if (self.isHdiInserted(hdi_id) == False):
                  return False
            if ((self.getHdi(hdi_id)).STATUS == "USED" ):
                  return False
            if (((self.getHdi(hdi_id)).transfer).STATUS != "ARRIVED"):
                  return False
            return True

      def canTbmBeUsed(self, tbm_id):
            if (self.isTbmInserted(tbm_id) == False):
                  return False
            if ((self.getTbm(tbm_id)).STATUS == "USED" ):
                  return False
            if (((self.getTbm(tbm_id)).transfer).STATUS != "ARRIVED"):
                  return False
            return True
      

           
#
# set used
#
      def setSensorStatus(self, sensor_id,status):
           if (self.canSensorBeUsed(sensor_id)):
                 (self.getSensor(sensor_id)).STATUS = unicode(status)
                 self.store.commit()                 
                 return True
           return False
     
      def setHdiStatus(self, hdi_id,status):
           if (self.canHdiBeUsed(hdi_id)):
                 (self.getHdi(hdi_id)).STATUS = unicode(status)
                 self.store.commit()                 
                 return True
           return False
           
      def setTbmStatus(self, tbm_id,status):
           if (self.canTbmBeUsed(tbm_id)):
                 (self.getTbm(tbm_id)).STATUS = unicode(status)
                 self.store.commit()                 
                 return True
           return False

      def setRocStatus(self, roc_id,status):
           if roc_id == '' : 
                 return True
	   if (self.canRocBeUsed(roc_id)):
                 (self.getRoc(roc_id)).STATUS = unicode(status)
                 self.store.commit()                 
                 return True
           return False
      def setFullModuleStatus(self, fullmodule_id,status):
           if (self.canFullModuleBeUsed(fullmodule_id)):
                 (self.getFullModule(fullmodule_id)).STATUS = unicode(status)
                 self.store.commit()                 
                 return True
           return False
      def setBareModuleStatus(self, baremodule_id,status):
           if (self.canBareModuleBeUsed(baremodule_id)):
                 (self.getBareModule(baremodule_id)).STATUS = unicode(status)
                 self.store.commit()                 
                 return True
           return False

     
# get methods
#
      def getSensor(self, sensor_id):
            temp=unicode(sensor_id)
            aa = self.store.find(Sensor, Sensor.SENSOR_ID==temp).one()
            return aa

      def getRoc(self, roc_id):
            temp=unicode(roc_id)
            aa = self.store.find(Roc, Roc.ROC_ID==temp).one()
            return aa

      def getTbm(self, tbm_id):
            temp=unicode(tbm_id)
            aa = self.store.find(Tbm, Tbm.TBM_ID==temp).one()
            return aa

      def getHdi(self, hdi_id):
            aa = self.store.find(Hdi, Hdi.HDI_ID==hdi_id).one()
            return aa

      def getBareModule(self, BareModule_id):
            temp=unicode(BareModule_id)
            aa = self.store.find(BareModule, BareModule.BAREMODULE_ID==temp).one()
            return aa

      def getFullModule(self, FullModule_id):
            aa = self.store.find(FullModule, FullModule.FULLMODULE_ID==FullModule_id).one()
            return aa

      def getTransfer(self, id):
            aa = self.store.find(Transfer, Transfer.TRANSFER_ID==id).one()
            return aa

      def getData(self, id):
            aa = self.store.find(Data, Data.DATA_ID==id).one()
            return aa


#
# get test
#

      def getFullModuleTestWithCkSumAndTimestamp(self, FullModule_id, CKSUM, TEMPNOMINAL,TIMESTAMP):
            aa = self.store.find(Test_FullModule, Test_FullModule.FULLMODULE_ID == unicode(FullModule_id), Test_FullModule.CKSUM == unicode(CKSUM), Test_FullModule.TEMPNOMINAL == unicode(TEMPNOMINAL),Test_FullModule.TIMESTAMP==unicode(TIMESTAMP)).one()
            return aa

#
# transfer
#

      def transferSensor(self, sensor_id, SENDER, RECEIVER, ISSUED_DATE=datetime(1970,1,1), RECEIVED_DATE=date.today(), STATUS="", COMMENT=""):
            #
            # moves only an EXISTING sensor
            #
            aa = self.getSensor(sensor_id)
            if (aa is None):
                  print "Trying to transfer a non existing sensor ", sensor_id
                  return None
            t = self.insertTransfer(Transfer(SENDER=SENDER, RECEIVER=RECEIVER, ISSUED_DATE=ISSUED_DATE, RECEIVED_DATE=RECEIVED_DATE, STATUS="SHIPPED", COMMENT=COMMENT))
            aa.TRANSFER_ID=t.TRANSFER_ID
            # log in history
            self.insertHistory(type="TRANSFER", id=t.TRANSFER_ID, target_type="SENSOR", target_id=aa.SENSOR_ID, operation="TRASFER", datee=date.today(), comment="NO COMMENT")
            self.store.commit()
            return aa

      def receiveTransfer(self,transferid):
            aa = self.getTransfer(transferid)
            if (aa is None):
                  return None
            if (aa.STATUS != unicode("SHIPPED")):
                  return None
            aa.STATUS = unicode("ARRIVED")
            return transferid
            

            

      def transferTbm(self, tbm_id, SENDER, RECEIVER, ISSUED_DATE=datetime(1970,1,1), RECEIVED_DATE=date.today(), STATUS="", COMMENT=""):
            #
            # moves only an EXISTING tbm
            #
            aa = self.getTbm(tbm_id)
            if (aa is None):
                  print "Trying to transfer a non existing tbm ", tbm_id
                  return None
            t = self.insertTransfer(Transfer(SENDER=SENDER, RECEIVER=RECEIVER, ISSUED_DATE=ISSUED_DATE, RECEIVED_DATE=RECEIVED_DATE, STATUS=STATUS, COMMENT=COMMENT))
            aa.TRANSFER_ID=t.TRANSFER_ID
            # log in history
            self.insertHistory(type="TRANSFER", id=t.TRANSFER_ID, target_type="TBM", target_id=aa.TBM_ID, operation="TRASFER", datee=date.today(), comment="NO COMMENT")
            self.store.commit()
            return aa

      def transferHdi(self, hdi_id, SENDER, RECEIVER, ISSUED_DATE=datetime(1970,1,1), RECEIVED_DATE=date.today(), STATUS="", COMMENT=""):
            #
            # moves only an EXISTING hdi
            #
            aa = self.getHdi(hdi_id)
            if (aa is None):
                  print "Trying to transfer a non existing hdi ", hdi_id
                  return None
            t = self.insertTransfer(Transfer(SENDER=SENDER, RECEIVER=RECEIVER, ISSUED_DATE=ISSUED_DATE, RECEIVED_DATE=RECEIVED_DATE, STATUS=STATUS, COMMENT=COMMENT))
            aa.TRANSFER_ID=t.TRANSFER_ID
            # log in history
            self.insertHistory(type="TRANSFER", id=t.TRANSFER_ID, target_type="HDI", target_id=aa.HDI_ID, operation="TRASFER", datee=date.today(), comment="NO COMMENT")
            self.store.commit()
            return aa
      def transferRoc(self, roc_id, SENDER, RECEIVER, ISSUED_DATE=datetime(1970,1,1), RECEIVED_DATE=date.today(), STATUS="", COMMENT=""):
            #
            # moves only an EXISTING roc
            #
            aa = self.getRoc(roc_id)
            if (aa is None):
                  print "Trying to transfer a non existing roc ", roc_id
                  return None
            t = self.insertTransfer(Transfer(SENDER=SENDER, RECEIVER=RECEIVER, ISSUED_DATE=ISSUED_DATE, RECEIVED_DATE=RECEIVED_DATE, STATUS=STATUS, COMMENT=COMMENT))
            aa.TRANSFER_ID=t.TRANSFER_ID
            # log in history
            self.insertHistory(type="TRANSFER", id=t.TRANSFER_ID, target_type="ROC", target_id=aa.ROC_ID, operation="TRASFER", datee=date.today(), comment="NO COMMENT")
            self.store.commit()
            return aa
      def transferFullModule(self, fullmodule_id, SENDER, RECEIVER, ISSUED_DATE=datetime(1970,1,1), RECEIVED_DATE=date.today(), STATUS="", COMMENT=""):
            #
            # moves only an EXISTING fullmodule
            #
            aa = self.getFullModule(fullmodule_id)
            if (aa is None):
                  print "Trying to transfer a non existing fullmodule ", fullmodule_id
                  return None
            t = self.insertTransfer(Transfer(SENDER=SENDER, RECEIVER=RECEIVER, ISSUED_DATE=ISSUED_DATE, RECEIVED_DATE=RECEIVED_DATE, STATUS=STATUS, COMMENT=COMMENT))
            aa.TRANSFER_ID=t.TRANSFER_ID
            # log in history
            self.insertHistory(type="TRANSFER", id=t.TRANSFER_ID, target_type="FULLMODULE", target_id=aa.FULLMODULE_ID, operation="TRASFER", datee=date.today(), comment="NO COMMENT")
            self.store.commit()
            return aa
      def transferBareModule(self, baremodule_id, SENDER, RECEIVER, ISSUED_DATE=datetime(1970,1,1), RECEIVED_DATE=date.today(), STATUS="", COMMENT=""):
            #
            # moves only an EXISTING baremodule
            #
            aa = self.getBareModule(baremodule_id)
            if (aa is None):
                  print "Trying to transfer a non existing baremodule ", baremodule_id
                  return None
            t = self.insertTransfer(Transfer(SENDER=SENDER, RECEIVER=RECEIVER, ISSUED_DATE=ISSUED_DATE, RECEIVED_DATE=RECEIVED_DATE, STATUS=STATUS, COMMENT=COMMENT))
            aa.TRANSFER_ID=t.TRANSFER_ID
            # log in history
            self.insertHistory(type="TRANSFER", id=t.TRANSFER_ID, target_type="BAREMODULE", target_id=aa.BAREMODULE_ID, operation="TRASFER", datee=date.today(), comment="NO COMMENT")
            self.store.commit()
            return aa
#
#
# TESTS
#
      def insertFullModuleTestSession(self,fms):
            if (self.isFullModuleInserted(fms.FULLMODULE_ID) == False):
                  print " Cannot insert a test on a not existing FM "
                  return None
            self.store.add(fms)
            self.store.commit()
            # log in history
            self.insertHistory(type="TEST_FMSession", id=fms.TEST_ID, target_type="FULLMODULE", target_id=fms.FULLMODULE_ID, operation="TEST", datee=date.today(), comment="NO COMMENT")
            return fms

      def insertFullModuleTestSummary(self,fms):
            if (self.isFullModuleInserted(fms.FULLMODULE_ID) == False):
                  print " Cannot insert a test on a not existing FM "
                  return None
            self.store.add(fms)
            self.store.commit()
            # log in history
            self.insertHistory(type="TEST_FMSummary", id=fms.TEST_ID,target_type="FULLMODULE", target_id=fms.FULLMODULE_ID, operation="TEST", datee=date.today(), comment="NO COMMENT")
            return fms

      def insertFullModuleTestAnalysis(self,fms):
            if (self.isFullModuleInserted(fms.FULLMODULE_ID) == False):
                  print " Cannot insert a test on a not existing FM "
                  return None
            self.store.add(fms)
            self.store.commit()
            # log in history
            self.insertHistory(type="TEST_FMAnalysis", id=fms.TEST_ID, target_type="FULLMODULE", target_id=fms.FULLMODULE_ID, operation="TEST", datee=date.today(), comment="NO COMMENT")
            return fms

            


      
      def insertFullModuleTest(self, test_fm):
            #
            # first check that the module exists
            #
            if (self.isFullModuleInserted(test_fm.FULLMODULE_ID) == False):
                  print " Cannot insert a test on a not existing FM "
                  return None
            self.store.add(test_fm)
            self.store.commit()
            # log in history
            self.insertHistory(type="TEST_FM", id=test_fm.TEST_ID, target_type="FULLMODULES", target_id=test_fm.TEST_ID, operation="TEST", datee=date.today(), comment="NO COMMENT")
            return test_fm

      def insertBareModuleTest(self, test_bm):
            #
            # first check that the module exists
            #
            if (self.isBareModuleInserted(test_bm.BAREMODULE_ID) == False):
                  print " Cannot insert a test on a not existing BM "
                  return None
            self.store.add(test_bm)
            self.store.commit()
            (self.getBareModule(test_bm.BAREMODULE_ID)).LASTTEST_BAREMODULE =  test_bm.TEST_ID
            self.store.commit()
            # log in history
            self.insertHistory(type="TEST_BM", id=test_bm.TEST_ID, target_type="BAREMODULE", target_id=test_bm.BAREMODULE_ID, operation="TEST", datee=date.today(), comment="NO COMMENT")
            return test_bm

      def insertSensorTest(self, test):
            #
            # first check that the module exists
            #
            if (self.isSensorInserted(test.SENSOR_ID) == False):
                  print " Cannot insert a test on a not existing S "
                  return None
            self.store.add(test)
            self.store.commit()
            (self.getSensor(test.SENSOR_ID)).LASTTEST_SENSOR =  test.TEST_ID
            self.store.commit()
            # log in history
            self.insertHistory(type="TEST_S", id=test.TEST_ID, target_type="SENSOR", target_id=test.SENSOR_ID, operation="TEST", datee=date.today(), comment="NO COMMENT")
            return test

      def insertHdiTest(self, test):
            #
            # first check that the module exists
            #

            if (self.isHdiInserted(test.HDI_ID) == False):
                  print " Cannot insert a test on a not existing HDI "
                  return None
            self.store.add(test)
            self.store.commit()
            (self.getHdi(test.HDI_ID)).LASTTEST_HDI =  test.TEST_ID
            self.store.commit()
            # log in history
            self.insertHistory(type="TEST_HDI", id=test.TEST_ID, target_type="HDI", target_id=test.HDI_ID, operation="TEST", datee=date.today(), comment="NO COMMENT")
            return test


      def insertTbmTest(self, test):
            #
            # first check that the module exists
            #
            if (self.isTbmInserted(test.TBM_ID) == False):
                  print " Cannot insert a test on a not existing TBM "
                  return None
            self.store.add(test)
            self.store.commit()
            (self.getTbm(test.TBM_ID)).LASTTEST_TBM =  test.TEST_ID
            self.store.commit()
            # log in history
            self.insertHistory(type="TEST_TBM", id=test.TEST_ID, target_type="TBM", target_id=test.TBM_ID, operation="TEST", datee=date.today(), comment="NO COMMENT")
            return test

      def insertRocTest(self, test):
            #
            # first check that the module exists
            #
            if (self.isInserted(test.ROC_ID) == False):
                  print " Cannot insert a test on a not existing ROC "
                  return None
            self.store.add(test)
            self.store.commit()
            (self.getRoc(test.ROC_ID)).LASTTEST_ROC =  test.TEST_ID
            self.store.commit()
            # log in history
            self.insertHistory(type="TEST_ROC", id=test.TEST_ID, target_type="ROC", target_id=test.ROC_ID, operation="TEST", datee=date.today(), comment="NO COMMENT")
            return test


#
# parses files (see '/afs/cern.ch/user/s/starodum/public/moduleDB/M1215-080320.09:34/T-10a/summaryTest.txt'
#
      def insertTestFullModuleDir(self,dir,sessionid,overwritemodid=0):
            #
            # tries to open a standard dir, as in the previous above
            # searches for summaryTest.txt inside + tars the dir in add_data
            #
            fileName = dir
            #
            # run php on it
            #

#
# run fulltestinfo to check whether this is new or not
#

            fulltestinfo = '/home/robot/cgi-bin/fulltestinfo.sh'

            command = str(fulltestinfo+" "+dir)

#            out = subprocess.check_output(["ls", dir])

            ppp = subprocess.Popen(fulltestinfo+" "+dir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            
            retval = ppp.wait()

            timestamp=0
            modulename='null'
            tempnominal2=0
            ck='null'

            if (retval == 0):
                  fileContent = []
                  
                  line = ppp.stdout.readlines()[0]
                  
                  line = line.rstrip(os.linesep)
                  
                  
                  
                  (timestamp,modulename, tempnominal2,ck) = line.split(" ")
            
            else:
# I try to get the same stuff from the dir name
                  fields = dir.split("/")
                  tempnominal2 = fields[-1]
                  modulename = fields[-2]
                  timestamp = 0
                  ck='null'
            

            #
            # check if this already exixts
            #

            print "asking for a module test with" ,modulename, ck, tempnominal2,timestamp

            ttt = self.getFullModuleTestWithCkSumAndTimestamp(modulename, ck, tempnominal2,timestamp)

            if (ttt is None) :
                  print "NEW MODULE TEST"
            else:
                  print "OLD MODULE TEST"

            p = subprocess.Popen("php prodTable.php "+fileName, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            print "FILE IS  "+fileName
            retval = p.wait()
            if (retval!=0):
                  return None
            fileContent = []
#
# set initially
#
            ModuleNumber=0
            Grade=0
            isThermalCycling=0
            TThermalCycling=0
            eTThermalCycling=0

            for line in p.stdout.readlines():
                  fields = (line.strip()).split(" ")
                  print "DEBUG ",fields
                  #
                  # real parsing
                  #                  
                  if (fields[0] == 'module' and len (fields)>1):
                        ModuleNumber = fields[1]
                  if (fields[0] == 'deadpi'):
                        DeadPixels=string.join(fields[1:]," ")
                              
                  if (fields[0] == 'mask'):
                        MaskPixels=string.join(fields[1:]," ")
                    


                  if (fields[0] == 'bump'):
                        BumpPixels=string.join(fields[1:]," ")


                  if (fields[0] == 'trim'):
                        TrimPixels=string.join(fields[1:]," ")


                  if (fields[0] == 'add'):
                        AddressPixels=string.join(fields[1:]," ")

                  if (fields[0] == 'noisy'):
                      NoisyPixels=string.join(fields[1:]," ")

                  if (fields[0] == 'thres'):
                        TreshPixels=string.join(fields[1:]," ")

                  if (fields[0] == 'gain'):
                       GainPixels=string.join(fields[1:]," ")
                    
                  if (fields[0] == 'pedestal'):
                       PedPixels=string.join(fields[1:]," ")

                  if (fields[0] == 'parameter1'):
                       ParPixels=string.join(fields[1:]," ")

                  if (fields[0] == 'finalGrade' and len(fields) >1 ):
                       FinalGrade = fields[1]
                  if (fields[0] == 'fullGrade'  and len (fields)>1):
                      FulltestGrade = fields[1]
                  if (fields[0] == 'grade'  and len (fields)>1):
                        Grade = fields[1]
                  if (fields[0] == 'shortGrade'  and len (fields)>1):
                        ShorttestGrade = fields[1]

                  if (fields[0] == 'rocs'):
                        RocDefects = string.join(fields[1:]," ")


                  if (fields[0] == 'date'):
                        Date = string.join(fields[1:]," ")
                  if (fields[0] == 'trimming' and len(fields)>1):
                        isTrimming = fields[1]
                  if (fields[0] == 'phcal'):
                        isphCal = string.join(fields[1:]," ")

                  if (fields[0] == 'noise'  and len (fields)>1):
                       NOISE = fields[1]
                  if (fields[0] == 'iv150'):
                      if (len(fields) >1):
                        I150 = fields[1]
                      else:
                        I150=0
                  if (fields[0] == 'iv150n2'):
                      if (len(fields) >1):
                        I1502 = fields[1]
                      else:
                         I1502=0   
                  if (fields[0] == 'current' ):
                       if (len(fields) >1):
                            Current = fields[1]
                       else:
                            Current=0
                  if (fields[0] == 'currentn2' ):
                      if (len(fields) >1):
                            Current2 = fields[1]
                      else:
                            Current2=0

                  if (fields[0] == 'com'):
                        if (len(fields) >1):
                           Comment=  fields[1]
                        else:
                              Comment=""
                
                  if (fields[0] == 'slope'):
                      if (len(fields) >1):
                            I150I100 = fields[1]
                      else:
                             I150I100 = 0
                  if (fields[0] == 'temp'):
                      Temp = fields[1]
                  if (fields[0] == 'etemp'):
                      eTemp = fields[1]
 
                  if (fields[0]=='tcy'  and len (fields)>1):
                      isThermalCycling=fields[1]
                  if (fields[0]=='tcycl'  and len (fields)>1):
                      TThermalCycling=fields[1]

                  if (fields[0]=='etcycl'  and len (fields)>1):
                      eTThermalCycling=fields[1]

                  if (fields[0] == 'mount'  and len (fields)>1):
                      position=fields[1]
                  if (fields[0] == 'testN'):
                      TestNumber=fields[1]


            #
            # create a data_id
            #
            data = Data(PFNs="file:"+dir)
            pp = self.insertData(data)
            if (pp is None):
                print"<br>Error inserting data"
                return None
            #
            # here I need to invent FM_ID otherwise the test cannot be inserted
            #
            if (overwritemodid ==0):
                  ppp=ModuleNumber
            else:
                  ppp=overwritemodid

            #
            # try and refuse inserting 
            #
            if (DeadPixels != '-' and Current != '-'):
                  print "HERE"
                  #
                  # new version, splitting in session, summary, test, analysis
                  #

                  # step #1 : create a fullmodulesession with an empty data
                  data1 = Data()
                  pp = self.insertData(data1)
                  if (pp is None):
                        print"<br>Error inserting data"
                        return None

                  fmsession = Test_FullModuleSession(DATA_ID=data1.DATA_ID,SESSION_ID=sessionid,FULLMODULE_ID=unicode(ppp))

                  pp=self.insertFullModuleTestSession(fmsession)
                  if pp is None:
                        print "ERRORE FMSESSION", fmsession.TEST_ID

                  # step #2 : create a test
                  data2 = Data(PFNs = "file:"+dir)
                  pp = self.insertData(data2)
                  if (pp is None):
                        print"<br>Error inserting data"
                        return None

                  TempNominal = tempnominal2


                  if (ttt is None):
                        t = Test_FullModule(SESSION_ID=fmsession.TEST_ID,
                        FULLMODULE_ID=ppp,
                                            DATA_ID = data2.DATA_ID,
                                            TEMPNOMINAL=unicode(TestNumber),
                                            COLDBOX="dummy",COLDBOX_SLOT="dummy",CKSUM=ck,TIMESTAMP=timestamp,
                                            RESULT = "n/a")

                        pp=self.insertFullModuleTest(t)
                        if pp is None:
                                                  print "ERRORE FMTEST"
                  
                  else:
                        t=ttt

                        

                  #
                  # step # 3: all the rest gos into an analysis
                        
                  fmanalysis = Test_FullModuleAnalysis(FULLMODULE_ID=ppp, DATA_ID=data.DATA_ID,FULLMODULETEST_ID=t.TEST_ID,
                   GRADE=Grade,
                   HOSTNAME="dummy",
                   DEADPIXELS=DeadPixels,
                   MASKEDPIXELS=MaskPixels,
                   BUMPDEFPIXELS=BumpPixels,
                   TRIMDEFPIXELS=TrimPixels,
                   ADDRESSDEFPIXELS=AddressPixels,
                   NOISYPIXELS=NoisyPixels,
                   THRESHDEFPIXELS=TreshPixels,
                   GAINDEFPIXELS=GainPixels,
                   PEDESTALDEFPIXELS=PedPixels,
                   PAR1DEFPIXELS=ParPixels,
                   I150=I150,
                   I150_2=I1502,
                   CURRENT=Current,CURRENT_2=Current2,
                   CYCLING=isThermalCycling,
                   TEMPVALUE=Temp,
                   TEMPERROR=eTemp,
                   TCYCLVALUE=TThermalCycling,
                        TCYCLERROR=eTThermalCycling,
                        MACRO_VERSION="dummyV0.0")
                  
                  print "ECCOMI" 
                  
                  rr = self.insertFullModuleTestAnalysis(fmanalysis)
                  if (rr is None):
                        print"<br>Error inserting test FM"
                        return None
                  



                  

                  #
                  #                create or search a session, based on dirname
                  #

                  path = os.path.abspath(os.path.join(os.path.dirname(dir),".."))

                  print " ECCO CHE PROVO A TROVARE IL SUMMARY", path

                  summ = self.searchFullModuleTestSummaryByDirName(path)
                  
                  if (summ is None):
                        print "create new FMSummary"
                        dataS = Data(PFNs = 'file:'+path)
                        pp = self.insertData(dataS)
                        
                        summary = Test_FullModuleSummary(FULLMODULE_ID=ppp,DATA_ID=dataS.DATA_ID)
                        pp = self.insertFullModuleTestSummary(summary)
                  else:
                        summary = summ
                  print " SUMM ", summ
                  #
                  # fill the correct one
                  #
                  if (TestNumber == 'T+17a'):
                        summary.FULLMODULETEST_T1 = t.TEST_ID
                  elif(TestNumber == 'T-10a'):
                        summary.FULLMODULETEST_T2 = t.TEST_ID
                  elif(TestNumber == 'T-10b'):
                        print "RIEMPIO ",t.TEST_ID

                        summary.FULLMODULETEST_T3 = t.TEST_ID
                  else:
                        print " CANNOT FILL SUMMARY, SINCE TEMP IS ",TestNumber
                  self.store.commit()
            
                  return rr     
            
             
            else:
                  print " Discarding bad result"
                  self.store.commit()
                              
                  return None



#
# loads IV curves
#

#
# define a general purpose parser, which parses things like
#A = B # this is a comment
#
      def textFileParser(self,filename):
            debug = True

            COMMENT_CHAR = '#'
            OPTION_CHAR =  ' '
            options = {}
            f = open(filename)
            for line in f:
                  if (debug == True):
                        print "line ...",line
                  
                  # First, remove comments:
                  if COMMENT_CHAR in line:
                        # split on comment char, keep only the part before
                        line, comment = line.split(COMMENT_CHAR, 1)
                  # Second, find lines with an option=value:
                  if OPTION_CHAR in line:
                        # split on option char:
                        option, value = line.split(OPTION_CHAR, 1)
                        # strip spaces:
                        option = option.strip()
                        value = value.strip()
                        # store in dictionary:
                        options[option] = value
                        if (debug == True):
                              print "SAVED ",option,"=", value
            f.close()
            return options
 
      def parseSensorTestFilename(self, filename):
            debug= True
            #it has to be of the form (batch_wafer_sensor_step[_(whatever)].inf.txt
            #first, match .inf.txt
            if (re.search(".inf.txt", filename) is None):
                  print "Filename "+filename+" does not end with .inf.txt"
                  return (None, None, None, None)
            mylist = filename.split("_")
            if (debug == True):
                  print "LIST ",mylist
            if (len(mylist) <4 ):
                  print "Filename "+filename+" not well formed."
                  return (None, None, None, None)
            # the step could be the last one, split it for "."
            batch = ((mylist[0]).split('/'))[-1]
            wafer = str(batch)+'-'+str(mylist[1])
            sensor = "S"+str(wafer)+'-'+str(mylist[2])
            step = ((mylist[3]).split("\."))[0]
            print "PARSED from "+filename+" is : ",batch, wafer, sensor, step
            return (batch, wafer, sensor, step)
#
# using the info as in Andrei's mail
# given a dir
#   - look for a *.inf.txt file and parse it
#   - put in data the relevant stuff
#
# I will also add later insertTestWaferDir e insertTestBatchDir
#

      def extractorTestSensorFile(self,filename):
            

            #
            # extract parameters from the file name
            #
            
            (batch, wafer, sensor, step) = self.parseSensorTestFilename(filename)
            if (batch is None):
                  print "Error in filename extraction from "+filename
                  return (0,0,0,0,0,0,0,0,0,0,0,0,0,0,False)

            #
            # now parse internally the file
            #
            debug = True
            if (debug == True):
                  print " ECCOMI"

            results = self.textFileParser(filename)
            #
            # search for stuff inside
            #
            if (debug == True):
                  print " ECCO",results
            batch1 = results['BATCH']
            centre1 = results['CENTRE']
            step1= results['STEP']
            wafer1 = results['BATCH']+'-'+results['WAFER']
            sensor1 = "S"+results['BATCH']+'-'+results['WAFER']+'-'+results['SENSOR']
            v1 = results['V1']
            v2 = results['V2']
            i1 = results['I1']
            i2 = results['I2']
            temperature =  results['TEMPERATURE']
            slope = results['SLOPE']
            grade = results['GRADE']
            date = results['DATE']
            comment = results['COMMENT']

            if (debug == True):
                  print batch1,batch,wafer1,wafer,sensor1,sensor,step,step1
            
            if (batch1 is None or centre1 is None or step1 is None or sensor1 is None or v1 is None or v2 is None or i1 is None or i2 is None or temperature is None or date is None or slope is None or grade is None):
                  print "Error in the content of "+filename
                  return (0,0,0,0,0,0,0,0,0,0,0,0,0,0,False)
            if (batch1 != batch or wafer1 != wafer or sensor1 != sensor or step != step1):
                  print " File content and name are not consistent "+filename

            return (batch, wafer, sensor, step, v1, i1, v2, i2, slope, temperature, date, grade, centre1, comment,True)
            

      def insertTestSensorDir(self,dir,session):
            #
            # what to do here :
            #   you need directly I_150V, I_150_100, preresult
            #   a root file containing the curves
            # return None if error, otherwise the sensortest
            #

            debug = True

            ppp = subprocess.Popen("ls -1 "+dir.rstrip()+"/*.inf.txt", shell=True, stdout=subprocess.PIPE, stderr=None)
            retval = ppp.wait()
            if (retval != 0):
                  print "no files *.inf.txt in ",str(dir)
                  return (0,0,0,0,0,0,0,0,0,0,0,0,0,False)
            lines = ppp.stdout.readlines()
            if ( len (lines) > 1):
                  print "too many *.inf.txt in ",str(dir)
                  return (0,0,0,0,0,0,0,0,0,0,0,0,0,False)
                  
            filename= lines[0]
            
            filename = filename.rstrip(os.linesep)

            if (debug is True): 
                  print "FILENAME = "+filename

            (batch, wafer, sensor, step, v1, i1, v2, i2, slope, temperature, date, grade, centre, comment, ok) = self.extractorTestSensorFile(filename)
#            (moduleid, i150v, i150100, rootpnfs,preresult, result, timestamp, temperature,ok) = self.extractorTestSensorDir(dir)
            if (ok is None):
                  print "InsertSensorTest Extractor returned False"
                  return None
            
#
# check if this sensor is existing
#

            if (self.isSensorInserted(sensor) is None):
                  print "Failure: the sensor was not inserted before in inventory "+sensor
                  return None
#
# take additional stuff: the .tab.txt file
#            
#search for a file anmed in the same way            --> [*].inf.txt -> [*].tab.txt
            tabfile = re.sub(r'.inf.txt$', '.tab.txt', filename) 
            if (os.path.isfile(tabfile) == False):
                  print "Associated tab file "+tabfile+" does not exist, exiting"
                  return None
            
            data_id = Data(PFNs = tabfile)
            pp = self.insertData(data_id)
            if (pp is None):
                  print "Cannot insert data"
                  return None
            
            st = Test_Sensor(SESSION_ID=session.SESSION_ID,SENSOR_ID=sensor,GRADE=grade,DATA_ID = data_id.DATA_ID,I1 = float(i1),I2=float(i2), V1= float(v1), V2 = float(v2),  temperature = float(temperature), DATE = int(date), SLOPE =float(slope), COMMENT=comment)
            

            self.insertSensorTest(st)
            if (st is None):
                  print "Failed Sensor Test Insertion"
                  return None
            return st
