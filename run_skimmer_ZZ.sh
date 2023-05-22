#srun --ntasks=1 --cpus-per-task=8 --mem=16gb -t 600 --pty bash -i

echo -e "Sample,Passed Trigger,b Jets Bypass,Found 3 Good Muons,Found Z' Candidate,Overall Efficiency" > Tables/cut_list.txt
echo -e "Sample,Failed 3 Good Muon,Medium Id,Sip3d,dxy,dz,Isolation" > Tables/GoodMu_list.txt
echo -e "Sample,Failed Z' Candidate,Muon Signs,Leading pT,Subleading pT,Trailing pT,3 Muon Invariant Mass" > Tables/ZpCandidate_list.txt
echo -e "Sample,Passed Trigger,Passed 2mu+DZ+Mass,Passed 3mu_12,Passed 3mu_10" > Tables/Trigger_list.txt

bkg_list=()
data_list=()
sig_list=()

#bkg_list+=( "DYJetsToLL_M10To50" )
##bkg_list+=( "DYJetsToLL_M50" )
#bkg_list+=( "TTJets_DiLept" )
#bkg_list+=( "WZTo3LNu" )
##bkg_list+=( "ZZTo4L" )
#bkg_list+=( "WJetsToLNu" )
#bkg_list+=( "WWTo2L2Nu" )
#bkg_list+=( "DYJetsToLL_M1To10" )
#bkg_list+=( "DYJetsToLL_M50" )
#bkg_list+=( "ZZTo4L" )
#bkg_list+=( "DYJetsToLL_M1To10" )
bkg_list+=( "ZZTo4L_M1Toinf" )

data_list+=( "DoubleMuon_B" )
data_list+=( "DoubleMuon_C" )
data_list+=( "DoubleMuon_D" )
data_list+=( "DoubleMuon_E" )
data_list+=( "DoubleMuon_F" )

sig_list+=( "Wto3l_M1" )
sig_list+=( "Wto3l_M4" )
sig_list+=( "Wto3l_M5" )
sig_list+=( "Wto3l_M10" )
sig_list+=( "Wto3l_M15" )
sig_list+=( "Wto3l_M30" )
sig_list+=( "Wto3l_M45" )
sig_list+=( "Wto3l_M60" )

echo -e "Sample,Sum Weight,Trigger,b Jets,3 Good Muons,Found Z'" > Tables/counts_list.txt
for i in ${!bkg_list[@]}; do
	python v2_skimmer.py ${bkg_list[i]}
done
python Tables/combine_samples.py bkg

#echo -e "Sample,Sum Weight,Trigger,b Jets,3 Good Muons,Found Z'" > Tables/counts_list.txt
#for i in ${!data_list[@]}; do
#    python v2_skimmer.py ${data_list[i]}
#done
#python Tables/combine_samples.py data
#
#echo -e "Sample,Sum Weight,Trigger,b Jets,3 Good Muons,Found Z'" > Tables/counts_list.txt
#for i in ${!sig_list[@]}; do
#    python v2_skimmer.py ${sig_list[i]}
#done
#python Tables/combine_samples.py sig
#
#python3 Tables/pretty_table.py > Tables/Efficiency_table.txt
#cat Tables/Efficiency_table.txt
#
#source removeDuplicates/removeDuplicates_UL.sh



