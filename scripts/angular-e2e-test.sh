#!/bin/bash

# Run angular end to end tests.
# Requires a running server that must be started separately,
# e.g. with runserver.sh

BASE_DIR=`dirname $0`

echo ""
echo "Starting Testacular Server (http://vojtajina.github.com/testacular)"
echo "-------------------------------------------------------------------"

testacular start $BASE_DIR/../config/testacular-e2e.conf.js $*
