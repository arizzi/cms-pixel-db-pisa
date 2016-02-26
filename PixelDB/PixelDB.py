from Objects import *
from MySQLdb import *
from storm.locals import *
import commands
import string
import subprocess
import os.path
import re
import secrets

class PixelDBInterface(object) :

      def __init__(self, operator, center, datee =datetime.now() ) :
            self.operator = operator
            self.center =  center
            self.date = datee
            
      def connectToDB(self) :
            self.database = create_database("mysql://%s:%s@localhost/prod_pixel"%(secrets.USER,secrets.PASSWORD))
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
            self.insertHistory(type="NULL", id=0, target_type="SENSOR", target_id=sensor.SENSOR_ID, operation="INSERT", datee=datetime.now(), comment="NO COMMENT")
            return sensor
      
      def insertRoc (self, roc):
            if (self.isRocInserted(roc.ROC_ID) == True):
                  print "ERROR: roc already inserted", roc.ROC_ID
                  return None
            self.store.add(roc)
            self.store.commit()
            # log in history
            self.insertHistory(type="NULL", id=0, target_type="ROC", target_id=roc.ROC_ID, operation="INSERT", datee=datetime.now(), comment="NO COMMENT")
            return roc

      def insertTbm (self, tbm):
            if (self.isTbmInserted(tbm.TBM_ID) == True):
                  print "ERROR: tbm already inserted", tbm.TBM_ID
                  return None
            self.store.add(tbm)
            self.store.commit()
            # log in history
            self.insertHistory(type="NULL", id=0, target_type="TBM", target_id=tbm.TBM_ID, operation="INSERT", datee=datetime.now(), comment="NO COMMENT")
            return tbm

      def insertHdi (self, hdi):
            if (self.isHdiInserted(hdi.HDI_ID) == True):
                  print "ERROR: hdi already inserted", hdi.HDI_ID
                  return None
            self.store.add(hdi)
            self.store.commit()
            # log in history
            self.insertHistory(type="NULL", id=0, target_type="HDI", target_id=hdi.HDI_ID, operation="INSERT", datee=datetime.now(), comment="NO COMMENT")
            return hdi      

      def insertRocWafer (self, rocwafer):
            if (self.isRocWaferInserted(rocwafer.ROCWAFER_ID) == True):
                  print "ERROR: rocwafer already inserted", rocwafer.ROCWAFER_ID
                  return None
            self.store.add(rocwafer)
            self.store.commit()
            # log in history
            self.insertHistory(type="NULL", id=0, target_type="ROCWAFER", target_id=rocwafer.ROCWAFER_ID, operation="INSERT", datee=datetime.now(), comment="NO COMMENT")
            return rocwafer
 

      def insertBatch (self, batch):
            if (self.isBatchInserted(batch.BATCH_ID) == True):
                  print "ERROR: batch already inserted", batch.BATCH_ID
                  return None
            self.store.add(batch)
            self.store.commit()
            # log in history
            self.insertHistory(type="NULL", id=0, target_type="BATCH", target_id=batch.BATCH_ID, operation="INSERT", datee=datetime.now(), comment="NO COMMENT")
            return batch      

      def insertWafer (self, wafer):
            if (self.isWaferInserted(wafer.WAFER_ID) == True):
                  print "ERROR: wafer already inserted", wafer.WAFER_ID
                  return None
            self.store.add(wafer)
            self.store.commit()
            # log in history
            self.insertHistory(type="NULL", id=0, target_type="WAFER", target_id=wafer.WAFER_ID, operation="INSERT", datee=datetime.now(), comment="NO COMMENT")
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
            self.insertHistory(type="SENSOR", id=bm.SENSOR_ID, target_type="BAREMODULE", target_id=bm.BAREMODULE_ID, operation="ASSEMBLE", datee=datetime.now(), comment="NO COMMENT")
            # log in history rocs
            for i in self.splitObjects(bm.ROC_ID):
                  self.insertHistory(type="ROC", id=i, target_type="BAREMODULE", target_id=bm.BAREMODULE_ID, operation="ASSEMBLE", datee=datetime.now(), comment="NO COMMENT")
            
            return bm

            
      def assembleBareModule(self, baremodule_id, roc_ids,  sensor_id, builtby, transfer_id,COMMENT="", LASTTEST_BAREMODULE=0, STATUS="",LABEL2D="",POWERCABLE="", SIGNALCABLE="", TYPE=""):
            newbm = BareModule(BAREMODULE_ID=baremodule_id, ROC_ID=self.joinObjects(roc_ids), SENSOR_ID=sensor_id, TRANSFER_ID=transfer_id,BUILTBY=builtby, COMMENT=COMMENT, LASTTEST_BAREMODULE=LASTTEST_BAREMODULE, STATUS=STATUS,LABEL2D=LABEL2D,POWERCABLE=POWERCABLE, SIGNALCABLE=SIGNALCABLE, TYPE=TYPE)
            bm = self.insertBareModule(newbm)
            if (bm is None):
                 print"<br>Error inserting BAREMODULE"
            return bm
            
      def insertTestDac(self, test):
#
# I add some smartness here: if the test refers to a fullmoduleanalysis whise fullmodule test already exists (which means the tar file has been already analyzed), refuse to add
#
#            fmtid = test.fullmoduleanalysistest.fullmoduletest.TEST_ID
            # search in the existing TestDacParameters a test which
            # point to the same fullmoduletest

            self.store.add(test)
            self.store.commit()
            return test

      def insertBareModuleTest_Roc_DacParameters(self,test):
            self.store.add(test)
            self.store.commit()
            return test

      def insertObject(self,o):
            self.store.add(o)
            self.store.commit()
            return o

      def insertTestPerformance(self, test):
            self.store.add(test)
            self.store.commit()
            return test
            
            
      def insertHistory(self, type, id, target_type, target_id, operation, datee=datetime.now(), comment=""):
            newHist=History(type, id, target_type, target_id, operation, datee, comment)
            self.store.add(newHist)
            self.store.commit()            
            return newHist

      def buildHdiPlusTbm(self, hdi, tbm1, tbm2):
# please note : tbm2 can be None is the hdi has just one TBM
            hdi.TBM1_ID=tbm1.TBM_ID
            if (tbm2 is not None):
                  hdi.TBM2_ID=tbm2.TBM_ID
            return hdi
      
      def insertFullModule(self,fm):
            #
            # check if all the objects are already in DB
            #
            if (self.canBareModuleBeUsed(fm.BAREMODULE_ID) == False):
                  print "ERROR: baremodule not available", fm.BAREMODULE_ID
                  return None
	    # TBMs are not tracked
	    #if (self.canTbmBeUsed(fm.TBM_ID) == False):
            #      print "ERROR: tbm not available",fm.TBM_ID
            #      return None
	    if (self.canHdiBeUsed(unicode(fm.HDI_ID)) == False):
                  print "ERROR: hdi not available",fm.HDI_ID
                  return None

            #
            self.setBareModuleStatus(fm.BAREMODULE_ID,"USED")
#            self.setHdiStatus(fm.TBM_ID,"USED")
            self.setHdiStatus(fm.HDI_ID,"USED")
            self.store.add(fm)
            self.store.commit()
            # log in history 
            self.insertHistory(type="BAREMODULE", id=fm.BAREMODULE_ID, target_type="FULLMODULE", target_id=fm.FULLMODULE_ID, operation="ASSEMBLE", datee=datetime.now(), comment="NO COMMENT")
            self.insertHistory(type="HDI", id=fm.HDI_ID, target_type="FULLMODULE", target_id=fm.FULLMODULE_ID, operation="ASSEMBLE", datee=datetime.now(), comment="NO COMMENT")
#            self.insertHistory(type="TBM", id=fm.TBM_ID, target_type="FULLMODULE", target_id=fm.FULLMODULE_ID, operation="ASSEMBLE", datee=datetime.now(), comment="NO COMMENT")
            return fm

            


      def assembleFullModule(self, fullmodule_id, baremodule_id, tbm_id, hdi_id,  builtby, transfer_id,builton=datetime.now(),comment=""):
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

      def isRocWaferInserted(self, id):
            aa = self.store.find(RocWafer, RocWafer.ROCWAFER_ID==id).one()
            return aa is not None

      def isBareModuleInserted(self, BareModule_id):
            temp=unicode(BareModule_id)
            aa = self.store.find(BareModule, BareModule.BAREMODULE_ID==temp).one()
            return aa is not None

      def isFullModuleInserted(self, FullModule_id):
            aa = self.store.find(FullModule, FullModule.FULLMODULE_ID==FullModule_id).one()
            return aa is not None

      def insertSummaryIdIntoFullModuleTest(self,test_id,summary_id):
            aa = self.store.find(Test_FullModule, Test_FullModule.TEST_ID==test_id).one()
            aa.SUMMARY_ID = summary_id
            self.store.commit()                 
            return aa
            

      def searchFullModuleTestSummaryByDirName(self, dirname):
#
# lo faccio in modo diverso: decido che e' lo stesso in base all'ultima parte del nome.
# per esempio, se passo 
#
            temp=unicode(dirname)
            result = self.store.find((Test_FullModuleSummary, Data),
                                Test_FullModuleSummary.DATA_ID == Data.DATA_ID,
                                Data.PFNs.like("%"+temp))

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
      #      if (((self.getSensor(sensor_id)).transfer).STATUS != "ARRIVED"):
      #            return False
            return True
            
      def canRocBeUsed(self, roc_id):
            if (roc_id == ''):
                  return True
            if (self.isRocInserted(roc_id) == False):
                  return False
#            print "ROC IDDDDDDD",roc_id 
            if ((self.getRoc(roc_id)).STATUS == "USED" ):
                  return False
       #     if (((self.getRoc(roc_id)).transfer).STATUS != "ARRIVED"):
       #           return False
            return True

      def canBareModuleBeUsed(self, baremodule_id):
            if (self.isBareModuleInserted(baremodule_id) == False):
                  return False
            if ((self.getBareModule(baremodule_id)).STATUS == "USED" ):
                  return False
       #     if (((self.getBareModule(baremodule_id)).transfer).STATUS != "ARRIVED"):
       #           return False
            return True

      def canFullModuleBeUsed(self, fullmodule_id):
            if (self.isFullModuleInserted(fullmodule_id) == False):
                  return False
            if ((self.getFullModule(fullmodule_id)).STATUS == "USED" ):
                  return False
        #    if (((self.getFullModule(fullmodule_id)).transfer).STATUS != "ARRIVED"):
        #          return False
            return True

      def canHdiBeUsed(self, hdi_id):
            if (self.isHdiInserted(hdi_id) == False):
                  return False
            if ((self.getHdi(hdi_id)).STATUS == "USED" ):
                  return False
        #    if (((self.getHdi(hdi_id)).transfer).STATUS != "ARRIVED"):
        #          return False
            return True

      def canTbmBeUsed(self, tbm_id):
            if (self.isTbmInserted(tbm_id) == False):
                  return False
            if ((self.getTbm(tbm_id)).STATUS == "USED" ):
                  return False
         #   if (((self.getTbm(tbm_id)).transfer).STATUS != "ARRIVED"):
         #         return False
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
      def getBatch(self, batch_id):
            temp=unicode(batch_id)
            aa = self.store.find(Batch, Batch.BATCH_ID==temp).one()
            return aa
 
      def getWafer(self, wafer_id):
            temp=unicode(wafer_id)
            aa = self.store.find(Wafer, Wafer.WAFER_ID==temp).one()
            return aa

      def getSensor(self, sensor_id):
            temp=unicode(sensor_id)
            aa = self.store.find(Sensor, Sensor.SENSOR_ID==temp).one()
            return aa

      def getRocWafer(self, roc_id):
            temp=unicode(roc_id)
            aa = self.store.find(RocWafer, RocWafer.ROCWAFER_ID==temp).one()
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
            aa = self.store.find(FullModule, FullModule.FULLMODULE_ID==unicode(FullModule_id)).one()
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
      def getModuleXrayHRTestSummaryWithTimestamp(self, FullModule_id, TIMESTAMP):
#            print "GOT   ", FullModule_id, TIMESTAMP, type(TIMESTAMP), type(FullModule_id)
            aa = self.store.find(Test_FullModule_XRay_HR_Summary, Test_FullModule_XRay_HR_Summary.FULLMODULE_ID == unicode(FullModule_id), Test_FullModule_XRay_HR_Summary.TIMESTAMP==unicode(TIMESTAMP)).one()
#            print "RETURNIONG ", aa
            return aa
      def getModuleXrayHRTestWithTimestampAndRate(self, FullModule_id, TIMESTAMP,RATE):
            aa = self.store.find(Test_FullModule_XRay_HR_Module, Test_FullModule_XRay_HR_Module.FULLMODULE_ID == unicode(FullModule_id), Test_FullModule_XRay_HR_Module.TIMESTAMP==unicode(TIMESTAMP),
				 Test_FullModule_XRay_HR_Module.HITRATENOMINAL==float(RATE)).one()
            return aa
  
      def getRocXrayHRTestWithPosAndModtestID(self,pos,  ModtestID):
            aa = self.store.find(Test_FullModule_XRay_HR_Roc, Test_FullModule_XRay_HR_Roc.TEST_XRAY_HR_MODULE_ID == ModtestID,Test_FullModule_XRay_HR_Roc.ROC_POS == int(pos)).one()
            return aa
 	

      def getXrayVcalTestWithTimestamp(self, FullModule_id, TIMESTAMP):
            aa = self.store.find(Test_FullModule_XRay_Vcal, Test_FullModule_XRay_Vcal.FULLMODULE_ID == unicode(FullModule_id), Test_FullModule_XRay_Vcal.TIMESTAMP==unicode(TIMESTAMP)).one()
            return aa

      def getFullModuleTestWithCkSumAndTimestampAndType(self, FullModule_id, CKSUM, TEMPNOMINAL,TIMESTAMP,TYPE):
            aa = self.store.find(Test_FullModule, Test_FullModule.FULLMODULE_ID == unicode(FullModule_id), Test_FullModule.CKSUM == unicode(CKSUM), Test_FullModule.TEMPNOMINAL == unicode(TEMPNOMINAL),Test_FullModule.TIMESTAMP==unicode(TIMESTAMP),Test_FullModule.TYPE==unicode(TYPE)).one()
            return aa

#
# transfer
#

      def transferSensor(self, sensor_id, SENDER, RECEIVER, ISSUED_DATE=datetime(1970,1,1), RECEIVED_DATE=datetime.now(), STATUS="", COMMENT=""):
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
            self.insertHistory(type="TRANSFER", id=t.TRANSFER_ID, target_type="SENSOR", target_id=aa.SENSOR_ID, operation="TRASFER", datee=datetime.now(), comment="NO COMMENT")
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
            

            

      def transferTbm(self, tbm_id, SENDER, RECEIVER, ISSUED_DATE=datetime(1970,1,1), RECEIVED_DATE=datetime.now(), STATUS="", COMMENT=""):
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
            self.insertHistory(type="TRANSFER", id=t.TRANSFER_ID, target_type="TBM", target_id=aa.TBM_ID, operation="TRASFER", datee=datetime.now(), comment="NO COMMENT")
            self.store.commit()
            return aa

      def transferHdi(self, hdi_id, SENDER, RECEIVER, ISSUED_DATE=datetime(1970,1,1), RECEIVED_DATE=datetime.now(), STATUS="", COMMENT=""):
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
            self.insertHistory(type="TRANSFER", id=t.TRANSFER_ID, target_type="HDI", target_id=aa.HDI_ID, operation="TRASFER", datee=datetime.now(), comment="NO COMMENT")
            self.store.commit()
            return aa
      def transferRoc(self, roc_id, SENDER, RECEIVER, ISSUED_DATE=datetime(1970,1,1), RECEIVED_DATE=datetime.now(), STATUS="", COMMENT=""):
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
            self.insertHistory(type="TRANSFER", id=t.TRANSFER_ID, target_type="ROC", target_id=aa.ROC_ID, operation="TRASFER", datee=datetime.now(), comment="NO COMMENT")
            self.store.commit()
            return aa
      def transferFullModule(self, fullmodule_id, SENDER, RECEIVER, ISSUED_DATE=datetime(1970,1,1), RECEIVED_DATE=datetime.now(), STATUS="", COMMENT=""):
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
            self.insertHistory(type="TRANSFER", id=t.TRANSFER_ID, target_type="FULLMODULE", target_id=aa.FULLMODULE_ID, operation="TRASFER", datee=datetime.now(), comment="NO COMMENT")
            self.store.commit()
            return aa
      def transferBareModule(self, baremodule_id, SENDER, RECEIVER, ISSUED_DATE=datetime(1970,1,1), RECEIVED_DATE=datetime.now(), STATUS="", COMMENT=""):
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
            self.insertHistory(type="TRANSFER", id=t.TRANSFER_ID, target_type="BAREMODULE", target_id=aa.BAREMODULE_ID, operation="TRASFER", datee=datetime.now(), comment="NO COMMENT")
            self.store.commit()
            return aa
#
#
# TESTS
#
      def insertFullModuleSummaryNewTest(self,summ,name, type, id):
            summ.FULLMODULETEST_NAMES+=","+unicode(name)
            summ.FULLMODULETEST_TYPES+=","+unicode(type)
            summ.FULLMODULETEST_IDS+=","+unicode(str(id))
            summ.FULLMODULETEST_NAMES=summ.FULLMODULETEST_NAMES.lstrip(',')
            summ.FULLMODULETEST_TYPES=summ.FULLMODULETEST_TYPES.lstrip(',')
            summ.FULLMODULETEST_IDS=summ.FULLMODULETEST_IDS.lstrip(',')
            
# strip ',' iniziale
            self.store.commit()
            


      def insertFullModuleTestSession(self,fms):
            if (self.isFullModuleInserted(fms.FULLMODULE_ID) == False):
                  print " Cannot insert a test on a not existing FM "
                  return None
            self.store.add(fms)
            self.store.commit()
            # log in history
            self.insertHistory(type="TEST_FMSession", id=fms.TEST_ID, target_type="FULLMODULE", target_id=fms.FULLMODULE_ID, operation="TEST", datee=datetime.now(), comment="NO COMMENT")
            return fms

      def insertFullModuleTestSummary(self,fms):
            if (self.isFullModuleInserted(fms.FULLMODULE_ID) == False):
                  print " Cannot insert a test on a not existing FM "
                  return None
            self.store.add(fms)
            self.store.commit()
            # log in history
            self.insertHistory(type="TEST_FMSummary", id=fms.TEST_ID,target_type="FULLMODULE", target_id=fms.FULLMODULE_ID, operation="TEST", datee=datetime.now(), comment="NO COMMENT")
            return fms

      def insertFullModuleTestAnalysis(self,fms):
            if (self.isFullModuleInserted(fms.FULLMODULE_ID) == False):
                  print " Cannot insert a test on a not existing FM "
                  return None
            self.store.add(fms)
            self.store.commit()
            # log in history
            self.insertHistory(type="TEST_FMAnalysis", id=fms.TEST_ID, target_type="FULLMODULE", target_id=fms.FULLMODULE_ID, operation="TEST", datee=datetime.now(), comment="NO COMMENT")
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
            self.insertHistory(type="TEST_FM", id=test_fm.TEST_ID, target_type="FULLMODULES", target_id=test_fm.TEST_ID, operation="TEST", datee=datetime.now(), comment="NO COMMENT")
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
            self.insertHistory(type="TEST_BM", id=test_bm.TEST_ID, target_type="BAREMODULE", target_id=test_bm.BAREMODULE_ID, operation="TEST", datee=datetime.now(), comment="NO COMMENT")
            return test_bm

      def insertIVTest(self, test):
            #
            # first check that the module exists
            #
            if (self.isSensorInserted(test.SENSOR_ID) == False):
                  print " Cannot insert a test on a not existing S ", test.SENSOR_ID
                  return None
            self.store.add(test)
            self.store.commit()
            (self.getSensor(test.SENSOR_ID)).LASTTEST_SENSOR_IV =  test.TEST_ID
            self.store.commit()
            # log in history
            self.insertHistory(type="TEST_S", id=test.TEST_ID, target_type="SENSOR", target_id=test.SENSOR_ID, operation="TEST_IV", datee=datetime.now(), comment="NO COMMENT")
            return test

      def insertHdiTest_Reception(self, test):
            #
            # first check that the module exists
            #

            if (self.isHdiInserted(test.HDI_ID) == False):
                  print " Cannot insert a test on a not existing HDI "
                  return None
            self.store.add(test)
            self.store.commit()
	    h = self.getHdi(test.HDI_ID)
	    last= self.store.find(Test_Hdi_Reception, Test_Hdi_Reception.TEST_ID==h.LASTTEST_HDI_RECEPTION).one()
	    if last is not None and last.session.DATE > test.session.DATE :
			print "LASTTEST NOT UPDATED BECAUSE OF EXISTING NEWER TEST<br>"
 	    else :
            		(self.getHdi(test.HDI_ID)).LASTTEST_HDI_RECEPTION =  test.TEST_ID

            self.store.commit()
            # log in history
            self.insertHistory(type="TEST_HDI_RECEPTION", id=test.TEST_ID, target_type="HDI", target_id=test.HDI_ID, operation="TEST", datee=datetime.now(), comment="NO COMMENT")
            return test

      def insertHdiTest_TbmGluing(self, test):
            #
            # first check that the module exists
            #

            if (self.isHdiInserted(test.HDI_ID) == False):
                  print " Cannot insert a test on a not existing HDI "
                  return None
            self.store.add(test)
            self.store.commit()
            h = self.getHdi(test.HDI_ID)
            last= self.store.find(Test_Hdi_TbmGluing, Test_Hdi_TbmGluing.TEST_ID==h.LASTTEST_HDI_TBMGLUING).one()
            if last is not None and last.session.DATE > test.session.DATE :
                        print "LASTTEST NOT UPDATED BECAUSE OF EXISTING NEWER TEST<br>"
            else :
                        (self.getHdi(test.HDI_ID)).LASTTEST_HDI_TBMGLUING =  test.TEST_ID

            self.store.commit()
            # log in history
            self.insertHistory(type="TEST_HDI_GLUING", id=test.TEST_ID, target_type="HDI", target_id=test.HDI_ID, operation="TEST", datee=datetime.now(), comment="NO COMMENT")
            return test

      def insertHdiTest_Bonding(self, test):
            #
            # first check that the module exists
            #

            if (self.isHdiInserted(test.HDI_ID) == False):
                  print " Cannot insert a test on a not existing HDI "
                  return None
            self.store.add(test)
            self.store.commit()
            h = self.getHdi(test.HDI_ID)
            last= self.store.find(Test_Hdi_Bonding, Test_Hdi_Bonding.TEST_ID==h.LASTTEST_HDI_BONDING).one()
            if last is not None and last.session.DATE > test.session.DATE :
                        print "LASTTEST NOT UPDATED BECAUSE OF EXISTING NEWER TEST<br>"
            else :
                        (self.getHdi(test.HDI_ID)).LASTTEST_HDI_BONDING =  test.TEST_ID

            self.store.commit()
            # log in history
            self.insertHistory(type="TEST_HDI_BONDING", id=test.TEST_ID, target_type="HDI", target_id=test.HDI_ID, operation="TEST", datee=datetime.now(), comment="NO COMMENT")
            return test

      def insertHdiTest_Electric(self, test):
            #
            # first check that the module exists
            #

            if (self.isHdiInserted(test.HDI_ID) == False):
                  print " Cannot insert a test on a not existing HDI "
                  return None
            #
            # check on SIZES etc
            #
            if (len(test.SIGNALS_AND_LVS) != test.TOT_SIZE):
                  print "Cannot insert Test HDI ELECTRIC: SIGNALS_AND_LVS not correct size"
                  return None
            self.store.add(test)
            self.store.commit()

            h = self.getHdi(test.HDI_ID)
            last= self.store.find(Test_Hdi_Electric, Test_Hdi_Electric.TEST_ID==h.LASTTEST_HDI_ELECTRIC).one()
            if last is not None and last.session.DATE > test.session.DATE :
                        print "LASTTEST NOT UPDATED BECAUSE OF EXISTING NEWER TEST<br>"
            else :
                        (self.getHdi(test.HDI_ID)).LASTTEST_HDI_ELECTRIC =  test.TEST_ID



            self.store.commit()
            # log in history
            self.insertHistory(type="TEST_HDI_ELECTRIC", id=test.TEST_ID, target_type="HDI", target_id=test.HDI_ID, operation="TEST", datee=datetime.now(), comment="NO COMMENT")
            return test

      def insertHdiTest_Validation(self, test):
            #
            # first check that the module exists
            #

            if (self.isHdiInserted(test.HDI_ID) == False):
                  print " Cannot insert a test on a not existing HDI "
                  return None
            self.store.add(test)
            self.store.commit()

            h = self.getHdi(test.HDI_ID)
            last= self.store.find(Test_Hdi_Validation, Test_Hdi_Validation.TEST_ID==h.LASTTEST_HDI_VALIDATION).one()
            if last is not None and last.session.DATE > test.session.DATE :
                        print "LASTTEST NOT UPDATED BECAUSE OF EXISTING NEWER TEST<br>"
            else :
                        (self.getHdi(test.HDI_ID)).LASTTEST_HDI_VALIDATION =  test.TEST_ID

            self.store.commit()
            # log in history
            self.insertHistory(type="TEST_HDI_VALIDATION", id=test.TEST_ID, target_type="HDI", target_id=test.HDI_ID, operation="TEST", datee=datetime.now(), comment="NO COMMENT")
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
            self.insertHistory(type="TEST_TBM", id=test.TEST_ID, target_type="TBM", target_id=test.TBM_ID, operation="TEST", datee=datetime.now(), comment="NO COMMENT")
            return test

      def insertRocTest(self, test):
            #
            # first check that the module exists
            #
            if (self.getRoc(test.ROC_ID) is None):
                  print " Cannot insert a test on a not existing ROC "
                  return None
            self.store.add(test)
            self.store.commit()
            (self.getRoc(test.ROC_ID)).LASTTEST_ROC =  test.TEST_ID
            self.store.commit()
            # log in history
            self.insertHistory(type="TEST_ROC", id=test.TEST_ID, target_type="ROC", target_id=test.ROC_ID, operation="TEST", datee=datetime.now(), comment="NO COMMENT")
            return test

#BM tests
#      
      def insertBareModuleTest_Chip(self, test):
            #
            # first check that the module exists
            #

            if (self.isBareModuleInserted(test.BAREMODULE_ID) == False):
                  print " Cannot insert a test on a not existing BareModule "
                  return None
            self.store.add(test)
            self.store.commit()
            h = self.getBareModule(test.BAREMODULE_ID)
            last= self.store.find(Test_BareModule_Chip, Test_BareModule_Chip.TEST_ID==h.getChipTest(test.CHIP_N)).one()
            if last is not None and last.session.DATE > test.session.DATE :
                        print "LASTTEST NOT UPDATED BECAUSE OF EXISTING NEWER TEST<br>"
            else :
                        # here the logic is cmplicated by the fact that we need to set the specific test
                        (self.getBareModule(test.BAREMODULE_ID)).setChipTest(test, test.CHIP_N)

            self.store.commit()
            # log in history
            self.insertHistory(type="TEST_BAREMODULE_CHIPS", id=test.TEST_ID, target_type="BAREMODULE", target_id=test.BAREMODULE_ID, operation="TEST", datee=datetime.now(), comment="NO COMMENT")
            return test


      def insertBareModuleTest_Inspection(self, test):
            #
            # first check that the module exists
            #

            if (self.isBareModuleInserted(test.BAREMODULE_ID) == False):
                  print " Cannot insert a test on a not existing BareModule "
                  return None
            self.store.add(test)
            self.store.commit()
            h = self.getBareModule(test.BAREMODULE_ID)
            last= self.store.find(Test_BareModule_Inspection, Test_BareModule_Inspection.TEST_ID==h.LASTTEST_BAREMODULE_INSPECTION).one()
            if last is not None and last.session.DATE > test.session.DATE :
                        print "LASTTEST NOT UPDATED BECAUSE OF EXISTING NEWER TEST<br>"
            else :
                        (self.getBareModule(test.BAREMODULE_ID)).LASTTEST_BAREMODULE_INSPECTION =  test.TEST_ID

            self.store.commit()
            # log in history
            self.insertHistory(type="TEST_BAREMODULE_INSPECTION", id=test.TEST_ID, target_type="BAREMODULE", target_id=test.BAREMODULE_ID, operation="TEST", datee=datetime.now(), comment="NO COMMENT")
            return test



      def insertBareModuleTest_Grading(self, test):
            #
            # first check that the module exists
            #

            if (self.isBareModuleInserted(test.BAREMODULE_ID) == False):
                  print " Cannot insert a test on a not existing BareModule "
                  return None
            self.store.add(test)
            self.store.commit()
            h = self.getBareModule(test.BAREMODULE_ID)
            last= self.store.find(Test_BareModule_Grading, Test_BareModule_Grading.TEST_ID==h.LASTTEST_BAREMODULE_GRADING).one()
            if last is not None and last.session.DATE > test.session.DATE :
                        print "LASTTEST NOT UPDATED BECAUSE OF EXISTING NEWER TEST<br>"
            else :
                        (self.getBareModule(test.BAREMODULE_ID)).LASTTEST_BAREMODULE_GRADING =  test.TEST_ID

            self.store.commit()
            # log in history
            self.insertHistory(type="TEST_BAREMODULE_GRADING", id=test.TEST_ID, target_type="BAREMODULE", target_id=test.BAREMODULE_ID, operation="TEST", datee=datetime.now(), comment="NO COMMENT")
            return test


      def insertBareModuleTest_QA(self, test):
            #
            # first check that the module exists
            #

            if (test.TYPE == "PixelAlive"):
                  myType = "+_PIXELALIVE"
                  intType=1
            elif (test.TYPE == "BumpBonding"):
                  myType = "+_BONDING"
                  intType=2
            else:
                  print " ERROR: QA test of type ",test.TYPE, " not allowed!"
                  return None
            if (self.isBareModuleInserted(test.BAREMODULE_ID) == False):
                  print " Cannot insert a test on a not existing BareModule "
                  return None
            self.store.add(test)
            self.store.commit()

            
            
            h = self.getBareModule(test.BAREMODULE_ID)
            if (intType==1):
                  last= self.store.find(Test_BareModule_QA, Test_BareModule_QA.TEST_ID==h.LASTTEST_BAREMODULE_QA_PIXELALIVE).one()
                  if last is not None and last.session.DATE > test.session.DATE :
                        print "LASTTEST NOT UPDATED BECAUSE OF EXISTING NEWER TEST<br>"
                  else :
                        (self.getBareModule(test.BAREMODULE_ID)).LASTTEST_BAREMODULE_QA_PIXELALIVE =  test.TEST_ID
            else:
                  last= self.store.find(Test_BareModule_QA, Test_BareModule_QA.TEST_ID==h.LASTTEST_BAREMODULE_QA_BONDING).one()
                  if last is not None and last.session.DATE > test.session.DATE :
                        print "LASTTEST NOT UPDATED BECAUSE OF EXISTING NEWER TEST<br>"
                  else :
                        (self.getBareModule(test.BAREMODULE_ID)).LASTTEST_BAREMODULE_QA_BONDING =  test.TEST_ID
                        


            self.store.commit()
            # log in history
            self.insertHistory(type=str("TEST_BAREMODULE_QA"+myType), id=test.TEST_ID, target_type="BAREMODULE", target_id=test.BAREMODULE_ID, operation="TEST", datee=datetime.now(), comment="NO COMMENT")
            return test




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
            f = open(filename,'U')
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
		  else:
			options[line]="" #for empty values with no delimiter
            f.close()
            return options
 
      def parseSensorTestFilename(self, filename):
            debug= True
            #it has to be of the form (batch_wafer_sensor_step[_(whatever)].inf.txt
            #first, match .inf.txt
            if (re.search(".inf.txt", filename) is None):
                  print "Filename "+filename+" does not end with .inf.txt"
                  return (None, None, None, None)
            print"BEING PASSED ",filename
	    filename1=re.sub(".*/","",filename) 	
	    filename1=re.sub("\..*","",filename1) 	
            mylist = re.split("[_-]",filename1)
            if (debug == True):
                  print "LIST ",mylist
            if (mylist[0] == "SensorTest"):
                  del mylist[0]
            if (len(mylist) <4 ):
                  print "Filename "+filename+" not well formed."
                  return (None, None, None, None)
            # the step could be the last one, split it for "."
            batch = str(mylist[0])
	    batch = re.sub("^S","",batch)	
            wafer = str(batch)+'-'+str(mylist[1])
            sensor = "S"+str(wafer)+'-'+str(mylist[2])
            step = ((mylist[3]).split("\."))[0]
            print "PARSED from "+filename+" is : ",batch, wafer, sensor, step
            return (batch, wafer, sensor, step.upper())
#
# using the info as in Andrei's mail
# given a dir
#   - look for a *.inf.txt file and parse it
#   - put in data the relevant stuff
#

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
	    try :
              batch1 = results['BATCH']
              centre1 = results['CENTRE']
              step1= results['STEP'].upper()
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
              comment = results.get('COMMENT',"")
	    except Exception,err:
	      print "Error in parsing due to missing fields",Exception, err
    	      return (0,0,0,0,0,0,0,0,0,0,0,0,0,0,False)
	
            if (debug == True):
                  print "batch", batch1,batch,"wafer", wafer1,wafer,"sensor", sensor1,sensor,"step",step,step1
            
            if (batch1 is None or centre1 is None or step1 is None or sensor1 is None or v1 is None or v2 is None or i1 is None or i2 is None or temperature is None or date is None or slope is None or grade is None):
                  print "Error in the content of "+filename
                  return (0,0,0,0,0,0,0,0,0,0,0,0,0,0,False)
            if (batch1 != batch or wafer1 != wafer or sensor1 != sensor or step != step1):
                  print "batch", batch1,batch,"wafer", wafer1,wafer,"sensor", sensor1,sensor,"step",step,step1
                  print " File content and name are not consistent "+filename
		  return (0,0,0,0,0,0,0,0,0,0,0,0,0,0,False)

            return (batch, wafer, sensor, step, v1, i1, v2, i2, slope, temperature, date, grade, centre1, comment,True)
            

      def insertIVTestDir(self,dir,session):
      #
            # what to do here :
            #   you need directly I_150V, I_150_100, preresult
            #   a root file containing the curves
            # return None if error, otherwise the sensortest
            #
	    print "pippa"
            debug = True

            ppp = subprocess.Popen("ls -1 "+dir.rstrip()+"/*.inf.txt", shell=True, stdout=subprocess.PIPE, stderr=None)
#            ppp = subprocess.Popen("find "+dir.rstrip()+" -name \*.inf.txt", shell=True, stdout=subprocess.PIPE, stderr=None)
            retval = ppp.wait()
            if (retval != 0):
                  print "no files *.inf.txt in ",str(dir)
#                  return (0,0,0,0,0,0,0,0,0,0,0,0,0,False)
                  (batch, wafer, sensor, step, v1, i1, v2, i2, slope, temperature, date, grade, centre, comment, ok) = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,False)
		  return None
            lines = ppp.stdout.readlines()
            if ( len (lines) > 1):
                  print "too many *.inf.txt in ",str(dir)
                  (batch, wafer, sensor, step, v1, i1, v2, i2, slope, temperature, date, grade, centre, comment, ok) = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,False)
		  return None
                  
            filename= lines[0]
            
            filename = filename.rstrip(os.linesep)

            if (debug is True): 
                  print "FILENAME = "+filename

            (batch, wafer, sensor, step, v1, i1, v2, i2, slope, temperature, date, grade, centre, comment, ok) = self.extractorTestSensorFile(filename)
#            (moduleid, i150v, i150100, rootpnfs,preresult, result, timestamp, temperature,ok) = self.extractorTestSensorDir(dir)
            if (ok is None or ok == False):
                  print "InsertSensorTest Extractor returned False"
                  return None
            
#
# check if this sensor is existing
#
            print "CHECK IF INSERTED",sensor
            if (self.isSensorInserted(sensor) == False):
                  print "Failure: the sensor was not inserted before in inventory "+sensor
                  return None
            print "PASSED", self.isSensorInserted(sensor)
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
            try:
               session = Session(CENTER=centre, OPERATOR='n/a',TYPE="IV",DATE=int(date), COMMENT=comment)
	       self.insertSession(session)
               st = Test_IV(SESSION_ID=session.SESSION_ID,SENSOR_ID=sensor,GRADE=grade,DATA_ID = data_id.DATA_ID,I1 = float(i1),I2=float(i2), V1= float(v1), V2 = float(v2),  TEMPERATURE = float(temperature), DATE = int(date), SLOPE =float(slope), COMMENT=comment, TYPE=step)
            except Exception,err:
		 print Exception,err
		 return None


            self.insertIVTest(st)
            if (st is None):
                  print "Failed Sensor Test Insertion"
                  return None
            return st


      DEBUG = False

      def safeFloat(self, fl):
        res = -100
        try:
            res = float(fl)
        except ValueError:
            print "Not a float"
            res = -100
        return res


      def safeInt(self, fl):
        res = -100
        try:
            res = int(fl)
        except ValueError:
            print "Not an int"
            res = -100
        return res
        


      def  insertBareModuleMultiTestDir(self, dir,session):
        #
        # here I need to understand which tests to upload
        # I will need to look for the files:
        #  Bare_module_reception.csv : reception test
        #  Bare_module_QA_Bump.csv + defects.json: QA_BumpBonding
        #  Bare_module_QA_Alive.csv + defects.json: QA_PixelAlive
        #  Bare_module_grading.csv: Grading
        #
        # in all cases we need to fix the session a posteriori
        
        # search for QA_Bonding test
        
        isQAInserted = self.insertBareModuleQADir(dir,session)
        if ( isQAInserted is not None):
           return isQAInserted
        
        isGradingInserted = self.insertBareModuleQAGradingDir(dir,session)
        if (isGradingInserted is not None):
            return isGradingInserted
        
        return "nothing known found, go ahead"


      def insertBareModuleQAGradingDir(self,dir,session):

        return None
        
        ppp = subprocess.Popen("ls -1 "+dir.rstrip()+"/Bare_module_grading.csv", shell=True, stdout=subprocess.PIPE, stderr=None)
        retval = ppp.wait()
        
        if (retval != 0):
            print "no files Bare_module_grading.csv   in ",str(dir)
            return None
        lines = ppp.stdout.readlines()
        if ( len (lines) > 1):
            print "too many Bare_module_grading.csv in ",str(dir)
            return None
        
        filename= lines[0]
        filename = filename.rstrip(os.linesep)
        print "FILENAME = "+filename
        
# WORKING
    


        return None


        

      def insertBareModuleQADir(self, dir,session):
        
        ppp = subprocess.Popen("ls -1 "+dir.rstrip()+"/Bare_module_QA_*.csv", shell=True, stdout=subprocess.PIPE, stderr=None)
        retval = ppp.wait()
        
        if (retval != 0):
            print "no files Bare_module_QA_*.csv   in ",str(dir)
            return None
        lines = ppp.stdout.readlines()
        if ( len (lines) > 1):
            print "too many Bare_module_QA_*.csv in ",str(dir)
            return None

        filename= lines[0]
        filename = filename.rstrip(os.linesep)
        print "FILENAME = "+filename

        
        if (re.match (".*Bump.*",filename))  :
            tyype = "BumpBonding"
        elif (re.match(".*Pixel.*", filename)):
            tyype = "PixelAlive"
        else:
            print" Unknown QA type", filename
            return None
        if self.DEBUG== True:
            print " TYPE IS QA_"+tyype
    
        (bmid, lab, operator, temperature, rh, deadmissingchannels, bbcut, ok) = self.extractorBareModuleQADir(filename)
        if (ok == False):
            print" insertBareModuleQABondingDir received an error"
            return None

        print "RECEIVED: ",bmid, lab, operator, temperature, rh, deadmissingchannels, bbcut, ok

        # now search for defects.json
        
        if self.DEBUG ==True:
            print "testing file ", dir.rstrip()+"/defects.json"

        ppp2 = subprocess.Popen("ls -1 "+dir.rstrip()+"/defects.json", shell=True, stdout=subprocess.PIPE, stderr=None)
        
        retval = ppp2.wait()
    
        if (retval != 0):
            print "no files defects.json   in ",str(dir)
            return None

        lines2 = ppp2.stdout.readlines()
        if ( len (lines2) > 1):
            print "too many defects.json in ",str(dir)
            return None
        
        filename2= lines2[0]
        filename2 = filename2.rstrip(os.linesep)

        defjson = file(filename2).read()

        if self.DEBUG == True:
            print " DEFECTS ARE ", defjson

        if self.DEBUG != True:
            session.CENTER=unicode(lab)
            session.OPERATOR =unicode(operator)

	    data_id = Data(PFNs = dir.rstrip())
      	    pp = self.insertData(data_id)
            if (pp is None):
                  print "Cannot insert data"
                  return None
    
#     def __init__ (self,DATA_ID,SESSION_ID,BAREMODULE_ID, TYPE, TEMPERATURE, HUMIDITY, TOTAL_FAILURES, FAILURES="" ):

            test = Test_BareModule_QA(DATA_ID=pp.DATA_ID,  SESSION_ID=session.SESSION_ID, BAREMODULE_ID = bmid, TYPE = tyype, TOTAL_FAILURES = deadmissingchannels, TEMPERATURE = temperature, HUMIDITY = rh, FAILURES = defjson )
    
            result = self.insertBareModuleTest_QA(test)
            
            if result is None:
                print " ERROR Inserting BareModuleTest_QA"
                return None
            
            self.store.commit()
        else:
            result = " FAKE FAKE FAKE"



#            at this point, I try and search for DAQ Parameters

            #
            # search for Bare_module_ROC[00-15]_setup.csv
            #
        for num in range(0,16):
            #
            # I need a two digit number like 00
            #
            pattern = str(num).zfill(2)
            searchname = "Bare_module_ROC"+pattern+"_setup.csv"
            
            ppp = subprocess.Popen("ls -1 "+dir.rstrip()+"/"+searchname, shell=True, stdout=subprocess.PIPE, stderr=None)
            retval = ppp.wait()

            if (retval != 0):
                print "no files", searchname,"  in ",str(dir)
                continue
            
            lines = ppp.stdout.readlines()
            if ( len (lines) > 1):
                print "too many "+ searchname+" in ",str(dir)
                continue
            filename= lines[0]	
            filename = filename.rstrip(os.linesep)
                
            print "FILENAME = "+filename

            
            
            (ROC_POS,
             BAREMODULE_ID,
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
             TEMPERATURE,
             HUMIDITY                 , ok  ) = self.extractorBareModuleRocDacParametersDir(filename)
            



            
#            print " DAC PARAMETERS: GOT ", ROC_POS,            BAREMODULE_ID,            IDIG  ,            CLK  ,            DESER ,             VDIG  ,            VANA  ,            VSH,            VCOMP,              VWLLPR ,             VWLLSH  ,            VHLDDEL  ,            VTRIM  ,            VTHRCOMP ,             VIBIAS_BUS,              VIBIAS_SF  ,            VOFFSETOP  ,                                                        PHOFFSET ,            VION ,            VCOMP_ADC ,            PHSCALE ,            VICOLOR ,            VCAL  ,            CALDEL ,             VD  ,            VA  ,            CTRLREG,              WBC  ,            RBREG  ,            TEMPERATURE,            HUMIDITY  

            if (ok != True):
                print "cannot extract from ", filename
                continue
                # i can create the test and attach
            # create a data id
            if True:
                data_id = Data(PFNs = filename)
                pp = self.insertData(data_id)
		
                if (pp is None):
                    print "Cannot insert data"
                    continue
		qatestid=0
		if result is not None :
			qatestid=result.TEST_ID
                dactest = Test_BM_ROC_DacParameters(
                    ROC_POS       =   ROC_POS         ,
                    BAREMODULE_ID =   BAREMODULE_ID    ,
                    DATA_ID       =   data_id.DATA_ID         ,
                    IDIG          =   IDIG            ,
                    CLK           =   CLK             ,
                    DESER         =   DESER           , 
                    VDIG          =   VDIG            ,
                    VANA          =   VANA            ,
                    VSH           =   VSH             ,
                    VCOMP         =   VCOMP           ,   
                    VWLLPR        =   VWLLPR          , 
                    VWLLSH        =   VWLLSH          ,
                    VHLDDEL       =   VHLDDEL          ,
                    VTRIM         =   VTRIM           ,
                    VTHRCOMP      =   VTHRCOMP         , 
                    VIBIAS_BUS    =   VIBIAS_BUS      ,  
                    VIBIAS_SF     =   VIBIAS_SF       ,
                    VOFFSETOP     =   VOFFSETOP       ,
                    PHOFFSET      =   PHOFFSET        ,
                    VION          =   VION            ,
                    VCOMP_ADC     =   VCOMP_ADC       ,
                    PHSCALE       =   PHSCALE         ,
                    VICOLOR       =   VICOLOR         ,
                    VCAL          =   VCAL            ,
                    CALDEL        =   CALDEL          , 
                    VD            =   VD              ,
                    VA            =   VA              ,
                    CTRLREG       =   CTRLREG         ,  
                    WBC           =   WBC             ,
                    RBREG         =   RBREG           ,
                    SESSION_ID    =   session.SESSION_ID      ,
                    TEMPERATURE   =   TEMPERATURE     ,
                    QATEST_ID  =   qatestid     ,
                    HUMIDITY      =   HUMIDITY             )
                
                ppp = self.insertBareModuleTest_Roc_DacParameters(dactest)



#
# now search if there is 
#
    
        return result



      def extractorBareModuleRocDacParametersDir(self, filename):
        file = open(filename)


        ROC_POS = -100 
        BAREMODULE_ID= ""
        IDIG  = -100
        CLK  = -100
        DESER = -100 
        VDIG  = -100
        VANA  = -100
        VSH= -100
        VCOMP= -100  
        VWLLPR = -100 
        VWLLSH  = -100
        VHLDDEL  = -100
        VTRIM  = -100
        VTHRCOMP = -100 
        VIBIAS_BUS= -100  
        VIBIAS_SF  = -100
        VOFFSETOP  = -100
        PHOFFSET = -100
        VION = -100
        VCOMP_ADC = -100
        PHSCALE = -100
        VICOLOR = -100
        VCAL  = -100
        CALDEL = -100 
        VD  = -100
        VA  = -100
        CTRLREG= -100  
        WBC  = -100
        RBREG  = -100
        TEMPERATURE= -100
        HUMIDITY  = -100
        
        for line in file:
            
            if self.DEBUG == True:
                print "LINE in Extractor DAC = ", line
                print " AFTER"
            if not line:
                    break

            
            if (re.match(".*:.*",line)):


                words= re.split(':',line)
                words = [i.strip() for i in words]
                
                print "SPLIT : ",words
                
                if len( words)!=2 :
                    continue
                key = words[0]
                value=words[1]


                
                if (key.upper() =="ROC_ID".upper()):
                    ROC_POS = self.safeInt(value.strip())

                if (key.upper() =="Bare_module_ID".upper()):
                    BAREMODULE_ID = value.strip()
                if (key.upper() == "Temperature".upper()):
                    TEMPERATURE = self.safeFloat(value.strip())
                if (key.upper() == "RH".upper()):
                    HUMIDITY = self.safeFloat(value.strip())
                if (key.upper() == "IDig".upper()):
                    IDIG = self.safeFloat(re.split("\s+",value.strip())[0])
                if (key.upper() == "deser".upper()):
                    DESER = self.safeInt(value.strip())
                if (key.upper() == "clk".upper()):
                    CLK = self.safeInt(value.strip())
                    
            else:
                
                # 
                fields = re.split('\s+',line.strip())
                
                fields = [i.strip() for i in fields]
                
                print "SPLIT_fields : ",fields
                
                if len(fields)<3 :
                    continue
                key = fields[1]
                value=fields[2]



            if (key.upper() =="VDIG".upper()):
                VDIG = self.safeInt(value.strip())

            if (key.upper() =="VANA".upper()):
                VANA = self.safeInt(value.strip())

            if (key.upper() =="VSF".upper()):
                VSF = self.safeInt(value.strip())

            if (key.upper() =="VCOMP".upper()):
                VCOMP = self.safeInt(value.strip())

            if (key.upper() =="VWLLPR".upper()):
                 VWLLPR= self.safeInt(value.strip())

            if (key.upper() =="VWLLSH".upper()):
                VWLLSH = self.safeInt(value.strip())

            if (key.upper() =="VHLDDEL".upper()):
                VHLDDEL = self.safeInt(value.strip())

            if (key.upper() =="VTRIM".upper()):
                VTRIM = self.safeInt(value.strip())

            if (key.upper() =="VTHRCOMP".upper()):
                VTHRCOMP = self.safeInt(value.strip())

            if (key.upper() =="VIBias_Bus".upper()):
                VIBIAS_BUS = self.safeInt(value.strip())

            if (key.upper() =="Vbias_sf".upper()):
                VIBIAS_SF = self.safeInt(value.strip())


            if (key.upper() =="VoffsetOp".upper()):
                VOFFSETOP = self.safeInt(value.strip())

            if (key.upper() =="VIon".upper()):
                VION = self.safeInt(value.strip())


            if (key.upper() =="Vcomp_ADC".upper()):
                VCOMP_ADC = self.safeInt(value.strip())


            if (key.upper() =="VIColOr".upper()):
                VICOLOR = self.safeInt(value.strip())


            if (key.upper() =="VCal".upper()):
                VCAL = self.safeInt(value.strip())


            if (key.upper() =="CalDel".upper()):
                CALDEL = self.safeInt(value.strip())


            if (key.upper() =="VD".upper()):
                VD = self.safeInt(value.strip())

            if (key.upper() =="VA".upper()):
                VA = self.safeInt(value.strip())

            if (key.upper() =="CtrlReg".upper()):
                CTRLREG  = self.safeInt(value.strip())

            if (key.upper() =="WBC".upper()):
                WBC = self.safeInt(value.strip())



        ok = True
        if self.DEBUG == True:
            print " SENDING", ROC_POS,BAREMODULE_ID,                IDIG  ,                CLK  ,                DESER ,                 VDIG  ,                VANA  ,                VSH,               VCOMP,                  VWLLPR ,                 VWLLSH  ,                VHLDDEL  ,                VTRIM  ,                VTHRCOMP ,                 VIBIAS_BUS,      VIBIAS_SF  ,                VOFFSETOP  ,                PHOFFSET ,                VION ,                VCOMP_ADC ,                PHSCALE ,                VICOLOR ,                VCAL  ,                CALDEL ,                 VD  ,                VA  ,                CTRLREG,                  WBC  ,                RBREG  ,                TEMPERATURE,                HUMIDITY                 , ok
        

        if (ROC_POS  == -100 or  
            BAREMODULE_ID == ""
# or 
#            IDIG  == None or 
#            CLK  == None or 
#            DESER == None or  
#            VDIG  == None or 
#            VANA  == None or 
#            VSH== None or 
#            VCOMP== None or   
#            VWLLPR == None or  
#            VWLLSH  == None or 
#            VHLDDEL  == None or 
#            VTRIM  == None or 
#            VTHRCOMP == None or  
#            VIBIAS_BUS== None or   
#            VIBIAS_SF  == None or 
#            VOFFSETOP  == None or 
#            PHOFFSET == None or 
#            VION == None or 
#            VCOMP_ADC == None or 
#            PHSCALE == None or 
#            VICOLOR == None or 
#            VCAL  == None or 
#            CALDEL == None or  
#            VD  == None or 
#            VA  == None or 
#            CTRLREG== None or   
#            WBC  == None or 
#            RBREG  == None or 
#            TEMPERATURE== None or 
#            HUMIDITY  == None
            ):
            ok = False
            



        return   (ROC_POS,
             BAREMODULE_ID,
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
             TEMPERATURE,
             HUMIDITY           
                  , ok  )








      def extractorBareModuleQADir(self,filename):
        # Bare_module_ID: B04322310-08-01
        # Laboratory_ID:  DESY
        # Operator_NickName:      AV
        # Temperature:
        # RH:
        # Dead_Missing_Channels:  383
        # BB_cut_criteria:        33

        file = open(filename)
    
        bmid = None
        lab= None
        temp = -99
        rh = -99
        dead = None
        bbcut = None
        op = "n/a"
        
        while 1:
            line = file.readline()

            if self.DEBUG == True:
                print "LINE in Extractor = ", line
                print " AFTER"
            if not line:
                break
            
                continue
            words= re.split(':',line)
            words = [i.strip() for i in words]

            print "SPLIT : ",words

            if len( words)!=2 :
                continue
            key = words[0]
            value=words[1]
            if (key.upper() =="Bare_module_ID".upper()):
                bmid = value.strip()
            if (key.upper() =="Laboratory_ID".upper()):
                lab = value.strip()
            if (key.upper() == "Operator_NickName".upper()):
                op = value.strip()
            if (key.upper() == "Temperature".upper()):
                temp = self.safeFloat(value.strip())
            if (key.upper() == "RH".upper()):
                rh = self.safeFloat(value.strip())
            if (key.upper() == "Dead_Missing_Channels".upper()):
                dead = self.safeInt(value.strip())
            if (key.upper() == "BB_cut_criteria".upper()):
                bbcut = self.safeInt(value.strip())
            
        ok = True
        
        if bbcut is None:
            bbcut = -1

        if (bmid ==  None  or lab  ==  None  or temp ==  None  or rh ==  None  or dead ==  None  or bbcut ==  None  or op ==  None):
	    print "Missing fields!"
            ok = False
                
#(bmid, lab, operator, temperature, rh, deadmissingchannels, bbcut, ok) 
                
        return (bmid, lab, op, temp, rh, dead, bbcut, ok)

      def setLastTest_XRay_HR(self,t):
            fm = self.getFullModule(t.FULLMODULE_ID)
            if fm is None:
                  print " Error: the FM ", t.FULLMODULE_ID, " does not seem to exist, passing..."
                  return None
	    old=self.store.find(Test_FullModule_XRay_HR_Summary,Test_FullModule_XRay_HR_Summary.TEST_ID==fm.LASTTEST_XRAY_HR )
            if old is not None and old.count()> 0 :
		old=old.one()
	    else :
		old=None
	    if old == None or old.TIMESTAMP < t.TIMESTAMP :
	           fm.LASTTEST_XRAY_HR = t.TEST_ID
	    	   print "Set last HR to " , t.TEST_ID
	    else :
		print "Not updating the lasttest because it was newer"
            self.store.commit()
            return t



      def setLastTest_XRay_VCAL(self,t):
            #
            # set this as lat test in the inventory only if it is really the last? to be decided....
            #
            fm = self.getFullModule(t.FULLMODULE_ID)
            if fm is None:
                  print " Error: the FM ", t.FULLMODULE_ID, " does not seem to exist, passing..."
                  return None
	    old=self.store.find(Test_FullModule_XRay_Vcal,Test_FullModule_XRay_Vcal.TEST_ID==fm.LASTTEST_XRAY_VCAL )
            if old is not None and old.count() > 0 :
                old=old.one()
            else :
                old=None
            if old == None or old.TIMESTAMP < t.TIMESTAMP :
                   fm.LASTTEST_XRAY_VCAL = t.TEST_ID
                   print "Set last VCAL to " , t.TEST_ID
            else :
                print "Not updating the lasttest because it was newer"
            self.store.commit()
            return t
   


      def insertHR (self,sessionid, HighRateDataModule , HighRateDataAggr, HighRateDataAllNoise, HighRateDataInterp
                                             ,HighRateDataRoc
                                             ,HighRateDataAggrRoc
                                             ,HighRateDataAllNoiseRoc
                                             ,HighRateDataInterpRoc):
	    results=[]
            #
            # MODULES
            #

            #
            #create Module part common to all the tests
            #
            fullmodule_id = HighRateDataModule['ModuleID']
            result = HighRateDataModule['HRGrade']
            macroVersion = HighRateDataModule['MacroVersion']
            addrPixBad = HighRateDataModule['AddrPixelsBad']
            addrPixHot = HighRateDataModule['AddrPixelsHot']
            n_hot_pixels = HighRateDataModule['NHotPixel']
            n_con_nonuniform= HighRateDataModule['ROCsWithUniformityProblems']
            module = self.getFullModule(fullmodule_id)
            if module is None :
                  print "Cannot insert on non existing module",modulename
                  return None
            timestamp = HighRateDataModule['TestDate']
            temperature = -99
            try :
                temperature = float(HighRateDataModule['TestTemp'])
            except :
                print "Cannot get temperature " 

	    dataTest=None
	    dataAna=None	

#
# prepare
#

            interpEffTestPoint = {}
            interpEff={}
            nPixelsNoise={}
            meanNoiseAllPixels = {}
            widthNoiseAllPixels = {}
            addrPixelNoise = {}
            measuredHitRate = {}
            nPixelNoHit = {}
            nBinsLowHigh = {}
            #
            # these are the common parts, now I do
            # 1- INTERP: search in HighRateDataInterp, HighRateDataInterpRoc , loop on the rates
            #            

            for rate, payload in HighRateDataInterp.iteritems():
                  print " Studying interpolation per Rate = ", rate
                  interpEffTestPoint[rate] = payload['InterpEffTestpoint']
                  interpEff[rate] = payload['InterpEffTestpoint']
                  
            #
            # now Noise
            #
            #
            for rate, payload in HighRateDataAllNoise.iteritems():
                  print " Studying Noise per Rate = ", rate            

                  nPixelsNoise[rate] = payload['NPixelsNoise']['Value']
                  meanNoiseAllPixels[rate] = payload['MeanNoiseAllPixels']
                  widthNoiseAllPixels[rate] = payload['WidthNoiseAllPixels']
                  addrPixelNoise[rate] = payload['AddrPixelsNoise']['Value']
                  
            #
            # now Aggregate (which is hitmap)
            #
            #
            for rate, payload in HighRateDataAggr.iteritems():
                  print ' Studying Hitmap per Rate = ', rate
                  measuredHitRate[rate] = payload['MeasuredHitrate']
                  nPixelNoHit[rate] = payload['NPixelNoHit']
                  nBinsLowHigh[rate] = payload['NBinsLowHigh']                  
                  

            #
            # try and accumulate
            #
                  
            rates = list(set(interpEffTestPoint.keys())|set(nPixelsNoise.keys())|set(measuredHitRate.keys()))

            # fill a result per rate



            #
            # per roc
            #
            # common
            
            addrPixBad_roc={}
            addrPixHot_roc = {}
            n_hot_pixels_roc = {}
            n_con_nonuniform_roc = {}
	    grade_roc = {}


            for roc, payload in HighRateDataRoc.iteritems():
                roc_pos = payload['RocPos']
                addrPixBad_roc[roc_pos] =  payload['AddrPixelsBad']
                addrPixHot_roc[roc_pos] =  payload['AddrPixelsHot']
                n_hot_pixels_roc[roc_pos] = payload['NHotPixel']
                n_con_nonuniform_roc[roc_pos] = payload['NColNonUniform']
		grade_roc[roc_pos] = payload['Grade']

            #
            # interp
            #
            interpEffTestPoint_roc = {}
            interpEff_roc = {}
            for rate, payload1 in HighRateDataInterpRoc.iteritems():
                interpEffTestPoint_roc[rate] = {}
                interpEff_roc[rate] = {}
                for roc, payload in payload1.iteritems():
                    roc_pos = payload['RocPos']
                    print " Studying interpolation per Rate = ", rate, " and ROC=",roc_pos
                    interpEffTestPoint_roc[rate][roc_pos] = payload['InterpEffTestpoint']
                    interpEff_roc[rate][roc_pos] = payload['InterpEffTestpoint']
                    
                
            #
            # Noise
            #
            nPixelsNoise_roc = {}
            meanNoiseAllPixels_roc = {}
            widthNoiseAllPixels_roc = {}
            addrPixelNoise_roc = {}
    
            for rate, payload1 in HighRateDataAllNoiseRoc.iteritems():
                nPixelsNoise_roc [rate] = {}
                meanNoiseAllPixels_roc[rate] = {}
                widthNoiseAllPixels_roc[rate] = {}
                addrPixelNoise_roc[rate] = {}
                for roc, payload in payload1.iteritems():
                    roc_pos = payload['RocPos']
                    print " Studying Noise per Rate = ", rate, " and ROC=",roc_pos
                    nPixelsNoise_roc[rate][roc_pos] = payload['NPixelsNoise']
                    meanNoiseAllPixels_roc[rate][roc_pos] = payload['MeanNoiseAllPixels']
                    widthNoiseAllPixels_roc[rate][roc_pos] = payload['WidthNoiseAllPixels']
                    addrPixelNoise_roc[rate][roc_pos] = "%s"%payload['AddrPixelsNoise'] #['Value']
            #        
            # Aggregate (hitmap)
            #
            measuredHitRate_roc = {}
            nPixelNoHit_roc = {}
            nBinsLowHigh_roc = {}

            for rate, payload1 in HighRateDataAggrRoc.iteritems():
                measuredHitRate_roc[rate] = {}
                nPixelNoHit_roc[rate] = {}
                nBinsLowHigh_roc[rate] = {}

                for roc, payload in payload1.iteritems():
                    roc_pos = payload['RocPos']
                    print " Studying Hitmap per Rate = ", rate, " and ROC=",roc_pos
                    measuredHitRate_roc[rate][roc_pos] = payload['MeasuredHitrate']
                    nPixelNoHit_roc[rate][roc_pos] = payload['NPixelNoHit']
                    nBinsLowHigh_roc[rate][roc_pos] = payload['NBinsLowHigh']                  



            print " ======================== DEBUG ==========================="        
            print "interpEffTestPoint", interpEffTestPoint 
            print "interpEff", interpEff
            print "nPixelsNoise", nPixelsNoise
            print "meanNoiseAllPixels", meanNoiseAllPixels
            print "widthNoiseAllPixels", widthNoiseAllPixels
            print "addrPixelNoise", addrPixelNoise
            print "measuredHitRate",measuredHitRate 
            print "nPixelNoHit", nPixelNoHit
            print "nBinsLowHigh", nBinsLowHigh
            print "", 
            print "", 
            print "", 
            print " ======================== DEBUG END ======================="






                    
            #
            # Summary!
            #         
            ms = self.getModuleXrayHRTestSummaryWithTimestamp(fullmodule_id,"%s"%timestamp)
            if (ms is None):
                          if (dataTest is None):
                                dataTestTmp = Data(PFNs = "file:"+HighRateDataModule['InputTarFile'])
                                dataTest = self.insertData(dataTestTmp)
                          if (dataTest is None):
                                print"<br>Error inserting data"
                                return None
#			  print "HERE   ", sessionid, datatest.DATA_ID, LAST_PROCESSING_ID, FULLMODULE_ID, temperature, timestamp
                          t = Test_FullModule_XRay_HR_Summary(SESSION_ID=sessionid,  DATA_ID=dataTest.DATA_ID, LAST_PROCESSING_ID=0,  FULLMODULE_ID=module.FULLMODULE_ID,
                                 TEMPNOMINAL=temperature,XRAY_SLOT=-99,
                                 TIMESTAMP=timestamp,
                                 COMMENT="" )
                          ms=self.insertObject(t)
                          if ms is None  :
                                print "ERRORE XRAYHRTEST summary"
                                return None
                          self.setLastTest_XRay_HR(ms)
                          print "...DONE creating the XRAY Summary TEST"
            else:
                        print "Test HR Module found, reusing it incrementing LASTPROC"
                        ms.LAST_PROCESSING_ID+=1
                        dataTest = ms.data
                        self.store.commit()

            if dataAna is None :
                          FullAnalysisPath = HighRateDataModule['AbsFulltestSubfolder']
                          pf = str('file:'+FullAnalysisPath)
                          data = Data(PFNs=pf)
                          dataAna = self.insertData(data)
                          if (dataAna is None):
                             print"<br>Error inserting data"
                             return None

	    ana = Test_FullModule_XRay_HR_Module_Analysis_Summary(SESSION_ID=sessionid,  DATA_ID=dataAna.DATA_ID,PROCESSING_ID=ms.LAST_PROCESSING_ID,TEST_XRAY_HR_SUMMARY_ID=ms.TEST_ID,
                                 GRADE=result,
				 MACRO_VERSION=macroVersion,
                                 N_PIXEL_NO_HIT_50= nPixelNoHit.get(50, -99) ,
                                 N_PIXEL_NO_HIT_150= nPixelNoHit.get(150, -99) ,
                                 MEASURED_HITRATE_50=measuredHitRate.get(50, -99),
                                 MEASURED_HITRATE_150=measuredHitRate.get(150, -99),
				 N_BINS_LOWHIGH_50=nBinsLowHigh.get(50,-99),
				 N_BINS_LOWHIGH_150=nBinsLowHigh.get(150,-99),
				 INTERP_EFF_50=interpEff.get(50, -99),
				 INTERP_EFF_120=interpEff.get(120, -99),
				 N_COL_NONUNIFORM = n_con_nonuniform,
				 N_HOT_PIXELS = n_hot_pixels)
	    print "Done with ana mod"
            anai = self.insertObject(ana)
            results.append(anai)

	    #now loop on noise rates
            for rate, payload in HighRateDataAllNoise.iteritems():
                  print " Studying Noise per Rate = ", rate
		  noise = Test_FullModule_XRay_HR_Module_Noise( DATA_ID=dataAna.DATA_ID,PROCESSING_ID=ms.LAST_PROCESSING_ID,TEST_XRAY_HR_SUMMARY_ID=ms.TEST_ID,
                            MACRO_VERSION=macroVersion,
			    N_PIXELS_NOISE= payload['NPixelsNoise']['Value'],
		            MEAN_NOISE_ALLPIXELS= payload['MeanNoiseAllPixels'],
	                    WIDTH_NOISE_ALLPIXELS= payload['WidthNoiseAllPixels'],
			    HITRATENOMINAL=float(rate))
 		  print "Done with ana noise mod",rate
                  noisei = self.insertObject(noise)
                  results.append(noisei)

	    #Now lets do the ROCs
            for roc in addrPixBad_roc.keys():
		  anar = Test_FullModule_XRay_HR_Roc_Analysis_Summary(SESSION_ID=sessionid,  DATA_ID=dataAna.DATA_ID,PROCESSING_ID=ms.LAST_PROCESSING_ID,TEST_XRAY_HR_SUMMARY_ID=ms.TEST_ID,
                                 ROC_POS=roc,
                                 MACRO_VERSION=macroVersion,
                                 N_PIXEL_NO_HIT_50= nPixelNoHit_roc[50][roc] if 50 in nPixelNoHit_roc else -99,
                                 N_PIXEL_NO_HIT_150= nPixelNoHit_roc[150][roc] if 150 in nPixelNoHit_roc else -99,
                                 MEASURED_HITRATE_50=measuredHitRate_roc[50][roc] if 50 in measuredHitRate_roc else  -99,
                                 MEASURED_HITRATE_150=measuredHitRate_roc[150][roc] if 150 in measuredHitRate_roc else  -99,
                                 N_BINS_LOWHIGH_50=nBinsLowHigh_roc[50][roc] if 50 in nBinsLowHigh_roc else -99,
                                 N_BINS_LOWHIGH_150=nBinsLowHigh_roc[150][roc] if 150 in nBinsLowHigh_roc else -99,
                                 INTERP_EFF_50=interpEff_roc[50][roc] if 50 in interpEff_roc else  -99,
                                 INTERP_EFF_120=interpEff_roc[120][roc] if 120 in interpEff_roc else  -99,
                                 N_COL_NONUNIFORM = n_con_nonuniform_roc[roc],
                                 N_HOT_PIXELS = n_hot_pixels_roc[roc],
                                 ADDR_PIXELS_BAD="%s"%list(addrPixBad_roc[roc]),
                                 ADDR_PIXELS_HOT="%s"%list(addrPixHot_roc[roc]),
				 GRADE=grade_roc[roc]
				 )
	          print "Done with ana roc"
                  anari = self.insertObject(anar)
                  results.append(anari)


            for rate, payload1 in HighRateDataAllNoiseRoc.iteritems():
                print " ENTERING", rate
                nPixelsNoise_roc [rate] = {}
                meanNoiseAllPixels_roc[rate] = {}
                widthNoiseAllPixels_roc[rate] = {}
                addrPixelNoise_roc[rate] = {}
                for roc, payload in payload1.iteritems():
                    print " ENTERING 2 ", rate, roc
                    roc_pos = payload['RocPos']
                    print " Studying Noise per Rate = ", rate, " and ROC=",roc_pos
                    nPixelsNoise_roc[rate][roc_pos] = payload['NPixelsNoise']
                    meanNoiseAllPixels_roc[rate][roc_pos] = payload['MeanNoiseAllPixels']
                    widthNoiseAllPixels_roc[rate][roc_pos] = payload['WidthNoiseAllPixels']
		    print "Addr pixel noise", payload['AddrPixelsNoise']
                    print " before creation", roc_pos
                    noise = Test_FullModule_XRay_HR_Roc_Noise( DATA_ID=dataAna.DATA_ID,PROCESSING_ID=ms.LAST_PROCESSING_ID,TEST_XRAY_HR_SUMMARY_ID=ms.TEST_ID,
                            MACRO_VERSION=macroVersion,
			    ROC_POS=roc_pos,	
                            N_PIXELS_NOISE= payload['NPixelsNoise'],
                            MEAN_NOISE_ALLPIXELS= payload['MeanNoiseAllPixels'],
                            WIDTH_NOISE_ALLPIXELS= payload['WidthNoiseAllPixels'],
                    	    ADDR_PIXELS_NOISE= "%s"%payload['AddrPixelsNoise'], #['Value'],
			    ADDR_PIXEL_NO_HIT="", #DA TOGLIERE
#                    	    ADDR_PIXEL_NO_HIT= "%s"%payload['AddrPixelsNoise'] #['Value']
                            HITRATENOMINAL=float(rate))
                    print "Done with ana noise mod roc",rate, roc
                    noisei = self.insertObject(noise)
                    results.append(noisei)

            return results


#INSERTING XRAY INTO DB /tmp/xray/out/REV001/R001/M0000_XRayVcalCalibration_2015-02-01_12h34m_1422794101 None {'ROCsMoreThanOnePercent': None, 'minSlope': 48.171999999999997, 'QualificationType': 'XRayVcalCalibration', 'InputTarFile': None, 'minOffset': -1681.7429999999999, 'IVSlope': None, 'CycleTempLow': None, 'PHCalibration': None, 'Temperature': None, 'Hostname': 'UNKNOWN', 'CycleTempHigh': None, 'Comments': None, 'nCycles': None, 'Operator': 'UNKNOWN', 'Noise': None, 'Trimming': None, 'Vcal_Offset_Module': 55.472000000000001, 'Vcal_Slope_Module': 55.472000000000001, 'Slopes': [53.566000000000003, 60.165999999999997, 51.061, 59.375, 57.948, 57.463000000000001, 50.793999999999997, 52.689, 48.171999999999997, 55.966999999999999, 58.633000000000003, 58.619999999999997, 53.923000000000002, 50.662999999999997, 68.081999999999994, 50.426000000000002], 'AbsFulltestSubfolder': '/tmp/xray/out/REV001/R001/M0000_XRayVcalCalibration_2015-02-01_12h34m_1422794101/QualificationGroup/XrayCalibrationSpectrum_1', 'maxOffset': 127.083, 'ModuleID': 'M0000', 'TestCenter': 'UNKNOWN', 'maxSlope': 68.081999999999994, 'initialCurrent': None, 'Offsets': [-475.48700000000002, -790.88900000000001, 5.5330000000000004, -802.52099999999996, -484.28899999999999, -425.40300000000002, -188.99700000000001, -141.07300000000001, 127.083, -457.90600000000001, -632.15999999999997, -766.46100000000001, -616.27700000000004, -108.502, -1681.7429999999999, -276.50299999999999], 'Grade': None, 'AbsModuleFulltestStoragePath': '/tmp/xray/out/REV001/R001/M0000_XRayVcalCalibration_2015-02-01_12h34m_1422794101', 'avrgSlope': 55.471750000000007, 'FulltestSubfolder': 'QualificationGroup/XrayCalibrationSpectrum_1', 'CurrentAtVoltage150V': None, 'RelativeModuleFinalResultsPath': 'out/REV001/R001/M0000_XRayVcalCalibration_2015-02-01_12h34m_1422794101', 'PixelDefects': None, 'TestDate': '1422794101', 'MacroVersion': None, 'avrgOffset': -482.22468750000002, 'TestType': 'XrayCalibration_Spectrum'}

      def insertTestXRayVCal(self,sessionid,Row,overwritemodid=0):
            print "*Xray Vcal DB insert*************************"
            print "ROW XRAY", Row
            modulename = unicode(Row['ModuleID'])
	    module = self.getFullModule(modulename)
	    if module is None :
		  print "Cannot insert on non existing module",modulename
		  return None
            timestamp = Row['TestDate']
     #       TestType = Row['TestType']
	    temperature = -99
	    try :	
		temperature = float(Row['Temperature'])
	    except :
		print "Cannot converte temperature " , Row['Temperature']
            print "asking for a module test with" ,modulename ,timestamp
            ttt = self.getXrayVcalTestWithTimestamp(modulename,timestamp)
	    if (ttt is None):
                  print "CREATE XRAY VCAL Test"
	          data2 = Data(PFNs = "file:"+Row['InputTarFile'])
	          data2i = self.insertData(data2)
        	  if (data2i is None):
                	  print"<br>Error inserting data"
	                  return None
		  t = Test_FullModule_XRay_Vcal(SESSION_ID=sessionid, TARGET="", DATA_ID=data2i.DATA_ID, LAST_PROCESSING_ID=0,  FULLMODULE_ID=module.FULLMODULE_ID,
				 XRAY_SLOT=0,#fixme
				 HITRATENOMINAL=0,
				 TEMPNOMINAL=temperature,
				 TIMESTAMP=timestamp,
		                 RESULT="", COMMENT=Row["Comments"])
                  pp=self.insertObject(t)

                  if pp is None:
                        print "ERRORE XRAYVCALTEST"
                        return None

#
# set lasttest_xray_vcal in the inventory
#
                  self.setLastTest_XRay_VCAL(t)
#

                  print "...DONE creating the XRAY VCAL TEST"
                  ttt=pp
	    else:
		print "Test Vcal Module found, reusing it incrementing LASTPROC"
	    ttt.LAST_PROCESSING_ID+=1
	    self.store.commit()
            print "Now doing the analysis"
	    FullAnalysisPath = Row['AbsFulltestSubfolder']
            pf = str('file:'+FullAnalysisPath)
	    data = Data(PFNs=pf)
	    datai = self.insertData(data)
            if (datai is None):
                     print"<br>Error inserting data"
                     return None
	    print "Creating ana"
	    #print sessionid,ttt.TEST_ID,datai.DATA_ID,"",ttt.LAST_PROCESSING_ID,Row["MacroVersion"],Row["avrgSlope"],Row["avrgOffset"]

	    ana=Test_FullModule_XRay_Vcal_Module_Analysis(SESSION_ID=sessionid,
			 FULLMODULETEST_ID=ttt.TEST_ID,
			 DATA_ID=datai.DATA_ID,
			 TARGET="", #fixme
			 PROCESSING_ID=ttt.LAST_PROCESSING_ID,
			 MACRO_VERSION=Row["MacroVersion"],
			 SLOPE=Row["avrgSlope"],
			 OFFSET=Row["avrgOffset"],
			 TARGET_HIT_RATE=-1, #fixme 
			 GRADE="" #fixme
			)
	    print "Done with ana"
	    anai = self.insertObject(ana)
  	    return anai
	


#
# methods to have automatic insert by moreweb
#

# Row is something like
# ROW  {'QualificationType': 'FullQualification', 'Temperature': '-10', 'PHCalibration': '0', 'CycleTempHigh': None, 'Comments': '', 'nCycles': None, 'CurrentAtVoltage150': 0, 'initialCurrent': 0, 'Noise': '0', 'nTrimDefects': '5', 'nMaskDefects': '0', 'nDeadPixels': '1', 'nBumpDefects': '3', 'nGainDefPixels': '0', 'Trimming': '5', 'TestType': 'm10_1', 'ROCsMoreThanOnePercent': '0', 'IVSlope': 0, 'CycleTempLow': None, 'nPedDefPixels': '0', 'StorageFolder': '../../../../../../data/pixels/FTTEST/OUT/M0823/1.1/M0823_FullQualification_2013-05-31_14h38m_1370003934/M0823_FullQualification_2013-05-31_14h38m_1370003934', 'nNoisyPixels': '0', 'RelativeModuleFulltestStoragePath': 'FinalResults/QualificationGroup/ModuleFulltest_m10_1', 'ModuleID': 'M0823', 'Grade': 'B', 'nPar1DefPixels': '0', 'PixelDefects': '1', 'TestDate': '1370003934'}
             
      
      

      def insertTestFullModuleDirPlusMapv96Plus(self,sessionid,Row,overwritemodid=0):
            #
            # tries to open a standard dir, as in the previous above
            # searches for summaryTest.txt inside + tars the dir in add_data
            #
            print "***************************"
            #
            # tryng to get if I already have this
            #
            print "ROOOW", Row
            modulename = Row['ModuleID']
            print "***************************"
            tempnominal2 = Row['Temperature']
            print "***************************"
            ck ='0000'
            print "***************************"
            timestamp = Row['TestDate']
            TestType = Row['TestType']
            QualificationType = Row['QualificationType']
            print "asking for a module test with" ,modulename, ck, TestType,timestamp,QualificationType
            ttt = self.getFullModuleTestWithCkSumAndTimestampAndType(modulename, ck, TestType,timestamp,QualificationType)

            if (ttt is None) :
                  print "NEW MODULE TEST"
            else:
                  print "OLD MODULE TEST"

#
# Parse Row and extract stuff
#

            ModuleNumber=modulename
            Grade=Row['Grade']
            isThermalCycling=Row['nCycles']
            if (isThermalCycling is None):
                  isThermalCycling = 1
            ThermalCyclingHigh=Row['CycleTempHigh']
            if (ThermalCyclingHigh is None):
                  ThermalCyclingHigh = 0
            ThermalCyclingLow=Row['CycleTempLow']
            if (ThermalCyclingLow is None):
                  ThermalCyclingLow = 0
#defects

            DeadPixels = Row['nDeadPixels']
            MaskPixels= Row['nMaskDefects']
            BumpPixels= Row['nBumpDefects']
            TrimPixels= Row['nTrimDefects']
# caveat
            AddressPixels = -10
            NoisyPixels = Row['nNoisyPixels']
# caveat    
            TreshPixels = -10
            GainPixels = Row['nGainDefPixels']

            PedPixels = Row['nPedDefPixels']
            ParPixels = Row['nPar1DefPixels']

            PHCalibration = Row['PHCalibration']
#caveat missing + unit of measurement
            I150 = Row['CurrentAtVoltage150V']
            I1502 = -10
            Current = Row['initialCurrent']
#caveat missing
            Current2 = -10
            I150I100 = Row['IVSlope']
            Temp = Row['Temperature']
#caveat
            eTemp = -10

            
            ROCsMoreThanOnePercent = Row['ROCsMoreThanOnePercent']
            Trimming = Row['Trimming']

            Comments = Row['Comments']


#
# produce a link to the real results
#

 #
# what is pixel defects????
#
            PixelDefects = Row['PixelDefects']
#
# try and build a FullModuleTest_analysis
#


#PATHS
            FullAnalysisPath = Row['AbsFulltestSubfolder']
            InputTarFile = Row['InputTarFile']
            FullSummaryPath = Row['AbsModuleFulltestStoragePath']
            Macro_version = Row['MacroVersion']
            #
            # create a data_id
            #


            pf = str('file:'+FullAnalysisPath)
            data = Data(PFNs=pf)
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

            QualificationType = Row['QualificationType']            

            pp=self.insertFullModuleTestSession(fmsession)
            if pp is None:
                  print "ERRORE FMSESSION", fmsession.TEST_ID
                  

            print "session inserted",InputTarFile

            # step #2 : create a test
            data2 = Data(PFNs = "file:"+InputTarFile)
            pp = self.insertData(data2)
            if (pp is None):
                  print"<br>Error inserting data"
                  return None


            if (ttt is None):
                  print "CREATE FMT"
                  t = Test_FullModule(SESSION_ID=fmsession.TEST_ID,
                                      FULLMODULE_ID=ppp,
                                      DATA_ID = data2.DATA_ID,
                                      TEMPNOMINAL=unicode(TestType),
                                      COLDBOX="dummy",COLDBOX_SLOT="dummy",CKSUM=ck,TIMESTAMP=timestamp,
                                      RESULT = "n/a",TYPE=QualificationType)

                  pp=self.insertFullModuleTest(t)
                  if pp is None:
                        print "ERRORE FMTEST"
			return None
                  print "...DONE"
                  t=pp
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
                                                 IVSLOPE=I150I100,PHCAL=PHCalibration,
                                                 CYCLING=isThermalCycling,
                                                 TEMPVALUE=Temp,
                                                 TEMPERROR=eTemp,
                                                 COMMENT=Comments,
                                                 PIXELDEFECTS=PixelDefects,
                                                 TCYCLHIGH=ThermalCyclingHigh,
                                                 TRIMMING=Trimming, ROCSWORSEPERCENT=ROCsMoreThanOnePercent,
                                                 TCYCLLOW=ThermalCyclingLow,
                                                 MACRO_VERSION=Macro_version)
                  
            print "ECCOMI" 
                  
            rr = self.insertFullModuleTestAnalysis(fmanalysis)
            if (rr is None):
                  print"<br>Error inserting test FM"
                  return None
                  
            print "CREATE FMA ... done"
	    print "Update FMT LASTANALYSIS_ID with ", fmanalysis.TEST_ID
	    t.LASTANALYSIS_ID=fmanalysis.TEST_ID
	    self.store.commit()
            #
            #                create or search a session, based on dirname
            #
            

            print " ECCO CHE PROVO A TROVARE IL SUMMARY", InputTarFile
            matchstring = InputTarFile
            print "uso come stringa" , matchstring

#            summ = self.searchFullModuleTestSummaryByDirName(path)
            summ = self.searchFullModuleTestSummaryByDirName(matchstring)
	    print t.SUMMARY_ID
            if summ is None and t.SUMMARY_ID is not 0:
		     print "AIUTO IL SUMMARY ERA VUOTO MA FULLMODULE GIA NE AVEVA UNO, USO QUELLO"
		     summ=self.store.find(Test_FullModuleSummary,Test_FullModuleSummary.TEST_ID==t.SUMMARY_ID).one()
		     print "CHE TRA L'ALTRO e':",summ
            if (summ is None):
                  print "create new FMSummary"
                  dataS = Data(PFNs = 'file:'+InputTarFile)
                  pp = self.insertData(dataS)
                  print "paperino"

                  summary = Test_FullModuleSummary(FULLMODULE_ID=ppp,DATA_ID=dataS.DATA_ID, QUALIFICATIONTYPE=QualificationType,TIMESTAMP=timestamp)
                  print "LLLLLLLLLLLLL ",ppp,dataS.DATA_ID
#                  summary = Test_FullModuleSummary(FULLMODULE_ID=unicode(ppp),DATA_ID=(dataS.DATA_ID))
                  print "paperino2"

                  pp = self.insertFullModuleTestSummary(summary)
		  pippo=self.updateLastTestFullModule(ppp,summary.TEST_ID,QualificationType,summary.TIMESTAMP)
		  if (pippo is None):
			print "CANNOT UPDATE LAST SUMMARY IN INVENTORY FOR",ppp	
                  summary = pp
            else:
                  summary = summ
                  print " SUMM ", summ
                  #
                  # fill the correct one
                  #
            print "riempio SUMMARY con ",summary.TEST_ID
#
# I want the test_fullmodule to know the summary
#
            self.insertSummaryIdIntoFullModuleTest(t.TEST_ID, summary.TEST_ID)
#
# now I search in the "names" to see if I find one
#

            thistype=t.__class__.__name__


            res = summary.findObjectFromCommaSeparatedList(summary.FULLMODULETEST_NAMES,TestType);

            print " RES is ", res, thistype, t.TEST_ID
            if (res is None):
                  # it is new, I insert
                  self.insertFullModuleSummaryNewTest(summary,TestType,thistype, t.TEST_ID)
            else:
                  print " I REFUSE TO FILL  THE SUMMARY WITH ",summary.FULLMODULETEST_NAMES,TestType
            

            self.store.commit()
            
            return rr     
            
             
	  
      def updateLastTestFullModule(self,moduleId,summaryId, newType, newDate):
	  fm=self.getFullModule(unicode(moduleId))
	  if fm is None :
	     return None
	  if newType == "FullQualification" :
	     if fm.LASTTEST_FULLMODULE != 0 and fm.LASTTEST_FULLMODULE != None and fm.lasttest != None:
  		prevSummary=fm.lasttest
		prevDate=prevSummary.TIMESTAMP
 		if prevDate < newDate :
		  fm.LASTTEST_FULLMODULE=summaryId
		  self.store.commit()	
	     else:
                  fm.LASTTEST_FULLMODULE=summaryId
	          self.store.commit()
	  elif newType == "Reception" :
             if fm.LASTTEST_RECEPTION != 0 and fm.RECEPTION != None and fm.lasttest_reception != None:
                prevSummary=fm.lasttest_reception
                prevDate=prevSummary.TIMESTAMP
                if prevDate < newDate :
	           fm.LASTTEST_RECEPTION=summaryId
                   self.store.commit()   
	     else :
	           fm.LASTTEST_RECEPTION=summaryId
                   self.store.commit()   

	  else :
             if fm.LASTTEST_OTHER != 0 and fm.LASTTEST_OTHER != None and fm.lasttest_other != None:
                prevSummary=fm.lasttest_other
                prevDate=prevSummary.TIMESTAMP
                if prevDate < newDate :
	         fm.LASTTEST_OTHER=summaryId
                 self.store.commit()   
   	     else:
	         fm.LASTTEST_OTHER=summaryId
                 self.store.commit()   
	
          return fm 

       
      def insertRocTestsFromDir(self,sessionid,filename, filenamePS, createROC=False):
            DEBUG=1
            if DEBUG==1:
                  print "working on FileName ",filename,filenamePS
#
# lines are like
#WAFER     POS  PX PY BIN C GR  IDIG0 IANA0 IDIGI IANAI VDREG VDAC  IANA V24  BLLVL ADSTP  DC DD WB TS DB DP  DPIX ADDR TRIM MASK NSIG NOIS THRO T2F T2P  PCNT PMEAN  PSTD PMCOL PMI PMA   NPH PHFAIL PHOMEAN PHOSTD PHGMEAN PHGSTD  FAIL  FAILSTRING
#K7NEF6T   03C   7  1  0  1  1   23.0   0.4  26.0  19.5  2.05 1.92  23.9 156    4.4  86.0   0  0  0  0  0  0     0    0    0    0    0    0    0          4160  72.8  2.69  1.03  66  85  4160      0    -6.3   17.0   172.2    6.1    23 
#with fixed width fields
            
            file = open(filename)
            x=0
            y=0
            delimiters = []
            for line in file :
                  #  print line
                  fields=  re.split('\W+',line)
                  if len(fields) > 0 and fields[0] == "WAFER" :
                        for field in fields : 
                              x=y
                              y+=re.search(field,line[y:len(line)]).start(0)+len(field)
                              if y == 5 :
                                    y+=2 # fix bad alignment in first column
                              delimiters.append([x,y])
                  else:
                        fields = [line[x:y] for (x,y) in delimiters]
                        if len(fields) > 15 and re.match(" *[0-9][0-9][A-D]",fields[1]): 
                              wafer=re.sub(" ","",fields[0])
                              pos=re.sub(" ","",fields[1])
                              grade=re.sub(" ","",fields[5])
                              idigi =re.sub(" ","", fields[9])
                              iana =re.sub(" ","", fields[13])
                              vdac =re.sub(" ","", fields[12])
                              v24 = re.sub(" ","", fields[14])
                              defpixel = re.sub(" ","", fields[23])
                              addpixel = re.sub(" ","", fields[24])
                              trimpixel = re.sub(" ","", fields[25])
                              maskpixel = re.sub(" ","", fields[26])
                              nsigpixel = re.sub(" ","", fields[27])
                              noisepixel = re.sub(" ","", fields[28])
                              thpixel = re.sub(" ","", fields[29])
                              phfail = re.sub(" ","", fields[39])
                              comment = (" ".join(fields[45:] )).rstrip()
                              if (DEBUG==1):
                                    print "ROC_ID",wafer+"-"+pos, "RESULT",grade,"CURRENT_D",idigi, "CURRENT_A",iana, "VDAC", vdac,   "DEFECTPIXELS", defpixel,"ADDRPIXEL",addpixel, "TRIMP", trimpixel, "MASKPIXEL",maskpixel,"NSIGPIXEL", nsigpixel, "NOISEPIXEL", noisepixel, "THRESHPIXEL", thpixel, "PHFAIL", phfail, "COMMENT", comment 

                              data = Data(PFNs = ('file:'+filenamePS+',file:'+filename))
                              pp = self.insertData(data)
                              if (pp is None):
                                    print "Cannot insert data"
                                    return None

                              testROC = Test_Roc(SESSION_ID=sessionid, ROC_ID=wafer+"-"+pos, RESULT=grade, DATA_ID=data.DATA_ID, IANA = iana, IDIGI=idigi, V24 =v24, VDAC=vdac,  DEFECTPIXELS=defpixel, ADDRPIXELS=addpixel, TRIMPIXELS=trimpixel, MASKPIXELS=maskpixel, NSIGPIXELS=nsigpixel, NOISEPIXELS=noisepixel, THRESHOLDPIXELS=thpixel, PHFAIL=phfail, COMMENT=comment)
                              aaa = self.insertRocTest(testROC)
                              if (aaa is None):
                                    print "Error inserting ROC TEST"
                                    return None
                              return aaa
