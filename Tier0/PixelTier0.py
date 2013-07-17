from ObjectsTier0 import *
from MySQLdb import *
import tempfile
from storm.locals import *
import string
import subprocess
import os.path
import ConfigParser
import re
import sys
sys.path.append("/home/robot/cms-pixel-db-pisa/PixelDB")
from PixelDB import *

class PixelTier0 (object):
      def __init__(self) :
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


      def initProcessingJustDB(self, DEBUG):
#
# also create a connection to Test DB
#
            self.PixelDB = PixelDBInterface(operator="tommaso",center="pisa")
            self.PixelDB.connectToDB()


      def initProcessing(self, CONFIG, DEBUG):
            self.Config = ConfigParser.ConfigParser()
            self.Config.read(CONFIG)
            #
            # force the presence of the fields
            #
            if (DEBUG == True):
                  print "Reading File ",CONFIG
            self.MACRO_VERSION = self.ConfigSectionMap("MACRO")["version"]
            self.MACRO_LOCATION = self.ConfigSectionMap("MACRO")['location']
            self.EXE =  self.ConfigSectionMap("EXECUTION")['script'] # assumes invocation via self.EXE $tarfile
            self.MAXEXE=int(self.ConfigSectionMap("EXECUTION")['maxinstances'] )
            self.PROCESSEDPREFIX=self.ConfigSectionMap("EXECUTION")['processedprefix'] 
            if (DEBUG == True):
                  print "Config Settings:"
                  print "MACRO.VERSION = ",self.MACRO_VERSION
                  print "MACRO.LOCATION = ", self.MACRO_LOCATION
                  print "EXECUTION.SCRIPT = ", self.EXE
                  print "EXECUTION.MAXEXE = ", self.MAXEXE
                  print "EXECUTION.PROCESSEDPREFIX = ",self.PROCESSEDPREFIX
            if (self.MACRO_VERSION=='null' or self.MACRO_LOCATION=='null' or self.EXE=='null' or self.PROCESSEDPREFIX == 'null'):
                  print "Config file NOT ok"
                  exit(1)                  
#
# also create a connection to Test DB
#
            self.PixelDB =  PixelDBInterface(operator="tommaso",center="pisa")
            self.PixelDB.connectToDB()


      def pixelDB():
            return self.PixelDB


      def connectToDB(self,string = "mysql://tester:pixels@cmspixel.pi.infn.it/test_tier0") :
            self.database = create_database(string)
            self.store = Store(self.database)            

      def insertHistoryTier0(self, TYPE, TAR_ID, DIR_ID, RUN_ID,  COMMENT,DATE=date.today()):
            newHist=HistoryTier0(TYPE, TAR_ID, DIR_ID, RUN_ID,  DATE, COMMENT)
            self.store.add(newHist)
            self.store.commit()
            return newHist

      def insertNewTar(self, tar):
            if (tar.STATUS != 'new'):
                  print 'failing: can insert only a NEW tar, while this has status = ', tar.STATUS
                  return None
            #
            # check if it can be inserted
            #
            othertar = self.getInputTarByName(tar.NAME,tar.LOCATION)
            if (othertar is not None):
                  print " An Input Tar with same name: ",tar.NAME, " is already present - exiting"
                  return None
            
            self.store.add(tar)
            self.store.commit()
            self.insertHistoryTier0(TYPE = 'insert', TAR_ID=tar.TAR_ID, DIR_ID=0, RUN_ID=0,  DATE=date.today(), COMMENT='new tar insertion')
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
            self.insertHistoryTier0(TYPE = 'insert', TAR_ID=0, DIR_ID=0, RUN_ID=pr.RUN_ID,  DATE=date.today(), COMMENT='new processing insertion')
            
            return pr


      def injectProcessingRunFromInputTar (self,tar):
            pr = ProcessingRun(MACRO_VERSION = self.MACRO_VERSION, EXECUTED_COMMAND = self.EXE, EXIT_CODE = -1,  MACRO_LOCATION = self.MACRO_LOCATION,STATUS="injected", DATE=date.today(), TAR_ID=tar.TAR_ID,PROCESSED_DIR_ID = 0)
            self.store.add(pr)
            self.store.commit()
            return pr
            


      def insertProcessedDir(self,     run,tar,
                             NAME,
                             STATUS,
                             UPLOAD_TYPE,
                             UPLOAD_STATUS,
                             UPLOAD_ID,
                             DATE = date.today()):
            if (run.STATUS != "done" and run.STATUS != "failed"):
                  print "Cannot insert a dir from a processing still in state=",run.STATUS
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
            self.insertHistoryTier0(TYPE = 'insert', TAR_ID=0, DIR_ID=pd.DIR_ID, RUN_ID=0,  DATE=date.today(), COMMENT='inserted processeddir')
            return pd

      def startProcessing(self,pr, DEBUG=False):
            if (self.RUNNING >= self.MAXEXE):
                  if (DEBUG==True):
                        print" I refuse to start a new processing, already running=",self.RUNNING," and max allowed is ",self.MAXEXE
                  return None
            self.setProcessingStatus(pr,'running')
            self.store.commit()
            #
            # execute the command
            #
            # get the tar
            tar =  self.getInputTarById (pr.TAR_ID)
            if (tar is None):
                  print " Cannot get tar with ID=",pr.TAR_ID
                  return None
                  
            (nameout,fulldir) = self.createDirOut(tar)


            procevd = subprocess.Popen(self.EXE+" "+tar.LOCATION+"/"+tar.NAME+" "+fulldir, stdin=None, stdout=None, stderr=subprocess.STDOUT, shell=True) 
            self.RUNNING=self.RUNNING+1
            self.RUNNINGINSTANCES.append([procevd,pr.RUN_ID])
            return procevd

      def setProcessedDir(self,pr,dir_id):
            pr.PROCESSED_DIR_ID=dir_id
            self.store.commit()


      def setProcessingStatus(self,pr,status):
            pr.STATUS=unicode(status)
            self.insertHistoryTier0(TYPE = 'changestatus', TAR_ID=0, DIR_ID=0, RUN_ID=pr.RUN_ID,  DATE=date.today(), COMMENT='status set to '+status)
            self.store.commit()

      def setProcessingExitCode(self,pr,status):
            pr.EXIT_CODE=status
            self.insertHistoryTier0(TYPE = 'changeexitcode', TAR_ID=0, DIR_ID=0, RUN_ID=pr.RUN_ID,  DATE=date.today(), COMMENT='status set to '+str(status))
            self.store.commit()


      def setInputStatus(self,tar,status):
            tar.STATUS=unicode(status)
            self.insertHistoryTier0(TYPE = 'changestatus', TAR_ID=tar.TAR_ID, DIR_ID=0, RUN_ID=0,  DATE=date.today(), COMMENT='status set to '+status)
            self.store.commit()

      def setDirStatus(self,dir,status):
            dir.STATUS=unicode(status)
            self.insertHistoryTier0(TYPE = 'changestatus', TAR_ID=0, DIR_ID=dir.DIR_ID, RUN_ID=0,  DATE=date.today(), COMMENT='status set to '+status)
            self.store.commit()

      def setAllDone(self,RUN, DIR, TAR,  STATUSDIR, STATUSTAR, STATUSRUN):
            self.setProcessingStatus(RUN,STATUSRUN)
            self.setInputStatus(RUN,STATUSTAR)
            self.setDirStatus(RUN,STATUSDIR)



      def checkAllRunning(self, DEBUG=False):
            #
            # loop on the list
            #
            if (DEBUG == True):
                  print "Starting check of who's running ... Initially Instances = ", len(self.RUNNINGINSTANCES)
            done=False
            while (done==False):
                  done=False
                  for i in self.RUNNINGINSTANCES:
                        if (DEBUG == True):
                              print " Instance ", i[1]
                        temp =  (i[0]).poll()
                        if ( temp is None):
                              if (DEBUG == True):
                                    print "Still running"
                              continue
                        else:
                              if (DEBUG == True):
                                    print " Process Finished!"
                              #
                              # at this point I can declare [i] (RUN_ID) done
                              #
                              statuscode = temp
                              status='failed'
                              if (statuscode ==0):
                                    status = 'done'
                              #
                              pr=self.getProcessingRunById(i[1])
                              self.setProcessingStatus(pr,status)
                              self.setProcessingExitCode(pr,statuscode)
                              

                              
                              tar = self.getInputTarById (pr.TAR_ID)

                              if (tar is None):
                                    print " ERROR NO TAR"
                                    return None

                              self.setInputStatus(tar,"processed")

                              (namedir,fulldir) = self.createDirOut(tar)
                              
                              #
                              # now I should also upload
                              #
                              
                              #self.uploadTest()
                              
                              pd  = self.insertProcessedDir(pr,tar,NAME=fulldir, STATUS=status, UPLOAD_TYPE = "test",
                                                            UPLOAD_STATUS="",
                                                            UPLOAD_ID=0)
                                                            
                              if (pd is None):
                                    print " ERROR in PD"
                                    return None
                              
                              self.setProcessedDir(pr,pd.DIR_ID)


                              self.RUNNING = self.RUNNING-1
                              self.RUNNINGINSTANCES.remove(i)
                              break
                  else:
                        done = True
            return (self.RUNNING)
                              
                  
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


      def getProcessingRunById (self, pr_id):
            aa = self.store.find(ProcessingRun, ProcessingRun.RUN_ID == pr_id).one()
            return aa


      def getInputTarByName(self, tar_name, loc_name):
            n = unicode(tar_name)
            l = unicode(loc_name)
            aa = self.store.find(InputTar, InputTar.NAME == n,InputTar.LOCATION == l).one()
            return aa

      def testInoutTarEquality(self, tar1,tar2):
            return ( tar1.NAME == tar2.NAME and  tar1.LOCATION == tar2.LOCATION and  tar1.CKSUM  == tar2.CKSUM)


      def createDirOut(self,tar):
#            namedir = (self.PROCESSEDPREFIX+'/'+re.sub('.tar','',tar.NAME)+"_"+re.sub("[\s/]","_",self.MACRO_VERSION))
            modname = re.split("_",tar.NAME)[0]
            namedir = (self.PROCESSEDPREFIX+'/'+modname+"/"+re.sub("[\s/]","_",self.MACRO_VERSION))

#            print " ECCCO ",tar.NAME,modname, namedir

            archivename = re.sub('.tar','',re.sub('.tar.gz','',tar.NAME))

            fulldir = namedir+'/'+re.sub('.tar','',re.split("_",tar.NAME)[1])
#            print " ECCCO ",tar.NAME,modname, namedir, fulldir, archivename

            return namedir,namedir+'/'+archivename



#
# recheck what is runnable
#

      def startProcessingJobs  (self):
            #
            # search for jobs in status = "injected"
            #
            jobs = self.store.find(ProcessingRun, ProcessingRun.STATUS==unicode('injected'))
            if (jobs is None):
                  return 0
            n=0
            for job in jobs:
                  n=n+1
                  self.startProcessing(job)
            return n


      def injectsProcessingJobs(self):
            tars = self.store.find(InputTar,InputTar.STATUS==unicode('new'))
            n=0
            for job in tars:
                  n=n+1
                  self.processInputTar(job)
            return n




      def killAllInstances(self, DEBUG=False):
            if (DEBUG == True):
                  print " In Signal hadler - killing all ",len(self.RUNNINGINSTANCES)," instances"
            # kill all the instances and sets back from running to injected the processingruns
            for i in self.RUNNINGINSTANCES:
                  prid = i[1]
                  if (DEBUG == True):
                        print " Setting processing run ",prid," to injected"
      
                  self.setProcessingStatus(self.getProcessingRunById(prid),"injected")
                  (i[0]).kill()

#
# Inventory/Test DB insertion
#

                  

#
# automatic publishing of FULL MODULE tests (!)
#
# idea is to add a new processingrunoutdir.status = "inserted"
# this method will take care of the transition done->inserted
# it uses in the end PixelDB.insertTestFullModuleDir()

      def  insertTestinDBAllTests(self,od):
            #
#please note we work at the level of OD. Each OD can produce more than one test
            # currently I take care of
            # FullmoduleTests, SensorTests                       
            #
            # first check the status is done, otherwise exit
            if (od.STATUS != 'done'):
                  print " Error: OutDir with ID",od.DIR_ID, "has status",od.STATUS
                  return None
# i save here the session ids of the tests, if any
# first create a session:
            session = Session(CENTER="Pisa", OPERATOR="Tommaso", DATE=date.today(), TYPE='Bulk Imported tests', COMMENT="")
            pp = self.PixelDB.insertSession(session)
            if (pp is None):
                  print "Cannot insert session"
                  return None                                                                  
            
            print "OOOO",od.NAME


# now, let's launch all the possible tests on that OUTDIR            
# search for fullmodule test:
            tmpfile =  (tempfile.mkstemp())[1]
            pattern = 'summaryTests.txt'


            
            os.system("find "+od.NAME+" -name "+pattern+" > "+tmpfile)
            f=open(tmpfile)
            for line in f:
                  line= line.rstrip(os.linesep)
                  print " working on file: ",line
                  dir = re.sub(pattern,"",line)
                  print "Going to add as FullModule Test",dir
                  res = self.PixelDB.insertTestFullModuleDir(dir,sessionid)
                  if (res is None):
                        print "Cannot insert FM test from",dir,"  ... exiting"
                        return None                                            
            
            os.system("rm -f "+tmpfile)

# sensor tests
            pattern = 'IV.LOG'
            

            os.system("find "+od.NAME+" -name "+pattern+" > "+tmpfile)
            
            f=open(tmpfile)
            for line in f:
                  line= line.rstrip(os.linesep)
                  print " working on file: ",line
                  dir = re.sub(pattern,"",line)
                  print "Going to add as Sensor Test",dir
                  res = self.PixelDB.insertTestSensorDir(dir,sessionid)
                  if (res is None):
                        print "Cannot insert Sensor test from",dir,"  ... exiting"
                        return None                                            
            
            os.system("rm -f "+tmpfile)
# done!
            od.STATUS=unicode("inserted")
# set back
            od.UPLOAD_ID=session.SESSION_ID
            self.store.commit()      
            return od



      def uploadAllTests(self):
#
# loop on outdir with status = 'done'
         aa = self.store.find(ProcessedDir,ProcessedDir.STATUS == unicode("done"))

         for od in aa:
               res = self.insertTestinDBAllTests(od)
               if (res is None):
                     print" Stopped uploadAllTests due to error"
                     return None
         return aa





