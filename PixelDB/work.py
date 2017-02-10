import subprocess
import os.path
import re


class Test(object):
    DEBUG = True

    def safeFloat(self, fl):
        res = -100
        try:
            res = float(fl)
        except ValueError:
            print "Not a float"
            res = -100
        return res


    def safeInt(self, fl):
        res = -100
        try:
            res = int(fl)
        except ValueError:
            print "Not an int"
            res = -100
        return res
        


    def  insertBareModuleMultiTestDir(self, dir,session):
        #
        # here I need to understand which tests to upload
        # I will need to look for the files:
        #  Bare_module_reception.csv : reception test
        #  Bare_module_QA_Bump.csv + defects.json: QA_BumpBonding
        #  Bare_module_QA_Alive.csv + defects.json: QA_PixelAlive
        #  Bare_module_grading.csv: Grading
        #
        # in all cases we need to fix the session a posteriori
        
        # search for QA_Bonding test
        
        isQAInserted = self.insertBareModuleQADir(dir,session)
        if ( isQAInserted is not None):
            return isQAInserted
        
        isGradingInserted = self.insertBareModuleQAGradingDir(dir,session)
        if (isGradingInserted is not None):
            return isGradingInserted
        
        return None


    def insertBareModuleQAGradingDir(self,dir,session):

        return None
        
        ppp = subprocess.Popen("ls -1 "+dir.rstrip()+"/Bare_module_grading.csv", shell=True, stdout=subprocess.PIPE, stderr=None)
        retval = ppp.wait()
        
        if (retval != 0):
            print "no files Bare_module_grading.csv   in ",str(dir)
            return None
        lines = ppp.stdout.readlines()
        if ( len (lines) > 1):
            print "too many Bare_module_grading.csv in ",str(dir)
            return None
        
        filename= lines[0]
        filename = filename.rstrip(os.linesep)
        print "FILENAME = "+filename
        
# WORKING
    


        return None


        

    def insertBareModuleQADir(self, dir,session):
        
        ppp = subprocess.Popen("ls -1 "+dir.rstrip()+"/Bare_module_QA_*.csv", shell=True, stdout=subprocess.PIPE, stderr=None)
        retval = ppp.wait()
        
        if (retval != 0):
            print "no files Bare_module_QA_*.csv   in ",str(dir)
            return None
        lines = ppp.stdout.readlines()
        if ( len (lines) > 1):
            print "too many Bare_module_QA_*.csv in ",str(dir)
            return None

        filename= lines[0]
        filename = filename.rstrip(os.linesep)
        print "FILENAME = "+filename

        
        if (re.match (".*Bump.*",filename))  :
            tyype = "BumpBonding"
        elif (re.match(".*Pixel.*", filename)):
            tyype = "PixelAlive"
        else:
            print" Unknown QA type", filename
            return None
        if self.DEBUG== True:
            print " TYPE IS QA_"+tyype
    
        (bmid, lab, operator, temperature, rh, deadmissingchannels, bbcut, ok) = self.extractorBareModuleQADir(filename)
        if (ok == False):
            print" insertBareModuleQABondingDir received an error"
            return None

#        print "RECEIVED: ",bmid, lab, operator, temperature, rh, deadmissingchannels, bbcut, ok

    # now search for defects.json
        
        if self.DEBUG ==True:
            print "testing file ", dir.rstrip()+"/defects.json"

        ppp2 = subprocess.Popen("ls -1 "+dir.rstrip()+"/defects.json", shell=True, stdout=subprocess.PIPE, stderr=None)
        
        retval = ppp2.wait()
    
        if (retval != 0):
            print "no files defects.json   in ",str(dir)
            return None

        lines2 = ppp2.stdout.readlines()
        if ( len (lines2) > 1):
            print "too many defects.json in ",str(dir)
            return None
        
        filename2= lines2[0]
        filename2 = filename2.rstrip(os.linesep)

        defjson = file(filename2).read()

        if self.DEBUG == True:
            print " DEFECTS ARE ", defjson

        if self.DEBUG != True:
            session.CENTER=lab
            session.OPERATOR = operator
    
            test = Test_BareModule_QA(  SESSION_ID=session.SESSION_ID, BAREMODULE_ID = bmid, TYPE = tyype, TOTAL_FAILURES = deadmissingchannels, TEMPERATURE = temperature, HUMIDITY = rh, FAILURES = defjson )
    
            result =     self.insertBareModuleTest_QA(test)        
            if result is None:
                print " ERROR Inserting BareModuleTest_QA"
                return None
            
            self.store.commit()
        else:
            result = " FAKE FAKE FAKE"


#            at this point, I try and search for DAQ Parameters

            #
            # search for Bare_module_ROC[00-15]_setup.csv
            #
        for num in range(0,16):
            #
            # I need a two digit number like 00
            #
            pattern = str(num).zfill(2)
            searchname = "Bare_module_ROC"+pattern+"_setup.csv"
            
            ppp = subprocess.Popen("ls -1 "+dir.rstrip()+"/"+searchname, shell=True, stdout=subprocess.PIPE, stderr=None)
            retval = ppp.wait()

            if (retval != 0):
                print "no files", searchname,"  in ",str(dir)
                continue
            
            lines = ppp.stdout.readlines()
            if ( len (lines) > 1):
                print "too many "+ searchname+" in ",str(dir)
                continue
            filename= lines[0]	
            filename = filename.rstrip(os.linesep)
                
            print "FILENAME = "+filename

            
            
            (ROC_POS,
             BAREMODULE_ID,
             IDIG  ,
             CLK  ,
             DESER , 
             VDIG  ,
             VANA  ,
             VSH,
             VCOMP,  
             VWLLPR , 
             VWLLSH  ,
             VHLDDEL  ,
             VTRIM  ,
             VTHRCOMP , 
             VIBIAS_BUS,  
             VIBIAS_SF  ,
             VOFFSETOP  ,
             PHOFFSET ,
             VION ,
             VCOMP_ADC ,
             PHSCALE ,
             VICOLOR ,
             VCAL  ,
             CALDEL , 
             VD  ,
             VA  ,
             CTRLREG,  
             WBC  ,
             RBREG  ,
             TEMPERATURE,
             HUMIDITY                 , ok  ) = self.extractorBareModuleRocDacParametersDir(filename)
            



            
#            print " DAC PARAMETERS: GOT ", ROC_POS,            BAREMODULE_ID,            IDIG  ,            CLK  ,            DESER ,             VDIG  ,            VANA  ,            VSH,            VCOMP,              VWLLPR ,             VWLLSH  ,            VHLDDEL  ,            VTRIM  ,            VTHRCOMP ,             VIBIAS_BUS,              VIBIAS_SF  ,            VOFFSETOP  ,                                                        PHOFFSET ,            VION ,            VCOMP_ADC ,            PHSCALE ,            VICOLOR ,            VCAL  ,            CALDEL ,             VD  ,            VA  ,            CTRLREG,              WBC  ,            RBREG  ,            TEMPERATURE,            HUMIDITY  

            if (ok != True):
                print "cannot extract from ", filename
                continue
                # i can create the test and attach
            # create a data id
            if self.DEBUG != True:
                data_id = Data(PFNs = filename)
                pp = self.insertData(data_id)
                if (pp is None):
                    print "Cannot insert data"
                    continue

                dactest = Test_BM_ROC_DacParameters(
                    ROC_POS       =   ROC_POS         ,
                    BAREMODULE_ID =   BAREMODULE_ID    ,
                    DATA_ID       =   data_id.DATA_ID         ,
                    IDIG          =   IDIG            ,
                    CLK           =   CLK             ,
                    DESER         =   DESER           , 
                    VDIG          =   VDIG            ,
                    VANA          =   VANA            ,
                    VSH           =   VSH             ,
                    VCOMP         =   VCOMP           ,   
                    VWLLPR        =   VWLLPR          , 
                    VWLLSH        =   VWLLSH          ,
                    VHLDDEL       =   VHLDDEL          ,
                    VTRIM         =   VTRIM           ,
                    VTHRCOMP      =   VTHRCOMP         , 
                    VIBIAS_BUS    =   VIBIAS_BUS      ,  
                    VIBIAS_SF     =   VIBIAS_SF       ,
                    VOFFSETOP     =   VOFFSETOP       ,
                    PHOFFSET      =   PHOFFSET        ,
                    VION          =   VION            ,
                    VCOMP_ADC     =   VCOMP_ADC       ,
                    PHSCALE       =   PHSCALE         ,
                    VICOLOR       =   VICOLOR         ,
                    VCAL          =   VCAL            ,
                    CALDEL        =   CALDEL          , 
                    VD            =   VD              ,
                    VA            =   VA              ,
                    CTRLREG       =   CTRLREG         ,  
                    WBC           =   WBC             ,
                    RBREG         =   RBREG           ,
                    SESSION_ID    =   session.SESSION_ID      ,
                    TEMPERATURE   =   TEMPERATURE     ,
                    HUMIDITY      =   HUMIDITY             )
                
                
                ppp = self.insertBareModuleTest_Roc_DacParameters(test)

        return result


    def extractorBareModuleRocDacParametersDir(self, filename):
        file = open(filename)


        ROC_POS = -100 
        BAREMODULE_ID= ""
        IDIG  = -100
        CLK  = -100
        DESER = -100 
        VDIG  = -100
        VANA  = -100
        VSH= -100
        VCOMP= -100  
        VWLLPR = -100 
        VWLLSH  = -100
        VHLDDEL  = -100
        VTRIM  = -100
        VTHRCOMP = -100 
        VIBIAS_BUS= -100  
        VIBIAS_SF  = -100
        VOFFSETOP  = -100
        PHOFFSET = -100
        VION = -100
        VCOMP_ADC = -100
        PHSCALE = -100
        VICOLOR = -100
        VCAL  = -100
        CALDEL = -100 
        VD  = -100
        VA  = -100
        CTRLREG= -100  
        WBC  = -100
        RBREG  = -100
        TEMPERATURE= -100
        HUMIDITY  = -100
        
        while 1:
            line = file.readline()
            
            if self.DEBUG == True:
                print "LINE in Extractor DAC = ", line
                print " AFTER"
                if not line:
                    break

            
            if (re.match(".*:.*",line)):


                words= re.split(':',line)
                words = [i.strip() for i in words]
                
                print "SPLIT : ",words
                
                if len( words)!=2 :
                    continue
                key = words[0]
                value=words[1]


                
                if (key.upper() =="ROC_ID".upper()):
                    ROC_POS = self.safeInt(value.strip())

                if (key.upper() =="Bare_module_ID".upper()):
                    BAREMODULE_ID = value.strip()
                if (key.upper() == "Temperature".upper()):
                    TEMPERATURE = self.safeFloat(value.strip())
                if (key.upper() == "RH".upper()):
                    HUMIDITY = self.safeFloat(value.strip())
                if (key.upper() == "IDig".upper()):
                    IDIG = self.safeInt(re.split("\s+",value.strip())[0])

            else:
                
                # 
                fields = re.split('\s+',line.strip())
                
                fields = [i.strip() for i in fields]
                
                print "SPLIT_fields : ",fields
                
                if len(fields)<3 :
                    continue
                key = fields[1]
                value=fields[2]



            if (key.upper() =="VDIG".upper()):
                VDIG = self.safeInt(value.strip())

            if (key.upper() =="VANA".upper()):
                VANA = self.safeInt(value.strip())

            if (key.upper() =="VSF".upper()):
                VSF = self.safeInt(value.strip())

            if (key.upper() =="VCOMP".upper()):
                VCOMP = self.safeInt(value.strip())

            if (key.upper() =="VWLLPR".upper()):
                 VWLLPR= self.safeInt(value.strip())

            if (key.upper() =="VWLLSH".upper()):
                VWLLSH = self.safeInt(value.strip())

            if (key.upper() =="VHLDDEL".upper()):
                VHLDDEL = self.safeInt(value.strip())

            if (key.upper() =="VTRIM".upper()):
                VTRIM = self.safeInt(value.strip())

            if (key.upper() =="VTHRCOMP".upper()):
                VTHRCOMP = self.safeInt(value.strip())

            if (key.upper() =="VIBias_Bus".upper()):
                VIBIAS_BUS = self.safeInt(value.strip())

            if (key.upper() =="Vbias_sf".upper()):
                VIBIAS_SF = self.safeInt(value.strip())


            if (key.upper() =="VoffsetOp".upper()):
                VOFFSETOP = self.safeInt(value.strip())




            if (key.upper() =="VIon".upper()):
                VION = self.safeInt(value.strip())


            if (key.upper() =="Vcomp_ADC".upper()):
                VCOMP_ADC = self.safeInt(value.strip())


            if (key.upper() =="VIColOr".upper()):
                VICOLOR = self.safeInt(value.strip())


            if (key.upper() =="VCal".upper()):
                VCAL = self.safeInt(value.strip())


            if (key.upper() =="CalDel".upper()):
                CALDEL = self.safeInt(value.strip())


            if (key.upper() =="VD".upper()):
                VD = self.safeInt(value.strip())

            if (key.upper() =="VA".upper()):
                VA = self.safeInt(value.strip())

            if (key.upper() =="CtrlReg".upper()):
                CTRLREG  = self.safeInt(value.strip())

            if (key.upper() =="WBC".upper()):
                WBC = self.safeInt(value.strip())



        ok = True
        if self.DEBUG == True:
            print " SENDING", ROC_POS,BAREMODULE_ID,                IDIG  ,                CLK  ,                DESER ,                 VDIG  ,                VANA  ,                VSH,               VCOMP,                  VWLLPR ,                 VWLLSH  ,                VHLDDEL  ,                VTRIM  ,                VTHRCOMP ,                 VIBIAS_BUS,      VIBIAS_SF  ,                VOFFSETOP  ,                PHOFFSET ,                VION ,                VCOMP_ADC ,                PHSCALE ,                VICOLOR ,                VCAL  ,                CALDEL ,                 VD  ,                VA  ,                CTRLREG,                  WBC  ,                RBREG  ,                TEMPERATURE,                HUMIDITY                 , ok
        

        if (ROC_POS  == -100 or  
            BAREMODULE_ID == ""
# or 
#            IDIG  == None or 
#            CLK  == None or 
#            DESER == None or  
#            VDIG  == None or 
#            VANA  == None or 
#            VSH== None or 
#            VCOMP== None or   
#            VWLLPR == None or  
#            VWLLSH  == None or 
#            VHLDDEL  == None or 
#            VTRIM  == None or 
#            VTHRCOMP == None or  
#            VIBIAS_BUS== None or   
#            VIBIAS_SF  == None or 
#            VOFFSETOP  == None or 
#            PHOFFSET == None or 
#            VION == None or 
#            VCOMP_ADC == None or 
#            PHSCALE == None or 
#            VICOLOR == None or 
#            VCAL  == None or 
#            CALDEL == None or  
#            VD  == None or 
#            VA  == None or 
#            CTRLREG== None or   
#            WBC  == None or 
#            RBREG  == None or 
#            TEMPERATURE== None or 
#            HUMIDITY  == None
            ):
            ok = False
            



        return   (ROC_POS,
             BAREMODULE_ID,
             IDIG  ,
             CLK  ,
             DESER , 
             VDIG  ,
             VANA  ,
             VSH,
             VCOMP,  
             VWLLPR , 
             VWLLSH  ,
             VHLDDEL  ,
             VTRIM  ,
             VTHRCOMP , 
             VIBIAS_BUS,  
             VIBIAS_SF  ,
             VOFFSETOP  ,
             PHOFFSET ,
             VION ,
             VCOMP_ADC ,
             PHSCALE ,
             VICOLOR ,
             VCAL  ,
             CALDEL , 
             VD  ,
             VA  ,
             CTRLREG,  
             WBC  ,
             RBREG  ,
             TEMPERATURE,
             HUMIDITY           
                  , ok  )






    def extractorBareModuleQADir(self,filename):
        # Bare_module_ID: B04322310-08-01
        # Laboratory_ID:  DESY
        # Operator_NickName:      AV
        # Temperature:
        # RH:
        # Dead_Missing_Channels:  383
        # BB_cut_criteria:        33

        file = open(filename)
    
        bmid = None
        lab= None
        temp = None
        rh = None
        dead = None
        bbcut = None
        op = None
        
        while 1:
            line = file.readline()

            if self.DEBUG == True:
                print "LINE in Extractor = ", line
                print " AFTER"
            if not line:
                break
            
                continue
            words= re.split(':',line)
            words = [i.strip() for i in words]

            print "SPLIT : ",words

            if len( words)!=2 :
                continue
            key = words[0]
            value=words[1]
            if (key.upper() =="Bare_module_ID".upper()):
                bmid = value.strip()
            if (key.upper() =="Laboratory_ID".upper()):
                lab = value.strip()
            if (key.upper() == "Operator_NickName".upper()):
                op = value.strip()
            if (key.upper() == "Temperature".upper()):
                temp = self.safeFloat(value.strip())
            if (key.upper() == "RH".upper()):
                rh = self.safeFloat(value.strip())
            if (key.upper() == "Dead_Missing_Channels".upper()):
                dead = self.safeInt(value.strip())
            if (key.upper() == "BB_cut_criteria".upper()):
                bbcut = self.safeInt(value.strip())
            
        ok = True
        
        if bbcut is None:
            bbcut = -1

        if (bmid ==  None  or lab  ==  None  or temp ==  None  or rh ==  None  or dead ==  None  or bbcut ==  None  or op ==  None):
            ok = False
                
#(bmid, lab, operator, temperature, rh, deadmissingchannels, bbcut, ok) 
                
        return (bmid, lab, op, temp, rh, dead, bbcut, ok)




            

    
print "INIZIO TEST"

session=None
dir = "/tmp/pp/B322310-08-01-BareModuleTestBumpBonding-2015-01-27_14h15m_1422364542"

test = Test()  

resu = test.insertBareModuleMultiTestDir(dir,session)

print "RESULT", resu
