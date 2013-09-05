#!/usr/bin/env python
# enable debugging
import cgitb
from datetime import *
cgitb.enable()

import sys
sys.path.append("../../PixelDB")
from storm.properties import *
from storm.references import *
from storm import *
from PixelDB import *
import random


pdb = PixelDBInterface(operator="webfrontend",center="cern")
pdb.connectToDB()


import re
import cgi
form = cgi.FieldStorage() # instantiate only once!

print "Content-Type: text/html"
print
print "<html>\n        <head>\n         </head><body>"      
print form.getfirst('center', 'n/a')

action = form.getfirst('submit', 'empty')
# Avoid script injection escaping the user input
action = cgi.escape(action)
if action == "submit" :
    batch = cgi.escape(form.getfirst('Batch', 'empty'))
    if batch == 'empty' :
      print "No batch ID given!" 
    else :   
      if batch[0] != 'B' :
        print "Batch name should start with <b>B</b>, pre-pending it automtically ==> <b>B%s</b><br>" % (batch)
        batch= "B%s"%(batch)
      t = pdb.insertTransfer(Transfer(cgi.escape(form.getfirst('Sender', 'Unknown')),"HERE"))
      s  = pdb.getBatch(batch)
      if not s :
         s = Batch(batch,t.TRANSFER_ID,form.getfirst('center', 'n/a'),cgi.escape(form.getfirst('comment', '')))
         if pdb.insertBatch(s) :
		print "<br><b> Batch inserted </b>"
		print "<br>Create Wafers ?<a href> Yes! </a> <a href>No</a>"
      else :
         print "Batch already exists<br>"
    
else : 
    print "<form action=newBatch.cgi method=POST>"
    print 'Batch ID (e.g. B12345): <input type="text" name="Batch"><br>'
    print 'Production Center: <select name=center><option value="FZK">FZK</option><option value="HPK">HPK</option><option value="ST">ST</option></select><br>'
    print 'Received from : <input type="text" name="Sender"><br>'
    print 'Number of Wafers:  <input type="text" name="NWafers"><br>' 
    print "Comment: <input type=\"text\" name=comment>"    
    print "<input type=\"submit\" name=submit value=submit>"    
    print "</form>"    

