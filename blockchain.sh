#!/bin/bash
export WALLET=gitface3
export UNLOCK=gitface3

cd /home/chrisg/steemit/

if ps -ef | grep -v grep | grep blockchain.py ; then
        exit 0
else
	/home/chrisg/miniconda3/bin/python3.6 /home/chrisg/steemit/blockchain.py
fi
