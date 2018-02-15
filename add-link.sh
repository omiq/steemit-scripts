#!/bin/bash
if [ -z "$1" ] && [ -z "$2" ]; then
	echo "add-link.sh blog link"

else
	/home/chrisg/miniconda3/bin/python3.6 /home/chrisg/steemit/og-upload.py $1 $2
fi
