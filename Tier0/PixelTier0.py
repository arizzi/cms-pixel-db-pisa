from ObjectsTier0 import *
from MySQLdb import *
from storm.locals import *
import string
import subprocess
import os.path
import ConfigParser




class PixelTier0 (object):
      def __init__() :
            self.date = date.today()
            self.MACRO_VERSION='null'
            self.MACRO_LOCATION='null'
            self.MACRO_PROCESSEDPREFIX='null'

            self.EXE='null'
            self.MAXEXE=1

            self.RUNNING=0
            self.RUNNINGINSTANCES = []

      def ConfigSectionMap(self, section):
            dict1 = {}
            options = self.Config.options(section)
            for option in options:
                  try:
                        dict1[option] = self.Config.get(section, option)
                        if dict1[option] == -1:
                              DebugPrint("skip: %s" % option)
                  except:
                        print("exception on %s!" % option)
                        dict1[option] = None
            return dict1

      def initProcessing(self, config):
            self.Config = ConfigParser.ConfigParser()
            self.Config.read(config)
            #
            # force the presence of the fields
            #
            self.MACRO_VERSION = self.ConfigSectionMap("MACRO")['VERSION']
            self.MACRO_VERSIONLOCATION = self.ConfigSectionMap("MACRO")['LOCATION']
            self.EXE =  self.ConfigSectionMap("EXECUTION")['SCRIPT'] # assumes invocation via self.EXE $tarfile
            self.MAXEXE=self.ConfigSectionMap("EXECUTION")['MAXINSTANCES'] 
            self.PROCESSEDPREFIX=self.ConfigSectionMap("EXECUTION")['PROCESSEDPREFIX'] 
            if (self.MACRO_VERSION=='null' or self.MACRO_LOCATION=='null' or self.EXE=='null' or self.PROCESSEDPREFIX == 'null'):
                  print "Config file NOT ok"
                  exit(1)
                  


      def connectToDB(self,string = "mysql://tester:pixels@cmspixel.pi.infn.it/test_tier0") :
            self.database = create_database(string)
            self.store = Store(self.database)            

      def insertHistory(self, TYPE, TAR_ID, DIR_ID, RUN_ID,  DATE=date.today(), COMMENT):
            newHist=History(TYPE, TAR_ID, DIR_ID, RUN_ID,  DATE, COMMENT)
            self.store.add(newHist)
            self.store.commit()
            return newHist

      def insertNewTar(self, tar):
            #
            # check if it can be inserted
            #
            othertar = self.getInputTarByName(tar.NAME)
            if (othertar is not None):
                  print " An Input Tar with same name: ",tar.NAME, " is already present - exiting"
                  return None
            
            self.InsertHistory(TYPE = 'insert', TAR_ID=tar.TAR_ID, DIR_ID=0, RUN_ID=0,  DATE=date.today(), 'new tar insertion')
            self.store.add(tar)
            self.store.commit()
            return tar


      def processInputTar(self,tar):
            #
            # CHECK if there is already a processing for this 
            #
            if (tar.STATUS != 'new'):
                  print 'Failed to process TAR with name=',tar.NAME,' and id=',tar.TAR_ID,'since status is ',tar.STATUS
                  return None
            #
            # launch a processing run on this
            #
            
            #
            # first, lock the status of the InputTar
            #
            self.setInputStatus(tar,'processing')
            # create a processingRUN
            pr = self.injectProcessingRunFromInputTar(tar)
            
            if (pr is None) :
                  print 'Failed to inject a ProcessingRun for tar_id=', tar.TAR_ID, ' name=',tar.NAME
                  return None
            self.InsertHistory(TYPE = 'insert', TAR_ID=0, DIR_ID=0, RUN_ID=pr.RUN_ID,  DATE=date.today(), 'new processing insertion')
            
            return pr


      def injectProcessingRunFromInputTar (self,tar):
            pr = ProcessingRun(MACRO_VERSION = self.MACRO_VERSION, EXECUTED_COMMAND = self.EXE, EXIT_CODE = -1, # temporary
                               MACRO_LOCATION = self.MACRO_LOCATION,STATUS="injected", DATE=date.today(), TAR_ID=tar.TAR_ID,PROCESSED_DIR_ID = 0)
            self.store.add(pr)
            self.store.commit()
            return pr
            


      def insertProcessedDir(self,     run,tar
                             NAME,
                             STATUS,
                             UPLOAD_TYPE,
                             UPLOAD_STATUS,
                             UPLOAD_ID,
                             DATE = date.today()):
            if (run.STATUS != "done" and run.STATUS != "failed"):
                  print "Cannot inserte a dir from a processing still in state=",run.STATUS
                  return None
            if (tar.STATUS != "processed"):
                  print "Cannot insert a dir from a inputtar still in state=",tar.STATUS
                  return None
            pd = ProcessedDir (
                  NAME=NAME,
                  DATE = DATE,
                  STATUS = STATUS,
                  UPLOAD_TYPE = UPLOAD_TYPE,
                  UPLOAD_STATUS = UPLOAD_STATUS,
                  UPLOAD_ID = UPLOAD_ID,
                  PROCESSING_RUN_ID = run.RUN_ID,
                  TAR_ID = tar.TAR_ID)
            
            self.store.add(pd)
            self.store.commit()
            self.InsertHistory(TYPE = 'insert', TAR_ID=0, DIR_ID=pd.DIR_ID, RUN_ID=0,  DATE=date.today(), 'inserted processeddir')
            return pd

      def startProcessing(self,pr):
            if (self.RUNNING >= self.MAXEXE):
                  print" I refuse to start a new processing, already running=",self.RUNNING," and max allowed is ",self.MAXEXE
                  return None
            pr.STATUS='running'
            self.InsertHistory(TYPE = 'changestatus', TAR_ID=0, DIR_ID=0, RUN_ID=pr.run_id,  DATE=date.today(), 'status set to running')
            self.store.commit()
            #
            # execute the command
            #
            # get the tar
            tar =  self.getInputTarById (pr.TAR_ID):
            if (tar is None):
                  print " Cannot get tar with ID=",pr.TAR_ID
                  return None
                  

            procevd = subprocess.Popen(self.EXE+" "+tar.LOCATION+"/"+tar.NAME, stdin=None, stdout=None, stderr=subprocess.STDOUT, shell=True) 
            self.RUNNING=self.RUNNING+1
            self.RUNNINGINSTANCES.append([procevd,pr.run_id])
            return procevd

      def setProcessingStatus(self,pr,status):
            pr.STATUS=status
            self.InsertHistory(TYPE = 'changestatus', TAR_ID=0, DIR_ID=0, RUN_ID=pr.run_id,  DATE=date.today(), 'status set to '+status)
            self.store.commit()

      def setInputStatus(self,tar,status):
            tar.STATUS=status
            self.InsertHistory(TYPE = 'changestatus', TAR_ID=tar.TAR_ID, DIR_ID=0, RUN_ID=0,  DATE=date.today(), 'status set to '+status)
            self.store.commit()

      def setDirStatus(self,dir,status):
            dir.STATUS=status
            self.InsertHistory(TYPE = 'changestatus', TAR_ID=0, DIR_ID=dir.DIR_ID, RUN_ID=0,  DATE=date.today(), 'status set to '+status)
            self.store.commit()

      def setAllDone(self,RUN, DIR, TAR,  STATUSDIR, STATUSTAR, STATUSRUN):
            self.setProcessingStatus(RUN,STATUSRUN)
            self.setInputStatus(RUN,STATUSTAR)
            self.setDirStatus(RUN,STATUSDIR)



      def checkAllRunning(self):
            #
            # loop on the list
            #
            done=False
            while (done==False):
                  for i in self.RUNNINGINSTANCES:
                        if ((i[0]).poll() == None):
                              continue
                        else:
                              print " Process Finished!"
                              #
                              # at this point I can declare [i] (RUN_ID) done
                              #
                              statuscode = i[0].returncode()
                              status='failed'
                              if (statuscode ==0):
                                    status = 'done'
                              pr = i[1]
                              self.setProcessingStatus(pr,status)


                              tar = getInputTarById (pr.tar_id)

                              if (tar is None):
                                    print " ERROR NO TAR"
                                    return None

                              self.setInputTarStatus(tar,"processed")

                              namedir = self.PROCESSEDPREFIX+'/'+re.sub('.tar','',tar.NAME)
                              
#
# now I should also upload
#

                              #self.uploadTest()


                              pd  = self.insertProcessedDir(pr,tar,NAME=namedir, STATUS=status, UPLOAD_TYPE = "test",
                                                      UPLOAD_STATUS="boh",
                                                      UPLOAD_ID=444)
                              
                              if (pd is None):
                                    print " ERROR in PD"
                                    return None
                              

                              self.RUNNING = self.RUNNING-1
                              self.RUNNINGINSTANCES.remove(i)
                              
                              break
                  done = True
            
                        
                  
#
# 
#
            
            
            
            # getmethods
#
      def getInputTarById (self, tar_id):
            aa = self.store.find(InputTar, InputTar.TAR_ID == tar_id).one()
            return aa

      def getProcessedDirById (self, tar_id):
            aa = self.store.find(ProcessedDir, ProcessedDir.DIR_ID == tar_id).one()
            return aa


      def getInputTarByName(self, tar_name):
            aa = self.store.find(InputTar, InputTar.NAME == tar_name).one()
            return aa

      def testInoutTarEquality(self, tar1,tar2):
            return ( tar1.NAME == tar2.NAME and  tar1.LOCATION == tar2.LOCATION and  tar1.CKSUM  == tar2.CKSUM)
