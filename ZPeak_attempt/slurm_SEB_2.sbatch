#!/bin/bash
#SBATCH --job-name=SEB2_Skim             # Job name.
#SBATCH --output=SEB_2.log    # Output file name. NOTE: %j=jobID
#SBATCH --error=SEB_2_error.log      # Error file name.
#SBATCH --mem=4gb                   # RAM request on a node. Default is 2gb.
#SBATCH --time=24:00:00               # Time limit (hh:mm:ss).
#SBATCH --account=Avery    # Use resources from this account.
#SBATCH --mail-user=nikmenendez@ufl.edu  # Get emailed the job status.
#SBATCH --mail-type=NONE              # Job status options: BEGIN, NONE, ALL, FAIL, NONE

# Put the code you want to run below:
pwd; hostname; date

source /orange/avery/nikmenendez/Wto3l/Skimmer/PyNanoSkimmer/setup.sh

source /orange/avery/nikmenendez/Wto3l/Skimmer/PyNanoSkimmer/ZPeak_attempt/run_skimmer_EGC_0.sh SingleElectron_B_2
