#!/usr/bin/env python
#import cgitb
import sys
import os
from datetime import *
#cgitb.enable()

from PixelDB import *
import random
import re

#from storm.tracer import debug
#debug(True, stream=sys.stdout)


pdb = PixelDBInterface(operator="tommaso",center="pisa")
pdb.connectToDB()

#insert most max, for debugging
num=0


filename = 'summaryTest.txt'


print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

if (len(sys.argv) != 2):
    print "Accepting just one argument: a txt file with all the files to study"
    exit(1)

#
#
#
basedir = sys.argv[1]

#
# here we go
#

s = Session("Pisa", "Tommaso")
pdb.insertSession(s)

#
# use the system
#

f=open(basedir)


for line in f:
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>> Studying "+line
    workdir = re.sub(filename,'',line)
    #        print "Studying "+workdir
    print "Inserting "+workdir+" ....."
    num = num+1
    rr = pdb.insertTestFullModuleDir(workdir,s.SESSION_ID)
    if rr is None:
        print"-->Error inserting test FM ..."
    else:
        print "done!"            

f.close()

print "DONE"
