#!/usr/bin/env python
#
# this is needed to observe a variety of full tests, ideally at least one per centre 
#


# enable debugging
import cgitb
import commands
import os
import tempfile
import datetime
from time import sleep
import signal
import sys
#sys.path.append("../../PixelDB")
sys.path.append("/home/robot/cms-pixel-db-pisa/Tier0")
import PixelTier0
#cgitb.enable()
#from storm.tracer import debug
#debug(True, stream=sys.stdout)

def handler (signum,frame):
    print "Interjected Signal - exiting"
    pdb.killAllInstances(DEBUG=True)
    exit(2)


import ConfigParser

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1
        
def initProcessing(CONFIG, DEBUG):
    Config.read(CONFIG)
    #
    # force the presence of the fields
    #
    if (DEBUG == True):
        print "Reading File ",CONFIG
        print ConfigSectionMap("MACRO")
    MACRO_INIT = ConfigSectionMap("MACRO")["init"]
    INPUTDIR = ConfigSectionMap("MACRO")["inputdir"]
    CENTER = ConfigSectionMap("MACRO")["center"]
    OPERATOR = ConfigSectionMap("MACRO")["operator"]
    PATTERN =  ConfigSectionMap("MACRO")["pattern"]
    TESTNAME =  ConfigSectionMap("MACRO")["testname"]
    if (MACRO_INIT=='null' or INPUTDIR=='null' or PATTERN == 'null'):
        print "Config file NOT ok"
        return (None, None, None,  None, None,False)
    return (MACRO_INIT, INPUTDIR, CENTER, PATTERN,OPERATOR, TESTNAME, True)


DEBUG=True
Config = ConfigParser.ConfigParser()

if (len(sys.argv) != 3):
    print " Need two inputs: the config file + processing mode"
    exit (2)
    
if (sys.argv[2] != 'insert' and sys.argv[2] != 'insert+process' and sys.argv[2] != 'process'):
    print "processing mode can be only insert, process, insert+process"
    exit (3)

insert=0
process=0

if (sys.argv[2] == 'insert'):
    insert=1
elif (sys.argv[2] == 'insert+process'):
    insert=1
    process=1
elif (sys.argv[2] == 'process'):
    process=1

    

MACRO_INIT = 'null'
INPUTDIR = 'null'
CENTER =  'null'
PATTERN ='null'
INSERTED=0
numinjected=0

(MACRO_INIT, INPUTDIR, CENTER, PATTERN, OPERATOR, TESTNAME, ok) = initProcessing(CONFIG=sys.argv[1], DEBUG=DEBUG)

if (ok == False):
    print "Failed in reading the ini file",sys.argv[1]
    exit(1)

  #
  # loop over the dir and search for tar files
  #

from PixelTier0 import *

signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGINT,handler)

MAX=100000

pdb = PixelTier0()
pdb.initProcessing(CONFIG=MACRO_INIT, DEBUG=False)
pdb.connectToDB()

tmpfile = (tempfile.mkstemp())[1]
print "TMPFILE ",tmpfile
listinserted=[]

if (insert==1):

    #
    # loop over a dir to search for tars

    basedir=INPUTDIR
    print "FILE", tmpfile
    pattern = PATTERN
    os.system("find "+basedir+" -name "+pattern+" -amin +2 > "+tmpfile)
    
    f=open(tmpfile)
    for line in f:

        if (INSERTED>MAX):
            continue
    
        line= line.rstrip(os.linesep)
#        (ret, ck) = commands.getstatusoutput('cksum \"'+line+"\" | awk \'{print $1}\'")
        ck=0
#        print " working on Tar file: ",line,' CKSUM: ', ck    


#        if (pdb.getInputTarByName(os.path.basename(line),os.path.dirname(line)) is not None):
#            print " ALREADY PROCESSED"
#            continue    
#        if (pdb.getInputTarByNameAndCksum(os.path.basename(line),ck) is not None):
        if (pdb.getInputTarByNameOnly(os.path.basename(line)) is not None):
 #           print " ALREADY PROCESSED"
            continue    
    
        #
        # get cksum
        #
    
#        (ret, ck) = commands.getstatusoutput('cksum '+line+" | awk \'{print $1}\'")
   	if CENTER == "unknown" :
		m=re.match("/home/(.*)/dropbox",os.path.dirname(line)) 
		if m :
			CENTER=m.group(1).upper()

        tar = InputTar (NAME=os.path.basename(line), LOCATION=os.path.dirname(line),    CKSUMTYPE='cksum', CKSUM=ck,         STATUS='new', CENTER = CENTER, DATE = datetime.now(),TESTNAME=TESTNAME)
        pp = pdb.insertNewTar(tar)
        if(pp is None):
            print "ERROR inserting Tar, skipping ...."
            continue
	print "tar status",tar.STATUS,pp.STATUS
	os.system("chmod 440 '%s'"%(line))
	print "doing os.system chmod 440 %s"%(line)
        listinserted.append(pp.TAR_ID)

        #
# I can ge the tar_ids in a vector!
#
        print "Inserted new tar = ", tar.TAR_ID
        INSERTED=INSERTED+1
        pdb.store.commit()
	
    numinjected = pdb.injectsProcessingJobs(tarlist=listinserted)

print "INSERTED ", INSERTED, " TAR FILES"
print "TARS are ",listinserted
print "injected processing runs " , numinjected

#
# pleasenote: in the way it is done, this will start ALL THE PROCESSING JOBS, not only these created here
#

if (process==1):
    passage=0
    while (True):
        passage=passage+1
        num = pdb.checkAllRunning(DEBUG=False)
        num2 = pdb.startProcessingJobs()
        print str(datetime.now())," Running Instances = ",num, " Waiting Instances = ",num2
        sleep (10)      
        if (passage%20 == 0):
                    pdb.uploadAllTests()
        if (num==0 and num2==0):
            print "---- FINISHED----"
            break
    #
    # upload what you can
    #
    number = pdb.checkNumberOfTestsToBeUploaded()
    print " I NEED TO UPLOAD ", number, " results ..."
    if (number>0):
#new session
#        s = Session (CENTER=CENTER, OPERATOR=OPERATOR,TYPE="TESTSESSION",DATE=datetime.now(), COMMENT="")
#        ppp= pdb.PixelDB.insertSession(s)
#        if (ppp is None):
#            print "Failed to create a session"
#            exit (2)
            
        pdb.uploadAllTests()
        #
        
os.system ("rm -f "+tmpfile)


