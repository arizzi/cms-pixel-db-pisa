#!/usr/bin/python
import re
import sys
import glob
from PixelDB import *

DEBUG=1
INSERTMISSINGROCS=1

fields=(
 ("WAFER",9,"%-9s","waferId"),
 ("POS"  ,4,"%i%i%c","mapY,mapX,ABCD[p->mapPos]"),
 ("PX"   ,4,"%2i","picX"),
 ("PY"   ,3,"%2i","picY"),
 ("BIN"  ,3,"%2i","bin"),
 ("C"    ,3,"%i","pickClass"),
 ("GR"   ,3,"%2i","pickGroup"),
 ("IDIG0",7,"%5.1f","IdigOn"),
 ("IANA0",6,"%5.1f","IanaOn"),
 ("IDIGI",6,"%5.1f","IdigInit"),
 ("IANAI",6,"%5.1f","IanaInit"),
 ("VDREG",6,"%5.2f","probecard.vd_reg"),
 ("VDAC" ,5,"%4.2f","probecard.v_dac"),
 ("IANA" ,6,"%4.1f","InitIana"),
 ("V24"  ,4,"%3i","InitVana"),
 #("BLL"  ,7,"%5.1f",""),
 ("ADSTP",6,"%5.1f","addressStep"),
 ("DC"   ,4,"%2i","nColDefect"),
 ("DD"   ,3,"%2i","nColDead"),
 ("WB"   ,3,"%2i","nColWBC"),
 ("TS"   ,3,"%2i","nColTS"),
 ("DB"   ,3,"%2i","nColDB"),
 ("DP"   ,3,"%2i","nColNoPix"),
 ("DPIX" ,6,"%4i","nPixDefect"),
 ("ADDR" ,5,"%4i","nPixAddrDefect"),
 ("TRIM" ,5,"%4i","nPixNoTrim)"),
 ("MASK" ,5,"%4i","nPixUnmaskable"),
 ("NSIG" ,5,"%4i","nPixNoSignal"),
 ("NOIS" ,5,"%4i","nPixNoisy"),
 ("THRO" ,5,"%4i","nPixThrOr"),
 #("T2F"  ,5,"%3i","pixtest2 >> 8"),
 #("T2P"  ,4,"%3i","pixtest2 & 0xff"),
 ("PCNT",6,"%i","n"),
 ("PMEAN",6,"%5.1f","pm"),
 ("PSTD",6,"%5.2f","pstd"),
 ("PMCOL",6,"%5.2f","pm_col_max"),
 ("PMI",4,"%3i","pm_pmin"),
 ("PMA",4,"%3i","pm_pmax"),
 ("NPH" ,6,"%4i","nPh"),
 ("PHFAIL",7,"%4i","nPhFail"),
 ("PHOMEAN",8,"%7.1f","ph1mean"),
 ("PHOSTD",7,"%7.1f","ph1std"),
 ("PHGMEAN",8,"%7.1f","ph21mean"),
 ("PHGSTD",7,"%7.1f","ph21std"),
 ("FAIL",6,"%3i","failcode"),
 ("FAILSTRING",0,"","PrintFailSTring()")
)



pdb = PixelDBInterface(operator="andrea",center="pisa")
pdb.connectToDB()

if DEBUG==1:
  print "ARGV:",sys.argv

if (len( sys.argv )) != 7 :
  print "ERROR: needs 6 PARAMETERS the txt(can be multiple, like  '*.txt'), the center, the operator, the year, the month, the day"
  exit (2)

sess = Session (OPERATOR = sys.argv[3], CENTER = sys.argv[2], DATE = datetime(int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])))
ppp = pdb.insertSession(sess)
if (ppp is None):
  print "ERROR INSERTING SESSION"
  exit (3)
  
#loop!

lista = glob.glob(sys.argv[1])
print "ECCO",sys.argv[1]
print "LISTA = ", lista

#exit(4)

for wafer in lista:
  print"opened file", wafer
  for l in open(wafer).readlines():
    mydict={}
    if l.startswith("WAFER"): 
      continue
    p=0
#    print "LINE ", l
    for f in fields:
            if f[1]>0:
                s=l[p:p+f[1]]
            else:
                s=l.strip()[p:]
            p+=f[1]
            mydict[f[0]] = re.sub(" ","",s)
# fill    
# if roc does not exist, create it    
    

    
#
#corrections
    if (mydict['PHFAIL'] == '' ):
      mydict['PHFAIL'] = '-99'
    if (mydict['DPIX'] == '' ):
      mydict['DPIX'] = '-99'
    if (mydict['VDAC'] == '' ):
      mydict['VDAC'] = '-99'
    if (mydict['IANA'] == '' ):
      mydict['IANA'] = '-99'
    if (mydict['V24'] == '' ):
      mydict['V24'] = '-99'
    if (mydict['IDIGI'] == '' ):
      mydict['IDIGI'] = '-99'
    if (mydict['ADDR'] == '' ):
      mydict['ADDR'] = '-99'
    if (mydict['TRIM'] == '' ):
      mydict['TRIM'] = '-99'
    if (mydict['MASK'] == '' ):
      mydict['MASK'] = '-99'
    if (mydict['NSIG'] == '' ):
      mydict['NSIG'] = '-99'
    if (mydict['NOIS'] == '' ):
      mydict['NOIS'] = '-99'
    if (mydict['THRO'] == '' ):
      mydict['THRO'] = '-99'
    if (mydict['GR'] == '' ):
      mydict['GR'] = '-99'



#



    roc_id = mydict['WAFER']+'-'+mydict['POS']
    sss = pdb.isRocInserted(roc_id)
    if (sss is False):
#      print "ROC_ID not inserted!",roc_id
      if (INSERTMISSINGROCS != 0):
#        print " I insert ROC", roc_id
        t = Transfer(SENDER='NULL', RECEIVER = 'NULL')
        
        tt = pdb.insertTransfer(t)
        if (tt is None):
          print "Error inserting Transfer"
          exit(1)
        roc = Roc(ROC_ID=roc_id, TRANSFER_ID = tt.TRANSFER_ID, WAFER_ID = mydict['WAFER'], ROC_POSITION=mydict['POS'])
        r = pdb.insertRoc(roc)
        if (r is None):
          print "Error inserting ROC", roc_id
          exit(1)
# now I can assume I have the ROC!

    roc_test = Test_Roc(SESSION_ID = sess.SESSION_ID,
                        ROC_ID = roc_id,
                        RESULT = mydict['GR'],
                        V24 = mydict['V24'],
                        IANA = mydict['IANA'],
                        IDIGI = mydict['IDIGI'],
                        VDAC = mydict['VDAC'],
                        DEFECTPIXELS = mydict['DPIX'],
                        ADDRPIXELS = mydict['ADDR'],
                        TRIMPIXELS = mydict['TRIM'],
                        MASKPIXELS= mydict['MASK'],
                        NSIGPIXELS = mydict['NSIG'],
                        NOISEPIXELS = mydict['NOIS'],
                        THRESHOLDPIXELS = mydict['THRO'],
                        PHFAIL = mydict['PHFAIL'],
                        COMMENT = mydict['FAILSTRING'])

    t = pdb.insertRocTest(roc_test)
    if (t is None):
      print "Error inserting ROC TEST", t.TEST_ID
      exit(1)



