!/bin/bash

#rm -f /cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/data/Zpeak/Eff/total_data.root
#rm -f /cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/data/Zpeak/Eff/total_data_no_dupe.root
#hadd -fk /cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/data/Zpeak/Eff/total_data.root /cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/data/Zpeak/Eff/*.root
hadd -fk /cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/background/Zpeak/Eff/DYJetsToLL_M50.root /cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/background/Zpeak/Eff/DYJetsToLL_M50_*.root
#root -l removeDuplicates/removeDuplicates.C\(\"/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/background/Zpeak/Eff/DYJetsToLL_M50.root\",\"/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/background/Zpeak/Eff/DYJetsToLL_M50_no_dupe.root\"\)
