#!/bin/bash

cd $(dirname $0)
python3 -m virtualenv venv
source venv/bin/activate
pip install -r package.conf
deactivate