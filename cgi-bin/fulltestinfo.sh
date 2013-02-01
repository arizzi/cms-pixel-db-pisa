#!/bin/sh

MODULE=`head -n 1 $1/46.out | perl -pe 's#.*(M[^/]*)/.*#\1#'`
TEMP=`head -n 1 $1/46.out | perl -pe 's#.*(M[^/]*)/([^/].*)/.*#\2#'`
DATE=`head -n 3 $1/46.out | tail -n 1`
TIMESTAMP=`date -d"$DATE" +%s`
CKSUM=`cksum $1/FullTest.root|awk '{print $1}'`

echo $TIMESTAMP $MODULE $TEMP $CKSUM


