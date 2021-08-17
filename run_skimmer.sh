#srun --ntasks=1 --cpus-per-task=8 --mem=16gb -t 600 --pty bash -i

echo -e "Sample,Passed Trigger,Had No b Jets,Found 3 Good Muons,Found Z' Candidate,Overall Efficiency" > Tables/cut_list.txt
echo -e "Sample,Medium Id,Sip3d,dxy,dz,Isolation" > Tables/GoodMu_list.txt
echo -e "Sample,Muon Signs,Leading pT,Subleading pT,Trailing pT,3 Muon Invariant Mass" > Tables/ZpCandidate_list.txt

dataset_list=()
isMC=()

dataset_list+=( "DYJetsToLL_M10To50" )
dataset_list+=( "DYJetsToLL_M50" )
dataset_list+=( "TTJets_DiLept" )
dataset_list+=( "WZTo3LNu" )
dataset_list+=( "ZZTo4L" )
dataset_list+=( "WJetsToLNu" )
dataset_list+=( "WWTo2L2Nu" )

dataset_list+=( "DoubleMuon_B" )
dataset_list+=( "DoubleMuon_C" )
dataset_list+=( "DoubleMuon_D" )
dataset_list+=( "DoubleMuon_E" )
dataset_list+=( "DoubleMuon_F" )

dataset_list+=( "Wto3l_M1" )
dataset_list+=( "Wto3l_M4" )
dataset_list+=( "Wto3l_M5" )
dataset_list+=( "Wto3l_M10" )
dataset_list+=( "Wto3l_M15" )
dataset_list+=( "Wto3l_M30" )
dataset_list+=( "Wto3l_M60" )

for i in ${!dataset_list[@]}; do
	python skimmer.py ${dataset_list[i]}
done

python3 Tables/pretty_table.py > Tables/Efficiency_table.txt
cat Tables/Efficiency_table.txt

source removeDuplicates/removeDuplicates_eff.sh



