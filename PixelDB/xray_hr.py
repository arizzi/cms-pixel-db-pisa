#
# create tables
# https://indico.cern.ch/event/360854/contribution/3/material/slides/4.pdf
#
 CREATE TABLE `Test_FullModule_XRay_HR_Module` (
  `TEST_ID` int(11) NOT NULL AUTO_INCREMENT,
  `SESSION_ID` int(11) DEFAULT NULL,
  `FULLMODULE_ID` varchar(14) NOT NULL DEFAULT '',
  `LAST_PROCESSING_ID` int(11) DEFAULT NULL,
  `RESULT` varchar(24) DEFAULT NULL,
  `DATA_ID` int(11) DEFAULT NULL,

  `MEASURED_EFFICIENCY` float DEFAULT NULL,
  `MEASURED_HITRATE_EFF` float DEFAULT NULL,
  `N_PIXEL_NO_HIT` int default NULL,
  `MEASURED_HITRATE` float DEFAULT NULL,
  `MEAN_NOISE_ALLPIXELS` float DEFAULT NULL,
  `WIDTH_NOISE_ALLPIXELS` float DEFAULT NULL,
  `MEASURED_HITRATE_NOISE` float DEFAULT NULL,

  `XRAY_SLOT` int DEFAULT NULL,
  `HITRATENOMINAL` float DEFAULT NULL,
  `TEMPNOMINAL` float DEFAULT NULL,
  `TIMESTAMP` varchar(30) DEFAULT NULL,
  `COMMENT` text,
  `MACRO_VERSION` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`TEST_ID`)
) 


CREATE TABLE `Test_FullModule_XRay_HR_Module_Analysis` (
  `TEST_ID` int(11) NOT NULL AUTO_INCREMENT,
  `DATA_ID` int(11) DEFAULT NULL,
  `PROCESSING_ID` int(11) DEFAULT NULL,
  `FULLMODULETEST_ID` int(11) DEFAULT NULL,
  `MACRO_VERSION` varchar(24) DEFAULT NULL,
  
  `N_PIXELS_EFF_BELOW_CUT` int DEFAULT NULL,
  `INTERP_EFF_TESTPOINT` float DEFAULT NULL,
  `N_HOT_PIXELS` int DEFAULT NULL,
  `N_COL_NONUNIFORM` int DEFAULT NULL,
  `N_COL_BELOW_CUT` int DEFAULT NULL,
  `N_PIXELS_NOISE_ABOVETH` int  DEFAULT NULL,

  `GRADE` varchar(30) NOT NULL DEFAULT '',
  `SESSION_ID` int(11) DEFAULT NULL,
  `COMMENT` text default NULL,
  PRIMARY KEY (`TEST_ID`)
) 



CREATE TABLE `Test_FullModule_XRay_HR_Roc_Analysis` (
  `TEST_ID` int(11) NOT NULL AUTO_INCREMENT,
  `ROC_POS` int(11) NOT NULL,
  `TEST_XRAY_HR_ROC_ID` int(11) DEFAULT NULL,

  `DATA_ID` int(11) DEFAULT NULL,
  `MACRO_VERSION` varchar(24) DEFAULT NULL,
  `PROCESSING_ID` int(11) DEFAULT NULL,
  `COMMENT` varchar(1000) DEFAULT NULL,

  `N_PIXELS_EFF_BELOW_CUT` int DEFAULT NULL,
  `ADDR_PIXELS_BAD` text DEFAULT NULL,
  `EFF_INTERP_TESTPOINT` float DEFAULT NULL,
  `N_HOT_PIXELS` int DEFAULT NULL,
  `ADDR_PIXELS_HOT` text DEFAULT NULL,
  `N_COL_NONUNIFORM` int DEFAULT NULL,
  `N_BINS_LOWHIGH` float DEFAULT NULL,
  `N_COL_LOWEFF` float DEFAULT NULL,
  `N_EVENTS_LOWEFF_COL` float DEFAULT NULL,

  `N_PIXELS_NOISE` float DEFAULT NULL,
  `ADDR_PIXELS_NOISE` float DEFAULT NULL,

  `GRADE` varchar(30) NOT NULL DEFAULT '',
  `SESSION_ID` int(11) DEFAULT NULL,
  PRIMARY KEY (`TEST_ID`)
) 


CREATE TABLE `Test_FullModule_XRay_HR_Roc` (
  `TEST_ID` int(11) NOT NULL AUTO_INCREMENT,
  `ROC_POS` int(11) NOT NULL,
  `TEST_XRAY_HR_MODULE_ID` int(11) DEFAULT NULL,
  `DATA_ID` int(11) DEFAULT NULL,
  `MACRO_VERSION` varchar(24) DEFAULT NULL,
  `LAST_PROCESSING_ID` int(11) DEFAULT NULL,
  `COMMENT` varchar(1000) DEFAULT NULL,

  `MEASURED_EFFICIENCY` float DEFAULT NULL,
  `MEASURED_HITRATE_EFF` float DEFAULT NULL,
  `N_PIXEL_NO_HIT` int default NULL,
  `ADDR_PIXEL_NO_HIT` text default NULL,
  `RELSIG_UNIFORM_COLUMNS` float DEFAULT NULL,
  `MEASURED_HITRATE` float DEFAULT NULL,
  `MEAN_NOISE_ALLPIXELS` float DEFAULT NULL,
  `WIDTH_NOISE_ALLPIXELS` float DEFAULT NULL,
  `MEASURED_HITRATE_NOISE` float DEFAULT NULL,

  `GRADE` varchar(30) NOT NULL DEFAULT '',
  `SESSION_ID` int(11) DEFAULT NULL,
  PRIMARY KEY (`TEST_ID`)
) 


#
# python
#

class Test_FullModule_XRay_HR_Module(object):
    __storm_table__ = "Test_FullModule_XRay_Module"
    TEST_ID = Int(primary=True)
    SESSION_ID=Int()
    session = Reference (SESSION_ID,Session.SESSION_ID)
    FULLMODULE_ID =  Unicode()
    fullmodule=Reference(FULLMODULE_ID, FullModule.FULLMODULE_ID)
    DATA_ID=Int()
    data=Reference(DATA_ID,Data.DATA_ID)
    LAST_PROCESSING_ID = Int()
    RESULT = Unicode()
    XRAY_SLOT = Int()
    HITRATENOMINAL = Float()
    TEMPNOMINAL = Float()
    TIMESTAMP = Unicode()
    COMMENT = Unicode()
    
    
    MEASURED_EFFICIENCY = Float() 
    MEASURED_HITRATE_EFF = Float() 
    N_PIXEL_NO_HIT  = Int() 
    MEASURED_HITRATE = Float() 
    MEAN_NOISE_ALLPIXELS = Float() 
    WIDTH_NOISE_ALLPIXELS = Float() 
    MEASURED_HITRATE_NOISE = Float() 
    
    XRAY_SLOT  = Int() 
    HITRATENOMINAL = Float() 
    TEMPNOMINAL = Float() 
    TIMESTAMP =Unicode() 
    COMMENT = Unicode()
    MACRO_VERSION = Unicode()

    def __init__(self, SESSION_ID,  FULLMODULE_ID ,  DATA_ID,   LAST_PROCESSING_ID , RESULT, HITRATENOMINAL, TEMPNOMINAL, TIMESTAMP, MEASURED_EFFICIENCY, MEASURED_HITRATE_EFF, N_PIXEL_NO_HIT  ,
                 MEASURED_HITRATE,
                 MEAN_NOISE_ALLPIXELS ,
                 WIDTH_NOISE_ALLPIXELS,
                 MEASURED_HITRATE_NOISE,                 
                 XRAY_SLOT,
                 HITRATENOMINAL,
                 TEMPNOMINAL ,
                 TIMESTAMP ,
                 MACRO_VERSION,
                 COMMENT ):
        self.SESSION_ID = int(SESSION_ID)
        self.MEASURED_HITRATE_EFF = float(MEASURED_HITRATE_EFF)
        self.FULLMODULE_ID = unicode(FULLMODULE_ID)
        self.DATA_ID = int(DATA_ID)
        self.MEASURED_EFFICIENCY = float(MEASURED_EFFICIENCY)
        self.RESULT = unicode(RESULT)
        self.LAST_PROCESSING_ID = int(LAST_PROCESSING_ID)
        self.TEMPNOMINAL = float(TEMPNOMINAL)
        self.MACRO_VERSION = unicode(MACRO_VERSION)
        self.XRAY_SLOT = int(XRAY_SLOT)
        self.HITRATENOMINAL = float(HITRATENOMINAL)
        self.TIMESTAMP = unicode(TIMESTAMP)
        self.N_PIXEL_NO_HIT = int(N_PIXEL_NO_HIT)
        self.MEASURED_HITRATE = float(MEASURED_HITRATE)
        self.MEAN_NOISE_ALLPIXELS = float(MEAN_NOISE_ALLPIXELS)
        self.COMMENT = unicode(COMMENT)
        self.WIDTH_NOISE_ALLPIXELS = float(WIDTH_NOISE_ALLPIXELS)
        self.MEASURED_HITRATE_NOISE = float(MEASURED_HITRATE_NOISE)
        self.HITRATENOMINAL = float(HITRATENOMINAL)
        self.TEMPNOMINAL = float(TEMPNOMINAL)
        self.TIMESTAMP = unicode(TIMESTAMP)

class Test_FullModule_XRay_HR_Module_Analysis(object):
    __storm_table__ = "Test_FullModule_XRay_Module_Analysis"
    TEST_ID = Int(primary=True)
    SESSION_ID=Int()
    session = Reference (SESSION_ID,Session.SESSION_ID)
    FULLMODULE_ID =  Unicode()
    fullmodule=Reference(FULLMODULE_ID, FullModule.FULLMODULE_ID)
    DATA_ID=Int()
    data=Reference(DATA_ID,Data.DATA_ID)
    PROCESSING_ID = Int()
    RESULT = Unicode()
    FULLMODULETEST_ID  = Int()
    fullmoduletest=Reference(FULLMODULETEST_ID,Test_FullModule_XRay_HR_Module.TEST_ID )
    MACRO_VERSION = Unicode()
    GRADE = Unicode()
    N_PIXELS_EFF_BELOW_CUT = Int() 
    INTERP_EFF_TESTPOINT = Float() 
    N_HOT_PIXELS = Int() 
    N_COL_NONUNIFORM = Int() 
    N_COL_BELOW_CUT = Int() 
    N_PIXELS_NOISE_ABOVETH = Int() 
    

    def __init__(self, SESSION_ID,  FULLMODULE_ID ,  DATA_ID, 
                 PROCESSING_ID , GRADE,RESULT, MACRO_VERSION, FULLMODULETEST_ID,     
                 N_PIXELS_EFF_BELOW_CUT,    INTERP_EFF_TESTPOINT,    N_HOT_PIXELS,    
                 N_COL_NONUNIFORM,     N_COL_BELOW_CUT,     N_PIXELS_NOISE_ABOVETH, COMMENT=""):
        self.SESSION_ID = int(SESSION_ID)
        self.DATA_ID = int(DATA_ID)
        self.PROCESSING_ID = int(PROCESSING_ID)
        self.FULLMODULETEST_ID = int(FULLMODULETEST_ID)
        self.N_PIXELS_EFF_BELOW_CUT = int(N_PIXELS_EFF_BELOW_CUT)
        self.N_HOT_PIXELS = int(    N_HOT_PIXELS)
        self.N_COL_NONUNIFORM = int(N_COL_NONUNIFORM)
        self.N_COL_BELOW_CUT = int(N_COL_BELOW_CUT)
        self.N_PIXELS_NOISE_ABOVETH = int(N_PIXELS_NOISE_ABOVETH)
        self.INTERP_EFF_TESTPOINT = float(INTERP_EFF_TESTPOINT)
        self.FULLMODULE_ID = unicode(FULLMODULE_ID)
        self.GRADE = unicode(GRADE)
        self.RESULT = unicode(RESULT)
        self.MACRO_VERSION = unicode(MACRO_VERSION)
        self.COMMENT = unicode(COMMENT)
        

    
class Test_FullModule_XRay_HR_Roc(object):
    __storm_table__ = "Test_FullModule_XRay_Roc"
    TEST_ID = Int(primary=True)
    ROC_POS = Int()
    SESSION_ID=Int()
    session = Reference (SESSION_ID,Session.SESSION_ID)
    TEST_XRAY_HR_MODULE_ID= Int()
    fullmodule=Reference(FULLMODULETEST_ID, Test_FullModule_XRay_Module.TEST_ID)
    DATA_ID=Int()
    data=Reference(DATA_ID,Data.DATA_ID)
    LAST_PROCESSING_ID = Int()
    COMMENT = Unicode()    
    
    MEASURED_EFFICIENCY = Float() 
    MEASURED_HITRATE_EFF = Float() 
    N_PIXEL_NO_HIT  = Int() 
    MEASURED_HITRATE = Float() 
    MEAN_NOISE_ALLPIXELS = Float() 
    WIDTH_NOISE_ALLPIXELS = Float() 
    MEASURED_HITRATE_NOISE = Float() 
    
    GRADE = Unicode()
    MACRO_VERSION= Unicode()


    def __init__(self,  ROC_POS,
                 SESSION_ID,
                 TEST_XRAY_HR_MODULE_ID,
                 DATA_ID,
                 LAST_PROCESSING_ID,MACRO_VERSION,
                 MEASURED_EFFICIENCY ,
                 MEASURED_HITRATE_EFF,
                 N_PIXEL_NO_HIT,
                 MEASURED_HITRATE,
                 MEAN_NOISE_ALLPIXELS, 
                 WIDTH_NOISE_ALLPIXELS,
                 MEASURED_HITRATE_NOISE,
                 GRADE,
                 COMMENT = ""):
        self.TEST_XRAY_HR_MODULE_ID =                  int(TEST_XRAY_HR_MODULE_ID)
        self.SESSION_ID = int(SESSION_ID)
        self.MEASURED_HITRATE_EFF = float(MEASURED_HITRATE_EFF)
        self.DATA_ID = int(DATA_ID)
        self.MEASURED_EFFICIENCY = float(MEASURED_EFFICIENCY)
        self.LAST_PROCESSING_ID = int(LAST_PROCESSING_ID)
        self.MACRO_VERSION = unicode(MACRO_VERSION)
        self.N_PIXEL_NO_HIT = int(N_PIXEL_NO_HIT)
        self.MEASURED_HITRATE = float(MEASURED_HITRATE)
        self.MEAN_NOISE_ALLPIXELS = float(MEAN_NOISE_ALLPIXELS)
        self.COMMENT = unicode(COMMENT)
        self.WIDTH_NOISE_ALLPIXELS = float(WIDTH_NOISE_ALLPIXELS)
        self.MEASURED_HITRATE_NOISE = float(MEASURED_HITRATE_NOISE)





class Test_FullModule_XRay_HR_Roc_Analysis(object):
    __storm_table__ = "Test_FullModule_XRay_Roc_Analysis"
    TEST_ID = Int(primary=True)
    SESSION_ID=Int()
    session = Reference (SESSION_ID,Session.SESSION_ID)
    DATA_ID=Int()
    data=Reference(DATA_ID,Data.DATA_ID)
    PROCESSING_ID = Int()
    RESULT = Unicode()
    TEST_XRAY_HR_ROC_ID = Int()
    test_xray_hr_roc=Reference(TEST_XRAY_HR_ROC_ID,Test_FullModule_XRay_HR_Roc.TEST_ID )
    MACRO_VERSION = Unicode()
    GRADE = Unicode()
    N_PIXELS_EFF_BELOW_CUT = Int() 
    INTERP_EFF_TESTPOINT = Float() 
    N_HOT_PIXELS = Int() 
    N_COL_BELOW_CUT = Int() 
    ADDR_PIXELS_BAD = Unicode()
    INTERP_EFF_TESTPOINT = Float()
    ADDR_PIXELS_HOT = Unicode()
    N_COL_NONUNIFORM = Int()
    N_BINS_LOWHIGH = Int()
    N_COL_LOWEFF = Int()
    N_EVENTS_LOWEFF_COL = Int()
    N_PIXELS_NOISE = Int()
    ADDR_PIX_NOISE = Unicode()
    COMMENT = Unicode()
    

    def __init__(self,  SESSION_ID,
                 DATA_ID,
                 PROCESSING_ID,
                 TEST_XRAY_HR_ROC_ID,
                 MACRO_VERSION,
                 GRADE,
                 N_PIXELS_EFF_BELOW_CUT,
                 INTERP_EFF_TESTPOINT,
                 N_HOT_PIXELS,
                 N_COL_BELOW_CUT,
                 ADDR_PIXELS_BAD,
                 INTERP_EFF_TESTPOINT,
                 ADDR_PIXELS_HOT,
                 N_COL_NONUNIFORM,
                 N_BINS_LOWHIGH,
                 N_COL_LOWEFF,
                 N_EVENTS_LOWEFF_COL,
                 N_PIXELS_NOISE,
                 ADDR_PIX_NOISE,
                 COMMENT=""):



        self.SESSION_ID = int(SESSION_ID)
        self.DATA_ID = int(DATA_ID)
        self.PROCESSING_ID = int(PROCESSING_ID)
        self.TEST_XRAY_HR_ROC_ID = int(TEST_XRAY_HR_ROC_ID)
        self.MACRO_VERSION = unicode(MACRO_VERSION)
        self.GRADE = unicode(GRADE)
        self.N_PIXELS_EFF_BELOW_CUT = int(N_PIXELS_EFF_BELOW_CUT)
        self.N_COL_NONUNIFORM = int(N_COL_NONUNIFORM)
        self.INTERP_EFF_TESTPOINT = float(INTERP_EFF_TESTPOINT)
        self.N_HOT_PIXELS = int(    N_HOT_PIXELS)
        self.ADDR_PIXELS_HOT = unicode(                 ADDR_PIXELS_HOT)
        self.ADDR_PIXELS_NOISE = unicode(                 ADDR_PIXELS_NOISE)
        self.ADDR_PIXELS_BAD = unicode(                 ADDR_PIXELS_BAD)
        self.N_BINS_LOWHIGH = int(                 N_BINS_LOWHIGH)
        self.N_COL_LOWEFF = int(N_COL_LOWEFF)
        self.N_EVENTS_LOWEFF_COL = int(N_EVENTS_LOWEFF_COL)
        self.N_PIXELS_NOISE= int(N_PIXELS_NOISE)
        self.N_COL_BELOW_CUT = int(N_COL_BELOW_CUT)
        self.N_PIXELS_NOISE_ABOVETH = int(N_PIXELS_NOISE_ABOVETH)
        self.INTERP_EFF_TESTPOINT = float(INTERP_EFF_TESTPOINT)
        self.FULLMODULE_ID = unicode(FULLMODULE_ID)
        self.COMMENT = unicode(COMMENT)
        
