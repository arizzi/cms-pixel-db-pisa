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
            self.date = datetime.now()
            self.MACRO_VERSION='null'
            self.MACRO_PROCESSEDPREFIX=None
            self.UPLOAD_METHOD = ""
            self.EXE=None
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
            self.EXE =  self.ConfigSectionMap("EXECUTION")['script'] # assumes invocation via self.EXE $tarfile
            self.MAXEXE=int(self.ConfigSectionMap("EXECUTION")['maxinstances'] )
            self.PROCESSEDPREFIX=self.ConfigSectionMap("EXECUTION")['processedprefix'] 
            self.UPLOAD_METHOD=self.ConfigSectionMap("EXECUTION")['uploadmethod'] 

            if (DEBUG == True):
                  print "Config Settings:"
                  print "MACRO.VERSION = ",self.MACRO_VERSION
                  print "EXECUTION.SCRIPT = ", self.EXE
                  print "EXECUTION.UPLOAD_METHOD = ", self.UPLOAD_METHOD
                  print "EXECUTION.MAXEXE = ", self.MAXEXE
                  print "EXECUTION.PROCESSEDPREFIX = ",self.PROCESSEDPREFIX
            if (self.MACRO_VERSION==None or self.EXE==None or self.PROCESSEDPREFIX == None):
                  print "Config file NOT ok"
                  exit(1)                  
#
# also create a connection to Test DB
#
            self.PixelDB =  PixelDBInterface(operator="tommaso",center="pisa")
            self.PixelDB.connectToDB()


      def pixelDB():
            return self.PixelDB


      def connectToDB(self,string = "mysql://%s:%s@localhost/test_tier0"%(secrets.USER,secrets.PASSWORD)) :
            self.database = create_database(string)
            self.store = Store(self.database)            

      def insertHistoryTier0(self, TYPE, TAR_ID, DIR_ID, RUN_ID,  COMMENT,DATE=datetime.now()):
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
            self.insertHistoryTier0(TYPE = 'insert', TAR_ID=tar.TAR_ID, DIR_ID=0, RUN_ID=0,  DATE=datetime.now(), COMMENT='new tar insertion')
            return tar


      def processInputTar(self,tar,center=""):
#
# # if center is set, processes only those from it, retrieving via inputtdir
#
            #
            # CHECK if there is already a processing for this 
            #
            if (tar.STATUS != 'new'):
                  print 'Failed to process TAR with name=',tar.NAME,' and id=',tar.TAR_ID,'since status is ',tar.STATUS
                  return None
            if (center != "" and center != tar.CENTER):
                  print "refusing to process TAR with name =",tar.NAME,' and id=',tar.TAR_ID,'since status is ',tar.STATUS, " since center is not matching", center, tar.CENTER
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
            else:
		print "Inserted PR from IT",pr.RUN_ID, tar.TAR_ID
            self.insertHistoryTier0(TYPE = 'insert', TAR_ID=0, DIR_ID=0, RUN_ID=pr.RUN_ID,  DATE=datetime.now(), COMMENT='new processing insertion')
            
            return pr


      def injectProcessingRunFromInputTar (self,tar):
            pr = ProcessingRun(MACRO_VERSION = self.MACRO_VERSION, EXECUTED_COMMAND = self.EXE, EXIT_CODE = -1,  STATUS="injected", DATE=datetime.now(), TAR_ID=tar.TAR_ID,PROCESSED_DIR_ID = 0, PROCESSEDPREFIX=self.PROCESSEDPREFIX,UPLOADMETHOD=self.UPLOAD_METHOD)
            self.store.add(pr)
            self.store.commit()
            return pr
            


      def insertProcessedDir(self,     run,tar,
                             NAME,
                             STATUS,
                             UPLOAD_TYPE,
                             UPLOAD_STATUS,
                             UPLOAD_ID,
                             DATE = datetime.now()):
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
            self.insertHistoryTier0(TYPE = 'insert', TAR_ID=0, DIR_ID=pd.DIR_ID, RUN_ID=0,  DATE=datetime.now(), COMMENT='inserted processeddir')
            return pd

      def startProcessing(self,pr, DEBUG=False):
            if (self.RUNNING >= self.MAXEXE):
                  if (DEBUG==True):
                        print" I refuse to start a new processing, already running=",self.RUNNING," and max allowed is ",self.MAXEXE
                  return None
            self.setProcessingStatus(pr,'running')
	    basedir="/data/pixels/t0logs/%s/"%datetime.now().strftime("%Y-%m-%d")
	    os.makedirs(basedir)
	    filename="%s/%s"%(basedir,pr.RUN_ID)
	    pr.OUTLOG=unicode(filename)
            self.store.commit()
            #
            # execute the command
            #
            # get the tar
            tar =  self.getInputTarById (pr.TAR_ID)
            if (tar is None):
                  print " Cannot get tar with ID=",pr.TAR_ID
                  return None
                  
            (nameout,fulldir) = self.createDirOut(tar,pr.PROCESSEDPREFIX,pr.MACRO_VERSION)

            my_env = os.environ
	    my_env["PIXEL_OPERATOR"] =  "robot"
	    my_env["PIXEL_CENTER"] = pr.tar_id.CENTER
##
## new interface : I pass to the macro
            # 1 - tar name
            # 2 - expected directory with the results (which is NOT supposed to be changed by the script
##
	   
	    outlog=file(filename,"w")
            procevd = subprocess.Popen(pr.EXECUTED_COMMAND+" "+tar.LOCATION+"/"+tar.NAME+" "+fulldir+" "+pr.MACRO_VERSION, stdin=None, stdout=outlog, stderr=subprocess.STDOUT, shell=True, env=my_env) 
	    outlog.close()
            self.RUNNING=self.RUNNING+1
            self.RUNNINGINSTANCES.append([procevd,pr.RUN_ID])
            return procevd

      def setProcessedDir(self,pr,dir_id):
            pr.PROCESSED_DIR_ID=dir_id
            self.store.commit()


      def setProcessingStatus(self,pr,status):
            pr.STATUS=unicode(status)
            self.insertHistoryTier0(TYPE = 'changestatus', TAR_ID=0, DIR_ID=0, RUN_ID=pr.RUN_ID,  DATE=datetime.now(), COMMENT='status set to '+status)
            self.store.commit()

      def setProcessingExitCode(self,pr,status):
            pr.EXIT_CODE=status
            self.insertHistoryTier0(TYPE = 'changeexitcode', TAR_ID=0, DIR_ID=0, RUN_ID=pr.RUN_ID,  DATE=datetime.now(), COMMENT='status set to '+str(status))
            self.store.commit()


      def setInputStatus(self,tar,status):
            tar.STATUS=unicode(status)
            self.insertHistoryTier0(TYPE = 'changestatus', TAR_ID=tar.TAR_ID, DIR_ID=0, RUN_ID=0,  DATE=datetime.now(), COMMENT='status set to '+status)
            self.store.commit()

      def setDirStatus(self,dir,status):
            dir.STATUS=unicode(status)
            self.insertHistoryTier0(TYPE = 'changestatus', TAR_ID=0, DIR_ID=dir.DIR_ID, RUN_ID=0,  DATE=datetime.now(), COMMENT='status set to '+status)
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

                              (namedir,fulldir) = self.createDirOut(tar,pr.PROCESSEDPREFIX,pr.MACRO_VERSION)
                              
                              #
                              # now I should also upload
                              #
                              
                              #self.uploadTest()
                              
                              pd  = self.insertProcessedDir(pr,tar,NAME=fulldir, STATUS=status, UPLOAD_TYPE = pr.UPLOADMETHOD,
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


      def createDirOut(self,tar,prefix,macro):
#            namedir = (self.PROCESSEDPREFIX+'/'+re.sub('.tar','',tar.NAME)+"_"+re.sub("[\s/]","_",self.MACRO_VERSION))
            modname = re.split("_",tar.NAME)[0]
            namedir = (prefix+'/'+modname+"/"+re.sub("[\s/]","_",macro))

#            print " ECCCO ",tar.NAME,modname, namedir

            archivename = re.sub('.tar','',re.sub('.tar.gz','',tar.NAME))

            fulldir = namedir+'/'+re.sub('.tar','',re.split("_",tar.NAME)[1])
#            print " ECCCO ",tar.NAME,modname, namedir, fulldir, archivename

            return namedir,namedir+'/'+archivename



#
# recheck what is runnable
#



      def startProcessingJobsFromList  (self,mylist):
#
# if center is set, processes only those from it, retrieving via inputtdir
#
            jobs=[]
            for i in mylist:
                  if (i.STATUS == 'injected'):
                        jobs.append(i)

            if (jobs ==[]):
                  return 0

            n=0
            for job in jobs:
                  n=n+1
                  self.startProcessing(job)
            return n


      def injectsProcessingJobs(self,mycenter="",tarlist=None):
	    if tarlist is not None :
		    tars= map(lambda x: self.store.find(InputTar,InputTar.TAR_ID==x)[0], tarlist)
	    else :
	            tars = self.store.find(InputTar,InputTar.STATUS==unicode('new'))
            n=0
	    print "len of tars", tars	
            for job in tars:
                  pr=self.processInputTar(job,mycenter)
		  if pr is None:
			print " failed inserting processing run for tar",job.TAR_ID
		  else:
                   print "Injected Processing ",pr.RUN_ID,"for tar",job.TAR_ID
                   n=n+1
            return n





      def startProcessingJobs  (self,initcenter=""):
#
# if center is set, processes only those from it, retrieving via inputtdir
#
            #
            # search for jobs in status = "injected"
            #
            jobs = self.store.find(ProcessingRun, ProcessingRun.STATUS==unicode('injected'))
            if (jobs is None):
                  return 0
            n=0
            for job in jobs:
		  print "starting ",job.TAR_ID
                  if (initcenter != "" and initcenter != job.tar_id.CENTER):
                        continue
                  n=n+1
                  self.startProcessing(job)
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
# idea: for every test there will be 
# self.uploadMYNAME(ProcessedDir, Session) (processed dir = table outputdir)
# "uploadMYNAME" will be in the macro definition
#

      def checkNumberOfTestsToBeUploaded(self):
          aa = self.store.find(ProcessedDir,ProcessedDir.STATUS == unicode("done"))
          return aa.count()
            

      def uploadAllTests(self,operator="n/a"):
# if initcenter != "" works only on these
 #
 # loop on outdir with status = 'done'
          aa = self.store.find(ProcessedDir,ProcessedDir.STATUS == unicode("done"))

          for od in aa:
                s = Session (CENTER=od.tar_id.CENTER , OPERATOR=operator,TYPE="TESTSESSION",DATE=datetime.now(), COMMENT="")
                ppp = self.PixelDB.insertSession(s)
                if (ppp is None):
                      print "Failed to create a session"
                      continue
                res = self.uploadGenericTest(od,s)
                if (res is None):
                      print" FAILED uploadAllTests due to error with ",od.NAME
#                     return None
          return aa



      def uploadGenericTest(self,pd,session):
#
# uses the field 
# ProcessedDir.UPLOAD_TYPE to decide which to use            
            print "USING UPLOAD = ",pd.UPLOAD_TYPE,"self.upload"+pd.UPLOAD_TYPE+"(pd,session)"
	    savestout = sys.stdout
	    ff = None
	    if pd.processing_run_id.OUTLOG != "" :
		    filename=pd.processing_run_id.OUTLOG+"_upload"
		    ff = open(filename, 'w')
 		    sys.stdout = ff
            ppp = eval ("self.upload"+pd.UPLOAD_TYPE+"(pd,session)")
	    if ff is not None :
		ff.close()
	    sys.stdout = savestout
	    print "ppp",ppp
            return ppp

      def uploadNull(self,pd, session):
      #do nothing
            pd.STATUS=unicode("uploaded")
            pd.UPLOAD_ID = 0
            self.store.commit()      

            return pd
      def uploadBareModuleMultiTest(self, pd, session):
            print "uploadBareModuleMultiTest"
            dir = pd.NAME
            aaa = self.PixelDB.insertBareModuleMultiTestDir(dir,session)
	    if aaa is None or not hasattr(aaa,"TEST_ID") :
	          print "Failed upload BMTest from DIR ",dir
                  pd.STATUS=unicode("upload-failed")
                  pd.UPLOAD_ID = 0
                  pd.UPLOAD_STATUS=unicode('failed')
                  self.store.commit()
                  return None

            pd.STATUS=unicode("uploaded")
            pd.UPLOAD_ID = aaa.TEST_ID
            pd.UPLOAD_STATUS=unicode("ok")
            self.store.commit()      
	    return aaa

      def uploadIVTest(self,pd, session):
            #
            # simply extract the dir from the pd, and use it to run 
            # pixeldb.insertTestSensorDir(self,dir,session)
            #
	    print "uploadIVTest"
            dir = pd.NAME
            aaa = self.PixelDB.insertIVTestDir(dir,session)
            if (aaa is None):
                  print "Failed upload from DIR ",dir
                  pd.STATUS=unicode("upload-failed")
                  pd.UPLOAD_ID = 0
                  pd.UPLOAD_STATUS=unicode('failed')
                  self.store.commit()      
                  return None
            pd.STATUS=unicode("uploaded")
            pd.UPLOAD_ID = aaa.TEST_ID
            pd.UPLOAD_STATUS=unicode('ok')
            self.store.commit()      
            return pd

#
# old stuff
#

# #
# # automatic publishing of FULL MODULE tests (!)
# #
# # idea is to add a new processingrunoutdir.status = "inserted"
# # this method will take care of the transition done->inserted
# # it uses in the end PixelDB.insertTestFullModuleDir()

#       def  insertTestFullModuleTest(self,od,session):

#             #
# #please note we work at the level of OD. Each OD can produce more than one test
#             # currently I take care of
#             # FullmoduleTests, SensorTests                       
#             #
#             # first check the status is done, otherwise exit
#             if (od.STATUS != 'done'):
#                   print " Error: OutDir with ID",od.DIR_ID, "has status",od.STATUS
#                   return None

# # now, let's launch all the possible tests on that OUTDIR            
# # search for fullmodule test:
#             tmpfile =  (tempfile.mkstemp())[1]
#             pattern = 'summaryTests.txt'
            
#             os.system("find "+od.NAME+" -name "+pattern+" > "+tmpfile)
#             f=open(tmpfile)
#             for line in f:
#                   line= line.rstrip(os.linesep)
#                   print " working on file: ",line
#                   dir = re.sub(pattern,"",line)
#                   print "Going to add as FullModule Test",dir
#                   res = self.PixelDB.insertTestFullModuleDir(dir,sessionid)
#                   if (res is None):
#                         print "Cannot insert FM test from",dir,"  ... exiting"
#                         return None                                            
            
#             os.system("rm -f "+tmpfile)

# # sensor tests
#             pattern = 'IV.LOG'
            

#             os.system("find "+od.NAME+" -name "+pattern+" > "+tmpfile)
            
#             f=open(tmpfile)
#             for line in f:
#                   line= line.rstrip(os.linesep)
#                   print " working on file: ",line
#                   dir = re.sub(pattern,"",line)
#                   print "Going to add as Sensor Test",dir
#                   res = self.PixelDB.insertTestSensorDir(dir,sessionid)
#                   if (res is None):
#                         print "Cannot insert Sensor test from",dir,"  ... exiting"
#                         return None                                            
            
#             os.system("rm -f "+tmpfile)
# # done!
#             od.STATUS=unicode("inserted")
# # set back
#             od.UPLOAD_ID=session.SESSION_ID
#             self.store.commit()      
#             return od







