#!/usr/bin/env python

#
# this is needed to observe a variety of full tests, ideally at least one per centre 
#


# enable debugging
import cgitb
import commands
import os
import tempfile
import datetime
from time import sleep
import signal
import sys
import PixelTier0
from PixelTier0 import *


pdb = PixelTier0()
pdb.initProcessingJustDB(False)
pdb.connectToDB()


#
# I simply need to call one method!
#

res = pdb.uploadAllTests()
if (res is None):
    print "Problems, stopping..."                                          
else:
    print " FINISHED, worked on ",res.count(), "directories"
