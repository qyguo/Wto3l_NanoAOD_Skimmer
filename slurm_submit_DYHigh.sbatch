#!/bin/bash
#SBATCH --job-name=DYHigh             # Job name.
#SBATCH --output=DYHigh.log    # Output file name. NOTE: %j=jobID
#SBATCH --error=DYHigh_error.log      # Error file name.
#SBATCH --mem=32gb                   # RAM request on a node. Default is 2gb.
#SBATCH --time=24:00:00               # Time limit (hh:mm:ss).
#SBATCH --account=Avery    # Use resources from this account.
#SBATCH --mail-user=nikmenendez@ufl.edu  # Get emailed the job status.
#SBATCH --mail-type=NONE              # Job status options: BEGIN, NONE, ALL, FAIL, NONE

# Put the code you want to run below:
pwd; hostname; date

cd /orange/avery/nikmenendez/Wto3l/Skimmer/PyNanoSkimmer/

source /orange/avery/nikmenendez/Wto3l/Skimmer/PyNanoSkimmer/setup.sh

source /orange/avery/nikmenendez/Wto3l/Skimmer/PyNanoSkimmer/run_skimmer_DYHigh.sh 
