#!/usr/bin/python
import re
import sys
DEBUG=1
from PixelDB import *
pdb = PixelDBInterface(operator="andrea",center="pisa")
pdb.connectToDB()

if DEBUG==1:
  print "ARGV:",sys.argv

if (len( sys.argv )) != 5 :
  print "ERROR: needs 4 PAMWETERS (the txt and the ps) + (center operator)"
  exit (2)

sess = Session (OPERATOR = sys.argv[4], CENTER = sys.argv[3])
ppp = pdb.insertSession(sess)
if (ppp is None):
  print "ERROR INSERTING SESSION"
  exit (3)
  
ppp=pdb.insertRocTestsFromDir(sess.SESSION_ID, sys.argv[1], sys.argv[2])
if (ppp is None):
  print "Error cannot insert roc"
exit(0)
