#!/usr/bin/env python

# enable debugging
import sys
import cgitb
from datetime import *
cgitb.enable()
import re
import cgi


print "Content-Type: text/html"
print
print "<html>\n        <head>\n         "      

sys.path.append("../../PixelDB")
sys.path.append("..")

from storm.properties import *
from storm.references import *
from storm.variables import (
    Variable, VariableFactory, BoolVariable, IntVariable, FloatVariable,
    DecimalVariable, RawStrVariable, UnicodeVariable, DateTimeVariable,
    DateVariable, TimeVariable, TimeDeltaVariable, PickleVariable,
    ListVariable, EnumVariable)

from storm import *
import random
import ConfigParser
from pixelwebui import *

from PixelDB import *
sys.path.append("/home/robot/cms-pixel-db-pisa/Tier0")
from  PixelTier0 import *
import random


pt0 = PixelTier0()
pt0.connectToDB()
form = cgi.FieldStorage() # instantiate only once!
procid = form.getfirst("processingrun","empty")
if procid != "empty" :
	pr=pt0.store.find(ProcessingRun,ProcessingRun.RUN_ID==int(procid))[0]
	it=pt0.store.find(InputTar,InputTar.TAR_ID==pr.TAR_ID)[0]
	pr2=pr.makeReRunCopy()
	it.status=u'new'
	pt0.store.add(pr2)
	pt0.store.commit()
	print pr.RUN_ID,it.TAR_ID,pr2.RUN_ID

