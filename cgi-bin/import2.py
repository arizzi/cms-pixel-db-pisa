#!/usr/bin/env python

import MySQLdb
db=MySQLdb.connect(host="cmspixel.pi.infn.it",user="tester",
                  passwd="pixels",db="cms-pixel")


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
