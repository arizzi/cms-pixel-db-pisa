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


c.execute("""select wafer_id,results,comment,storage from roc_wafer""")


roc_positions = ["03A", "03B", "03C", "03D", "04A", "04B", "04C", "04D", "05A", "05B", "05C", "05D", "06A", "06B", "06C", "06D", "11A", "11B", "11C", "11D", "12A", "12B", "12C", "12D", "13A", "13B", "13C", "13D", "14A", "14B", "14C", "14D", "15A", "15B", "15C", "15D", "16A", "16B", "16C", "16D", "17A", "17B", "17C", "17D", "18A", "18B", "18C", "18D", "20A", "20B", "20C", "20D", "21A", "21B", "21C", "21D", "22A", "22B", "22C", "22D", "23A", "23B", "23C", "23D", "24A", "24B", "24C", "24D", "25A", "25B", "25C", "25D", "26A", "26B", "26C", "26D", "27A", "27B", "27C", "27D", "28A", "28B", "28C", "28D", "29A", "29B", "29C", "29D", "30A", "30B", "30C", "30D", "31A", "31B", "31C", "31D", "32A", "32B", "32C", "32D", "33A", "33B", "33C", "33D", "34A", "34B", "34C", "34D", "35A", "35B", "35C", "35D", "36A", "36B", "36C", "36D", "37A", "37B", "37C", "37D", "38A", "38B", "38C", "38D", "39A", "39B", "39C", "39D", "40A", "40B", "40C", "40D", "41A", "41B", "41C", "41D", "42A", "42B", "42C", "42D", "43A", "43B", "43C", "43D", "44A", "44B", "44C", "44D", "45A", "45B", "45C", "45D", "46A", "46B", "46C", "46D", "47A", "47B", "47C", "47D", "48A", "48B", "48C", "48D", "49A", "49B", "49C", "49D", "51A", "51B", "51C", "51D", "52A", "52B", "52C", "52D", "53A", "53B", "53C", "53D", "54A", "54B", "54C", "54D", "55A", "55B", "55C", "55D", "56A", "56B", "56C", "56D", "57A", "57B", "57C", "57D", "58A", "58B", "58C", "58D", "61A", "61B", "61C", "61D", "62A", "62B", "62C", "62D", "63A", "63B", "63C", "63D", "64A", "64B", "64C", "64D", "65A", "65B", "65C", "65D", "66A", "66B", "66C", "66D", "67A", "67B", "67C", "67D", "68A", "68B", "68C", "68D", "73A", "73B", "73C", "73D", "74A", "74B", "74C", "74D", "75A", "75B", "75C", "75D", "76A", "76B", "76C", "76D"]


#
# now loop over the results
#
a=c.fetchone()
while (a):
    print a
    #get hdi_id
    wafer_id = a[0]
    comment = a[2]
    result = a[1]
    storage = a[3]

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

#
# create all the possible rocs
#

    for pos in roc_positions:
        name = wafer_id+'-'+pos

#        print "POS", name
        roc = Roc(ROC_ID=name, TRANSFER_ID=transfid, COMMENT=comment, WAFER_ID = wafer_id)

        pp = pdb.insertRoc(roc)
        if (pp is None):
            print"<br>Error inserting ROC",name


        print "INSERTED ROC ", roc.ROC_ID

    a=c.fetchone()


