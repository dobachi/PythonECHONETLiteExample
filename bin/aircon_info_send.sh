#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0); pwd)
python ${SCRIPT_DIR}/../python/AirConInfoSend.py $1
