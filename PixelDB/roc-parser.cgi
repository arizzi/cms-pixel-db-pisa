#!/usr/bin/python
import re
from PixelDB import *
pdb = PixelDBInterface(operator="andrea",center="pisa")
pdb.connectToDB()

file = open("rocinputtest.txt")
x=0
y=0
delimiters = []
for line in file :
#  print line
  fields=  re.split('\W+',line)
  #print len(fields) 
 # if len(fields) > 0  :
   # print "--"+fields[0]+"--"
  if len(fields) > 0 and fields[0] == "WAFER" :
     for field in fields : 
      x=y
      y+=re.search(field,line[y:len(line)]).start(0)+len(field)
    #  print x,y
      if y == 5 :
         y+=2 # fix bad alignment in first column
      delimiters.append([x,y])
  else:
   fields = [line[x:y] for (x,y) in delimiters]
   if len(fields) > 15 and re.match(" *[0-9][0-9][A-D]",fields[1]): 
     wafer=re.sub(" ","",fields[0])
     pos=re.sub(" ","",fields[1])
     grade=re.sub(" ","",fields[5])
     idigi =re.sub(" ","", fields[9])
     iana =re.sub(" ","", fields[10])
     vana =re.sub(" ","", fields[14])
     t=pdb.insertTransfer(Transfer(SENDER="",RECEIVER=pdb.operator))
     ppp=pdb.insertRoc(Roc(ROC_ID=wafer+"_"+pos, TRANSFER_ID=t.TRANSFER_ID,WAFER_ID=wafer,ROC_POSITION=pos,GRADING_CLASS=grade,CURRENT_D=idigi,CURRENT_A=iana,VANA=vana))
     if (ppp is None):
         print "Error cannot insert roc"

#  for field in fields :
#     print field , 
#  print "0:", fields[0] , "1:", fields[1], "2:", fields[2]
