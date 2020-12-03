#!/bin/bash

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
set -e
OLDDIR=$(pwd)

$SCRIPT_DIR/repkey_xor.py $SCRIPT_DIR/data/6.txt "Terminator X: Bring the noise"