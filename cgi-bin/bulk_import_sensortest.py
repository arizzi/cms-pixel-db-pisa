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

center = "Pisa"
operator="Tommaso"

pdb = PixelDBInterface(operator=operator,center=center)
pdb.connectToDB()

#insert most max, for debugging
num=0


filenamePattern = '*.inf.txt'

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


s = Session (OPERATOR=operator, CENTER=center)

#
# here we go
#

#
# use the system
#
tmpfile = "tmp9999.txt"
os.system("rm -f "+tmpfile)
os.system("find "+basedir+" -name "+filenamePattern+" > "+tmpfile)
f=open(tmpfile)


for line in f:
    if (num >= maxentries):
        break
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>> Studying "+line
    dir = os.path.dirname(line)
    print " DIR IS ", dir
    
    num = num+1
    rr = pdb.insertTestSensorDir(dir,s)
    if rr is None:
        print"-->Error inserting Sensor test  ..."
    else:
        print "done!"            

f.close()

print "DONE"
