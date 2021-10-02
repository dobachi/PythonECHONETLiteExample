#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0); pwd)
python ${SCRIPT_DIR}/../python/AirConTemp.py $1 $2
