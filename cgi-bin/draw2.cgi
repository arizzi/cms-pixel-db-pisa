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
import json
import urllib2
import urlparse
import operator

from pixelwebui import *

pdb = PixelDBInterface(operator="webfrontend",center="cern")
pdb.connectToDB()
debug=False

def map2d(data):
   points=[]
   for d in data :	
	if d != "" and len(d) < 30000:
	   try :
		   di=json.loads(d)
	   except :
		if debug :
			print "Ohhh " , d
	   for roc,defs in di.iteritems() :
		m=re.match(".*ROC(.+)",roc)
		rocn=int(m.group(1))
		ry=int(rocn/8)
		rx=rocn%8 if ry == 1 else 7-rocn%8
		xoffset=rx*54
		yoffset=ry*80
		for d in defs :
		      x=d[0]
		      y=d[1]
		      if ry == 0 :
			points.append((54-x+xoffset,y+yoffset))
		      else : 
			points.append((3+x+xoffset,80-y+yoffset))
   return points

def makeHistoFromData(data,out,bins,xmin,xmax):
   ROOT.gStyle.SetPadRightMargin(0.32)
   canvas= ROOT.TCanvas("plot","plot",900,400)
   text=False
   is2d=False
   if True :
	  data=map(lambda x : -100 if x=='n/a' else x,data) 
	  data=map(lambda x : -100 if x=="None" else x,data) 
	  data=map(lambda x : float(x),data)
	  dmin=float(min(data))
	  dmax=float(max(data))
	  if dmax > 0 :
		dmax*=1.1
	  else:
		dmax*=0.9
	  if dmin > 0 :
		dmin*=0.9
	  else:
		dmin*=1.1

#	  print dmin,dmax
	  nbins=100
   if bins and bins != "":
	   nbins=int(bins)
   if xmin and xmin != "":	
	dmin=float(xmin)
   if xmax and xmax != "" :	
	dmax=float(xmax)
#   print nbins,dmin,dmax,xmin,xmax
   if is2d :
	  hist = ROOT.TH2F("his","his",8*60,0,8*60,2*85,0,2*85)
	  canvas.SetLogz()
   else :
	  hist = ROOT.TH1F("his","his",nbins,dmin,dmax)
#   legend = ROOT.TLegend(0.7,0.1,1.0,0.9)
   di={}
   j=0
   for i in data :
	if not text and not is2d:
  	  hist.Fill(float(i),1.0)
	elif is2d :
  	  hist.Fill(float(i[0]),2*85-float(i[1]),1.0)
	else : #except ValueError:
	  v=re.sub('<[^<]+?>', '', "%s"%i)
	  v=re.sub('\([^\(]+?\)', '',v)
	  v=re.sub('&nbsp;', ' ',v)
  	  hist.Fill(v,1.0)
   hist.Draw("COLZ" if is2d else "")
   if log != '0':
	canvas.SetLogy(1)
	canvas.Update()
#   legend.Draw()
   canvas.SaveAs(out.name)


out = tempfile.NamedTemporaryFile(suffix=".png",delete=False)
import cgi
form = cgi.FieldStorage() # instantiate only once!
dtids = form.getlist('dtid')
viewNumber = form.getlist('viewNumber')
objName = form.getlist('objName')
bins = form.getfirst('nbins',None)
xmin = form.getfirst('xmin',None)
xmax = form.getfirst('xmax',None)

if "coltoDraw" in form :
 opener = urllib2.build_opener()
 url = os.environ["REQUEST_URI"] 
 parsed = urlparse.urlparse(url) 
 f = opener.open("http://localhost/cgi-bin/rawPredefinedView-backend.cgi?draw=1&all=%s&%s"%(form.getfirst('all','0'),parsed.query))
 rawdata=f.read()
 js = json.loads(rawdata)['aaData']
 dtids=map(operator.itemgetter(unicode(form.getfirst('coltoDraw'))),js)


log = form.getfirst('log','0')
correct = int(form.getfirst('correct',0))
fixrange = form.getfirst('fixrange')
files =[]
if debug :
 print "Content-Type: text/plain"
 print
makeHistoFromData(dtids,out,bins,xmin,xmax)
f = open(out.name, 'r')
if not debug :
  print "Content-Type: image/png"
  print
  print f.read()
os.unlink(out.name)

