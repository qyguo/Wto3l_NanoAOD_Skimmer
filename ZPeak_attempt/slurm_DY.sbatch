#!/bin/bash
#SBATCH --job-name=DYlow_Skim             # Job name.
#SBATCH --output=DYlow.log    # Output file name. NOTE: %j=jobID
#SBATCH --error=DYlow_error.log      # Error file name.
#SBATCH --mem=32gb                   # RAM request on a node. Default is 2gb.
#SBATCH --time=48:00:00               # Time limit (hh:mm:ss).
#SBATCH --account=Avery    # Use resources from this account.
#SBATCH --mail-user=nikmenendez@ufl.edu  # Get emailed the job status.
#SBATCH --mail-type=NONE              # Job status options: BEGIN, NONE, ALL, FAIL, NONE

# Put the code you want to run below:
pwd; hostname; date

source /orange/avery/nikmenendez/Wto3l/Skimmer/PyNanoSkimmer/setup.sh

source /orange/avery/nikmenendez/Wto3l/Skimmer/PyNanoSkimmer/ZPeak_attempt/run_skimmer_Zpeak_0.sh DYJetsToLL_M1To10
