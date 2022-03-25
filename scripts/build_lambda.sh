#!/bin/bash

# Exit if any of the intermediate steps fail
set -e

LAMBDA_DIR="build/lambda"

if [ -d $LAMBDA_DIR ]
then
    rm -r $LAMBDA_DIR
fi

# archive_file does not actually zip the containing directory, and 
# we need the "src" directory for Python to resolve imports correctly.
# This workaround copies our "src" directory to an intermediate parent
# directory, which archive_file can then zip safely (including "src").
mkdir -p $LAMBDA_DIR
cp -r src $LAMBDA_DIR