#!/bin/bash
#SBATCH --job-name=DY9_Skim_9             # Job name.
#SBATCH --output=DY9_9.log    # Output file name. NOTE: %j=jobID
#SBATCH --error=DY9_9_error.log      # Error file name.
#SBATCH --mem=4gb                   # RAM request on a node. Default is 2gb.
#SBATCH --time=24:00:00               # Time limit (hh:mm:ss).
#SBATCH --account=Avery    # Use resources from this account.
#SBATCH --mail-user=nikmenendez@ufl.edu  # Get emailed the job status.
#SBATCH --mail-type=NONE              # Job status options: BEGIN, NONE, ALL, FAIL, NONE

# Put the code you want to run below:
pwd; hostname; date

source /orange/avery/nikmenendez/Wto3l/Skimmer/PyNanoSkimmer/setup.sh

source /orange/avery/nikmenendez/Wto3l/Skimmer/PyNanoSkimmer/ZPeak_attempt/run_skimmer_Zpeak_0.sh DYJetsToLL_M50_9 
