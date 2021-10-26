# Wto3l_NanoAOD_Skimmer

# Skimmer.py

skimmer.py is the main file. Add path to unskimmed MC and data files to input_path under isMC and else. Also add output path.

Modify the logic of the skimmer in this file.

# Out_dict.py

In out_dict.py, choose what branches want to be saved in the skimmed ntuple.

# run_skimmer.sh

Add the names of the datasets you want to skim to the dataset lists. Then run run_skimmer.sh to run.

# Z+X and Z peak skimmers

There is also a Z+X and a 2e Z peak version of the skimmer.py and run_skimmer.sh scripts used for each of those selections. Modify and run those if you are looking for 2e+1mu or 2e, respectively.
