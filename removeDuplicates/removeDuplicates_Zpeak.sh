!/bin/bash

rm -f /cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/data/Zpeak/UL/total_data.root
rm -f /cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/data/Zpeak/UL/total_data_no_dupe.root
hadd -fk /cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/data/Zpeak/UL/total_data.root /cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/data/Zpeak/UL/*.root
root -l removeDuplicates/removeDuplicates.C\(\"/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/data/Zpeak/UL/total_data.root\",\"/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/data/Zpeak/UL/total_data_no_dupe.root\"\)
