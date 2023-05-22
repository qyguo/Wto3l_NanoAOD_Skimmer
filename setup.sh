#!/bin/bash

export PYTHONPATH=${PYTHONPATH}:${PWD}/

cd /cvmfs/cms.cern.ch/slc7_amd64_gcc700/cms/cmssw/CMSSW_10_6_19/src/
eval `scramv1 runtime -sh`
cd -

#srun --ntasks=1 --cpus-per-task=8 --mem=32gb -t 2000 --pty bash -i
