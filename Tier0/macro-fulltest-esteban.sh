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
tar xf $1

#set analysis paths
ANALYSISPATH=/home/robot/Analysis/moreweb/Analyse

echo ECCOMI $ANALYSISPATH $CONFIGPATH $CONFIGPATHTEMPLATE

#
# now create the configuration files
#

TEMPDIR=`mktemp -d \`pwd\`/tempXXXX`
#echo CREATED TEMPDIR $TEMPDIR
mkdir $TEMPDIR

CONFIGPATH=$TEMPDIR/Configuration

cp -rf $ANALYSISPATH/*  $TEMPDIR/.

cd $TEMPDIR

CONFIGPATHTEMPLATE=$ANALYSISPATH/ConfigurationTemplates
CONFIGPATH=$TEMPDIR/Configuration

#
#
#there must be just one directory inside
#
#ADDDIR=`ls -1d *`
cat $CONFIGPATHTEMPLATE/PathsTemplate.cfg |sed "s#DIRECTORY#$2#g" > $CONFIGPATH/Paths.cfg 

#cd $ANALYSISPATH
#echo PATHS:::::
#cat $CONFIGPATH/Paths.cfg
#pwd
echo TEMPDIR $TEMPDIR
export PYTHONPATH=$PYTHONPATH:/home/robot/cms-pixel-db-pisa/PixelDB/
python Controller.py
exstatus=$?
echo EXIT STATUS $exstatus
cd -
rm -rf $TEMPDIR
exit  $exstatus
#
