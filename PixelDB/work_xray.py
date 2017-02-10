

create table Test_FullModule_XRay_Vcal  (
    TEST_ID int (11) NOT NULL AUTO_INCREMENT,
  `SESSION_ID` int(11) DEFAULT NULL,
  `FULLMODULE_ID` varchar(14) NOT NULL DEFAULT '',
  `LAST_PROCESSING_ID` int(11),
  `RESULT` varchar(24) DEFAULT NULL,
  `DATA_ID` int(11) DEFAULT NULL,
  `XRAY_SLOT` int(11),
  `HITRATENOMINAL` decimal(10,3) DEFAULT NULL,
  `TEMPNOMINAL` decimal(10,3) DEFAULT NULL,
  `TIMESTAMP` varchar(30) DEFAULT NULL,
  `COMMENT` test,
primary_KEY (TEST_ID) )

create table Test_FullModule_XRay_Vcal_Roc_Analysis(
  `TEST_ID` int(11) NOT NULL AUTO_INCREMENT,
  `ROC_POS` int(11) NOT NULL,
  `TEST_XRAY_VCAL_MODULE_ID` int(11),
  `TARGET` varchar(100),
  `DATA_ID` int(11) DEFAULT NULL,
  `FULLMODULETEST_ID` int(11) DEFAULT NULL,
  `MACRO_VERSION` varchar(24) DEFAULT NULL,
  `PROCESSING_ID` int(11),
  `COMMENT` varchar(1000) DEFAULT NULL,
  `SLOPE` decimal (20,10),
  `OFFSET` decimal (20,10),
  `CHI2NDF` decimal (20,10),
  `TARGET_PEAK_ENERGY` decimal (20,10),
  `TARGET_HIT_RATE` decimal (20,10),
  `GRADE`  decimal (20,10)
  PRIMARY KEY (`TEST_ID`)
)

create table Test_FullModule_XRay_Vcal_Module_Analysis(
  `TEST_ID` int(11) NOT NULL AUTO_INCREMENT,
  `TARGET` varchar(100),
  `DATA_ID` int(11) DEFAULT NULL,
  `PROCESSING_ID` int(11),
  `FULLMODULETEST_ID` int(11) DEFAULT NULL,
  `MACRO_VERSION` varchar(24) DEFAULT NULL,
  `COMMENT` text DEFAULT NULL,
  `SLOPE` decimal (20,10),
  `OFFSET` decimal (20,10),
  `CHI2NDF` decimal (20,10),
  `TARGET_HIT_RATE` decimal (20,10),
  `GRADE`  decimal (20,10)
  PRIMARY KEY (`TEST_ID`)
)

class Test_FullModule_XRay_Vcal(object):
        __storm_table__ = "Test_FullModule_XRay_Vcal"
        TEST_ID = Int()
        SESSION_ID=Int()
        session = Reference (SESSION_ID,Session.SESSION_ID)
        FULLMODULE_ID =  Unicode()
        fullmodule=Reference(FULLMODULE_ID, FullModule.FULLMODULE_ID)
        DATA_ID=Int()
        data=Reference(DATA_ID,Data.DATA_ID)
        LAST_PROCESSING_ID = Int()
        RESULT = Unicode()
        XRAY_SLOT = Int()
        MACRO_VERSION = Unicode()
        HITRATENOMINAL = Float()
        TEMPNOMINAL = Float()
        TIMESTAMP = Unicode()
        COMMENT = Unicode()
        def __init__(SESSION_ID, TARGET, DATA_ID, LAST_PROCESSING_ID, MACRO_VERSION,  FULLMODULE_ID, XRAY_SLOT,HITRATENOMINAL, TEMPNOMINAL, TIMESTAMP,
                     RESULT="", COMMENT="", MACRO_VERSION = ""):
            self.SESSION_ID = int(SESSION_ID)
            self.TARGET = unicode(TARGET)
            self.DATA_ID = int(DATA_ID)
            self.LAST_PROCESSING_ID  = int(LAST_PROCESSING_ID )
            self.RESULT = unicode(RESULT)
            self.XRAY_SLOT = int(XRAY_SLOT)
            self.HITRATENOMINAL = float(HITRATENOMINAL)
            self.TEMPNOMINAL = float(TEMPNOMINAL)
            self.TIMESTAMP = unicode(TIMESTAMP)
            self.COMMENT = unicode(COMMENT)
            self.MACRO_VERSION = unicode(MACRO_VERSION)
            self.FULLMODULE_ID = unicode(FULLMODULE_ID)

class Test_FullModule_XRay_Vcal_Module_Analysis(object):
    __storm_table__ = "Test_FullModule_XRay_Module_Analysis"
    TEST_ID = Int()
    SESSION_ID=Int()
    session = Reference (SESSION_ID,Session.SESSION_ID)
    FULLMODULETEST_ID =  Int()
    fullmoduletest=Reference(FULLMODULETEST_ID, Test_FullModule_XRay_Vcal.TEST_ID)
    DATA_ID=Int()
    data=Reference(DATA_ID,Data.DATA_ID)
    TARGET = Unicode()
    PROCESSING_ID = Int()
    MACRO_VERSION = Unicode()
    COMMENT = Unicode()
    SLOPE  =Float()
    OFFSET = Float()
    CHI2NDF  = Float()
    TARGET_HIT_RATE = Float()
    GRADE = Float()
    def __init__(self, SESSION_ID, FULLMODULETEST_ID, DATA_ID, TARGET, PROCESSING_ID, MACRO_VERSION, SLOPE, OFFSET, CHi2NDF, TARGET_HIT_RATE, GRADE, COMMENT=""):
        self.SESSION_ID = int(SESSION_ID)
        self.TARGET = unicode(TARGET)
        self.DATA_ID = int(DATA_ID)
        self.PROCESSING_ID  = int(PROCESSING_ID )
        self.TARGET_HIT_RATE = float(TARGET_HIT_RATE)
        self.COMMENT = unicode(COMMENT)
        self.MACRO_VERSION = unicode(MACRO_VERSION)
        self.FULLMODULETEST_ID = unicode(FULLMODULETEST_ID)
        self.GRADE = float(GRADE)



class  Test_FullModule_XRay_Vcal_Roc_Analysis (object):
    __storm_table__ = "Test_FullModule_XRay_Roc_Analysis"
    TEST_ID = Int()
    ROC_POS = Int()
    TEST_XRAY_VCAL_MODULE_ID = Int()
    testxraymodule = Reference(TEST_XRAY_VCAL_MODULE_ID, Test_FullModule_XRay_Vcal_Module_Analysis.TEST_ID)
    FULLMODULETEST_ID = Int()
    fullmoduletest=Reference(FULLMODULETEST_ID, Test_FullModule_XRay_Vcal.TEST_ID)
    DATA_ID=Int()
    data=Reference(DATA_ID,Data.DATA_ID)
    MACRO_VERSION = Unicode()
    PROCESSING_ID = Int()
    TARGET = Unicode()
    SLOPE  =Float()
    OFFSET = Float()
    CHI2NDF  = Float()
    TARGET_HIT_RATE = Float()
    TARGET_PEK_ENERGY = Float()
    GRADE = Float()
    def __init__(self, SESSION_ID, FULLMODULETEST_ID, DATA_ID, TARGET, PROCESSING_ID, MACRO_VERSION, SLOPE, OFFSET, CHi2NDF, TARGET_HIT_RATE, TARGET_PEAK_ENERGY, 
                 TEST_XRAY_VCAL_MODULE_ID, ROC_POS, GRADE, COMMENT=""):
        self.SESSION_ID = int(SESSION_ID)
        self.TARGET = unicode(TARGET)
        self.DATA_ID = int(DATA_ID)
        self.PROCESSING_ID  = int(PROCESSING_ID )
        self.TARGET_HIT_RATE = float(TARGET_HIT_RATE)
        self.COMMENT = unicode(COMMENT)
        self.MACRO_VERSION = unicode(MACRO_VERSION)
        self.FULLMODULETEST_ID = unicode(FULLMODULETEST_ID)
        self.GRADE = float(GRADE)
        self.ROC_POS = int(ROC_POS)
        self.TARGET_PEAK_ENERGY = float(TARGET_PEAK_ENERGY)
        self.TEST_XRAY_VCAL_MODULE_ID = int(TEST_XRAY_VCAL_MODULE_ID)









