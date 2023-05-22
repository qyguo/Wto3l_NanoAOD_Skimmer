from __future__ import division
import numpy as np
import uproot
import sys
from ROOT import TLorentzVector
from tqdm import tqdm
from Utils.DeltaR import deltaR
from Utils.PartOrigin import PartOrigin
from out_dict import *
import concurrent.futures

oto1 = True

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
	out_file = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/signal/Zpeak/UL/"+dataset+".root"
	sumW_file = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/signal/Zpeak/UL/sumW/"+dataset+".txt"
elif isMC==1:
	in_file = "/cmsuf/data/store/user/t2/users/nikmenendez/2017_MC_bkg/ZpX_UL/"+dataset+".root"
	if "DY" in sys.argv[1] and oto1:
		out_file = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/background/Zpeak/UL/"+dataset+"_M0To1.root"
		sumW_file = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/background/Zpeak/UL/sumW/"+dataset+"_M0To1.txt"
	else:
		out_file = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/background/Zpeak/UL/"+dataset+".root"
		sumW_file = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/background/Zpeak/UL/sumW/"+dataset+".txt"
else:
	in_file = "/cmsuf/data/store/user/t2/users/nikmenendez/data_wto3l/2017/ZpX_UL/"+dataset+".root"
	out_file = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/data/Zpeak/UL/"+dataset+".root"

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
	file_sumW = open(sumW_file,"w")
	file_sumW.write(str(sumW))
	file_sumW.close()
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
Zmass = 91.1876

#Import tree from ROOT
vars_in = ["run","event","luminosityBlock","nMuon","Muon_pt","Muon_pdgId","Muon_eta","Muon_phi","Muon_mass","Muon_pfRelIso03_all","Muon_tightId","Muon_mediumId","Muon_softId","Muon_mvaId","Muon_ip3d","Muon_sip3d","Muon_dxy","Muon_dz","nJet","Jet_pt","Jet_btagCSVV2","MET_pt","MET_phi","nElectron","Electron_pdgId","Electron_phi","Electron_eta","Electron_mass","Electron_pt","Electron_cutBased","Electron_pfRelIso03_all","Electron_ip3d","Electron_sip3d","Electron_dxy","Electron_dz","Muon_looseId","Muon_softMvaId","Muon_highPtId"]
triggers = ["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"]
vars_in.extend(triggers)
if isMC:
	vars_in.extend(["genWeight","Pileup_nTrueInt","Muon_genPartFlav","Electron_genPartFlav","GenPart_genPartIdxMother","GenPart_pdgId","Muon_genPartIdx","GenPart_pt","GenPart_eta","GenPart_phi","GenPart_mass"])
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

pbar = tqdm(total=nEntries)
for data in (events.iterate(vars_in)):
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
	
	for ev in (range(nEntries)):
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
		last_diff = 9999999.0
		for m1 in range(len(GoodE)-1):
			for m2 in range(m1+1,len(GoodE)):
				passes=True
				if abs(data["Electron_pdgId"][ev][GoodE[m1]] + data["Electron_pdgId"][ev][GoodE[m2]])!=0:
					cutBy2.append(0)
					passes=False
	
				if not passes: continue

				mu1 = TLorentzVector()
				mu2 = TLorentzVector()
				mu1.SetPtEtaPhiM(data["Electron_pt"][ev][GoodE[m1]],data["Electron_eta"][ev][GoodE[m1]],data["Electron_phi"][ev][GoodE[m1]],data["Electron_mass"][ev][GoodE[m1]])
				mu2.SetPtEtaPhiM(data["Electron_pt"][ev][GoodE[m2]],data["Electron_eta"][ev][GoodE[m2]],data["Electron_phi"][ev][GoodE[m2]],data["Electron_mass"][ev][GoodE[m2]])

				diff = abs((mu1+mu2).M() - Zmass)

				if diff < last_diff:
	
					last_diff = diff
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
	
		if nGoodM<1:
			selection[ev] = False
		if not selection[ev]: continue

		yesPho = True
		if isMC==1:
			yesPho = False
			gen_idx = data["Muon_genPartIdx"][ev][i3]
			gen_id = data["GenPart_pdgId"][ev][gen_idx]

			mom_idx = data["GenPart_genPartIdxMother"][ev][gen_idx]
			mom_id = data["GenPart_pdgId"][ev][mom_idx]
			while (mom_id == gen_id) and (mom_idx>0):
				mom_idx = data["GenPart_genPartIdxMother"][ev][mom_idx]
				mom_id = data["GenPart_pdgId"][ev][mom_idx]

			mommom_idx = data["GenPart_genPartIdxMother"][ev][mom_idx]
			mommom_id = data["GenPart_pdgId"][ev][mommom_idx]
			while (mommom_id == mom_id) and (mommom_idx>0):
				mommom_idx = data["GenPart_genPartIdxMother"][ev][mommom_idx]
				mommom_id = data["GenPart_pdgId"][ev][mommom_idx]

			#gen_deltapT = abs(data["Muon_pt"][ev][i3] - data["GenPart_pt"][ev][gen_idx])
			#gen_deltaR  = deltaR(data["Muon_eta"][ev][i3],data["Muon_phi"][ev][i3],data["GenPart_eta"][ev][gen_idx],data["GenPart_phi"][ev][gen_idx])
			origin =  PartOrigin(gen_id,mom_id,mommom_id,data["Muon_pdgId"][ev][i3])

			nPhotonDaughters,nGenMu = 0,0
			DaughterIdxs = []
			DaughterIds  = []
			allIds = []
			TheseMass = [999.0]
			if (origin==2):# and (data["nMuon"][ev]==3):
				yesPho = True
				ml1, ml2 = 0, 0
				for gidx in range(len(data["GenPart_genPartIdxMother"][ev])):
					allIds.append(data["GenPart_pdgId"][ev][gidx])
					midx = data["GenPart_genPartIdxMother"][ev][gidx]
					if abs(data["GenPart_pdgId"][ev][gidx])==13:
							if abs(data["GenPart_pdgId"][ev][midx])!=13: nGenMu+=1
					if midx==mom_idx:
						nPhotonDaughters+=1
						DaughterIdxs.append(gidx)
						DaughterIds.append(data["GenPart_pdgId"][ev][gidx])
				if len(DaughterIds)==2:
					daught1, daught2 = TLorentzVector(), TLorentzVector()
					daught1.SetPtEtaPhiM(data["GenPart_pt"][ev][DaughterIdxs[0]],data["GenPart_eta"][ev][DaughterIdxs[0]],data["GenPart_phi"][ev][DaughterIdxs[0]],.1056583755)#data["GenPart_mass"][ev][DaughterIdxs[0]])
					daught2.SetPtEtaPhiM(data["GenPart_pt"][ev][DaughterIdxs[1]],data["GenPart_eta"][ev][DaughterIdxs[1]],data["GenPart_phi"][ev][DaughterIdxs[1]],.1056583755)#data["GenPart_mass"][ev][DaughterIdxs[1]])
					invMass = (daught1 + daught2).M()
					TheseMass.append(invMass)
			
			if all(i >= 1 for i in TheseMass): yesPho = False

		if "DY" in in_file and oto1:
			if not yesPho:
				selection[ev] = False
			if not selection[ev]: continue

		lep1 = TLorentzVector()
		lep2 = TLorentzVector()
		lep1.SetPtEtaPhiM(data["Electron_pt"][ev][i1],data["Electron_eta"][ev][i1],data["Electron_phi"][ev][i1],data["Electron_mass"][ev][i1])
		lep2.SetPtEtaPhiM(data["Electron_pt"][ev][i2],data["Electron_eta"][ev][i2],data["Electron_phi"][ev][i2],data["Electron_mass"][ev][i2])
	
		twoleps = lep1+lep2
		Met = TLorentzVector()
		Met.SetPtEtaPhiM(data["MET_pt"][ev],0,data["MET_phi"][ev],0)
	
		output["idL1"].append(data["Electron_pdgId"][ev][i1]); output["idL2"].append(data["Electron_pdgId"][ev][i2])
		output["pTL1"].append(data["Electron_pt"][ev][i1]); output["pTL2"].append(data["Electron_pt"][ev][i2])
		output["etaL1"].append(data["Electron_eta"][ev][i1]); output["etaL2"].append(data["Electron_eta"][ev][i2])
		output["phiL1"].append(data["Electron_phi"][ev][i1]); output["phiL2"].append(data["Electron_phi"][ev][i2])
		output["IsoL1"].append(data["Electron_pfRelIso03_all"][ev][i1]); output["IsoL2"].append(data["Electron_pfRelIso03_all"][ev][i2])
		output["ip3dL1"].append(data["Electron_ip3d"][ev][i1]); output["ip3dL2"].append(data["Electron_ip3d"][ev][i2])
		output["sip3dL1"].append(data["Electron_sip3d"][ev][i1]); output["sip3dL2"].append(data["Electron_sip3d"][ev][i2])
		output["dxyL1"].append(data["Electron_dxy"][ev][i1]); output["dxyL2"].append(data["Electron_dxy"][ev][i2])
		output["dzL1"].append(data["Electron_dz"][ev][i1]); output["dzL2"].append(data["Electron_dz"][ev][i2])
		output["massL1"].append(data["Electron_mass"][ev][i1]); output["massL2"].append(data["Electron_mass"][ev][i2])
		output["tightIdL1"].append(True); output["tightIdL2"].append(True)
		output["looseIdL1"].append(True); output["looseIdL2"].append(True)
		output["medIdL1"].append(True); output["medIdL2"].append(True)
		output["softIdL1"].append(True); output["softIdL2"].append(True)
		output["mvaIdL1"].append(True); output["mvaIdL2"].append(True)
	
		output["dR12"].append(deltaR(lep1.Eta(),lep1.Phi(),lep2.Eta(),lep2.Phi()))
		output["met"].append(data["MET_pt"][ev]); output["met_phi"].append(data["MET_phi"][ev])
	
		output["nMuons"].append(data["nMuon"][ev]); output["nGoodMuons"].append(len(GoodM))
		output["nElectrons"].append(data["nElectron"][ev]); output["nGoodElectrons"].append(len(GoodE))
		output["nLeptons"].append(data["nElectron"][ev]+data["nMuon"][ev]); output["nGoodLeptons"].append(len(GoodM)+len(GoodE))
		output["nbJets"].append(nbjets)
		output["nJets"].append(data["nJet"][ev])
		output["mt"].append((twoleps+Met).Mt())
	
		output["Run"].append(data["run"][ev])
		output["Event"].append(data["event"][ev])
		output["LumiSect"].append(data["luminosityBlock"][ev])
		output["inAcceptance"].append(0)
	
		if isMC==1: 
			output["genWeight"].append(data["genWeight"][ev])
			output["pileupWeight"].append(data["Pileup_nTrueInt"][ev])
			output["sourceL1"].append(data["Electron_genPartFlav"][ev][i1]); output["sourceL2"].append(data["Electron_genPartFlav"][ev][i2])
		else: 
			output["genWeight"].append(1)
			output["pileupWeight"].append(1)
			output["sourceL1"].append(0); output["sourceL2"].append(0)

		if nGoodM>0:
			lep3 = TLorentzVector()
			lep3.SetPtEtaPhiM(data["Muon_pt"][ev][i3],data["Muon_eta"][ev][i3],data["Muon_phi"][ev][i3],data["Muon_mass"][ev][i3])
			threeleps = lep1+lep2+lep3
			output["m3l"].append(threeleps.M())
			output["idL3"].append(data["Muon_pdgId"][ev][i3])
			output["pTL3"].append(data["Muon_pt"][ev][i3])
			output["etaL3"].append(data["Muon_eta"][ev][i3])
			output["phiL3"].append(data["Muon_phi"][ev][i3])
			output["IsoL3"].append(data["Muon_pfRelIso03_all"][ev][i3])
			output["ip3dL3"].append(data["Muon_ip3d"][ev][i3])
			output["sip3dL3"].append(data["Muon_sip3d"][ev][i3])
			output["massL3"].append(data["Muon_mass"][ev][i3])
			output["tightIdL3"].append(data["Muon_tightId"][ev][i3])
			output["looseIdL3"].append(data["Muon_looseId"][ev][i3])
			output["medIdL3"].append(data["Muon_mediumId"][ev][i3])
			output["softIdL3"].append(data["Muon_softId"][ev][i3])
			output["mvaIdL3"].append(data["Muon_mvaId"][ev][i3])
			output["dxyL3"].append(data["Muon_dxy"][ev][i3])
			output["dzL3"].append(data["Muon_dz"][ev][i3])
			output["dR13"].append(deltaR(lep1.Eta(),lep1.Phi(),lep3.Eta(),lep3.Phi()))
			output["dR23"].append(deltaR(lep2.Eta(),lep2.Phi(),lep3.Eta(),lep3.Phi()))
			output["softMvaIdL3"].append(data["Muon_softMvaId"][ev][i3])
			output["highPtIdL3"].append(data["Muon_highPtId"][ev][i3])
			if isMC==1:
				#gen_idx = data["Muon_genPartIdx"][ev][i3]
				#gen_id = data["GenPart_pdgId"][ev][gen_idx]

				#mom_idx = data["GenPart_genPartIdxMother"][ev][gen_idx]
				#mom_id = data["GenPart_pdgId"][ev][mom_idx]
				#while (mom_id == gen_id) and (mom_idx>0):
				#	mom_idx = data["GenPart_genPartIdxMother"][ev][mom_idx]
				#	mom_id = data["GenPart_pdgId"][ev][mom_idx]

				#mommom_idx = data["GenPart_genPartIdxMother"][ev][mom_idx]
				#mommom_id = data["GenPart_pdgId"][ev][mommom_idx]
				#while (mommom_id == mom_id) and (mommom_idx>0):
				#	mommom_idx = data["GenPart_genPartIdxMother"][ev][mommom_idx]
				#	mommom_id = data["GenPart_pdgId"][ev][mommom_idx]

				##gen_deltapT = abs(data["Muon_pt"][ev][i3] - data["GenPart_pt"][ev][gen_idx])
				##gen_deltaR  = deltaR(data["Muon_eta"][ev][i3],data["Muon_phi"][ev][i3],data["GenPart_eta"][ev][gen_idx],data["GenPart_phi"][ev][gen_idx])
				#origin =  PartOrigin(gen_id,mom_id,mommom_id,data["Muon_pdgId"][ev][i3])

				#nPhotonDaughters,nGenMu = 0,0
                #DaughterIdxs = []
                #DaughterIds  = []
                #allIds = []
                #if (origin==2):# and (data["nMuon"][ev]==3):
                #    yesPho = True
                #    ml1, ml2 = 0, 0
                #    for gidx in range(len(data["GenPart_genPartIdxMother"][ev])):
                #        allIds.append(data["GenPart_pdgId"][ev][gidx])
                #        midx = data["GenPart_genPartIdxMother"][ev][gidx]
                #        if abs(data["GenPart_pdgId"][ev][gidx])==13:
                #                if abs(data["GenPart_pdgId"][ev][midx])!=13:
                #                    nGenMu+=1
                #        if midx==mom_idx:
                #            nPhotonDaughters+=1
                #            DaughterIdxs.append(gidx)
                #            DaughterIds.append(data["GenPart_pdgId"][ev][gidx])
                #    if len(DaughterIds)==2:
                #        daught1, daught2 = TLorentzVector(), TLorentzVector()
                #        daught1.SetPtEtaPhiM(data["GenPart_pt"][ev][DaughterIdxs[0]],data["GenPart_eta"][ev][DaughterIdxs[0]],data["GenPart_phi"][ev][DaughterIdxs[0]],.1056583755)#data["GenPart_mass"][ev][DaughterIdxs[0]])
                #        daught2.SetPtEtaPhiM(data["GenPart_pt"][ev][DaughterIdxs[1]],data["GenPart_eta"][ev][DaughterIdxs[1]],data["GenPart_phi"][ev][DaughterIdxs[1]],.1056583755)#data["GenPart_mass"][ev][DaughterIdxs[1]])
                #        invMass = (daught1 + daught2).M()
                #        TheseMass.append(invMass)

				#if all(i >= 1 for i in TheseMass): yesPho = False

				output["sourceL3"].append(origin)
				if "DY" in in_file and oto1: output["photon_mass"].append(TheseMass[1])
				else: output["photon_mass"].append(-1)
			else:
				output["sourceL3"].append(0)
				output["photon_mass"].append(-1)
		else:
			output["m3l"].append(-99)
			output["idL3"].append(-99)
			output["pTL3"].append(-99)
			output["etaL3"].append(-99)
			output["phiL3"].append(-99)
			output["IsoL3"].append(-99)
			output["ip3dL3"].append(-99)
			output["sip3dL3"].append(-99)
			output["massL3"].append(-99)
			output["tightIdL3"].append(-99)
			output["looseIdL3"].append(-99)
			output["medIdL3"].append(-99)
			output["softIdL3"].append(-99)
			output["mvaIdL3"].append(-99)
			output["dxyL3"].append(-99)
			output["dzL3"].append(-99)
			output["dR13"].append(-99)
			output["dR23"].append(-99)
			output["softMvaIdL3"].append(-99)
			output["highPtIdL3"].append(-99)
			if isMC==1:
				output["sourceL3"].append(-99)
			else:
				output["sourceL3"].append(-99)
			output["photon_mass"].append(-1)
			
		output["idL4"].append(-99)
		output["pTL4"].append(-99)
		output["etaL4"].append(-99)
		output["phiL4"].append(-99)
		output["IsoL4"].append(-99)
		output["ip3dL4"].append(-99)
		output["sip3dL4"].append(-99)
		output["massL4"].append(-99)
		output["tightIdL4"].append(-99)
		output["looseIdL4"].append(-99)
		output["medIdL4"].append(-99)
		output["softIdL4"].append(-99)
		output["mvaIdL4"].append(-99)
		output["dxyL4"].append(-99)
		output["dzL4"].append(-99)

		output["passedDiMu1"].append(1)
		output["passedDiMu2"].append(1)
		output["passedTriMu"].append(1)
	
		output["m4l"].append(-1)
	
	left6 += np.count_nonzero(selection)
	pbar.update(nEntries)

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

f1 = open("/blue/avery/nikmenendez/Wto3l/Skimmer/PyNanoSkimmer/Tables/cut_list.txt","a")
f2 = open("/blue/avery/nikmenendez/Wto3l/Skimmer/PyNanoSkimmer/Tables/GoodMu_list.txt","a")

f1.write("%s,%.2f%%,%.2f%%,%.2f%%,%.2f%%\n"%(dataset,eff1,eff5,eff6,left6/left0*100))
f2.write("%s,%.2f%%,%.2f%%,%.2f%%,%.2f%%,%.2f%%,%.2f%%\n"%(dataset,100-eff5,causePer[0],causePer[1],causePer[2],causePer[3],causePer[4]))

f1.close()
f2.close()
