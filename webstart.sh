#!/bin/bash
cd /home/chrisg/steemit/
if ps -ef | grep -v grep | grep curate.py ; then
        exit 0
else
	cd /home/chrisg/steemit
	export FLASK_APP=/home/chrisg/steemit/curate.py
	/home/chrisg/miniconda3/bin/python3.6 -m flask run --host=0.0.0.0
fi
