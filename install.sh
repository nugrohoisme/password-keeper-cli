#!/bin/bash

DIR=$(dirname $0)

python3 -m virtualenv $DIR/venv
source $DIR/venv/bin/activate
pip install -r $DIR/package.conf
deactivate