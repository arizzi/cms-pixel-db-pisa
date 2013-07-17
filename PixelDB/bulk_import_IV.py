#!/usr/bin/env python
#import cgitb
import sys
import os
from datetime import *
#cgitb.enable()

from PixelDB import *
import random
import re

from storm.tracer import debug
debug(True, stream=sys.stdout)


pdb = PixelDBInterface(operator="tommaso",center="pisa")
pdb.connectToDB()

#insert most max, for debugging
num=0


filename = 'IV.LOG'

maxentries = 100

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

if (len(sys.argv) != 2):
    print "Accepting just one argument: a directory. \n It will recursively loop under that spotting all the tests\n" 
    exit(1)

#
#
#
basedir = sys.argv[1]

#
# here we go
#
center = "Pisa"
operator="Tommaso"

#
# use the system
#
tmpfile = "tmp9999.txt"
os.system("rm -f "+tmpfile)
os.system("find "+basedir+" -name "+filename+" > "+tmpfile)
f=open(tmpfile)


for line in f:
    if (num >= maxentries):
        break
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>> Studying "+line
    workdir = re.sub(filename,'',line)
    #        print "Studying "+workdir
    print "Inserting "+workdir+" ....."
    num = num+1
#    rr = pdb.insertTestFullModuleDir(workdir,s.SESSION_ID)
    rr = pdb.insertTestSensorDir(workdir,center, operator)
    if rr is None:
        print"-->Error inserting test IV ..."
    else:
        print "done!"            

f.close()

print "DONE"
