#!/bin/bash

BASE_DIR=`dirname $0`
options="--single-run"

if [ "$1" == "-w" ]
then
    options="--no-single-run"
fi

echo ""
echo "Starting Testacular Server (http://vojtajina.github.com/testacular)"
echo "-------------------------------------------------------------------"

testacular start $BASE_DIR/../config/testacular.conf.js $options $*
