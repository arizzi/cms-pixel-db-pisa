import glob
import re
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

for wafer in glob.glob("*_list.txt"):
    print "opened wafer"
    mydict = {}
    for l in open(wafer).readlines():
        if l.startswith("WAFER"): continue
        p=0
        for f in fields:
            if f[1]>0:
                s=l[p:p+f[1]]
            else:
                s=l.strip()[p:]
            p+=f[1]
            mydict[f[0]] = re.sub(" ","",s)

#            print "%10s  '%s'"%(f[0],s)
        print "DICT",mydict


    

