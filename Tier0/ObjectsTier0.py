#!/usr/bin/env python

# enable debugging
#import cgitb
from datetime import *
#cgitb.enable()

from MySQLdb import *
from storm.locals import *

"""
CREATE TABLE `historyTier0` (
  `HISTORY_ID` int(11) NOT NULL AUTO_INCREMENT,
  `TYPE` varchar(32) NOT NULL DEFAULT '',
  `TAR_ID` int(11) default 0,
  `RUN_ID` int(11) default 0 ,
  `DIR_ID` int(11) default 0,
  `DATE` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `COMMENT` text,
  PRIMARY KEY (`HISTORY_ID`)
);


 CREATE TABLE `outputdir` (
  `DIR_ID`  int(11) NOT NULL AUTO_INCREMENT,
  `STATUS` varchar(24) DEFAULT NULL,
  `DATE` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `NAME` varchar(400) DEFAULT NULL,
  `UPLOAD_TYPE` varchar(100) DEFAULT NULL,
  `UPLOAD_STATUS` varchar(100) DEFAULT NULL,
  `UPLOAD_ID` varchar(1000) default NULL,
  `TAR_ID` int(11) NOT NULL,
  `PROCESSING_RUN_ID` int(11) NOT NULL,
  PRIMARY KEY (`DIR_ID`)
) ;

 CREATE TABLE `processingrun` (
  `RUN_ID`  int(11) NOT NULL AUTO_INCREMENT,
  `STATUS` varchar(24) DEFAULT NULL,
  `DATE` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `NAME` varchar(100) DEFAULT NULL,
  `MACRO_VERSION` varchar(30) DEFAULT NULL,
  `MACRO_LOCATION` varchar(400) DEFAULT NULL,
  `EXECUTED_COMMAND` varchar(100) DEFAULT NULL,
  `EXIT_CODE` int(5),
  `TAR_ID` int(11) NOT NULL,
  `PROCESSED_DIR_ID` int(11) NOT NULL,
  PRIMARY KEY (`RUN_ID`)
) ;



 CREATE TABLE `inputtar` (
  `TAR_ID`  int(11) NOT NULL AUTO_INCREMENT,
  `STATUS` varchar(24) DEFAULT NULL,
  `DATE` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `CKSUMTYPE` varchar(24) DEFAULT NULL,
  `CKSUM` varchar(24) DEFAULT NULL,
  `CENTER` varchar(24) DEFAULT NULL,
  `NAME` varchar(100) DEFAULT NULL,
  `LOCATION` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`TAR_ID`)
) ;



"""




class InputTar (object):
    __storm_table__ = "inputtar"
    TAR_ID = Int(primary=True)
    NAME = Unicode()
    LOCATION = Unicode()
    CKSUM = Unicode()
    CKSUMTYPE = Unicode()
    DATE = datetime(1970,1,1)
    STATUS = Unicode()
    CENTER = Unicode()
    def __init__ (self, NAME,    LOCATION,    CKSUM   ,CKSUMTYPE,  DATE, STATUS, CENTER):
        self.NAME = unicode(NAME)
        self.LOCATION  = unicode(LOCATION)
        self.CKSUM = unicode(CKSUM)
        self.CKSUMTYPE = unicode(CKSUMTYPE)
        self.DATE = DATE 
        self.STATUS =unicode(STATUS)
        self.CENTER = unicode(CENTER)

class ProcessedDir (object):
    __storm_table__ = "outputdir"
    DIR_ID = Int(primary=True)
    NAME = Unicode()
    DATE = datetime(1970,1,1)
    STATUS = Unicode()
    UPLOAD_TYPE = Unicode()
    UPLOAD_STATUS = Unicode()
    UPLOAD_ID = Int()
    PROCESSING_RUN_ID = Int()
    TAR_ID = Int()
    def __init__(self,     NAME    , STATUS,     UPLOAD_TYPE,     UPLOAD_STATUS,     UPLOAD_ID,     PROCESSING_RUN_ID, TAR_ID, DATE = date.today()):
        self.NAME=unicode(NAME)
        self.STATUS = unicode(STATUS )
        self.UPLOAD_TYPE = unicode(UPLOAD_TYPE )
        self.UPLOAD_ID = UPLOAD_ID
        self.PROCESSING_RUN_ID = (PROCESSING_RUN_ID )
        self.TAR_ID = TAR_ID
        self.DATE = DATE


class ProcessingRun (object):
    __storm_table__ = "processingrun"
    RUN_ID = Int(primary=True)
    TAR_ID = Int()
    MACRO_VERSION = Unicode()
    EXECUTED_COMMAND = Unicode()
    EXIT_CODE = Int()
    STATUS = Unicode()
    DATE = datetime(1970,1,1)
    PROCESSED_DIR_ID = Int()
    def __init__(self, MACRO_VERSION, EXECUTED_COMMAND, EXIT_CODE, DATE, STATUS, TAR_ID, PROCESSED_DIR_ID=0):
        self.TAR_ID = TAR_ID
        self.MACRO_VERSION = unicode(MACRO_VERSION)
        self.EXECUTED_COMMAND = unicode(EXECUTED_COMMAND)
        self.EXIT_CODE = (EXIT_CODE)
        self.DATE = DATE
        self.STATUS = unicode(STATUS)
        self.PROCESSED_DIR_ID = PROCESSED_DIR_ID
    

class HistoryTier0(object):
    __storm_table__ = "historyt0"
    HISTORY_ID = Int(primary=True)
    TYPE=Unicode()
    TAR_ID = Int()
    DIR_ID = Int()
    RUN_ID=Int()
    DATE=date.today()
    COMMENT=Unicode()
    def __init__(self, TYPE, TAR_ID, DIR_ID, RUN_ID,  DATE=date.today(), COMMENT=""):
        self.TYPE=unicode(TYPE)
        self.TAR_ID = TAR_ID
        self.DIR_ID = DIR_ID
        self.RUN_ID= RUN_ID
        self.DATE=DATE
        self.COMMENT=unicode(COMMENT)

ProcessedDir.processing_run_id = Reference (ProcessedDir.PROCESSING_RUN_ID, ProcessingRun.RUN_ID)
ProcessedDir.processing_run_id = Reference (ProcessedDir.PROCESSING_RUN_ID, ProcessingRun.RUN_ID)
ProcessingRun.processed_dir_id = Reference( ProcessingRun.PROCESSED_DIR_ID, ProcessedDir.DIR_ID)
ProcessingRun.tar_id = Reference( ProcessingRun.TAR_ID, InputTar.TAR_ID)
ProcessedDir.tar_id = Reference (ProcessedDir.TAR_ID, InputTar.TAR_ID)


HistoryTier0.tar_id = Reference (HistoryTier0.TAR_ID, InputTar.TAR_ID)
HistoryTier0.dir_id = Reference (HistoryTier0.DIR_ID, ProcessedDir.DIR_ID)
HistoryTier0.run_id = Reference (HistoryTier0.RUN_ID, ProcessingRun.RUN_ID)


