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
 	 return o.data.PFNs,"%s (%s)" %(o.SENSOR_ID,o.TYPE),o.TEMPERATURE
  else:
         return None 

def readIVFile(ff,temp,correct):
	f = open(ff, "r")
	lines = f.readlines()
	i=[]
	v=[]
	for line in lines:
	  line= re.sub("#.*","",line)
	  line= re.sub("^\s*","",line)
	  fields = re.split("\s+",line)
          if len(fields) >= 2 and fields[0]!= '' and fields[1] != '':
#		print fields 
		v.append(abs(float(fields[0])))
		if correct == 1:
			i.append(corTemp(abs(float(fields[1])),temp))
		else:
			i.append(abs(float(fields[1])))
	return (i,v)

def makeTGraph((ii,vv)) :
	i = n.array(ii)
        v =  n.array(vv)
        graph = ROOT.TGraph(len(i),v,i)
        return graph

colors = [1,2,4,5,6]

def makePlotForFiles(files):
   ROOT.gStyle.SetPadRightMargin(0.32)
   canvas= ROOT.TCanvas("plot","plot",900,400)
   legend = ROOT.TLegend(0.7,0.1,1.0,0.9)
   g = []
   i=0
   for f,name,temp in files:
      g.append(makeTGraph(readIVFile(f,temp,correct)))
      g[-1].SetMarkerColor(colors[i%5])
      g[-1].SetLineColor(colors[i%5])
      g[-1].SetMarkerStyle(20+i/5)
      if len(g) == 1 :
        g[-1].Draw("ALP")
        #canvas.SetPad(0.1,0.1,0.6,0.9)
	legend.SetFillStyle(0)
	legend.AddEntry(g[-1],name,"LP")
   	if log != '0':
         g[-1].SetTitle("IV (log scale)")
	if fixrange == '1':
         g[-1].SetTitle("IV (zoomed)")
#	 g[-1].GetXaxis().SetRangeUser(0,200)	
	 g[-1].GetXaxis().SetLimits(0,200)	
	 g[-1].GetYaxis().SetRangeUser(0,0.3e-5)	
	 g[-1].GetYaxis().SetLimits(0,0.3e-5)
      else:	
	g[-1].Draw("LP")
	legend.AddEntry(g[-1],name,"LP")
      i+=1 
   if log != '0':
	canvas.SetLogy(1)
	canvas.Update()
   legend.Draw()
   canvas.SaveAs(out.name)


out = tempfile.NamedTemporaryFile(suffix=".png",delete=False)
import cgi
form = cgi.FieldStorage() # instantiate only once!
#tests = [40680]#form.getlist('test')
tests = form.getlist('test')
log = form.getfirst('log')
correct = int(form.getfirst('correct',0))
fixrange = form.getfirst('fixrange')
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

