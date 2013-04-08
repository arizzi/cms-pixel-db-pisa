#!/bin/bash
# here is the convention:
# $1 is the tarfile to be accessed
# $2 is the dir where to write the output (in a specific dir)
#   create that dir are $2 (script needs to)
#

echo MACROTEST PARAMETERS $1 $2

#rm -rf ${2}.old
#mv -f $2 ${2}.old
#rm -rf $2
mkdir -p $2
cd $2
#
# i go up once to go to the main dir
#
tar zxf $1

# now i should have in lowerdirectoried fulltests, iv, etc

#1) search for fulltests, whch are dirts with FullTest.root

#for all full test */*/*FullTest.root

for i in $2/*/*/*Full?est.root; do
    ln -s $i `dirname $i`/FullTest.root

    cd /data/pixels/software/psi46expert/trunk/src/macros/

    /home/robot/Tier0/macrov1.pl  `dirname $i` >& `dirname $i`/FULLTEST.LOG 
    
    cd -

done

cd $2

#2) search all the dirs containing ivCurve.log

for i in $2/*/*/ivCurve.log; do

    /home/robot/Tier0/IVParser/psiParser.sh `dirname $i` >& `dirname $i`/IV.LOG

done

exit  0 
