#!/usr/bin/python
import re
import sys
DEBUG=1

if DEBUG==1:
  print "ARGV:",sys.argv

if (len( sys.argv )) != 2 :
  print "ERROR: needs 2: filename"
  exit (2)


filename = sys.argv[1]

print "working on FileName ",filename
#
# lines are like
#WAFER     POS  PX PY BIN C GR  IDIG0 IANA0 IDIGI IANAI VDREG VDAC  IANA V24  BLLVL ADSTP  DC DD WB TS DB DP  DPIX ADDR TRIM MASK NSIG NOIS THRO T2F T2P  PCNT PMEAN  PSTD PMCOL PMI PMA   NPH PHFAIL PHOMEAN PHOSTD PHGMEAN PHGSTD  FAIL  FAILSTRING
#K7NEF6T   03C   7  1  0  1  1   23.0   0.4  26.0  19.5  2.05 1.92  23.9 156    4.4  86.0   0  0  0  0  0  0     0    0    0    0    0    0    0          4160  72.8  2.69  1.03  66  85  4160      0    -6.3   17.0   172.2    6.1    23 
#with fixed width fields
            
file = open(filename)
x=0
y=0
delimiters = []
for line in file :
#     print line
     fields=  re.split('\W+',line)
     if len(fields) > 0 and fields[0] == "WAFER" :
         print "learning", len(fields)
         for field in fields : 
             x=y
             y+=re.search(field,line[y:len(line)]).start(0)+len(field)
             print "FIELD",field,x,y
             if y == 5 :
                 y+=2 # fix bad alignment in first column
             delimiters.append([x,y])
         print " LEARNED ", delimiters
     else:
                 fields = [line[x:y] for (x,y) in delimiters]
                 print "GIELDS", fields
                 if len(fields) > 15 and re.match(" *[0-9][0-9][A-D]",fields[1]): 
                     wafer=re.sub(" ","",fields[0])
                     pos=re.sub(" ","",fields[1])
                     grade=re.sub(" ","",fields[5])
                     idigi =re.sub(" ","", fields[9])
                     iana =re.sub(" ","", fields[13])
                     vdac =re.sub(" ","", fields[12])
                     v24 = re.sub(" ","", fields[14])
                     defpixel = re.sub(" ","", fields[23])
                     addpixel = re.sub(" ","", fields[24])
                     trimpixel = re.sub(" ","", fields[25])
                     maskpixel = re.sub(" ","", fields[26])
                     nsigpixel = re.sub(" ","", fields[27])
                     noisepixel = re.sub(" ","", fields[28])
                     thpixel = re.sub(" ","", fields[29])
                     phfail = re.sub(" ","", fields[39])
                     comment = (" ".join(fields[45:] )).rstrip()
                     if (DEBUG==1):
                                    print "ROC_ID",wafer+"-"+pos, "RESULT",grade,"CURRENT_D",idigi, "CURRENT_A",iana, "VDAC", vdac,   "DEFECTPIXELS", defpixel,"ADDRPIXEL",addpixel, "TRIMP", trimpixel, "MASKPIXEL",maskpixel,"NSIGPIXEL", nsigpixel, "NOISEPIXEL", noisepixel, "THRESHPIXEL", thpixel, "PHFAIL", phfail, "COMMENT", comment 
#


sys.exit(0)
