from Objects import *
from MySQLdb import *
from storm.locals import *
import string

class PixelDBInterface(object) :

      def __init__(self, operator, center, datee =date.today() ) :
            self.operator = operator
            self.center =  center
            self.date = datee
            
      def connectToDB(self) :
            self.database = create_database("mysql://tester:pixels@cmspisa001/test_pixel")
            self.store = Store(self.database)
            
      def insertTransfer(self,transfer):
            self.store.add(transfer)
            self.store.commit()
            return transfer
    
      def insertSensor(self,sensor) :
            self.store.add(sensor)
            self.store.commit()
            # log in history
            self.insertHistory(type="NULL", id=0, target_type="SENSOR", target_id=sensor.SENSOR_ID, operation="INSERT", datee=date.today(), comment="SPERIAMO BENE")
            return sensor
      
      def insertRoc (self, roc):
            self.store.add(roc)
            self.store.commit()
            # log in history
            self.insertHistory(type="NULL", id=0, target_type="ROC", target_id=roc.ROC_ID, operation="INSERT", datee=date.today(), comment="SPERIAMO BENE")
            return roc

      def insertTbm (self, tbm):
            self.store.add(tbm)
            self.store.commit()
            # log in history
            self.insertHistory(type="NULL", id=0, target_type="TBM", target_id=tbm.TBM_ID, operation="INSERT", datee=date.today(), comment="SPERIAMO BENE")
            return roc

      def insertHdi (self, hdi):
            self.store.add(hdi)
            self.store.commit()
            # log in history
            self.insertHistory(type="NULL", id=0, target_type="HDI", target_id=hdi.HDI_ID, operation="INSERT", datee=date.today(), comment="SPERIAMO BENE")
            return roc      
      
      def joinRocs(self, arrayofrocids):
            print"ECCO ", arrayofrocids
            return string.join(arrayofrocids,",")
      
      def assembleBareModule(self, baremodule_id, roc_ids,  sensor_id, builtby, transfer_id=0):
            #
            # check if all the objects are already in DB
            #
            if (self.isSensorInserted(sensor_id) == False):
                  print "ERROR: sensor not existing", sensor_id
		  return 
            for i in roc_ids:
                  if (self.isRocInserted(i) == False):
                        print "ERROR: roc not existing", i
			return
            #
            
            if (transfer_id ==0):
                  # creo un transfer
                  tr = self.insertTransfer(Transfer(SENDER="",RECEIVER=self.operator, ISSUED_DATE= datetime(1970,1,1), RECEIVED_DATE=self.date))
                  self.insertTransfer(tr)
                  transfer_id=tr.TRANSFER_ID
            newbm = BareModule(BAREMODULE_ID=baremodule_id, ROC_ID=self.joinRocs(roc_ids), SENSOR_ID=sensor_id, TRANSFER_ID=transfer_id,BUILTBY=builtby)
            self.store.add(newbm)
            self.store.commit()
            # log in history sensor
            self.insertHistory(type="SENSOR", id=sensor_id, target_type="BAREMODULE", target_id=baremodule_id, operation="ASSEMBLE", datee=date.today(), comment="SPERIAMO BENE")
            # log in history rocs
            for i in roc_ids:
                  self.insertHistory(type="ROC", id=i, target_type="BAREMODULE", target_id=baremodule_id, operation="ASSEMBLE", datee=date.today(), comment="SPERIAMO BENE")
            
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
            if (self.isBareModuleInserted(baremodule_id) == False):
                  print "ERROR: baremodule not existing", baremodule_id
		  return
	    if (self.isTbmInserted(tbm_id) == False):
                  print "ERROR: tbm not existing",tbm_id 
		  return
	    if (self.isHdiInserted(hdi_id) == False):
                  print "ERROR: hdi not existing",hdi_id
                  return
            #
            if (transfer_id ==0):
                  # creo un transfer
                  tr = self.insertTransfer(Transfer(SENDER="",RECEIVER=self.operator, ISSUED_DATE= datetime(1970,1,1), RECEIVED_DATE=self.date))
                  self.insertTransfer(tr)
                  transfer_id=tr.TRANSFER_ID
            newfm = FullModule(FULLMODULE_ID=fullmodule_id, BAREMODULE_ID=baremodule_id, HDI_ID=hdi_id, TBM_ID=tbm_id,TRANSFER_ID=transfer_id, BUILTBY=builtby, BUILTON=builton, COMMENT=comment)
            self.store.add(newfm)
            self.store.commit()
            # log in history 
            self.insertHistory(type="BAREMODULE", id=baremodule_id, target_type="FULLMODULE", target_id=fullmodule_id, operation="ASSEMBLE", datee=date.today(), comment="SPERIAMO BENE")
            self.insertHistory(type="HDI", id=hdi_id, target_type="FULLMODULE", target_id=fullmodule_id, operation="ASSEMBLE", datee=date.today(), comment="SPERIAMO BENE")
            self.insertHistory(type="TBM", id=tbm_id, target_type="FULLMODULE", target_id=fullmodule_id, operation="ASSEMBLE", datee=date.today(), comment="SPERIAMO BENE")
            return newfm
            
#
# check methods 
#
      def isSensorInserted(self, sensor_id):
            aa = self.store.find(Sensor, Sensor.SENSOR_ID==sensor_id).one()
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
            temp=unicode(hdi_id)
            aa = self.store.find(Hdi, Hdi.HDI_ID==temp).one()
            return aa is not None

      def isBareModuleInserted(self, BareModule_id):
            temp=unicode(BareModule_id)
            aa = self.store.find(BareModule, BareModule.BAREMODULE_ID==temp).one()
            return aa is not None

      def isFullModuleInserted(self, FullModule_id):
            aa = self.store.find(FullModule, FullModule.BAREMODULE_ID==FullModule_id).one()
            return aa is not None
#
#
#
             
      
