#!/usr/bin/python
import tempfile
import sys
import ROOT
import re
import numpy as n
sys.path.append("../PixelDB")
from storm.properties import *
from storm.references import *
from storm import *
from PixelDB import *
import random

from pixelwebui import *

pdb = PixelDBInterface(operator="webfrontend",center="cern")
pdb.connectToDB()

def findFileFromTestID(id) :
  o = pdb.store.find(Test_IV ,Test_IV.TEST_ID==id).one()
  if o:
 	 return o.data.PFNs,"%s(%s)" %(o.SENSOR_ID,o.TYPE)
  else:
         return None 

def readIVFile(ff):
	f = open(ff, "r")
	lines = f.readlines()
	i=[]
	v=[]
	for line in lines:
	  line= re.sub("#.*","",line)
	  line= re.sub("^\s*","",line)
	  fields = re.split("\s+",line)
	  print fields
	  if len(fields) >= 2 and fields[0]!= '' and fields[1] != '':
		print fields 
		v.append(float(fields[0]))
		i.append(float(fields[1]))
	return (i,v)

def makeTGraph((ii,vv)) :
	i = n.array(ii)
        v =  n.array(vv)
        graph = ROOT.TGraph(len(i),v,i)
        return graph

colors = [1,2,4,5,6]

def makePlotForFiles(files):
   print files
   canvas= ROOT.TCanvas("plot") 
   g = []
   i=0
   legend = None
   for f,name in files:
      g.append(makeTGraph(readIVFile(f)))
      g[-1].SetMarkerColor(colors[i])
      g[-1].SetLineColor(colors[i])
      g[-1].SetMarkerStyle(20)
      if len(g) == 1 :
        g[-1].Draw("ALP")
	legend = ROOT.TLegend(0.2,0.7,0.7,0.9)
	legend.SetFillStyle(0)
	legend.AddEntry(g[-1],name,"LP")
      else:	
	g[-1].Draw("LP")
	legend.AddEntry(g[-1],name,"LP")
      i+=1 
   legend.Draw()
   canvas.SaveAs(out.name)


out = tempfile.NamedTemporaryFile(suffix=".png",delete=False)
import cgi
form = cgi.FieldStorage() # instantiate only once!
tests = ['42209']
#tests = form.getlist('test')
files =[]
for t in tests:
   fn = findFileFromTestID(int(t))
   if fn :
	files.append(fn)
makePlotForFiles(files)

print "Content-Type: image/png"
print
#findFileFromTestID(40680)
f = open(out.name, 'r')
print f.read()
os.unlink(out.name)

