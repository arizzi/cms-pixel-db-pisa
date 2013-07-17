#!/bin/sh
TEMP=`mktemp`
DATE=`grep "OG from" $1/ivCurve.log | perl -pe 's/.*from//' | perl -pe 's/s\s-*//g; s/h:/:/; s/m:/:/; s/ at//; '`
TIMESTAMP=`date -d"$DATE" +%s`

#Fri 01 Feb 2013 at 15h:43m:05s
MODULE=`echo $1 | perl -pe 's@.*/M@M@; s/^(M[0-9]+).*/\1/'`
cat $1/ivCurve.log  | awk '{if($1 > 1000000 &&  $2 > -1000 && $2 < 1000  ) print $0 }' > $TEMP
TEMPERATURE=`echo $1|awk -F'_' '{print $NF}'|sed "s#/##"| sed "s#m#-#"|sed "s#p#+#"`
SENSOR=$MODULE
OUTDIR=/data/IVOUT/$SENSOR
OUT=$OUTDIR/${TIMESTAMP}.root
mkdir -p $OUTDIR
RESULTS=`root -b -l /home/robot/Tier0/IVParser/psiNtupler.C\(\"$TEMP\",\"$OUT\"\) 2>/dev/null | grep Result | perl -pe 's/Results: //'`

echo $MODULE $RESULTS $OUT $TIMESTAMP $TEMPERATURE 

rm $TEMP
