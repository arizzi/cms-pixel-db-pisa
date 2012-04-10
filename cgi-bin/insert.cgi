#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
from datetime import *
cgitb.enable()

print "Content-Type: text/html"
print


from MySQLdb import *
from storm.locals import *
database = create_database("mysql://tester:pixels@cmspisa001/test_pixel")
store = Store(database)

from Objects import *
 
bm = store.find( BareModule ).one()
temp = (bm.roc(0))
#print "Roc id ", temp.LASTTEST_ROC

#
# add new one
#

newtransf = Transfer(3,'pippo','pluto')
#newtransf = Transfer()
#newtransf.SENDER=u'cheneso'
#newtransf.RECEIVER=u'io'
#newtransf.RECEIVED_DATE=date.today()
#newtransf.ISSUED_DATE=date(1955,6,7)
#newtransf.STATUS=u'buono!'
#newtransf.COMMENT=u'aaaaaa'##

#print "\n adesso: ",newtransf.TRANSFER_ID

#store.add(newtransf)

#print "\n adesso: ",newtransf.TRANSFER_ID


#store.commit()
#print "SALVATO"

#print "\n adesso: ",newtransf.TRANSFER_ID






