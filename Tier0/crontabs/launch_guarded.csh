#!/bin/tcsh 

set guard=$1
set log=$2
set mycommand=$3:q

echo `date +'%d-%m-%Y/%H:%M:%S'` $guard - Starting cron with command $mycommand

set guarddir=/home/robot/cms-pixel-db-pisa/Tier0/crontabs/guards

#if guard exists, do nothing
if ( -f $guarddir/$guard ) then
    echo `date +'%d-%m-%Y/%H:%M:%S'` $guard - lock file exists
    exit 1
endif

# launch command

touch  $guarddir/$guard

set logfile=$log.`date +'%d-%m-%Y_%H:%M:%S'`

eval $mycommand >& $log/$guard.`date +'%d-%m-%Y_%H:%M:%S'`

set code=$?

rm -f  $guarddir/$guard

echo `date +'%d-%m-%Y/%H:%M:%S'` $guard - Execution Finished with code $code

