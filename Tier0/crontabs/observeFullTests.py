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
    print " APRO", CONFIG
    if (DEBUG == True):
        print "Reading File ",CONFIG
        print ConfigSectionMap("MACRO")
    MACRO_INIT = ConfigSectionMap("MACRO")["init"]
    INPUTDIR = ConfigSectionMap("MACRO")["inputdir"]
    CENTER = ConfigSectionMap("MACRO")["center"]
    OPERATOR = ConfigSectionMap("MACRO")["operator"]
    PATTERN =  ConfigSectionMap("MACRO")["pattern"]
    if (MACRO_INIT=='null' or INPUTDIR=='null' or PATTERN == 'null'):
        print "Config file NOT ok"
        return (Null, Null, Null, Null, False)
    return (MACRO_INIT, INPUTDIR, CENTER, PATTERN,OPERATOR, True)


DEBUG=True
Config = ConfigParser.ConfigParser()

if (len(sys.argv) != 2):
    print " Need one input: the config file!"
    exit (2)
    
MACRO_INIT = 'null'
INPUTDIR = 'null'
CENTER =  'null'
PATTERN ='null'


(MACRO_INIT, INPUTDIR, CENTER, PATTERN, OPERATOR, ok) = initProcessing(CONFIG=sys.argv[1], DEBUG=DEBUG)

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

#
# loop over a dir to search for tars

basedir=INPUTDIR
tmpfile = (tempfile.mkstemp())[1]
print "FILE", tmpfile
pattern = PATTERN
os.system("find "+basedir+" -name "+pattern+" > "+tmpfile)

INSERTED=0
f=open(tmpfile)
for line in f:

    if (INSERTED>MAX):
        continue
    
    line= line.rstrip(os.linesep)
    print " working on Tar file: ",line
    
    
    if (pdb.getInputTarByName(os.path.basename(line),os.path.dirname(line)) is not None):
        print " ALREADY PROCESSED"
        continue

    print " CI SONO" 
    
    
    #
    # get cksum
    #
    
    (ret, ck) = commands.getstatusoutput('cksum '+line+" | awk \'{print $1}\'")
    
    tar = InputTar (NAME=os.path.basename(line), LOCATION=os.path.dirname(line),    CKSUMTYPE='cksum', CKSUM=ck,         STATUS='new', CENTER = CENTER, DATE = date.today())
    print "PIPPO"
    pp = pdb.insertNewTar(tar)




    if(pp is None):
        print "ERROR inserting Tar, skipping ...."
        continue


    print "Inserted new tar = ", tar.TAR_ID
    INSERTED=INSERTED+1

    #
    # process it
    #
    
    print " try and process it"
    pr = pdb.processInputTar(tar)
    if(pr is None):
        print "ERROR inserting PR - skipping"
        continue
    print "Insert done! ID=",pr.RUN_ID
    
    #
     #process it
     #
    procevd = pdb.startProcessing(pr)
#
# inject processing for all tars with status still new
#

numinjected = pdb.injectsProcessingJobs()



#
# check

print "Starting check of who's running"

while (True):
   num = pdb.checkAllRunning(DEBUG=False)
   num2 = pdb.startProcessingJobs()
   print str(datetime.now())," Running Instances = ",num, " Waiting Instances = ",num2
   sleep (2)   
   if (num==0 and num2==0):
       print "---- FINISHED----"
       break

#
# upload what you can
#

#new session
s = Session (CENTER=CENTER, OPERATOR=OPERATOR,TYPE="TESTSESSION",DATE=date.today(), COMMENT="")
ppp= pdb.PixelDB.insertSession(s)
if (ppp is None):
    print "Failed to create a session"
    exit (2)

pdb.uploadAllTests(s)
#

os.system ("rm -f "+tmpfile)


