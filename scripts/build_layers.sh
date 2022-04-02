#!/bin/bash

# Exit if any of the intermediate steps fail
set -e

LAYERS_DIR="build/layers"
REQUIREMENTS_FILE="build/requirements.txt"

if [ -d $LAYERS_DIR ]
then
    rm -r $LAYERS_DIR
fi

mkdir -p "$LAYERS_DIR"
poetry export --output="$REQUIREMENTS_FILE"
pip install --quiet -r "$REQUIREMENTS_FILE" -t "$LAYERS_DIR/python/lib/python3.9/site-packages/"