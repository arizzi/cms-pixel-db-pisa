#!/usr/bin/python
import sys
import ROOT
import re
sys.path.append("../PixelDB")
from storm.properties import *
from storm.references import *
from storm import *
from PixelDB import *
from pixelwebui import *

pdb = PixelDBInterface(operator="webfrontend",center="cern")
pdb.connectToDB()
import cgi
form = cgi.FieldStorage() # instantiate only once!
id = form.getfirst('id',None)
if id is None :
	if len(sys.argv) > 1:	
		id=sys.argv[1]
zeronine=map(lambda x:"%d"%x,xrange(0,9))
if id is not None :
  newlocation=""
  objName= None
  multiResult={}
  if id[0] == "L" :
	idd=id[1:]
        objName="Test_Logbook"
        idName=idField(objName)
        newlocation="/cgi-bin/viewdetails.cgi?objName=%s&%s=%s"%(objName,idName,idd)
  elif id[0] in letterToObjName and id[1] in zeronine :
	objName=letterToObjName[id[0]]
        idName=idField(objName)
        newlocation="/cgi-bin/viewdetails.cgi?objName=%s&%s=%s"%(objName,idName,id)
  elif id[-1] in ["A","B","C","D"] and id[-2] in zeronine and id[-3] in zeronine :
	objName="Roc"
        idName=idField(objName)
        newlocation="/cgi-bin/viewdetails.cgi?objName=%s&%s=%s"%(objName,idName,id)
  else :
	objToLetter = dict(zip(letterToObjName.values(), letterToObjName.keys()))
	for ob in legalNames :
	  try:
	   idd=id
	   if not idd[0] in zeronine:
		if ob in objToLetter.keys():
			idd=objToLetter[ob]+idd	

	   idName=idField(ob)
	   filter=eval(ob+"."+idName)
	   filterValue = idFieldTypedValue(ob,idd)
	   objects = pdb.store.find(eval(ob),filter==filterValue)
	   for o in objects :
		multiResult[ob]="/cgi-bin/viewdetails.cgi?objName=%s&%s=%s"%(ob,idName,idd)
	 	newlocation=multiResult[ob]	
          except :
		pass 
  if len(multiResult) > 1 :
     print "Content-Type: text/html"
     print
     print "<h2> Multiple matching ID found for %s </h2>" % id
     for o in multiResult :
		print "<li><a href=",multiResult[o],">as ",o,"</a>"
  elif newlocation !="" :
     print "Location: %s" % newlocation
     print
  else :
     print "Content-Type: text/html"
     print
     print id," not found in any category"


#  print newlocation
	

