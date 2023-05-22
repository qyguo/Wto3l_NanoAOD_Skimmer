#echo -e "Sample,Had 2e,Found Good 2e+1mu,Found Z Candidate,Overall Efficiency" > Tables/cut_list.txt
#echo -e "Sample,Failed Good 2e,Tight Id,e pT,e Iso,e SIP,e dxyz" > Tables/GoodMu_list.txt
#echo -e "Sample,Failed Z Candidate,Electron Signs" > Tables/ZpCandidate_list.txt
#echo -e "Sample,Passed Trigger,Passed 2e+1mu,Passed 2e,Passed 1e+1mu" > Tables/Trigger_list.txt

bkg_list=()
data_list=()

#bkg_list+=( "DYJetsToLL_M1To10" )
#bkg_list+=( "DYJetsToLL_M10To50" )
##bkg_list+=( "DYJetsToLL_M50" )
#bkg_list+=( "TTJets_DiLept" )
#bkg_list+=( "WZTo3LNu" )
#bkg_list+=( "ZZTo4L" )
#bkg_list+=( "ZZTo4L_M1Toinf" )
#bkg_list+=( "WJetsToLNu" )
#bkg_list+=( "WWTo2L2Nu" )

#data_list+=( "DoubleEG_B" )
#data_list+=( "DoubleEG_C" )
#data_list+=( "DoubleEG_D" )
#data_list+=( "DoubleEG_E" )
#data_list+=( "DoubleEG_F" )
##data_list+=( "MuonEG_B" )
##data_list+=( "MuonEG_C" )
##data_list+=( "MuonEG_D" )
##data_list+=( "MuonEG_E" )
##data_list+=( "MuonEG_F" )
#data_list+=( "SingleElectron_B" )
#data_list+=( "SingleElectron_C" )
#data_list+=( "SingleElectron_D" )
#data_list+=( "SingleElectron_E" )
#data_list+=( "SingleElectron_F" )

for i in ${!data_list[@]}; do
    python /orange/avery/nikmenendez/Wto3l/Skimmer/PyNanoSkimmer/skimmer_Zpeak.py ${data_list[i]}
done

for i in ${!bkg_list[@]}; do
	python /orange/avery/nikmenendez/Wto3l/Skimmer/PyNanoSkimmer/skimmer_Zpeak.py ${bkg_list[i]}
done

#python3 Tables/pretty_table.py > Tables/Efficiency_table.txt
#cat Tables/Efficiency_table.txt

#source removeDuplicates/removeDuplicates_Zpeak.sh



