#!/bin/tcsh

cd /home/cmsweb/cms-pixel-db-pisa/Tier0/crontabs/log
set pattern=`date +'%d-%m-%Y'`

tar zcvf logs_$pattern.tar.gz insert*${pattern}* process*${pattern}* 
rm -f insert*${pattern}* process*${pattern}* 

