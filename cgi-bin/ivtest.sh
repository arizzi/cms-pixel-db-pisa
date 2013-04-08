#!/bin/sh

if [  -f $1/IV.LOG ];
then
    MODULE=`cat $1/IV.LOG|head -1|awk '{print $1}'`
    I150V=`cat $1/IV.LOG|head -1|awk '{print $2}'`
    I150100=`cat $1/IV.LOG|head -1|awk '{print $3}'`
    PFN=`cat $1/IV.LOG|head -1|awk '{print $4}'`
    TIMESTAMP=`cat $1/IV.LOG|head -1|awk '{print $5}'`
echo  $MODULE $I150V $I150100 $PFN $TIMESTAMP
else
 exit 1 
fi

exit 0
