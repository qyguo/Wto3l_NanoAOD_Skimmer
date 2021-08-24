from __future__ import division
import numpy as np
import uproot
import sys
from ROOT import TLorentzVector
from tqdm import tqdm
from Utils.DeltaR import deltaR
from out_dict import *
import concurrent.futures

dataset = str(sys.argv[1])
isSignal = 0
isMC = 1
if "To3l_M" in sys.argv[1] or "to3l_M" in sys.argv[1]:
	isSignal = 1
if "Muon" in sys.argv[1]:
	isMC = 0
in_file = ""
out_file = ""
if isSignal==1:
	in_file = "/cmsuf/data/store/user/t2/users/nikmenendez/signal/NanoAOD/"+dataset+".root"
	out_file = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/signal/signal_sel/Eff/"+dataset+".root"
	sumW_file = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/signal/signal_sel/Eff/"+dataset+".txt"
elif isMC==1:
	in_file = "/cmsuf/data/store/user/t2/users/nikmenendez/2017_MC_bkg/NanoAOD/"+dataset+".root"
	out_file = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/background/signal_sel/Eff/"+dataset+".root"
	sumW_file = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/background/signal_sel/Eff/"+dataset+".txt"
else:
	in_file = "/cmsuf/data/store/user/t2/users/nikmenendez/data_wto3l/2017/"+dataset+".root"
	out_file = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/data/signal_sel/Eff/"+dataset+".root"

print("Skimming file %s"%(in_file))

file = uproot.open(in_file)
executor = concurrent.futures.ThreadPoolExecutor()

events = file["Events"]
runs = file["Runs"]

if isMC==1:
	#Get SumWeight
	sumW = 0
	SumWeights = runs["genEventSumw"].array()
	sumW = np.sum(SumWeights)
else:
	sumW = 1

#Define cuts
cut0, cut1, cut2, cut3, cut4 = 0, 0, 0, 0, 0
leadingPtCut, subleadingPtCut, trailingPtCut = 10.0, 5.0, 5.0
iso_cut = 0.1
sip_cut = 4
dxy_cut = 0.05
dz_cut = 0.1
Wmass = 83.0

#Import tree from ROOT
vars_in = ["run","event","luminosityBlock","nMuon","Muon_pt","Muon_pdgId","Muon_eta","Muon_phi","Muon_mass","Muon_pfRelIso03_all","Muon_tightId","Muon_mediumId","Muon_ip3d","Muon_sip3d","Muon_dxy","Muon_dz","nJet","Jet_pt","Jet_btagCSVV2","MET_pt","MET_phi","HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8","HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ","HLT_TripleMu_10_5_5_DZ","HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL","HLT_TripleMu_12_10_5"]
if isMC:
	vars_in.extend(["genWeight","Pileup_nPU"])
if isSignal:
	vars_in.extend(["GenPart_pdgId","GenPart_eta","GenPart_pt"])

data = events.arrays(vars_in,executor=executor)

nEntries = len(data["nMuon"])

if isMC==1:
    print("Skimming %i events. SumWeight = %i"%(nEntries,sumW))
else:
	print("Skimming %i events."%(nEntries))

#Find acceptance of signal
left0 = nEntries
eff0 = left0/nEntries*100
selection = data["nMuon"] >= 0
if isSignal==1:
	for ev in tqdm(range(len(data["GenPart_pdgId"]))):
		m_found = 0
		gen = np.unique(np.array([data["GenPart_pdgId"][ev],data["GenPart_eta"][ev],data["GenPart_pt"][ev]]), axis=1)
		for i in range(len(gen[0])):
			if abs(gen[0][i])==13 and abs(gen[1][i])<=2.4 and gen[2][i]>=5: m_found+=1
		if m_found<3: selection[ev] = False
	left0 = np.count_nonzero(selection)
	eff0 = left0/nEntries*100
#
#Begin selection
selection *= data["nMuon"] >= 3
left1 = np.count_nonzero(selection)
eff1 = left1/left0*100
passedDiMu1 = (data["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8"]==1)
passedDiMu2 = (data["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ"]==1) | (data["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL"]==1)
passedTriMu = (data["HLT_TripleMu_10_5_5_DZ"]==1) | (data["HLT_TripleMu_12_10_5"]==1)
selection *= passedDiMu1 | passedDiMu2 | passedTriMu
left2 = np.count_nonzero(selection)
eff2 = left2/left1*100

num3 = 0
num4 = 0
cause = np.array([0,0,0,0,0])
cause2= np.array([0,0,0,0,0])

for ev in tqdm(range(len(data["nMuon"]))):
	if not selection[ev]: continue

	nbjets = 0
	for i in range(data["nJet"][ev]):
		if data["Jet_pt"][ev][i] > 25 and data["Jet_btagCSVV2"][ev][i] > .46:
			nbjets+=1
	if nbjets > 0:
		selection[ev] = False
		num3+=1
	if not selection[ev]: continue


	nGood = 0
	GoodMu = []
	cutBy = []
	for i in range(data["nMuon"][ev]):
		passes=True
		if data["Muon_mediumId"][ev][i] != 1: 
			cutBy.append(0)
			passes=False
		if data["Muon_sip3d"][ev][i] > sip_cut: 
			cutBy.append(1)
			passes=False
		if data["Muon_dxy"][ev][i] > dxy_cut: 
			cutBy.append(2)
			passes=False
		if data["Muon_dz"][ev][i] > dz_cut: 
			cutBy.append(3)
			passes=False
		if data["Muon_pfRelIso03_all"][ev][i] > iso_cut: 
			cutBy.append(4)
			passes=False
		if not passes: continue

		GoodMu.append(i)

	if len(GoodMu) < 3: 
		selection[ev] = False
		#cause[max(set(cutBy), key = cutBy.count)]+=1
		for i in cutBy:
			cause[i]+=1
		num4+=1
	if not selection[ev]: continue

	foundZp = False
	cutBy2 = []
	for m1 in range(len(GoodMu)-2):
		for m2 in range(m1+1,len(GoodMu)-1):
			for m3 in range(m2+1,len(GoodMu)):
				passes=True
				if abs(data["Muon_pdgId"][ev][GoodMu[m1]] + data["Muon_pdgId"][ev][GoodMu[m2]] + data["Muon_pdgId"][ev][GoodMu[m3]])!=13:
					cutBy2.append(0)
					passes=False

				if data["Muon_pt"][ev][GoodMu[m1]] < leadingPtCut:
					cutBy2.append(1)
					passes=False
				if data["Muon_pt"][ev][GoodMu[m2]] < subleadingPtCut:
					cutBy2.append(2)
					passes=False
				if data["Muon_pt"][ev][GoodMu[m3]] < trailingPtCut:
					cutBy2.append(3)
					passes=False

				mu1 = TLorentzVector()
				mu2 = TLorentzVector()
				mu3 = TLorentzVector()
				mu1.SetPtEtaPhiM(data["Muon_pt"][ev][GoodMu[m1]],data["Muon_eta"][ev][GoodMu[m1]],data["Muon_phi"][ev][GoodMu[m1]],data["Muon_mass"][ev][GoodMu[m1]])
				mu2.SetPtEtaPhiM(data["Muon_pt"][ev][GoodMu[m2]],data["Muon_eta"][ev][GoodMu[m2]],data["Muon_phi"][ev][GoodMu[m2]],data["Muon_mass"][ev][GoodMu[m2]])
				mu3.SetPtEtaPhiM(data["Muon_pt"][ev][GoodMu[m3]],data["Muon_eta"][ev][GoodMu[m3]],data["Muon_phi"][ev][GoodMu[m3]],data["Muon_mass"][ev][GoodMu[m3]])

				m3l = (mu1+mu2+mu3).M()
				if m3l > Wmass:
					cutBy2.append(4)
					passes=False
				if not passes: continue

				i1 = GoodMu[m1]
				i2 = GoodMu[m2]
				i3 = GoodMu[m3]

				foundZp = True

	if not foundZp:
		selection[ev] = False
		#cause2[max(set(cutBy2), key = cutBy2.count)]+=1
		for i in cutBy2:
			cause2[i]+=1
	if not selection[ev]: continue

	lep1 = TLorentzVector()
	lep2 = TLorentzVector()
	lep3 = TLorentzVector()
	lep1.SetPtEtaPhiM(data["Muon_pt"][ev][i1],data["Muon_eta"][ev][i1],data["Muon_phi"][ev][i1],data["Muon_mass"][ev][i1])
	lep2.SetPtEtaPhiM(data["Muon_pt"][ev][i2],data["Muon_eta"][ev][i2],data["Muon_phi"][ev][i2],data["Muon_mass"][ev][i2])
	lep3.SetPtEtaPhiM(data["Muon_pt"][ev][i3],data["Muon_eta"][ev][i3],data["Muon_phi"][ev][i3],data["Muon_mass"][ev][i3])

	threeleps = lep1+lep2+lep3
	Met = TLorentzVector()
	Met.SetPtEtaPhiM(data["MET_pt"][ev],0,data["MET_phi"][ev],0)

	output["idL1"], output["idL2"], output["idL3"] = np.append(output["idL1"],data["Muon_pdgId"][ev][i1]), np.append(output["idL2"],data["Muon_pdgId"][ev][i2]), np.append(output["idL3"],data["Muon_pdgId"][ev][i3])
	output["pTL1"], output["pTL2"], output["pTL3"] = np.append(output["pTL1"],data["Muon_pt"][ev][i1]), np.append(output["pTL2"],data["Muon_pt"][ev][i2]), np.append(output["pTL3"],data["Muon_pt"][ev][i3])
	output["etaL1"], output["etaL2"], output["etaL3"] = np.append(output["etaL1"],data["Muon_eta"][ev][i1]), np.append(output["etaL2"],data["Muon_eta"][ev][i2]), np.append(output["etaL3"],data["Muon_eta"][ev][i3])
	output["phiL1"], output["phiL2"], output["phiL3"] = np.append(output["phiL1"],data["Muon_phi"][ev][i1]), np.append(output["phiL2"],data["Muon_phi"][ev][i2]), np.append(output["phiL3"],data["Muon_phi"][ev][i3])
	output["IsoL1"], output["IsoL2"], output["IsoL3"] = np.append(output["IsoL1"],data["Muon_pfRelIso03_all"][ev][i1]), np.append(output["IsoL2"],data["Muon_pfRelIso03_all"][ev][i2]), np.append(output["IsoL3"],data["Muon_pfRelIso03_all"][ev][i3])
	output["ip3dL1"], output["ip3dL2"], output["ip3dL3"] = np.append(output["ip3dL1"],data["Muon_ip3d"][ev][i1]), np.append(output["ip3dL2"],data["Muon_ip3d"][ev][i2]), np.append(output["ip3dL3"],data["Muon_ip3d"][ev][i3])
	output["sip3dL1"], output["sip3dL2"], output["sip3dL3"] = np.append(output["sip3dL1"],data["Muon_sip3d"][ev][i1]), np.append(output["sip3dL2"],data["Muon_sip3d"][ev][i2]), np.append(output["sip3dL3"],data["Muon_sip3d"][ev][i3])
	output["massL1"], output["massL2"], output["massL3"] = np.append(output["massL1"],data["Muon_mass"][ev][i1]), np.append(output["massL2"],data["Muon_mass"][ev][i2]), np.append(output["massL3"],data["Muon_mass"][ev][i3])
	output["tightIdL1"], output["tightIdL2"], output["tightIdL3"] = np.append(output["tightIdL1"],data["Muon_tightId"][ev][i1]), np.append(output["tightIdL2"],data["Muon_tightId"][ev][i2]), np.append(output["tightIdL3"],data["Muon_tightId"][ev][i3])
	output["medIdL1"], output["medIdL2"], output["medIdL3"] = np.append(output["medIdL1"],data["Muon_mediumId"][ev][i1]), np.append(output["medIdL2"],data["Muon_mediumId"][ev][i2]), np.append(output["medIdL3"],data["Muon_mediumId"][ev][i3])

	output["maxdxy"] = np.append(output["maxdxy"], np.amax(np.absolute([data["Muon_dxy"][ev][i1],data["Muon_dxy"][ev][i2],data["Muon_dxy"][ev][i3]])))
	output["maxdz"] =  np.append(output["maxdz"], np.amax(np.absolute([data["Muon_dz"][ev][i1],data["Muon_dz"][ev][i2],data["Muon_dz"][ev][i3]])))

	output["dR12"] = np.append(output["dR12"], deltaR(lep1.Eta(),lep1.Phi(),lep2.Eta(),lep2.Phi()))
	output["dR13"] = np.append(output["dR13"], deltaR(lep1.Eta(),lep1.Phi(),lep3.Eta(),lep3.Phi()))
	output["dR23"] = np.append(output["dR23"], deltaR(lep2.Eta(),lep2.Phi(),lep3.Eta(),lep3.Phi()))
	output["met"], output["met_phi"] = np.append(output["met"],data["MET_pt"][ev]), np.append(output["met_phi"],data["MET_phi"][ev])

	output["nMuons"], output["nGoodMuons"] = np.append(output["nMuons"],data["nMuon"][ev]), np.append(output["nGoodMuons"],len(GoodMu))
	output["nbJets"] = np.append(output["nbJets"],nbjets)
	output["m3l"], output["mt"] = np.append(output["m3l"],threeleps.M()), np.append(output["mt"],(threeleps+Met).M())

	output["Run"] = np.append(output["Run"],data["run"][ev])
	output["Event"] = np.append(output["Event"],data["event"][ev])
	output["LumiSect"] = np.append(output["LumiSect"],data["luminosityBlock"][ev])

	if isMC==1: output["genWeight"] = np.append(output["genWeight"],data["genWeight"][ev])
	else: output["genWeight"] = np.append(output["genWeight"],1)

	output["passedDiMu1"] = np.append(output["passedDiMu1"],passedDiMu1[ev])
	output["passedDiMu2"] = np.append(output["passedDiMu2"],passedDiMu2[ev])
	output["passedTriMu"] = np.append(output["passedTriMu"],passedTriMu[ev])


with uproot.recreate(out_file) as f:
	f["passedEvents"] = uproot.newtree(branches)
	f["passedEvents"].extend(output)

left5 = np.count_nonzero(selection)

left3 = left2-num3
eff3 = left3/left2*100
left4 = left3-num4
eff4 = left4/left3*100
causePer = ((cause/np.sum(cause)))*100
num5 = left4-left5
eff5 = left5/left4*100
causePer2 = ((cause2/np.sum(cause2)))*100

print("Efficiencies for each cut")
print("=====================================================")
print("Total events before cuts: %i"%(nEntries))
if isSignal==1: print("In acceptance: %i. Efficiency = %.2f%%"%(left0,eff0))
print("Pass 3 muon cut: %i. Efficiency = %.2f%%"%(left1,eff1))
print("Pass Trigger: %i. Efficiency = %.2f%%"%(left2,eff2))
print("Event has no b jets: %i. Efficiency = %.2f%%"%(left3,eff3))
print("Found 3 good muons: %i. Efficiency = %.2f%%"%(left4,eff4))
print("Found Z' candidate: %i. Efficiency = %.2f%%"%(left5,eff5))
print("=====================================================")
print("Total Efficiency = %.2f%%"%(left5/left1*100))
print("Wrote to file %s"%(out_file))
print("")

print("Percent that fail good muon cuts: medId %.2f%%, sip %.2f%%, dxy %.2f%%, dz %.2f%%, iso %.2f%%"%(causePer[0],causePer[1],causePer[2],causePer[3],causePer[4]))
print("Didn't find Z' because of: mu signs %.2f%%, leading pT %.2f%%, subleading pT %.2f%%, trailing pT %.2f%%, m3l %.2f%%"%(causePer2[0],causePer2[1],causePer2[2],causePer2[3],causePer2[4]))
print("")

f1 = open("Tables/cut_list.txt","a")
f2 = open("Tables/GoodMu_list.txt","a")
f3 = open("Tables/ZpCandidate_list.txt","a")
f4 = open("Tables/counts_list.txt","a")

f1.write("%s,%.2f%%,%.2f%%,%.2f%%,%.2f%%,%.2f%%\n"%(dataset,eff2,eff3,eff4,eff5,left5/left1*100))
f2.write("%s,%.2f%%,%.2f%%,%.2f%%,%.2f%%,%.2f%%,%.2f%%\n"%(dataset,100-eff4,causePer[0],causePer[1],causePer[2],causePer[3],causePer[4]))
f3.write("%s,%.2f%%,%.2f%%,%.2f%%,%.2f%%,%.2f%%,%.2f%%\n"%(dataset,100-eff5,causePer2[0],causePer2[1],causePer2[2],causePer2[3],causePer2[4]))
f4.write("%s,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i\n"%(dataset,sumW,left1,left2,left3,left4,left5,cause[0],cause[1],cause[2],cause[3],cause[4],cause2[0],cause2[1],cause2[2],cause2[3],cause2[4]))

f1.close()
f2.close()
f3.close()
f4.close()
