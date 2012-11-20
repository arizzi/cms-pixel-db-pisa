from Objects import *
from MySQLdb import *
from storm.locals import *
import string
import subprocess

class PixelDBInterface(object) :

      def __init__(self, operator, center, datee =date.today() ) :
            self.operator = operator
            self.center =  center
            self.date = datee
            
      def connectToDB(self) :
            self.database = create_database("mysql://tester:pixels@cmspixelsvc/test_pixel")
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
      
      def joinObjects(self, arrayofrocids):
            return string.join(arrayofrocids,",")
      def splitObjects(self, pp):
            return string.split(pp,",")
#
#
#
      def assembleBareModule(self, baremodule_id, roc_ids,  sensor_id, builtby, transfer_id=0):
            #
            # check if all the objects are already in DB
            #
            if (self.canSensorBeUsed(sensor_id) == False):
                  print "ERROR: sensor not available", sensor_id
                  return None
            
            for i in roc_ids:
                  if (self.canRocBeUsed(i) == False):
                        print "ERROR: roc not available", i
                        return None
            #
            
            if (transfer_id ==0):
                  # creo un transfer
                  tr = self.insertTransfer(Transfer(SENDER="",RECEIVER=self.operator, ISSUED_DATE= datetime(1970,1,1), RECEIVED_DATE=self.date, STATUS="ARRIVED"))
                  self.insertTransfer(tr)
                  transfer_id=tr.TRANSFER_ID
            newbm = BareModule(BAREMODULE_ID=baremodule_id, ROC_ID=self.joinObjects(roc_ids), SENSOR_ID=sensor_id, TRANSFER_ID=transfer_id,BUILTBY=builtby)
            self.setSensorStatus(sensor_id,"USED")
            for i in roc_ids:
                  self.setRocStatus(i,"USED")
            self.store.add(newbm)
            self.store.commit()
            # log in history sensor
            self.insertHistory(type="SENSOR", id=sensor_id, target_type="BAREMODULE", target_id=baremodule_id, operation="ASSEMBLE", datee=date.today(), comment="NO COMMENT")
            # log in history rocs
            for i in roc_ids:
                  self.insertHistory(type="ROC", id=i, target_type="BAREMODULE", target_id=baremodule_id, operation="ASSEMBLE", datee=date.today(), comment="NO COMMENT")
            
            return newbm
            
            
      def insertHistory(self, type, id, target_type, target_id, operation, datee=date.today(), comment=""):
            newHist=History(type, id, target_type, target_id, operation, datee, comment)
            self.store.add(newHist)
            self.store.commit()            
            return newHist

      def assembleFullModule(self, fullmodule_id, baremodule_id, tbm_id, hdi_id,  builtby, builton=date.today(),comment="",transfer_id=0):
            #
            # check if all the objects are already in DB
            #
            if (self.canBareModuleBeUsed(baremodule_id) == False):
                  print "ERROR: baremodule not available", baremodule_id
                  return None
	    if (self.canTbmBeUsed(tbm_id) == False):
                  print "ERROR: tbm not available",tbm_id
                  return None
	    if (self.canHdiBeUsed(unicode(hdi_id)) == False):
                  print "ERROR: hdi not available",hdi_id
                  return None

            #
            if (transfer_id ==0):
                  # creo un transfer
                  tr = self.insertTransfer(Transfer(SENDER="",RECEIVER=self.operator, ISSUED_DATE= datetime(1970,1,1), RECEIVED_DATE=self.date, STATUS="ARRIVED"))
                  self.insertTransfer(tr)
                  transfer_id=tr.TRANSFER_ID
            newfm = FullModule(FULLMODULE_ID=fullmodule_id, BAREMODULE_ID=baremodule_id, HDI_ID=hdi_id, TBM_ID=tbm_id,TRANSFER_ID=transfer_id, BUILTBY=builtby, BUILTON=builton, COMMENT=comment)
            self.setBareModuleStatus(baremodule_id,"USED")
            self.setHdiStatus(hdi_id,"USED")
            self.setTbmStatus(tbm_id,"USED")
            self.store.add(newfm)
            self.store.commit()
            # log in history 
            self.insertHistory(type="BAREMODULE", id=baremodule_id, target_type="FULLMODULE", target_id=fullmodule_id, operation="ASSEMBLE", datee=date.today(), comment="NO COMMENT")
            self.insertHistory(type="HDI", id=hdi_id, target_type="FULLMODULE", target_id=fullmodule_id, operation="ASSEMBLE", datee=date.today(), comment="NO COMMENT")
            self.insertHistory(type="TBM", id=tbm_id, target_type="FULLMODULE", target_id=fullmodule_id, operation="ASSEMBLE", datee=date.today(), comment="NO COMMENT")
            return newfm
            
#
# check methods 
#
      def isSensorInserted(self, sensor_id):
            temp=unicode(sensor_id)
            aa = self.store.find(Sensor, Sensor.SENSOR_ID==temp).one()
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
            if (self.isRocInserted(roc_id) == False):
                  return False
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
      def insertFullModuleTest(self, test_fm):
            #
            # first check that the module exists
            #
            if (self.isFullModuleInserted(test_fm.FULLMODULE_ID) == False):
                  print " Cannot insert a test on a not existing FM "
                  return None
            self.store.add(test_fm)
            self.store.commit()
            (self.getFullModule(test_fm.FULLMODULE_ID)).LASTTEST_FULLMODULE =  test_fm.TEST_ID
            self.store.commit()
            # log in history
            self.insertHistory(type="TEST_FM", id=test_fm.TEST_ID, target_type="FULLMODULE", target_id=test_fm.FULLMODULE_ID, operation="TEST", datee=date.today(), comment="NO COMMENT")
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
            if (self.isInserted(test.SENSOR_ID) == False):
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
            if (self.isInserted(test.HDI_ID) == False):
                  print " Cannot insert a test on a not existing HDI "
                  return None
            self.store.add(test)
            self.store.commit()
            (self.getHdi(test.HDI_ID)).LASTTEST_HDI =  test.TEST_ID
            self.store.commit()
            # log in history
            self.insertHistory(type="TEST_HDI", id=test.TEST_ID, target_type="HDI", target_id=test.HDI_ID, operation="TEST", datee=date.today(), comment="NO COMMENT")
            return test

      def insertHdiTest(self, test):
            #
            # first check that the module exists
            #
            if (self.isInserted(test.HDI_ID) == False):
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
            if (self.isInserted(test.TBM_ID) == False):
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
#
#

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
            p = subprocess.Popen("php prodTable.php "+fileName, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            retval = p.wait()
            if (retval!=0):
                  return None
            fileContent = []
            for line in p.stdout.readlines():
                  fileContent.append( line )
                  #
                  # parse it
                  #
                  for line in fileContent:
                     fields = (line.strip()).split(" ")
                     #
                     # real parsing
                     #
                     if (fields[0] == 'module'):
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

                     if (fields[0] == 'finalGrade'):
                       FinalGrade = fields[1]
                     if (fields[0] == 'fullGrade'):
                      FulltestGrade = fields[1]
                     if (fields[0] == 'grade'):
                        Grade = fields[1]
                     if (fields[0] == 'shortGrade'):
                        ShorttestGrade = fields[1]

                     if (fields[0] == 'rocs'):
                        RocDefects = string.join(fields[1:]," ")


                     if (fields[0] == 'date'):
                        Date = string.join(fields[1:]," ")
                     if (fields[0] == 'trimming'):
                        isTrimming = fields[1]
                     if (fields[0] == 'phcal'):
                        isphCal = string.join(fields[1:]," ")

                     if (fields[0] == 'noise'):
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
 
                     if (fields[0]=='tcy'):
                      isThermalCycling=fields[1]
                     if (fields[0]=='tcycl'):
                      TThermalCycling=fields[1]

                     if (fields[0]=='etcycl'):
                      eTThermalCycling=fields[1]

                     if (fields[0] == 'mount'):
                      position=fields[1]
                     if (fields[0] == 'testN'):
                      TestNumber=fields[1]


            #
            # create a data_id
            #
            #
            #
            # create a Test_FullModule
            #
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
            t = Test_FullModule(SESSION_ID=sessionid,
                                FULLMODULE_ID=ppp,
                                RESULT=33,
                                DATA_ID=pp.DATA_ID,
                                ROCSWORSEPERCENT=RocDefects,
                                NOISE=NOISE,
                                TRIMMING =isTrimming,
                                PHCAL = isphCal,
                                IVSLOPE  = float(I150I100),
                                GRADE=Grade,
                                FINALGRADE=FinalGrade,
                                SHORTTESTGRADE=ShorttestGrade,
                                FULLTESTGRADE=FulltestGrade,
                                TESTNAME=TestNumber,
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
                                COMMENT= Comment,
                                TEMPVALUE=Temp,
                                TEMPERROR=eTemp,
                                TCYCLVALUE=TThermalCycling,
                                TCYCLERROR=eTThermalCycling)
            rr = self.insertFullModuleTest(t)
            if (rr is None):
                  print"<br>Error inserting test FM"
                  return None
            return rr
                  
                  
      #
      # cosa manca?
      #
