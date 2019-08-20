#!/bin/sh

echo "Dir of setWLSEnv.sh: "$1
echo "script:              "$2 
echo "Args of script:      "$3
echo

/bin/bash -c "source $1/setWLSEnv.sh && java weblogic.WLST wlst.py $2 $3"