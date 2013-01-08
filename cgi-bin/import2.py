#!/usr/bin/env python

import MySQLdb
db=MySQLdb.connect(host="cmspixel.pi.infn.it",user="tester",
                  passwd="pixels",db="cms-pixel")


from PixelDB import *

c=db.cursor()

c.execute("""select barcode,comment,testresult,storage from hdis""")


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
# now loop over the results
#
a=c.fetchone()
while (a):
    print a
    a=c.fetchone()
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

