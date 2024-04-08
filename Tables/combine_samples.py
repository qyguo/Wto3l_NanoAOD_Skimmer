from __future__ import division
import sys
import numpy as np

if str(sys.argv[1]) == "bkg":
	comb_str = "Combined MC Background"
elif str(sys.argv[1]) == "data":
	comb_str = "Combined Data"
else:
	comb_str = "Combined Signal"

xs = {	"DYJetsToLL_M1To10":  2037.0,
		"DYJetsToLL_M10To50":18610.0,
		"DYJetsToLL_M50":    6077.22,
		"WJetsToLNu":        61526.7,
		"TTJets_DiLept":       54.23,
		"WZTo3LNu":            5.052,
		"ZZTo4L":              1.369,
		"WWTo2L2Nu":          12.178,
		"DoubleMuon_B":            1,
		"DoubleMuon_C":            1,
		"DoubleMuon_D":            1,
		"DoubleMuon_E":            1,
		"DoubleMuon_F":            1,
		"Wto3l_M1": 36.06,
		"Wto3l_M2": 23.33,
		"Wto3l_M3": 17.233,
		"Wto3l_M4":  10.078,
		"Wto3l_M5":  7.425,
		"Wto3l_M10": 3.108,
		"Wto3l_M15": 1.5523,
		"Wto3l_M20": 0.8346,
		"Wto3l_M25": 0.4537,
		"Wto3l_M30": 0.2484,
		"Wto3l_M35": 0.13339,
		"Wto3l_M40": 0.06842,
		"Wto3l_M45": 0.0338,
		"Wto3l_M50": 0.015906,
		"Wto3l_M55": 0.007053,
		"Wto3l_M60": 0.003014,
		"Wto3l_M65": 0.0013914,
		"Wto3l_M70": 0.0008662,
		"Wto3l_M75": 0.000615,
		"Wto3l_M80": 0.0004572,
		#"Wto3l_M1":			   27.40,
		#"Wto3l_M4":			   7.474,
		#"Wto3l_M5":            5.453,
		#"Wto3l_M10":          2.2391,
		#"Wto3l_M15":          1.0042,
		#"Wto3l_M30":         0.17985,
		#"Wto3l_M60":       0.0021799,
		}

sumW = {}
counts = {}
final_counts = np.array([0,0,0,0,0])
final_cause1 = np.array([0,0,0,0,0])
final_cause2 = np.array([0,0,0,0,0])
final_trig   = np.array([0,0,0])

with open("Tables/counts_list.txt","r") as f:
	for line in f:
		current = line.split(",")
		if str(current[1])=="Sum Weight": continue
		sumW[str(current[0])] = int(current[1])
		
		count_arr = np.array([int(current[2]),int(current[3]),int(current[4]),int(current[5]),int(current[6])])
		count_arr = count_arr*xs[str(current[0])]/sumW[str(current[0])]
		counts[str(current[0])] = count_arr
		final_counts = final_counts+count_arr

		cause1 = np.array([int(current[7]),int(current[8]),int(current[9]),int(current[10]),int(current[11])])
		cause1 = cause1*xs[str(current[0])]/sumW[str(current[0])]
		final_cause1 = final_cause1+cause1

		cause2 = np.array([int(current[12]),int(current[13]),int(current[14]),int(current[15]),int(current[16])])
		cause2 = cause2*xs[str(current[0])]/sumW[str(current[0])]
		final_cause2 = final_cause2+cause2

		trig = np.array([int(current[17]),int(current[18]),int(current[19])])
		trig = trig*xs[str(current[0])]/sumW[str(current[0])]
		final_trig = final_trig+trig

final_eff = np.array([0.,0.,0.,0.,0.])
final_causePer1 = np.array([0.,0.,0.,0.,0.])
final_causePer2 = np.array([0.,0.,0.,0.,0.])
final_trigPer   = np.array([0.,0.,0.])
for i in range(len(final_eff)-1):
	final_eff[i] = final_counts[i+1]/final_counts[i]*100
	#final_causePer1[i] = (final_cause1[i]/(final_counts[2]-final_counts[3]))*100
	#final_causePer2[i] = (final_cause2[i]/(final_counts[3]-final_counts[4]))*100
	final_causePer1[i] = (final_cause1[i]/np.sum(final_cause1))*100
	final_causePer2[i] = (final_cause2[i]/np.sum(final_cause2))*100
	if i < len(final_trigPer):
		final_trigPer[i] = final_trig[i]/final_counts[0]*100
final_eff[-1] = final_counts[-1]/final_counts[0]*100
#final_causePer1[-1] = (final_cause1[-1]/(final_counts[2]-final_counts[3]))*100
#final_causePer2[-1] = (final_cause2[-1]/(final_counts[3]-final_counts[4]))*100
final_causePer1[-1] = (final_cause1[-1]/np.sum(final_cause1))*100
final_causePer2[-1] = (final_cause2[-1]/np.sum(final_cause2))*100
final_trigPer[-1] = final_trig[-1]/final_counts[0]*100

f1 = open("Tables/cut_list.txt","a")
f1.write("%s,%.2f%%,%.2f%%,%.2f%%,%.2f%%,%.2f%%\n"%(comb_str,final_eff[0],final_eff[1],final_eff[2],final_eff[3],final_eff[4]))
f1.close()

f2 = open("Tables/GoodMu_list.txt","a")
f2.write("%s,%.2f%%,%.2f%%,%.2f%%,%.2f%%,%.2f%%,%.2f%%\n"%(comb_str,100-final_eff[2],final_causePer1[0],final_causePer1[1],final_causePer1[2],final_causePer1[3],final_causePer1[4]))
f2.close()

f3 = open("Tables/ZpCandidate_list.txt","a")
f3.write("%s,%.2f%%,%.2f%%,%.2f%%,%.2f%%,%.2f%%,%.2f%%\n"%(comb_str,100-final_eff[3],final_causePer2[0],final_causePer2[1],final_causePer2[2],final_causePer2[3],final_causePer2[4]))
f3.close()

f4 = open("Tables/Trigger_list.txt","a")
f4.write("%s,%.2f%%,%.2f%%,%.2f%%,%.2f%%\n"%(comb_str,final_eff[0],final_trigPer[0],final_trigPer[1],final_trigPer[2]))
f4.close()
