#!/usr/bin/env python

import MySQLdb
import secrets
db=MySQLdb.connect(host="localhost",user=secrets.USER,
                  passwd=sectrets.PASSWORD,db="cms-pixel")


from PixelDB import *

pdb = PixelDBInterface(operator="tommaso",center="pisa")
pdb.connectToDB()


#create a session in the test_pixel DB

s = Session(CENTER="Pisa", OPERATOR="Tommaso", COMMENT="Bulk Import")
pp = pdb.insertSession(s)
if (pp is None):
    print"<br>Error inserting session"
sessionid = s.SESSION_ID

print sessionid
#
# read
#
c=db.cursor()

#
# start from HDI
#


c.execute("""select barcode,comment,testresult,storage from hdis""")



#
# now loop over the results
#
a=c.fetchone()
while (a):
    print a
    #get hdi_id
    hdi_id = a[0]
    comment = a[1]
    testresult = a[2]
    if (testresult == 'A' or testresult == 'a'):
        result = 1.
    elif (testresult == 'b' or testresult == 'B'):
                result = .5
    elif (testresult == 'c' or testresult == 'C'):
        result = 0
    else:
        result = -1
        
    if (hdi_id ==''):
        a=c.fetchone()
        continue
    pnf = a[3]
    #creata a data

    
    td = Data(PFNs=pnf,COMMENT="Bulk Import")
    pp = pdb.insertData(td)
    if (pp is None):
        print"<br>Error inserting data"

    dataid  = td.DATA_ID

    tr = Transfer(SENDER="Imported", RECEIVER="Pisa", COMMENT="Bulk Import")
    pp = pdb.insertTransfer(tr)
    if (pp is None):
        print"<br>Error inserting transfer"
    transfid= tr.TRANSFER_ID


    hdi = Hdi(TRANSFER_ID =transfid, HDI_ID= hdi_id, COMMENT=comment)

    pp = pdb.insertHdi(hdi)
    if (pp is None):
        print"<br>Error inserting HDI"

    pp = pdb.insertTransfer(tr)

    if (pp is None):
        print"<br>Error inserting Transfer"

    t = Test_Hdi(SESSION_ID=sessionid, HDI_ID = hdi_id, RESULT=result, DATA_ID=dataid)
    if (pp is None):
        print"<br>Error inserting test hdi"

    pp = pdb.insertHdiTest(t)

    print "INSERTED HDI ", hdi.HDI_ID

    a=c.fetchone()


#
# start from TBM
#

c.execute("""select barcode,comment,testresult,storage,gain,bl_a,bl_b from tbms""")

a=c.fetchone()
while (a):
    print a
    #get hdi_id
    tbm_id = a[0]
    if (tbm_id ==''):
        a=c.fetchone()
        continue
    comment = a[1]
    testresult = a[2]
    storage = a[3]
    gain = a[4]
    bl_a = a [5]
    bl_b = a [6]
    
    if (testresult == 'A' or testresult == 'a'):
        result = 1.
    elif (testresult == 'b' or testresult == 'B'):
                result = .5
    elif (testresult == 'c' or testresult == 'C'):
        result = 0
    else:
        result = -1
        
    #creata a data
    
    td = Data(PFNs=storage,COMMENT="Bulk Import")
    pp = pdb.insertData(td)
    if (pp is None):
        print"<br>Error inserting data"

    dataid  = td.DATA_ID

    tr = Transfer(SENDER="Imported", RECEIVER="Pisa", COMMENT="Bulk Import")
    pp = pdb.insertTransfer(tr)
    if (pp is None):
        print"<br>Error inserting transfer"
    transfid= tr.TRANSFER_ID


    tbm = Tbm(TRANSFER_ID =transfid, TBM_ID= tbm_id, COMMENT=comment)

    pp = pdb.insertTbm(tbm)
    if (pp is None):
        print"<br>Error inserting TBM"

    pp = pdb.insertTransfer(tr)

    if (pp is None):
        print"<br>Error inserting Transfer"

    t = Test_Tbm(SESSION_ID=sessionid, TBM_ID = tbm_id, RESULT=result, DATA_ID=dataid, GAIN=gain, BL_A=bl_a, BL_B=bl_b)
    if (pp is None):
        print"<br>Error inserting test tbm"

    pp = pdb.insertTbmTest(t)

    print "INSERTED TBM ", tbm.TBM_ID

    a=c.fetchone()

#
# sensors
#

c.execute("""select barcode,i_150v,`I_150/100`,comment,storage,pretest,finaltest,type from sensors""")

a=c.fetchone()
while (a):
    print a
    #get hdi_id
    sensor_id = a[0]
    if (sensor_id ==''):
        a=c.fetchone()
        continue
    comment = a[3]
    pretest = a[5]
    finaltest = a[6]
    storage = a[4]
    i150v=a[1]
    i150100=a[2]
    type_=a[7]
    
    #creata a data
    
    td = Data(PFNs=storage,COMMENT="Bulk Import")
    pp = pdb.insertData(td)
    if (pp is None):
        print"<br>Error inserting data"

    dataid  = td.DATA_ID

    tr = Transfer(SENDER="Imported", RECEIVER="Pisa", COMMENT="Bulk Import")
    pp = pdb.insertTransfer(tr)
    if (pp is None):
        print"<br>Error inserting transfer"
    transfid= tr.TRANSFER_ID


    sensor = Sensor(TRANSFER_ID =transfid, SENSOR_ID= sensor_id, COMMENT=comment, TYPE=type_)

    pp = pdb.insertSensor(sensor)
    if (pp is None):
        print"<br>Error inserting SENSOR"

    pp = pdb.insertTransfer(tr)

    if (pp is None):
        print"<br>Error inserting Transfer"

    t = Test_Sensor(SESSION_ID=sessionid, SENSOR_ID = sensor_id, PRERESULT=pretest,RESULT=finaltest, DATA_ID=dataid,I_150V=i150v,I_150_100=i150100)
    if (pp is None):
        print"<br>Error inserting test sensor"

    pp = pdb.insertSensorTest(t)

    print "INSERTED SENSOR ", sensor.SENSOR_ID

    a=c.fetchone()

#
#    create fullmodules  - only inventory for the moment
#

c.execute("""select barcode,`2d-label`,type,hdi,tbm,rocs,powercable,signalcable,sensor,storage,comment   from modules""")

a=c.fetchone()
while (a):
    print a
    #get hdi_id
    module_id = a[0]
    if (module_id ==''):
        a=c.fetchone()
        continue
    label2d = a[1]
    type_ = a[2]
    hdi_id = a[3]
    tbm_id = a[4]
    rocs = a[5]
    powercable = a[6]
    signalcable = a[7]
    sensor_id = a[8]
    storage = a[9]
    comment = a[10]




    #
    # first I need to create the rocs
    #
    #
    # create a transfer for this 
    #
    tr = Transfer(SENDER="Imported", RECEIVER="Pisa", COMMENT="Bulk Import")
    pp = pdb.insertTransfer(tr)
    if (pp is None):
        print"<br>Error inserting transfer"
    transfid= tr.TRANSFER_ID
    for i in pdb.splitObjects(rocs):
        #
        # create roc
        #
        roc = Roc(ROC_ID=i, TRANSFER_ID=transfid)
        pp = pdb.insertRoc(roc)
        if (pp is None):
            print"<br>Error inserting ROC ", roc.ROC_ID



    #
    # first I need to create a baremodule, I give it the same id as the module
    #
    #
    # create a transfer for this 
    #
    tr = Transfer(SENDER="Imported", RECEIVER="Pisa", COMMENT="Bulk Import")
    pp = pdb.insertTransfer(tr)
    if (pp is None):
        print"<br>Error inserting transfer"
    transfid= tr.TRANSFER_ID

    bm = BareModule(BAREMODULE_ID=module_id,ROC_ID=rocs,SENSOR_ID=sensor_id,TRANSFER_ID=transfid,  BUILTBY="Imported",COMMENT=comment,TYPE=type_, POWERCABLE=powercable, SIGNALCABLE=signalcable, LABEL2D=label2d)

    pp = pdb.insertBareModule(bm)
    if (pp is None):
        print"<br>Error inserting BAREMODULE"

    print "INSERTED BAREMODULE ", bm.BAREMODULE_ID
    #
    # Now I insert the fullmodule; just inventory at the moment
    #        
    fm = FullModule(FULLMODULE_ID=a[0], BAREMODULE_ID=a[0], HDI_ID=hdi_id, TBM_ID=tbm_id,TRANSFER_ID=transfid, BUILTBY="imported", BUILTON=date.today(), COMMENT=a[10])

    pp = pdb.insertFullModule(fm)
    if (pp is None):
        print"<br>Error inserting Full Module"

    #
    a=c.fetchone()
