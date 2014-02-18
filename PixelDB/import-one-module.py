#!/usr/bin/env python

import MySQLdb
import secrets
db=MySQLdb.connect(host="localhost",user=secrets.USER,
                  passwd=secrets.PASSWORD,db="cms-pixel")


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

c.execute("""select barcode,`2d-label`,type,hdi,tbm,rocs,powercable,signalcable,sensor,storage,comment   from modules where barcode like '%722%'""")

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
    tr = Transfer(SENDER="Imported", RECEIVER="Pisa", COMMENT="SINGLE MODULE Import")
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
