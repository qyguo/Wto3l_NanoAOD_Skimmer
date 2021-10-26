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
if "Double" in sys.argv[1] or "Muon" in sys.argv[1] or "Electron" in sys.argv[1]:
	isMC = 0
in_file = ""
out_file = ""
if isSignal==1:
	in_file = "/cmsuf/data/store/user/t2/users/nikmenendez/signal/NanoAOD/"+dataset+".root"
	out_file = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/signal/Zpeak/Eff/"+dataset+".root"
	sumW_file = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/signal/Zpeak/Eff/"+dataset+".txt"
elif isMC==1:
	in_file = "/cmsuf/data/store/user/t2/users/nikmenendez/2017_MC_bkg/ZpX/"+dataset+".root"
	out_file = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/background/Zpeak/Eff/"+dataset+".root"
	sumW_file = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/background/Zpeak/Eff/"+dataset+".txt"
else:
	in_file = "/cmsuf/data/store/user/t2/users/nikmenendez/data_wto3l/2017/ZpX/"+dataset+".root"
	out_file = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/data/Zpeak/Eff/"+dataset+".root"

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
iso_cut = 999.0
sip_cut = 4
dxy_cut = 0.05
dz_cut = 0.1
Wmass = 83.0

#Import tree from ROOT
vars_in = ["run","event","luminosityBlock","nMuon","Muon_pt","Muon_pdgId","Muon_eta","Muon_phi","Muon_mass","Muon_pfRelIso03_all","Muon_tightId","Muon_mediumId","Muon_ip3d","Muon_sip3d","Muon_dxy","Muon_dz","nJet","Jet_pt","Jet_btagCSVV2","MET_pt","MET_phi","nElectron","Electron_pdgId","Electron_phi","Electron_eta","Electron_mass","Electron_pt","Electron_cutBased","Electron_pfRelIso03_all","Electron_ip3d","Electron_sip3d","Electron_dxy","Electron_dz"]
triggers = ["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"]
vars_in.extend(triggers)
if isMC:
	vars_in.extend(["genWeight","Pileup_nTrueInt","Muon_genPartFlav","Electron_genPartFlav"])
if isSignal:
	vars_in.extend(["GenPart_pdgId","GenPart_eta","GenPart_pt"])

#data = events.arrays(vars_in,executor=executor)

nEntries = events.numentries

if isMC==1:
	print("Skimming %i events. SumWeight = %i"%(nEntries,sumW))
else:
	print("Skimming %i events."%(nEntries))

left0 = 0
left1, left2, left3, left4, left5, left6 = 0,0,0,0,0,0
num3 = 0
num4 = 0
cause = np.array([0,0,0,0,0,0])
cause2= np.array([0,0,0,0,0,0])

for data in tqdm(events.iterate(vars_in)):
	nEntries = len(data["nElectron"])
	
	#Find acceptance of signal
	left0 += nEntries
	selection = data["nElectron"] >= 0
	selection *= data["nElectron"] >= 2
	left1 += np.count_nonzero(selection)
	#selection *= data["nMuon"] >= 1
	left2 += np.count_nonzero(selection)
	
	# Calculate trigger efficiencies
	passedTrigger = data[triggers[0]]==1
	for i in range(1,len(triggers)):
		passedTrigger = passedTrigger | data[triggers[i]]==1
	selection *= passedTrigger
	left3 += np.count_nonzero(selection)
	
	for ev in tqdm(range(nEntries),leave=False):
		if not selection[ev]: continue
	
		nbjets = 0
		for i in range(data["nJet"][ev]):
			if data["Jet_pt"][ev][i] > 25 and data["Jet_btagCSVV2"][ev][i] > .46:
				nbjets+=1
		#if nbjets > 0:
		#	selection[ev] = False
		#num3+=1
		#if not selection[ev]: continue
	
	
		nGood = 0
		GoodE = []
		GoodM = []
		cutBy = []
		for i in range(data["nElectron"][ev]):
			passes=True
			if data["Electron_cutBased"][ev][i]<4:
				cutBy.append(0)
				passes=False
			if data["Electron_pt"][ev][i]<10:
				cutBy.append(1)
				passes=False
			if data["Electron_pfRelIso03_all"][ev][i]>0.1:
				cutBy.append(2)
				passes=False
			if data["Electron_sip3d"][ev][i]>4:
				cutBy.append(3)
				passes=False
			if (data["Electron_dxy"][ev][i]>0.05) | (data["Electron_dz"][ev][i]>0.1):
				cutBy.append(4)
				passes=False
			if not passes: continue
	
			GoodE.append(i)
	
		for i in range(data["nMuon"][ev]):
			passes=True
			if data["Muon_pt"][ev][i]<5:
				passes=False
			if not passes: continue
	
			GoodM.append(i)
		nGoodM = len(GoodM)
	
		if len(GoodE) < 2: 
			selection[ev] = False
			for i in cutBy:
				cause[i]+=1
			num4+=1
		if not selection[ev]: continue
	
		foundZp = False
		cutBy2 = []
		for m1 in range(len(GoodE)-1):
			for m2 in range(m1+1,len(GoodE)):
				passes=True
				if abs(data["Electron_pdgId"][ev][GoodE[m1]] + data["Electron_pdgId"][ev][GoodE[m2]])!=0:
					cutBy2.append(0)
					passes=False
	
				if not passes: continue
	
				i1 = GoodE[m1]
				i2 = GoodE[m2]
				if nGoodM>0:
					i3 = GoodM[0]
	
				foundZp = True
	
		if not foundZp:
			selection[ev] = False
			for i in cutBy2:
				cause2[i]+=1
		if not selection[ev]: continue
	
		lep1 = TLorentzVector()
		lep2 = TLorentzVector()
		lep1.SetPtEtaPhiM(data["Electron_pt"][ev][i1],data["Electron_eta"][ev][i1],data["Electron_phi"][ev][i1],data["Electron_mass"][ev][i1])
		lep2.SetPtEtaPhiM(data["Electron_pt"][ev][i2],data["Electron_eta"][ev][i2],data["Electron_phi"][ev][i2],data["Electron_mass"][ev][i2])
	
		twoleps = lep1+lep2
		Met = TLorentzVector()
		Met.SetPtEtaPhiM(data["MET_pt"][ev],0,data["MET_phi"][ev],0)
	
		output["idL1"], output["idL2"] = np.append(output["idL1"],data["Electron_pdgId"][ev][i1]), np.append(output["idL2"],data["Electron_pdgId"][ev][i2])
		output["pTL1"], output["pTL2"] = np.append(output["pTL1"],data["Electron_pt"][ev][i1]), np.append(output["pTL2"],data["Electron_pt"][ev][i2])
		output["etaL1"], output["etaL2"] = np.append(output["etaL1"],data["Electron_eta"][ev][i1]), np.append(output["etaL2"],data["Electron_eta"][ev][i2])
		output["phiL1"], output["phiL2"] = np.append(output["phiL1"],data["Electron_phi"][ev][i1]), np.append(output["phiL2"],data["Electron_phi"][ev][i2])
		output["IsoL1"], output["IsoL2"] = np.append(output["IsoL1"],data["Electron_pfRelIso03_all"][ev][i1]), np.append(output["IsoL2"],data["Electron_pfRelIso03_all"][ev][i2])
		output["ip3dL1"], output["ip3dL2"] = np.append(output["ip3dL1"],data["Electron_ip3d"][ev][i1]), np.append(output["ip3dL2"],data["Electron_ip3d"][ev][i2])
		output["sip3dL1"], output["sip3dL2"] = np.append(output["sip3dL1"],data["Electron_sip3d"][ev][i1]), np.append(output["sip3dL2"],data["Electron_sip3d"][ev][i2])
		output["massL1"], output["massL2"] = np.append(output["massL1"],data["Electron_mass"][ev][i1]), np.append(output["massL2"],data["Electron_mass"][ev][i2])
		output["tightIdL1"], output["tightIdL2"] = np.append(output["tightIdL1"],True), np.append(output["tightIdL2"],True)
		output["medIdL1"], output["medIdL2"] = np.append(output["medIdL1"],True), np.append(output["medIdL2"],True)
	
		output["maxdxy"] = np.append(output["maxdxy"], np.amax(np.absolute([data["Electron_dxy"][ev][i1],data["Electron_dxy"][ev][i2]])))
		output["maxdz"] =  np.append(output["maxdz"], np.amax(np.absolute([data["Electron_dz"][ev][i1],data["Electron_dz"][ev][i2]])))
	
		output["dR12"] = np.append(output["dR12"], deltaR(lep1.Eta(),lep1.Phi(),lep2.Eta(),lep2.Phi()))
		output["met"], output["met_phi"] = np.append(output["met"],data["MET_pt"][ev]), np.append(output["met_phi"],data["MET_phi"][ev])
	
		output["nMuons"], output["nGoodMuons"] = np.append(output["nMuons"],data["nMuon"][ev]), np.append(output["nGoodMuons"],len(GoodM))
		output["nbJets"] = np.append(output["nbJets"],nbjets)
		output["mt"] = np.append(output["mt"],(twoleps+Met).Mt())
	
		output["Run"] = np.append(output["Run"],data["run"][ev])
		output["Event"] = np.append(output["Event"],data["event"][ev])
		output["LumiSect"] = np.append(output["LumiSect"],data["luminosityBlock"][ev])
	
		if isMC==1: 
			output["genWeight"] = np.append(output["genWeight"],data["genWeight"][ev])
			output["pileupWeight"] = np.append(output["pileupWeight"],data["Pileup_nTrueInt"][ev])
			output["sourceL1"], output["sourceL2"] = np.append(output["sourceL1"],data["Electron_genPartFlav"][ev][i1]), np.append(output["sourceL2"],data["Electron_genPartFlav"][ev][i2])
		else: 
			output["genWeight"] = np.append(output["genWeight"],1)
			output["pileupWeight"] = np.append(output["pileupWeight"],1)
			output["sourceL1"], output["sourceL2"] = np.append(output["sourceL1"],0), np.append(output["sourceL2"],0)

		if nGoodM>0:
			lep3 = TLorentzVector()
			lep3.SetPtEtaPhiM(data["Muon_pt"][ev][i3],data["Muon_eta"][ev][i3],data["Muon_phi"][ev][i3],data["Muon_mass"][ev][i3])
			threeleps = lep1+lep2+lep3
			output["m3l"] = np.append(output["m3l"],threeleps.M())
			output["idL3"] = np.append(output["idL3"],data["Muon_pdgId"][ev][i3])
			output["pTL3"] = np.append(output["pTL3"],data["Muon_pt"][ev][i3])
			output["etaL3"] = np.append(output["etaL3"],data["Muon_eta"][ev][i3])
			output["phiL3"] = np.append(output["phiL3"],data["Muon_phi"][ev][i3])
			output["IsoL3"] = np.append(output["IsoL3"],data["Muon_pfRelIso03_all"][ev][i3])
			output["ip3dL3"] = np.append(output["ip3dL3"],data["Muon_ip3d"][ev][i3])
			output["sip3dL3"] = np.append(output["sip3dL3"],data["Muon_sip3d"][ev][i3])
			output["massL3"] = np.append(output["massL3"],data["Muon_mass"][ev][i3])
			output["tightIdL3"] = np.append(output["tightIdL3"],data["Muon_tightId"][ev][i3])
			output["medIdL3"] = np.append(output["medIdL3"],data["Muon_mediumId"][ev][i3])
			output["dR13"] = np.append(output["dR13"], deltaR(lep1.Eta(),lep1.Phi(),lep3.Eta(),lep3.Phi()))
			output["dR23"] = np.append(output["dR23"], deltaR(lep2.Eta(),lep2.Phi(),lep3.Eta(),lep3.Phi()))
			if isMC==1:
				output["sourceL3"] = np.append(output["sourceL3"],data["Muon_genPartFlav"][ev][i3])
			else:
				output["sourceL3"] = np.append(output["sourceL3"],0)
		else:
			output["m3l"] = np.append(output["m3l"],-99)
			output["idL3"] = np.append(output["idL3"],-99)
			output["pTL3"] = np.append(output["pTL3"],-99)
			output["etaL3"] = np.append(output["etaL3"],-99)
			output["phiL3"] = np.append(output["phiL3"],-99)
			output["IsoL3"] = np.append(output["IsoL3"],-99)
			output["ip3dL3"] = np.append(output["ip3dL3"],-99)
			output["sip3dL3"] = np.append(output["sip3dL3"],-99)
			output["massL3"] = np.append(output["massL3"],-99)
			output["tightIdL3"] = np.append(output["tightIdL3"],-99)
			output["medIdL3"] = np.append(output["medIdL3"],-99)
			output["dR13"] = np.append(output["dR13"],-99)
			output["dR23"] = np.append(output["dR23"],-99)
			if isMC==1:
				output["sourceL3"] = np.append(output["sourceL3"],-99)
			else:
				output["sourceL3"] = np.append(output["sourceL3"],-99)
			
		output["passedDiMu1"] = np.append(output["passedDiMu1"],1)
		output["passedDiMu2"] = np.append(output["passedDiMu2"],1)
		output["passedTriMu"] = np.append(output["passedTriMu"],1)
	
		output["m4l"] = np.append(output["m4l"],-1)
	
	left6 += np.count_nonzero(selection)


with uproot.recreate(out_file) as f:
	f["passedEvents"] = uproot.newtree(branches)
	f["passedEvents"].extend(output)

eff1 = left1/left0*100
eff2 = left2/left1*100
eff3 = left3/left2*100
left4 = left3-num3
eff4 = left4/left3*100
causePer = ((cause/np.sum(cause)))*100
left5 = left4-num4
eff5 = left5/left4*100
causePer2 = ((cause2/np.sum(cause2)))*100
eff6 = left6/left5*100

print("Efficiencies for each cut")
print("=====================================================")
print("Total events before cuts: %i"%(left0))
print("Pass 2e cut: %i. Efficiency = %.2f%%"%(left1,eff1))
#print("Pass 1mu cut: %i. Efficiency = %.2f%%"%(left2,eff2))
print("Pass Trigger: %i. Efficiency = %.2f%%"%(left3,eff3))
#print("Event has no b jets: %i. Efficiency = %.2f%%"%(left4,eff4))
print("Found good 2e: %i. Efficiency = %.2f%%"%(left5,eff5))
print("Found Z' candidate: %i. Efficiency = %.2f%%"%(left6,eff6))
print("=====================================================")
print("Total Efficiency = %.2f%%"%(left6/left0*100))
print("Wrote to file %s"%(out_file))

print("Percent that fail good 2e cut: tightId %.2f%%, e pt %.2f%%, e Iso %.2f%%, e SIP %.2f%%, e dxyz %.2f%%"%(causePer[0],causePer[1],causePer[2],causePer[3],causePer[4]))
print("Didn't find Z' because of: e signs %.2f%%"%(causePer2[0]))
print("")

f1 = open("Tables/cut_list.txt","a")
f2 = open("Tables/GoodMu_list.txt","a")

f1.write("%s,%.2f%%,%.2f%%,%.2f%%,%.2f%%\n"%(dataset,eff1,eff5,eff6,left6/left0*100))
f2.write("%s,%.2f%%,%.2f%%,%.2f%%,%.2f%%,%.2f%%,%.2f%%\n"%(dataset,100-eff5,causePer[0],causePer[1],causePer[2],causePer[3],causePer[4]))

f1.close()
f2.close()
