from __future__ import division
from __future__ import print_function
import numpy as np
#import sys;sys.path.append('/workfs2/cms/qyguo/.local/lib64/python3.6/site-packages')
import sys;sys.path.append('/publicfs/cms/user/qyguo/.local/lib/python3.6/site-packages')
import sys;sys.path.append('/publicfs/cms/user/qyguo/.local/lib64/python3.6/site-packages')
import uproot
import sys
from ROOT import TLorentzVector
#import uproot3_methods.classes.TLorentzVector as TLorentzVector
#import sys;sys.path.append('/workfs2/cms/qyguo/.local/lib/python3.6/site-packages')
from tqdm import tqdm
from Utils.DeltaR import deltaR
from Utils.PartOrigin import PartOrigin
from out_dict import *
#import matplotlib.pyplot as plt
import concurrent.futures

ZpX_Sel = False
#ZpX_Sel = True

year = 2018
BTagCut = {'-2016':0.6001,
	'2016':0.5847,
	'2017':0.4506,
	'2018':0.4168,
	}
#print("BtagCut: ",BTagCut[str(year)])

examples = 0
nInReg = 0
untaggedMu = []
invMasses = []
passed_sel = 0
so_far = 0

dataset = str(sys.argv[1])
isSignal = 0
isMC = 1
if "To3l_M" in sys.argv[1] or "to3l_M" in sys.argv[1]:
	isSignal = 1
if "Muon" in sys.argv[1]:
	isMC = 0
in_file = ""
out_file = ""
is_DY = "DY" in sys.argv[1]
is_DY = False
if ZpX_Sel:
	subname = "3mu_ZpX"
else:
	subname = "UL"

if isSignal==1:
	in_file = "/publicfs/cms/data/hzz/guoqy/Zprime/UL/2018/Ntuple/signal_Skim_hadd/"+dataset+".root"
	out_file = "/publicfs/cms/data/hzz/guoqy/Zprime/UL/2018/Ntuple/signal_sel/"+subname+"/"+dataset+".root"
	sumW_file = "/publicfs/cms/data/hzz/guoqy/Zprime/UL/2018/Ntuple/signal_sel/sumW/"+subname+"/"+dataset+".txt"
	#in_file = "/cmsuf/data/store/user/t2/users/nikmenendez/signal/NanoAOD/"+dataset+".root"
	#out_file = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/signal/signal_sel/"+subname+"/"+dataset+".root"
	#sumW_file = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/signal/signal_sel/"+subname+"/sumW/"+dataset+".txt"
elif isMC==1:
	#in_file = "/cmsuf/data/store/user/t2/users/nikmenendez/2017_MC_bkg/NanoAOD_UL/"+dataset+".root"
	in_file = "/publicfs/cms/data/hzz/guoqy/Zprime/UL/2018/Ntuple/BKG/bkg_Skim_hadd/"+dataset+".root"
	out_file = "/publicfs/cms/data/hzz/guoqy/Zprime/UL/2018/Ntuple/BKG/signal_sel/"+subname+"/"+dataset+".root"
	sumW_file = "/publicfs/cms/data/hzz/guoqy/Zprime/UL/2018/Ntuple/BKG/signal_sel/sumW/"+subname+"/"+dataset+".txt"
	if is_DY:
		out_file = "/publicfs/cms/data/hzz/guoqy/Zprime/UL/2018/Ntuple/BKG/signal_sel/"+subname+"/"+"DY_M0To1/"+dataset+"_M0To1.root"
		sumW_file = "/publicfs/cms/data/hzz/guoqy/Zprime/UL/2018/Ntuple/BKG/signal_sel/"+subname+"/"+"DY_M0To1/"+dataset+"_M0To1.txt"
		#out_file = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/background/signal_sel/"+subname+"/"+dataset+"_M0To1.root"
		#sumW_file = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/background/signal_sel/"+subname+"/sumW/"+dataset+"_M0To1.txt"
	#else:
	#	out_file = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/background/signal_sel/"+subname+"/"+dataset+".root"
	#	sumW_file = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/background/signal_sel/"+subname+"/sumW/"+dataset+".txt"
	#	
else:
	in_file = "/cmsuf/data/store/user/t2/users/nikmenendez/data_wto3l_UL/2017/"+dataset+".root"
	out_file = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/data/signal_sel/"+subname+"/"+dataset+".root"

print("Skimming file %s"%(in_file))

file = uproot.open(in_file)
executor = concurrent.futures.ThreadPoolExecutor()

events = file["Events"]
runs = file["Runs"]

if isMC==1:
	#Get SumWeight
	sumW = 0
	#SumWeights = runs["genEventSumw"].array()
	SumWeights = runs["genEventSumw"].array(library="np")
	sumW = np.sum(SumWeights)
	if isSignal==1:
		#sumW = events.numentries
		sumW = events.num_entries
	file_sumW = open(sumW_file,"w")
	file_sumW.write(str(sumW))
	file_sumW.close()
else:
	sumW = 1

#Define cuts
cut0, cut1, cut2, cut3, cut4 = 0, 0, 0, 0, 0
if not ZpX_Sel: leadingPtCut, subleadingPtCut, trailingPtCut = 12.0, 10.0, 5.0
else: leadingPtCut, subleadingPtCut, trailingPtCut = 20.0, 10.0, 5.0
iso_cut = 999.0 #0.3
sip_cut = 999.0 #4
dxy_cut = 999.0 #0.05
dz_cut = 999.0 #0.1
Wmass = 9999.0 #83.0
#iso_cut = 0.3
#sip_cut = 4
#dxy_cut = 0.05
#dz_cut = 0.1
#Wmass = 83.0
n_other = 0

#Import tree from ROOT
#triggers = ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL","HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ","HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8","HLT_TripleMu_12_10_5","HLT_TripleMu_10_5_5_DZ"]
#triggers = ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8","HLT_TripleMu_12_10_5","HLT_TripleMu_10_5_5_DZ"]
#triggers = ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8","HLT_TripleMu_12_10_5","HLT_TripleMu_10_5_5_DZ"]
triggers = ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8","HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8","HLT_TripleMu_12_10_5","HLT_TripleMu_10_5_5_DZ"]
#triggers = ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8","HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8","HLT_TripleMu_12_10_5","HLT_TripleMu_10_5_5_DZ"]
trigger_ZpX = ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8"]
vars_in = ["run","event","luminosityBlock","nMuon","Muon_pt","Muon_pdgId","Muon_eta","Muon_phi","Muon_mass","Muon_pfRelIso03_all","Muon_tightId","Muon_mediumId","Muon_ip3d","Muon_sip3d","Muon_dxy","Muon_dz","nJet","Jet_pt","Jet_btagCSVV2","MET_pt","MET_phi","Muon_softId","Muon_mvaId","Muon_isGlobal","Muon_isTracker","Muon_looseId","Muon_segmentComp"]
#vars_in = ["run","event","luminosityBlock","nMuon","Muon_pt","Muon_pdgId","Muon_eta","Muon_phi","Muon_mass","Muon_pfRelIso03_all","Muon_tightId","Muon_mediumId","Muon_ip3d","Muon_sip3d","Muon_dxy","Muon_dz","MET_pt","MET_phi","Muon_softId","Muon_mvaId","Muon_isGlobal","Muon_isTracker","Muon_looseId","Muon_segmentComp"]
vars_in.extend(triggers)
if isMC:
	vars_in.extend(["genWeight","Pileup_nTrueInt","Muon_genPartFlav","GenPart_genPartIdxMother","GenPart_pdgId","Muon_genPartIdx","GenPart_pt","GenPart_eta","GenPart_phi","GenPart_mass"])
	#vars_in.extend(["genWeight","Muon_genPartFlav","GenPart_genPartIdxMother","GenPart_pdgId","Muon_genPartIdx","GenPart_pt","GenPart_eta","GenPart_phi","GenPart_mass"])
if isSignal:
	vars_in.extend(["GenPart_pdgId","GenPart_eta","GenPart_pt","nGenPart"])

#data = events.arrays(vars_in,executor=executor)

#nEntries = len(data["nMuon"])
#nEntries = events.numentries
nEntries = events.num_entries

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
trig = np.array([0,0,0])
if len(triggers)==4:  trig = np.array([0,0,0,0])
if len(triggers)==5:  trig = np.array([0,0,0,0,0])

pbar = tqdm(total=nEntries)
for data in (events.iterate(vars_in, library="np")):
	#Find acceptance of signal
	#left0 += nEntries
	#eff0 = left0/nEntries*100
	selection = data["nMuon"] >= 0
	nComp = np.count_nonzero(selection)
	so_far += nComp
	#print("check1")
	if isSignal==1:
		for ev in (range(len(data["GenPart_pdgId"]))):
			m_found = 0
			gen = np.unique(np.array([data["GenPart_pdgId"][ev],data["GenPart_eta"][ev],data["GenPart_pt"][ev]]), axis=1)
			for i in range(len(gen[0])):
				if abs(gen[0][i])==13 and abs(gen[1][i])<=2.4 and gen[2][i]>=5: m_found+=1
			#print("m_found: ",m_found)
			if m_found<3: selection[ev] = False

			if 999888 not in data["GenPart_pdgId"][ev]:
				selection[ev] = False
			#event_mask = (m_found >= 3) and (999888 not in data["GenPart_pdgId"][ev])
			#print("check3")
			#selection[ev] = event_mask
			#print("check4")
		#left0 += np.count_nonzero(selection)
		#eff0 = left0/nEntries*100
	left0 += np.count_nonzero(selection)
	
	#Begin selection
	selection *= data["nMuon"] >= 3
	left1 += np.count_nonzero(selection)
	#print("check2")
	#eff1 = left1/left0*100
	
	# Calculate trigger efficiencies
	#trig = np.array([np.count_nonzero((data[triggers[0]]==1)*selection),np.count_nonzero((data[triggers[1]]==1)*selection),np.count_nonzero((data[triggers[2]]==1)*selection),np.count_nonzero((data[triggers[3]]==1)*selection),np.count_nonzero((data[triggers[4]]==1)*selection)])
	#trigE = trig/left1*100
	passedDiMu0 = (data["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8"]==1)
	passedDiMu1 = (data["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8"]==1)
	passedDiMu2 = (data["HLT_TripleMu_12_10_5"]==1) #(data["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ"]==1) | (data["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL"]==1)
	passedTriMu = (data["HLT_TripleMu_10_5_5_DZ"]==1) #| (data["HLT_TripleMu_12_10_5"]==1)
	##if not ZpX_Sel: selection *= passedDiMu1 | passedDiMu2 | passedTriMu | passedDiMu0
	##else: selection *= passedDiMu1
	if not ZpX_Sel:
		selection_trigger = (data[triggers[0]]==1)
		for i in range(len(triggers)-1):
			selection_trigger |= (data[triggers[i+1]]==1) 
		selection *= selection_trigger
	else: selection *= (data[trigger_ZpX[0]]==1)
	left2 += np.count_nonzero(selection)
	#eff2 = left2/left1*100
	
	if len(triggers)>4:
		trig += np.array([np.count_nonzero((data[triggers[0]]==1)*selection),np.count_nonzero((data[triggers[1]]==1)*selection),np.count_nonzero((data[triggers[2]]==1)*selection),np.count_nonzero((data[triggers[3]]==1)*selection),np.count_nonzero((data[triggers[4]]==1)*selection)])
	elif len(triggers)==4:
		trig += np.array([np.count_nonzero((data[triggers[0]]==1)*selection),np.count_nonzero((data[triggers[1]]==1)*selection),np.count_nonzero((data[triggers[2]]==1)*selection),np.count_nonzero((data[triggers[3]]==1)*selection)])
	else:
		trig += np.array([np.count_nonzero((data[triggers[0]]==1)*selection),np.count_nonzero((data[triggers[1]]==1)*selection),np.count_nonzero((data[triggers[2]]==1)*selection)])
	#trigE = trig/left1*100
	#trig = np.array([left2,left2,left2,left2,left2])
	#trigE = trig/left1*100
	
	#num3 = 0
	#num4 = 0
	#cause = np.array([0,0,0,0,0])
	#cause2= np.array([0,0,0,0,0])
	
	for ev in (range(len(data["nMuon"]))):
		if not selection[ev]: continue
	
		nbjets = 0
		for i in range(data["nJet"][ev]):
			#if data["Jet_pt"][ev][i] > 25 and data["Jet_btagCSVV2"][ev][i] > .46:
			if data["Jet_pt"][ev][i] > 25 and data["Jet_btagCSVV2"][ev][i] > BTagCut[str(year)]:
				nbjets+=1
		#if nbjets > 0:
		#	selection[ev] = False
		#	num3+=1
		#if not selection[ev]: continue
	
	
		nGood = 0
		GoodMu = []
		cutBy = []
		for i in range(data["nMuon"][ev]):
			passes=True
			#if data["Muon_softId"][ev][i] != 1: 
			#	cutBy.append(0)
			#	passes=False
			if data["Muon_sip3d"][ev][i] > sip_cut: 
				cutBy.append(1)
				passes=False
			if abs(data["Muon_dxy"][ev][i]) > dxy_cut: 
				cutBy.append(2)
				passes=False
			if abs(data["Muon_dz"][ev][i]) > dz_cut: 
				cutBy.append(3)
				passes=False
			if data["Muon_pfRelIso03_all"][ev][i] > iso_cut: 
				cutBy.append(4)
				passes=False
			if not passes: continue
	
			GoodMu.append(i)

		if len(GoodMu) < 3: 
			selection[ev] = False
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
					#if (m3l < Wmass) or (m3l > 95):
						cutBy2.append(4)
						passes=False
					if not passes: continue

					if ZpX_Sel:
						# ======================== FOR 3MU ZPX SELECTION =============================================
						if (data["Muon_pdgId"][ev][GoodMu[m1]] + data["Muon_pdgId"][ev][GoodMu[m2]]) == 0:
							M1 = (mu1 + mu2).M()
							if (data["Muon_pdgId"][ev][GoodMu[m1]] + data["Muon_pdgId"][ev][GoodMu[m3]]) == 0:
								M2 = (mu1 + mu3).M()
								if abs(M1-91)<abs(M2-91):
									z1 = m1
									z2 = m2
									z3 = m3
								else:
									z1 = m1
									z2 = m3
									z3 = m2
							elif (data["Muon_pdgId"][ev][GoodMu[m2]] + data["Muon_pdgId"][ev][GoodMu[m3]]) == 0:
								M2 = (mu2 + mu3).M()
								if abs(M1-91)<abs(M2-91):
									z1 = m1
									z2 = m2
									z3 = m3
								else:
									z1 = m2
									z2 = m3
									z3 = m1
						elif (data["Muon_pdgId"][ev][GoodMu[m1]] + data["Muon_pdgId"][ev][GoodMu[m3]]) == 0:
							M1 = (mu1 + mu3).M()
							M2 = (mu2 + mu3).M()
							if abs(M1-91)<abs(M2-91):
								z1 = m1
								z2 = m3
								z3 = m2
							else:
								z1 = m2
								z2 = m3
								z3 = m1

						#if (M1 < 4) or (M2 < 4): continue
						i1 = GoodMu[z1]
						i2 = GoodMu[z2]
						i3 = GoodMu[z3]
						# ======================== FOR 3MU ZPX SELECTION =============================================
					else:
						i1 = GoodMu[m1]
						i2 = GoodMu[m2]
						i3 = GoodMu[m3]
	
					foundZp = True
	
		if not foundZp:
			selection[ev] = False
			for i in cutBy2:
				cause2[i]+=1
		if not selection[ev]: continue
	
		passed_sel+=1

		lep1 = TLorentzVector()
		lep2 = TLorentzVector()
		lep3 = TLorentzVector()
		lep1.SetPtEtaPhiM(data["Muon_pt"][ev][i1],data["Muon_eta"][ev][i1],data["Muon_phi"][ev][i1],data["Muon_mass"][ev][i1])
		lep2.SetPtEtaPhiM(data["Muon_pt"][ev][i2],data["Muon_eta"][ev][i2],data["Muon_phi"][ev][i2],data["Muon_mass"][ev][i2])
		lep3.SetPtEtaPhiM(data["Muon_pt"][ev][i3],data["Muon_eta"][ev][i3],data["Muon_phi"][ev][i3],data["Muon_mass"][ev][i3])

		yesPho = False
		if isMC==1:
			idxs = [i1,i2,i3]
			gen_id, mom_id, mommom_id = {}, {}, {}
			gen_deltapT, gen_deltaR, origin = {}, {}, {}

			nInReg+=1
			TheseMass = [999.0]
			for idx in idxs:
				gen_idx = data["Muon_genPartIdx"][ev][idx]
				gen_id[idx] = data["GenPart_pdgId"][ev][gen_idx]

				mom_idx = data["GenPart_genPartIdxMother"][ev][gen_idx]
				mom_id[idx] = data["GenPart_pdgId"][ev][mom_idx]
				while (mom_id[idx] == gen_id[idx]) and (mom_idx>0):
					#print("gen_id = %i, mom_id = %i, gen_idx = %i, mom_idx = %i"%(gen_id[idx],mom_id[idx],gen_idx,mom_idx))
					mom_idx = data["GenPart_genPartIdxMother"][ev][mom_idx]
					mom_id[idx] = data["GenPart_pdgId"][ev][mom_idx]


				mommom_idx = data["GenPart_genPartIdxMother"][ev][mom_idx]
				mommom_id[idx] = data["GenPart_pdgId"][ev][mommom_idx]
				while (mommom_id[idx] == mom_id[idx]) and (mommom_idx>0):
					mommom_idx = data["GenPart_genPartIdxMother"][ev][mommom_idx]
					mommom_id[idx] = data["GenPart_pdgId"][ev][mommom_idx]

				origin[idx] =  PartOrigin(gen_id[idx],mom_id[idx],mommom_id[idx],data["Muon_pdgId"][ev][idx])

				# ======================== FIGURING STUFF OUT =============================================
				nPhotonDaughters,nGenMu = 0,0
				DaughterIdxs = []
				DaughterIds  = []
				allIds = []
				if (mom_id[idx]==22):# and (data["nMuon"][ev]==3):
					yesPho = True
					ml1, ml2 = 0, 0
					for gidx in range(len(data["GenPart_genPartIdxMother"][ev])):
						allIds.append(data["GenPart_pdgId"][ev][gidx])
						midx = data["GenPart_genPartIdxMother"][ev][gidx]
						if abs(data["GenPart_pdgId"][ev][gidx])==13: 
								if abs(data["GenPart_pdgId"][ev][midx])!=13: 
									nGenMu+=1
						if midx==mom_idx:
							nPhotonDaughters+=1
							DaughterIdxs.append(gidx)
							DaughterIds.append(data["GenPart_pdgId"][ev][gidx])
					if len(DaughterIds)==2:
						daught1, daught2 = TLorentzVector(), TLorentzVector()
						daught1.SetPtEtaPhiM(data["GenPart_pt"][ev][DaughterIdxs[0]],data["GenPart_eta"][ev][DaughterIdxs[0]],data["GenPart_phi"][ev][DaughterIdxs[0]],.1056583755)#data["GenPart_mass"][ev][DaughterIdxs[0]])
						daught2.SetPtEtaPhiM(data["GenPart_pt"][ev][DaughterIdxs[1]],data["GenPart_eta"][ev][DaughterIdxs[1]],data["GenPart_phi"][ev][DaughterIdxs[1]],.1056583755)#data["GenPart_mass"][ev][DaughterIdxs[1]])
						invMass = (daught1 + daught2).M()
						invMasses.append(invMass)
						TheseMass.append(invMass)
						if invMass < .2:
							print("Muon mom is a photon with %i daughters with invariant mass %.2f : "%(nPhotonDaughters,invMass))#,end='')
							print("The two muons have pT  = %.2f, %.2f"%(daught1.Pt(),daught2.Pt()))
							print("The two muons have eta = %.2f, %.2f"%(daught1.Eta(),daught2.Eta()))
							print("The two muons have phi = %.2f, %.2f"%(daught1.Phi(),daught2.Phi()))
							print("The two muons have mass= %.2f, %.2f"%(daught1.M(),daught2.M()))
							print("The two muons have id  = %.2f, %.2f"%(data["GenPart_pdgId"][ev][DaughterIdxs[0]],data["GenPart_pdgId"][ev][DaughterIdxs[1]]))
						#print("Photon mom is a %i"%(mommom_id[idx]))
					#else:
					#	#print("Muon mom is a photon with %i daughters: "%(nPhotonDaughters),end='')
					#print(*DaughterIds,sep=", ")
					#print("There are %i loose muons and %i gen muons in this event"%(data["nMuon"][ev],nGenMu))
					gidx1 = data["Muon_genPartIdx"][ev][i1]
					gidx2 = data["Muon_genPartIdx"][ev][i2]
					gidx3 = data["Muon_genPartIdx"][ev][i3]
					gidMu1 = data["GenPart_pdgId"][ev][data["Muon_genPartIdx"][ev][i1]]
					gidMu2 = data["GenPart_pdgId"][ev][data["Muon_genPartIdx"][ev][i2]]
					gidMu3 = data["GenPart_pdgId"][ev][data["Muon_genPartIdx"][ev][i3]]

					if gidx1==DaughterIdxs[0]:
						ml1 = 1
					elif gidx2==DaughterIdxs[0]:
						ml1 = 2
					elif gidx3==DaughterIdxs[0]:
						ml1 = 3
					else:
						untaggedMu.append(data["GenPart_pt"][ev][DaughterIdxs[0]])

					if (nPhotonDaughters<2):  continue

					if gidx1==DaughterIdxs[1]:
						ml2 = 1
					elif gidx2==DaughterIdxs[1]:
						ml2 = 2
					elif gidx3==DaughterIdxs[1]:
						ml2 = 3
					else:
						untaggedMu.append(data["GenPart_pt"][ev][DaughterIdxs[1]])


					#if len(GoodMu)==3:
					#	print("The three selected muons have id %i, %i, and %i"%(gidMu1,gidMu2,gidMu3))
					#else:
					#	for dex in GoodMu:
					#		if (dex!=i1) and (dex!=i2) and (dex!=i3):
					#			i4 = dex
					#			break
					#	gidx4 = data["Muon_genPartIdx"][ev][i4]
					#	if gidx4==DaughterIdxs[0]:
					#		ml1 = 4
					#	if gidx4==DaughterIdxs[1]:
					#		ml2 = 4
					#	gidMu4 = data["GenPart_pdgId"][ev][gidx4]
					#	#print("The four selected muons have id %i, %i, %i, and %i"%(gidMu1,gidMu2,gidMu3,gidMu4))
					#if len(DaughterIds)==2:
					#	print("The two photon daughters are lep %i and lep %i"%(ml1,ml2))
					#examples+=1
					#if examples>500 or (so_far/nEntries>.95): 
					#	print()
					#	print("%.2f%% of events in CR peak were this category"%((examples/nInReg)*100))
					#	#print("pTs of untagged muons from phtotons:")
					#	#print(untaggedMu)
					#	#print("Only %i events had an untagged mu above 5 GeV"%(np.count_nonzero(untaggedMu>5)))
					#	#print("Invariant masses of the photon:")
					#	#print(np.array(invMasses)>1)
					#	#nBelow1 = np.count_nonzero(np.array(invMasses)<1)/len(invMasses)*100
					#	nBelow1 = np.count_nonzero(np.array(invMasses)<1)/passed_sel*100
					#	print("%.2f%% of events the photon has a mass below 1 GeV"%(nBelow1))
					#	plt.hist(invMasses,bins=24,range=(0,6))
					#	plt.plot([], [], ' ', label="Total Events in CR: %i"%(passed_sel))
					#	plt.xlabel("Photon Invariant Mass")
					#	plt.ylabel("Number of Events")
					#	plt.title("GEN Photon Mass Distribution in CR")
					#	plt.legend()
					#	plt.savefig("Photon_Masses_CR.png")
					#	quit()
							
				# ======================== FIGURING STUFF OUT =============================================

				if all(i >= 1 for i in TheseMass): yesPho = False
				#yesPho = True
				gen_deltapT[idx] = abs(data["Muon_pt"][ev][idx] - data["GenPart_pt"][ev][gen_idx])
				gen_deltaR[idx]  = deltaR(data["Muon_eta"][ev][idx],data["Muon_phi"][ev][idx],data["GenPart_eta"][ev][gen_idx],data["GenPart_phi"][ev][gen_idx])
				origin[idx] =  PartOrigin(gen_id[idx],mom_id[idx],mommom_id[idx],data["Muon_pdgId"][ev][idx])

		if isSignal==1:
			W_idx = -1
			for i in range(data["nGenPart"][ev]):
				if abs(data["GenPart_pdgId"][ev][i])==999888:
					#print(data["GenPart_pdgId"][ev][i])
					mommy_idx = data["GenPart_genPartIdxMother"][ev][i]
					if abs(data["GenPart_pdgId"][ev][mommy_idx])==24:
						W_idx = mommy_idx
						break
					##else:
					##	print("Z' mother is a %i???"%(data["GenPart_pdgId"][ev][W_idx]))
			if W_idx>=0:
				W_gen_mass = data["GenPart_mass"][ev][W_idx]
			else:
				##for i in range(data["nGenPart"][ev]):
				##	print(data["GenPart_pdgId"][ev][i])
				W_gen_mass = -1
			##print(W_gen_mass)
			##print("****************************************")

		if is_DY:
			#if yesPho: print()
			if not yesPho:
				selection[ev] = False
			if not selection[ev]: continue


		threeleps = lep1+lep2+lep3
		Met = TLorentzVector()
		Met.SetPtEtaPhiM(data["MET_pt"][ev],0,data["MET_phi"][ev],0)
	
		output["idL1"].append(data["Muon_pdgId"][ev][i1]); output["idL2"].append(data["Muon_pdgId"][ev][i2]); output["idL3"].append(data["Muon_pdgId"][ev][i3])
		output["pTL1"].append(data["Muon_pt"][ev][i1]); output["pTL2"].append(data["Muon_pt"][ev][i2]); output["pTL3"].append(data["Muon_pt"][ev][i3])
		output["etaL1"].append(data["Muon_eta"][ev][i1]); output["etaL2"].append(data["Muon_eta"][ev][i2]); output["etaL3"].append(data["Muon_eta"][ev][i3])
		output["phiL1"].append(data["Muon_phi"][ev][i1]); output["phiL2"].append(data["Muon_phi"][ev][i2]); output["phiL3"].append(data["Muon_phi"][ev][i3])
		output["IsoL1"].append(data["Muon_pfRelIso03_all"][ev][i1]); output["IsoL2"].append(data["Muon_pfRelIso03_all"][ev][i2]); output["IsoL3"].append(data["Muon_pfRelIso03_all"][ev][i3])
		output["ip3dL1"].append(data["Muon_ip3d"][ev][i1]); output["ip3dL2"].append(data["Muon_ip3d"][ev][i2]); output["ip3dL3"].append(data["Muon_ip3d"][ev][i3])
		output["sip3dL1"].append(data["Muon_sip3d"][ev][i1]); output["sip3dL2"].append(data["Muon_sip3d"][ev][i2]); output["sip3dL3"].append(data["Muon_sip3d"][ev][i3])
		output["massL1"].append(data["Muon_mass"][ev][i1]); output["massL2"].append(data["Muon_mass"][ev][i2]); output["massL3"].append(data["Muon_mass"][ev][i3])
		output["tightIdL1"].append(data["Muon_tightId"][ev][i1]); output["tightIdL2"].append(data["Muon_tightId"][ev][i2]); output["tightIdL3"].append(data["Muon_tightId"][ev][i3])
		output["looseIdL1"].append(data["Muon_looseId"][ev][i1]); output["looseIdL2"].append(data["Muon_looseId"][ev][i2]); output["looseIdL3"].append(data["Muon_looseId"][ev][i3])
		output["medIdL1"].append(data["Muon_mediumId"][ev][i1]); output["medIdL2"].append(data["Muon_mediumId"][ev][i2]); output["medIdL3"].append(data["Muon_mediumId"][ev][i3])
		output["mvaIdL1"].append(data["Muon_mvaId"][ev][i1]); output["mvaIdL2"].append(data["Muon_mvaId"][ev][i2]); output["mvaIdL3"].append(data["Muon_mvaId"][ev][i3])
		output["softIdL1"].append(data["Muon_softId"][ev][i1]); output["softIdL2"].append(data["Muon_softId"][ev][i2]); output["softIdL3"].append(data["Muon_softId"][ev][i3])
	
		output["dxyL1"].append(data["Muon_dxy"][ev][i1]); output["dxyL2"].append(data["Muon_dxy"][ev][i2]); output["dxyL3"].append(data["Muon_dxy"][ev][i3])
		output["dzL1"].append(data["Muon_dz"][ev][i1]); output["dzL2"].append(data["Muon_dz"][ev][i2]); output["dzL3"].append(data["Muon_dz"][ev][i3])
	
		output["dR12"].append(deltaR(lep1.Eta(),lep1.Phi(),lep2.Eta(),lep2.Phi()))
		output["dR13"].append(deltaR(lep1.Eta(),lep1.Phi(),lep3.Eta(),lep3.Phi()))
		output["dR23"].append(deltaR(lep2.Eta(),lep2.Phi(),lep3.Eta(),lep3.Phi()))
		output["met"].append(data["MET_pt"][ev]); output["met_phi"].append(data["MET_phi"][ev])
	
		output["nMuons"].append(data["nMuon"][ev]); output["nGoodMuons"].append(len(GoodMu))
		output["nElectrons"].append(0); output["nGoodElectrons"].append(0)
		output["nLeptons"].append(data["nMuon"][ev]); output["nGoodLeptons"].append(len(GoodMu))
		output["nbJets"].append(nbjets)
		output["nJets"].append(data["nJet"][ev])
		output["m3l"].append(threeleps.M()); output["mt"].append((threeleps+Met).Mt())
	
		output["Run"].append(data["run"][ev])
		output["Event"].append(data["event"][ev])
		output["LumiSect"].append(data["luminosityBlock"][ev])
		output["inAcceptance"].append(left0)
	
		if isMC==1: 
			output["genWeight"].append(data["genWeight"][ev])
			output["pileupWeight"].append(data["Pileup_nTrueInt"][ev])
			#output["sourceL1"].append(data["Muon_genPartFlav"][ev][i1]); output["sourceL2"].append(data["Muon_genPartFlav"][ev][i2]); output["sourceL3"].append(data["Muon_genPartFlav"][ev][i3])

			#for idx in idxs:
			#	if origin[idx]==2:
			#		print("gen_id = %i, mom_id = %i, mommom_id = %i"%(gen_id[idx],mom_id[idx],mommom_id[idx]))
			#		print("gen deltaPt = %.2f, gen deltaR = %.2f"%(gen_deltapT[idx],gen_deltaR[idx]))
			#		print("")
			#		n_other+=1
			#		if n_other>=50: quit()

			output["sourceL1"].append(origin[i1]); output["sourceL2"].append(origin[i2]); output["sourceL3"].append(origin[i3])
			#output["gen_dPtL1"].append(gen_deltapT[i1]); output["gen_dPtL2"].append(gen_deltapT[i2]); output["gen_dPtL3"].append(gen_deltapT[i3]);
			#output["gen_dRL1"].append(gen_deltaR[i1]); output["gen_dRL2"].append(gen_deltaR[i2]); output["gen_dRL3"].append(gen_deltaR[i3]);
			#if is_DY: output["photon_mass"].append(TheseMass[1]);
			#else: output["photon_mass"].append(-1)
			output["photon_mass"].append(-1)
		else: 
			output["genWeight"].append(1)
			output["pileupWeight"].append(1)
			output["sourceL1"].append(-2); output["sourceL2"].append(-2); output["sourceL3"].append(-2)
			#output["gen_dPtL1"].append(-1); output["gen_dPtL2"].append(-1); output["gen_dPtL3"].append(-1);
			#output["gen_dRL1"].append(-1); output["gen_dRL2"].append(-1); output["gen_dRL3"].append(-1);
			output["photon_mass"].append(-1)
	
		if isSignal==1:
			output["GenWMass"].append(W_gen_mass)
		else:
			output["GenWMass"].append(-1)

		output["passedDiMu0"].append(passedDiMu0[ev])
		output["passedDiMu1"].append(passedDiMu1[ev])
		output["passedDiMu2"].append(passedDiMu2[ev])
		output["passedTriMu"].append(passedTriMu[ev])
	
		if len(GoodMu)>3:
			lep4 = TLorentzVector()
			for dex in GoodMu:
				if (dex!=i1) and (dex!=i2) and (dex!=i3):
					i4 = dex
					break
			lep4.SetPtEtaPhiM(data["Muon_pt"][ev][i4],data["Muon_eta"][ev][i4],data["Muon_phi"][ev][i4],data["Muon_mass"][ev][i4])
			output["m4l"].append((threeleps+lep4).M())
			output["idL4"].append(data["Muon_pdgId"][ev][i4]); output["pTL4"].append(data["Muon_pt"][ev][i4])
			output["etaL4"].append(data["Muon_eta"][ev][i4]); output["phiL4"].append(data["Muon_phi"][ev][i4])
			output["IsoL4"].append(data["Muon_pfRelIso03_all"][ev][i4]); output["ip3dL4"].append(data["Muon_ip3d"][ev][i4]); output["sip3dL4"].append(data["Muon_sip3d"][ev][i4])
			output["massL4"].append(data["Muon_mass"][ev][i4]); output["tightIdL4"].append(data["Muon_tightId"][ev][i4]); output["looseIdL4"].append(data["Muon_looseId"][ev][i4])
			output["medIdL4"].append(data["Muon_mediumId"][ev][i4]); output["softIdL4"].append(data["Muon_softId"][ev][i4]); output["mvaIdL4"].append(data["Muon_mvaId"][ev][i4])
			output["dxyL4"].append(data["Muon_dxy"][ev][i4]); output["dzL4"].append(data["Muon_dz"][ev][i4])
		else:
			output["m4l"].append(-999)
			output["idL4"].append(-999); output["pTL4"].append(-999)
			output["etaL4"].append(-999); output["phiL4"].append(-999)
			output["IsoL4"].append(-999); output["ip3dL4"].append(-999); output["sip3dL4"].append(-999)
			output["massL4"].append(-999); output["tightIdL4"].append(-999); output["looseIdL4"].append(-999)
			output["medIdL4"].append(-999); output["softIdL4"].append(-999); output["mvaIdL4"].append(-999)
			output["dxyL4"].append(-999); output["dzL4"].append(-999)

	prev_len = len(output["idL1"])
	for key in output:
		this_len = len(output[key])
		if this_len!=prev_len:
			print("%s has wrong fill"%(key))
			print("%s has %i entries vs %i entries"%(key,this_len,prev_len))
			print(output[key])
			exit()

	left5 += np.count_nonzero(selection)
	pbar.update(nComp)

pbar.close()

with uproot.recreate(out_file) as f:
	#f["passedEvents"] = uproot.newtree(branches)
	#f["passedEvents"].newtree(branches)
	f.mktree("passedEvents", branches)
	f["passedEvents"].extend(output)

#left5 = np.count_nonzero(selection)

eff0 = left0/nEntries*100
eff1 = left1/left0*100
eff2 = left2/left1*100
trigE = trig/left2*100
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
print("B Jet Veto Bypass: %i. Efficiency = %.2f%%"%(left3,eff3))
print("Found 3 good muons: %i. Efficiency = %.2f%%"%(left4,eff4))
print("Found Z' candidate: %i. Efficiency = %.2f%%"%(left5,eff5))
print("=====================================================")
print("Total Efficiency = %.2f%%"%(left5/left1*100))
print("Wrote to file %s"%(out_file))
print("")

print("Percent that fail good muon cuts: softId %.2f%%, sip %.2f%%, dxy %.2f%%, dz %.2f%%, iso %.2f%%"%(causePer[0],causePer[1],causePer[2],causePer[3],causePer[4]))
print("Didn't find Z' because of: mu signs %.2f%%, leading pT %.2f%%, subleading pT %.2f%%, trailing pT %.2f%%, m3l %.2f%%"%(causePer2[0],causePer2[1],causePer2[2],causePer2[3],causePer2[4]))
if len(triggers)>4:
	print("Trigger efficiencies: 2mu: %.2f%%, 2mu+DZ: %.2f%%, 2mu+DZ+mass: %.2f%%, 3mu_12: %.2f%%, 3mu_10: %.2f%%"%(trigE[0],trigE[1],trigE[2],trigE[3],trigE[4]))
elif len(triggers)==4:
	print("Trigger efficiencies: 2mu+DZ+mass3p8: %.2f%%, 2mu+DZ+mass8: %.2f%%, 3mu_12: %.2f%%, 3mu_10: %.2f%%"%(trigE[0],trigE[1],trigE[2],trigE[3]))
else:
	print("Trigger efficiencies: 2mu+DZ+mass: %.2f%%, 3mu_12: %.2f%%, 3mu_10: %.2f%%"%(trigE[0],trigE[1],trigE[2]))
print("")

f1_Name = "Tables/cut_list"
f2_Name = "Tables/GoodMu_list"
f3_Name = "Tables/ZpCandidate_list"
f4_Name = "Tables/counts_list"
f5_Name = "Tables/Trigger_list"
if "Mass3p8" in triggers[0] and "Mass8" in triggers[1] or "Mass3p8" in triggers[1] and "Mass8" in triggers[0]:
	f1_Name += "_all"
	f2_Name += "_all"
	f3_Name += "_all"
	f4_Name += "_all"
	f5_Name += "_all"
elif "Mass3p8" in triggers[0] or "Mass3p8" in triggers[1]:
	f1_Name += "_Mass3p8"
	f2_Name += "_Mass3p8"
	f3_Name += "_Mass3p8"
	f4_Name += "_Mass3p8"
	f5_Name += "_Mass3p8"

if ZpX_Sel:
        f1_Name += "_ZpX"
        f2_Name += "_ZpX"
        f3_Name += "_ZpX"
        f4_Name += "_ZpX"
        f5_Name += "_ZpX"


f1 = open(f1_Name+".txt","a")
f2 = open(f2_Name+".txt","a")
f3 = open(f3_Name+".txt","a")
f4 = open(f4_Name+".txt","a")
f5 = open(f5_Name+".txt","a")

#f1 = open("Tables/cut_list.txt","a")
#f2 = open("Tables/GoodMu_list.txt","a")
#f3 = open("Tables/ZpCandidate_list.txt","a")
#f4 = open("Tables/counts_list.txt","a")
#f5 = open("Tables/Trigger_list.txt","a")

f1.write("%s,%.2f%%,%.2f%%,%.2f%%,%.2f%%,%.2f%%\n"%(dataset,eff2,eff3,eff4,eff5,left5/left1*100))
f2.write("%s,%.2f%%,%.2f%%,%.2f%%,%.2f%%,%.2f%%,%.2f%%\n"%(dataset,100-eff4,causePer[0],causePer[1],causePer[2],causePer[3],causePer[4]))
f3.write("%s,%.2f%%,%.2f%%,%.2f%%,%.2f%%,%.2f%%,%.2f%%\n"%(dataset,100-eff5,causePer2[0],causePer2[1],causePer2[2],causePer2[3],causePer2[4]))
if len(triggers)>4:
	f5.write("%s,%.2f%%,%.2f%%,%.2f%%,%.2f%%,%.2f%%,%.2f%%\n"%(dataset,eff2,trigE[0],trigE[1],trigE[2],trigE[3],trigE[4]))
elif len(triggers)==4:
	f5.write("%s,%.2f%%,%.2f%%,%.2f%%,%.2f%%,%.2f%%\n"%(dataset,eff2,trigE[0],trigE[1],trigE[2],trigE[3]))
else:
	f5.write("%s,%.2f%%,%.2f%%,%.2f%%,%.2f%%\n"%(dataset,eff2,trigE[0],trigE[1],trigE[2]))
if len(triggers)>4:
	f4.write("%s,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i\n"%(dataset,sumW,left1,left2,left3,left4,left5,cause[0],cause[1],cause[2],cause[3],cause[4],cause2[0],cause2[1],cause2[2],cause2[3],cause2[4],trig[0],trig[1],trig[2],trig[3],trig[4]))
elif len(triggers)==4:
	f4.write("%s,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i\n"%(dataset,sumW,left1,left2,left3,left4,left5,cause[0],cause[1],cause[2],cause[3],cause[4],cause2[0],cause2[1],cause2[2],cause2[3],cause2[4],trig[0],trig[1],trig[2],trig[3]))
else:
	f4.write("%s,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i\n"%(dataset,sumW,left1,left2,left3,left4,left5,cause[0],cause[1],cause[2],cause[3],cause[4],cause2[0],cause2[1],cause2[2],cause2[3],cause2[4],trig[0],trig[1],trig[2]))

f1.close()
f2.close()
f3.close()
f4.close()
f5.close()
