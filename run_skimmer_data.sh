#srun --ntasks=1 --cpus-per-task=8 --mem=16gb -t 600 --pty bash -i

while getopts s: flag
do
	case "${flag}" in
		s) sort=${OPTARG};;
	esac
done

sort="pt"

echo "Running with ${sort} sorting"

dataset_list=()
isMC=()


dataset_list+=( "DoubleMuon_B" )
dataset_list+=( "DoubleMuon_C" )
dataset_list+=( "DoubleMuon_D" )
dataset_list+=( "DoubleMuon_E" )
dataset_list+=( "DoubleMuon_F" )

#hadd -fk /cmsuf/data/store/user/t2/users/nikmenendez/data_wto3l/2017/DoubleMuon.root /cmsuf/data/store/user/nimenend/NanoAOD/Data/DoubleMuon/*/210529*/*/*.root

for i in ${!dataset_list[@]}; do
	python skimmer.py ${dataset_list[i]}
done

if [ "${sort}" = "pt" ]; then
	#source signal_hadd/hadd_pt.sh
	source removeDuplicates/removeDuplicates_new.sh
elif [ "${sort}" = "iso" ]; then
	#source signal_hadd/hadd_iso.sh
	source removeDuplicates/removeDuplicates_iso.sh
elif [ "${sort}" = "ip" ]; then
	#source signal_hadd/hadd_ip.sh
	source removeDuplicates/removeDuplicates_ip.sh
elif [ "${sort}" = "sip" ]; then
	#source signal_hadd/hadd_sip.sh
	source removeDuplicates/removeDuplicates_sip.sh
fi

#source hadd_all.sh
#source removeDuplicates.sh
