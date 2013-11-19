#!/bin/bash
# here is the convention:
# $1 is the tarfile to be accessed
# $2 is the dir where to write the output (in a specific dir)
#   create that dir are $2 (script needs to)
#

#
# this is the version for moreweb 96, and the differences are
#  - outdir ($2) is automatically filled by moreweb
#  - the system needs a /tmp dir where to process; it will be deleted afterwards - please note Controller.py needs to be changed to remove "REV00X"
#$3 is macro version
#

echo MACROTEST PARAMETERS $1 $2 $3

MACRO=$3


mkdir -p $2
cd $2
cd ..
GLOBALDIR=`pwd`

#create tmp dir

TEMPDIR=`mktemp -d /tmp/tempXXXX`

cd $TEMPDIR
mkdir INPUT
cd INPUT
#
# i go up once to go to the main dir
#
tar xf $1

cd ../

#set analysis paths
ANALYSISPATH=/home/robot/Analysis/moreweb-98/Analyse

#
# now create the configuration files
#

cp -rf $ANALYSISPATH/*  $TEMPDIR/.

CONFIGPATHTEMPLATE=$ANALYSISPATH/ConfigurationTemplates
CONFIGPATH=$TEMPDIR/Configuration

#
#
#there must be just one directory inside
#
#ADDDIR=`ls -1d *`
cat $CONFIGPATHTEMPLATE/PathsTemplate.cfg |sed "s#DIRECTORY#$TEMPDIR/INPUT#g" | sed "s#OUTGLOBAL#$GLOBALDIR#g"  > $CONFIGPATH/Paths.cfg 

#cd $ANALYSISPATH
#echo PATHS:::::
#cat $CONFIGPATH/Paths.cfg
#pwd
echo TEMPDIR $TEMPDIR
export TARFILE=$1
export MACROVERSION=$MACRO
export PYTHONPATH=$PYTHONPATH:/home/robot/cms-pixel-db-pisa/PixelDB/
python Controller.py
exstatus=$?
echo EXIT STATUS $exstatus
cd /tmp
#rm -rf $TEMPDIR
exit  $exstatus
#
