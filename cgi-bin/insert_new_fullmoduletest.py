#!/usr/bin/env python


from datetime import *

from PixelDB import *
import random

#
# add new one
#
pdb = PixelDBInterface(operator="tommaso",center="pisa")
pdb.connectToDB()
newtransf = Transfer(SENDER="pippo",RECEIVER="pluto")
pdb.insertTransfer(newtransf)
print "THE TID IS ", newtransf.TRANSFER_ID
newroc = Roc(ROC_ID=random.randint(1, 10000000), TRANSFER_ID=newtransf.TRANSFER_ID)
pp = pdb.insertRoc(newroc)
if pp is None:
    print "ERRORE ROC", newroc.ROC_ID
newhdi = Hdi(HDI_ID=random.randint(1, 10000000), TRANSFER_ID=newtransf.TRANSFER_ID)
pp = pdb.insertHdi(newhdi)
if pp is None:
    print "ERRORE HDI", newhdi.HDI_ID

newsensor=Sensor(SENSOR_ID=random.randint(1, 10000000) , TRANSFER_ID=newtransf.TRANSFER_ID,TYPE="BOH")
pp = pdb.insertSensor(newsensor)
if pp is None:
    print "ERRORE SENSOR", newsensor.SENSOR_ID

newtbm = Tbm(TBM_ID=random.randint(1, 10000000), TRANSFER_ID=newtransf.TRANSFER_ID)
pp = pdb.insertTbm(newtbm)
if pp is None:
    print "ERRORE TBM", newtbm.TBM_ID

#baremodule
newbm = BareModule(BAREMODULE_ID=random.randint(1, 10000000),ROC_ID=newroc.ROC_ID,SENSOR_ID=newsensor.SENSOR_ID,TRANSFER_ID=newtransf.TRANSFER_ID,  BUILTBY="paperino")
pp = pdb.insertBareModule(newbm)
if pp is None:
    print "ERRORE BAREMODULE", newbm.BAREMODULE_ID

newfm = FullModule (FULLMODULE_ID=random.randint(1, 10000000), BAREMODULE_ID=newbm.BAREMODULE_ID, HDI_ID=newhdi.HDI_ID, TBM_ID=newtbm.TBM_ID, TRANSFER_ID= newtransf.TRANSFER_ID, BUILTBY = "stpcazzo")

pp = pdb.insertFullModule(newfm)
if pp is None:
    print "ERRORE FULLMODULE", newfm.FULLMODULE_ID
#
# tests ...
#
newsession = Session("Pisa", "Tommaso")
pp=pdb.insertSession(newsession)
if pp is None:
    print "ERRORE SESSION", newsession.SESSION_ID

newdata = Data(URLs="so", PFNs="na", COMMENT="sega")
pp=pdb.insertData(newdata)
if pp is None:
    print "ERRORE DATA", newdata.DATA_ID

newtest_fmsession = Test_FullModuleSession (DATA_ID=newdata.DATA_ID,SESSION_ID=newsession.SESSION_ID,FULLMODULE_ID=newfm.FULLMODULE_ID)

pp=pdb.insertFullModuleTestSession(newtest_fmsession)
if pp is None:
    print "ERRORE FMSESSION", newtest_fmsession.TEST_ID


newtest_fmtest1 = Test_FullModule(SESSION_ID=newtest_fmsession.TEST_ID,FULLMODULE_ID=newfm.FULLMODULE_ID,RESULT="una merda",DATA_ID=newdata.DATA_ID,COLDBOX="quella rubata",COLDBOX_SLOT="quello che non abiamo",TEMPNOMINAL=44)
pp=pdb.insertFullModuleTest(newtest_fmtest1)
if pp is None:
    print "ERRORE FMTEST", newtest_fmtest1.TEST_ID
newtest_fmtest2 = Test_FullModule(SESSION_ID=newtest_fmsession.TEST_ID,FULLMODULE_ID=newfm.FULLMODULE_ID,RESULT="una merda",DATA_ID=newdata.DATA_ID,COLDBOX="quella rubata",COLDBOX_SLOT="quello che non abiamo",TEMPNOMINAL=44)
pp=pdb.insertFullModuleTest(newtest_fmtest2)
if pp is None:
    print "ERRORE FMTEST", newtest_fmtest2.TEST_ID
newtest_fmtest3 = Test_FullModule(SESSION_ID=newtest_fmsession.TEST_ID,FULLMODULE_ID=newfm.FULLMODULE_ID,RESULT="una merda",DATA_ID=newdata.DATA_ID,COLDBOX="quella rubata",COLDBOX_SLOT="quello che non abiamo",TEMPNOMINAL=44)
pp=pdb.insertFullModuleTest(newtest_fmtest3)
if pp is None:
    print "ERRORE FMTEST", newtest_fmtest3.TEST_ID


newtest_fmsummary = Test_FullModuleSummary (FULLMODULE_ID=newfm.FULLMODULE_ID, FULLMODULETEST_T1=newtest_fmtest1.TEST_ID, FULLMODULETEST_T2=newtest_fmtest2.TEST_ID, FULLMODULETEST_T3=newtest_fmtest3.TEST_ID, FULLTESTGRADE="cacca", SHORTTESTGRADE="puzza")
pp=pdb.insertFullModuleTestSummary(newtest_fmsummary)
if pp is None:
    print "ERRORE FMSummry", newtest_fmsummary.TEST_ID

#
# create an analysis
#

newtest_fmanalysis = Test_FullModuleAnalysis(FULLMODULE_ID=newfm.FULLMODULE_ID, DATA_ID=newdata.DATA_ID,GRADE="buttalo",HOSTNAME="cmsonline.cern.ch", FULLMODULETEST_ID=newtest_fmtest2.TEST_ID)
pdb.insertFullModuleTestAnalysis(newtest_fmanalysis)
if pp is None:
    print "ERRORE FMAnalysis", newtest_fmanalysis.TEST_ID







