#!/bin/bash
# here is the convention:
# $1 is the tarfile to be accessed
# $2 is the dir where to write the output (in a specific dir)
#   create that dir are $2 (script needs to)
#
rm -rf ${2}.old
mv -f $2 ${2}.old
rm -rf $2
mkdir -p $2
cd $2
tar xf $1

cd /data/pixels/software/psi46expert/trunk/src/macros/
for i in $2/T*; do

/home/robot/Tier0/macrov1.pl  $i >& ${i}.LOG 
done
#execute sruff

exit  0 
