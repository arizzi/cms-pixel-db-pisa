#!/bin/sh
V1=150
V2=100
TEMP=`mktemp`
DATE=`grep "OG from" $1/ivCurve.log | perl -pe 's/.*from//' | perl -pe 's/s\s-*//g; s/h:/:/; s/m:/:/; s/ at//; '`
TIMESTAMP=`date -d"$DATE" +%s`

#Fri 01 Feb 2013 at 15h:43m:05s
MODULE=`echo $1 | perl -pe 's@.*/M@M@; s/^(M[0-9]+).*/\1/'`
cat $1/ivCurve.log  | awk '{if($1 > 1000000 &&  $2 > -1000 && $2 < 1000  ) print $0 }' > $TEMP
TEMPERATURE=`echo $1|awk -F'_' '{print $NF}'|sed "s#/##"| sed "s#m#-#"|sed "s#p#+#"`
STEP=`echo $1|awk -F'_' '{print $NF}'|sed "s#/##"`
SENSOR=$MODULE
OUTDIR=/data/IVOUT/$SENSOR
OUT=$OUTDIR/${TIMESTAMP}.root
mkdir -p $OUTDIR
RESULTS=`root -b -l /home/robot/cms-pixel-db-pisa/Tier0/IVParser/psiNtupler.C\(\"$TEMP\",\"$OUT\",$V1,$V2\) 2>/dev/null | grep Result | perl -pe 's/Results: //'`
echo $RESULTS
I1=`echo $RESULTS | perl -pe 's/(.+) (.+) (.+)/\1/'`
I2=`echo $RESULTS | perl -pe 's/(.+) (.+) (.+)/\2/'`
SLOPE=`echo $RESULTS |  perl -pe 's/(.+) (.+) (.+)/\3/'`

#echo $MODULE $RESULTS $OUT $TIMESTAMP $TEMPERATURE 
rm $TEMP


if [ $SLOPE -gt 2.0 ] || [ $I1 -gt 0.000010  ] ; then  
   GRADE="C"
else
   if [ $I1 -gt 0.000002] ; then
     GRADE="B"
   else
     GRADE="A"
  fi	
fi 

#GRADE
#4) numbers extracted from the IV curve analysis and grading:
#- I( at 150V). Grade 1: I<2muA, grade B: 2<I<10muA and grade C: I>10muA
#- slope: I(at 150V)/I(at 100V). Grade a: slope < 2; grade C: slope >2

TEMP2=`mktemp`
#MODULE=M0001
echo STEP $STEP >>  $TEMP2
/home/robot/cms-pixel-db-pisa/Tier0/IVParser/module2sensor.py $MODULE >> $TEMP2 
echo V1 $V1  >> $TEMP2
echo V2 $V2 >> $TEMP2
echo I1 $I1 >> $TEMP2
echo I2 $I2 >> $TEMP2
echo SLOPE $SLOPE >> $TEMP2
echo TEMPERATURE $TEMPERATURE  >> $TEMP2
echo GRADE $GRADE >> $TEMP2
echo DATE $TIMESTAMP >> $TEMP2
echo COMMENT Auto-gen from full test ivCurve.log >> $TEMP

FINALFILENAME='test'
mv $TEMP2 $FINALFILENAME
