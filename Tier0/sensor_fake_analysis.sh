#!/bin/bash
# here is the convention:
# $1 is the tarfile to be accessed
# $2 is the dir where to write the output (in a specific dir)
#   create that dir are $2 (script needs to)
#
touch /tmp/outdebug
date >> /tmp/outdebug
echo MACROTEST PARAMETERS $1 $2 >>  /tmp/outdebug

rm -rf ${2}.old
mv -f $2 ${2}.old
rm -rf $2
mkdir -p $2
cd $2
#
# i go up once to go to the main dir
#
tar zxf $1

exit  0 
