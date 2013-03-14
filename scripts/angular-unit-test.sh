#!/bin/bash

# Run all angular unit tests with testacular
# 
# When run without arguments, it will do a single run (e.g. as part of a build)
# 
# When run with '-w', it will stay running, watch over file changes and
# trigger a re-run when these are modified (useful during development).

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
