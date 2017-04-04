#!/bin/bash

sublist=$1
srcdir='/scr/ilz2/LEMON_LSD'

while read sub
do

    cd /afs/cbs.mpg.de/projects/mar004_lsd-lemon-preproc/

    if [ -d probands/${sub}/ ] ; then
	# copy freesurfer and structural data to ilz2
	echo "removing subject from ilz"
	rm -rf ${srcdir}/${sub}/preprocessed/anat/*
	rm -rf ${srcdir}/freesurfer_mark/${sub}/*
	echo "copying freesurfer data ${sub}"
	cp -r freesurfer/${sub}/* ${srcdir}/freesurfer_mark/${sub}/
	echo "copying anat data"
	cp -r probands/${sub}/preprocessed/anat/* ${srcdir}/${sub}/preprocessed/anat/
	echo "${sub} done"

    fi

done < $sublist



