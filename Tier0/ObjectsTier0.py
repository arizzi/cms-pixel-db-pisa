#!/usr/bin/env python

# enable debugging
#import cgitb
from datetime import *
#cgitb.enable()

from MySQLdb import *
from storm.locals import *


#
# transfer
#
class InputTar (object):
    __storm_table__ = "inputtar"
    TAR_ID = Int(primary=True)
    NAME = Unicode()
    LOCATION = Unicode()
    CKSUM = Unicode()
    CKSUMTYPE = Unicode()
    DATE = datatime(1970,1,1)
    STATUS = Unicode()
    CENTER = Unicode()
    def __init__ (self, NAME,    LOCATION,    CKSUM,     DATE, STATUS, CENTER):
        self.NAME = NAME
        self.LOCALTION  = LOCATION
        self.CKSUM = CKSUM
        self.DATE = DATE 
        self.STATUS =STATUS 
        self.CENTER = CENTER

class ProcessedDir (object):
    __storm_table__ = "outputdir"
    DIR_ID = Int(primary=True)
    NAME = Unicode()
    DATE = datatime(1970,1,1)
    STATUS = Unicode()
    UPLOAD_TYPE = Unicode()
    UPLOAD_STATUS = Unicode()
    UPLOAD_ID = Int()
    PROCESSING_RUN_ID = Int()
    TAR_ID = Int()

class ProcessingRun (object):
    __storm_table__ = "processingrun"
    RUN_ID = Int(primary=True)
    TAR_ID = Int()
    MACRO_VERSION = Unicode()
    EXECUTED_COMMAND = Unicode()
    EXIT_CODE = Int()
    STATUS = Unicode()
    MACRO_LOCATION = Unicode()
    DATE = datatime(1970,1,1)
    PROCESSED_DIR_ID = Int()
    def __init__(self, RUN_ID, MACRO_VERSION, EXECUTED_COMMAND, EXIT_CODE, MACRO_LOCATION, DATE, STATUS, ,TAR_ID, PROCESSED_DIR_ID=0):
        self.RUN_ID = RUN_ID
        self.TAR_ID = TAR_ID
        self.MACRO_VERSION = MACRO_VERSION
        self.EXECUTED_COMMAND = EXECUTED_COMMAND
        self.EXIT_CODE = EXIT_CODE
        self.MACRO_LOCATION = MACRO_LOCATION
        self.DATE = DATE
        self.STATUS = STATUS
        self.PROCESSED_DIR_ID = PROCESSED_DIR_ID
    

class History(object):
    __storm_table__ = "history"
    HISTORY_ID = Int(primary=True)
    TYPE=Unicode()
    TAR_ID = Int()
    DIR_ID = Int()
    RUN_ID=Int()
    DATE=date.today()
    COMMENT=Unicode()
    def __init__(self, TYPE, TAR_ID, DIR_ID, RUN_ID,  DATE=date.today(), COMMENT=""):
        self.TYPE=unicode(TYPE)
        self.ID=unicode(ID)
        self.TAR_ID = TAR_ID
        self.DIR_ID = DIR_ID
        self.RUN_ID= DIR_ID
        self.DATE=DATE
        self.COMMENT=unicode(COMMENT)

ProcessedDir.processing_run_id = Reference (ProcessedDir.PROCESSING_RUN_ID, ProcessingRun.RUN_ID)
ProcessedDir.processing_run_id = Reference (ProcessedDir.PROCESSING_RUN_ID, ProcessingRun.RUN_ID)
ProcessingRun.processed_dir_id = Reference( ProcessingRun.PROCESSED_DIR_ID, ProcessedDir.DIR_ID)
ProcessingRun.tar_id = Reference( ProcessingRun.TAR_ID, InputTar.TAR_ID)
ProcessedDir.tar_id = Reference (ProcessedDir.TAR_ID, InputTar.TAR_ID)


History.tar_id = Reference (History.TAR_ID, InputTar.TAR_ID)
History.dir_id = Reference (History.DIR_ID, ProcessedDir.DIR_ID)
History.run_id = Reference (History.RUN_ID, ProcessingRun.RUN_ID)


