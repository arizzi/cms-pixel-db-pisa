#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import MySQLdb
db=MySQLdb.connect(host="cmspixel.pi.infn.it",user="tester",
                  passwd="pixels",db="cms-pixel")


c=db.cursor()
d=db.cursor()

c.execute("""select barcode,comment,testresult,storage from hdis""")


#create a session in the test_pixel DB

d.execute("""INSERT INTO test_pixel.sessions (center,operator,comment) VALUES (%s,%s,%s)""",["Pisa","Robot","Bulk insert"])

d.execute("""select max(session_id) from test_pixel.sessions""")

sessionid  = (d.fetchone())[0]

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
    d.execute("""INSERT INTO test_pixel.test_data (urls,pfns,comment) VALUES (%s,%s,%s)""",["",pnf,"Bulk Insert"])
    d.execute("""select max(data_id) from test_pixel.test_data""")
    dataid  = (d.fetchone())[0]

    d.execute("""INSERT INTO test_pixel.test_hdi (session_id,hdi_id,result,data_id) VALUES (%s,%s,%s,%s)""",[sessionid,hdi_id,result,dataid])
    # i need the test id
    d.execute("""select max(test_id) from test_pixel.test_hdi""")
    testid  = (d.fetchone())[0]
    #since i create out of the blue, i need a transfer
    d.execute("""insert into test_pixel.transfers  (sender,receiver,comment) VALUES (%s,%s,%s)""",["imported","Pisa","Bulk Insert"])
    d.execute("""select max(transfer_id) from test_pixel.transfers""")
    transfid  = (d.fetchone())[0]
    # insert the hdi!
    d.execute("""INSERT INTO test_pixel.inventory_hdi (hdi_id,transfer_id, comment) VALUES (%s,%s,%s)""",[hdi_id,transfid,comment])

