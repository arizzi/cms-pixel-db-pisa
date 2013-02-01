#!/bin/sh

if [ ! -f $1/46.out ];
then
    exit 1
fi


MODULE=`head -n 1 $1/46.out | perl -pe 's#.*(M[0-9]+)[^0-9]*.*/.*#\1#'`
TEMP=`head -n 1 $1/46.out | perl -pe 's#.*(M[^/]*)/([^/].*)/.*#\2#'`
DATE=`head -n 3 $1/46.out | tail -n 1`
TIMESTAMP=`date -d"$DATE" +%s`
CKSUM=`cksum $1/FullTest.root|awk '{print $1}'`

echo $TIMESTAMP $MODULE $TEMP $CKSUM
#echo $MODULE


exit 0
