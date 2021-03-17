from __future__ import division
import sys
from ROOT import TFile, TTree, TLorentzVector
from tqdm import tqdm
import numpy as np
from Utils.DeltaR import deltaR
import output_tree as ot

#dataset = "WJetsToLNu"
dataset = str(sys.argv[1])
isMC = sys.argv[2]
in_file = ""
out_file = ""
if isMC=="1":
	in_file = "/cmsuf/data/store/user/t2/users/nikmenendez/2017_MC_bkg/NanoAOD/"+dataset+".root"
	out_file = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/"+dataset+".root"
else:
	in_file = "/cmsuf/data/store/user/t2/users/nikmenendez/data_wto3l/2017/"+dataset+".root"
	out_file = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/data/"+dataset+".root"

print("Skimming file %s"%(in_file))

File = TFile(in_file,"READ")

t = File.Get("Events")
nEntries = t.GetEntries()

if isMC=="1":
	# Get SumWeight
	sumW = 0
	s = File.Get("Runs")
	for w in range(0,s.GetEntries()):
		s.GetEntry(w)
		sumW+=s.genEventSumw

# Define Cuts
cut1, cut2, cut3 = 0, 0, 0
leadingPtCut, subleadingPtCut = 20.0, 10.0
iso_cut = 0.35
debug = False

if isMC=="1":
	print("Skimming %i events. SumWeight = %i"%(nEntries,sumW))
else:
	print("Skimming %i events."%(nEntries))

for event in tqdm(range(0,nEntries)):
	t.GetEntry(event)

	# Combine leptons into single arrays
	nLep = t.nElectron+t.nMuon
	lep_id   = np.zeros(nLep)
	lep_pt   = np.zeros(nLep)
	lep_phi  = np.zeros(nLep)
	lep_eta  = np.zeros(nLep)
	lep_mass = np.zeros(nLep)
	lep_iso  = np.zeros(nLep)
	lep_tight= np.zeros(nLep)
	lep_med  = np.zeros(nLep)

	for lep in range(0,t.nElectron):
		lep_id[lep]   = t.Electron_pdgId[lep]
		lep_pt[lep]   = t.Electron_pt[lep]
		lep_phi[lep]  = t.Electron_phi[lep]
		lep_eta[lep]  = t.Electron_eta[lep]
		lep_iso[lep]  = t.Electron_miniPFRelIso_all[lep]
		lep_mass[lep] = t.Electron_mass[lep]
		lep_tight[lep]= 1
		lep_med[lep]  = 1
	for lep in range(0,t.nMuon):
		lep_id[lep+t.nElectron]   = t.Muon_pdgId[lep]
		lep_pt[lep+t.nElectron]   = t.Muon_pt[lep]
		lep_phi[lep+t.nElectron]  = t.Muon_phi[lep]
		lep_eta[lep+t.nElectron]  = t.Muon_eta[lep]
		lep_iso[lep+t.nElectron]  = t.Muon_miniPFRelIso_all[lep]
		lep_mass[lep+t.nElectron] = t.Muon_mass[lep]
		lep_tight[lep+t.nElectron]= t.Muon_tightId[lep]
		lep_med[lep+t.nElectron]  = t.Muon_mediumId[lep]

	# Define needed variables
	index1, index2, index3 = 0, 0, 0
	trueL3 = False
	foundZ1LCandidate = False

	Zmass = 91.1876
	mZ1Low = 0.0
	mZ1High = 200.0

	# 3 Lepton cut
	if nLep < 3 or t.nMuon < 1:
		cut1+=1
		continue

	# Find Z Candidates
	n_Zs=0
	Z_Z1L_lepindex1 = []
	Z_Z1L_lepindex2 = []

	for i in range(0,nLep):
		for j in range(i+1,nLep):
			if not (lep_id[i]+lep_id[j]==0): continue

			li = TLorentzVector()
			li.SetPtEtaPhiM(lep_pt[i],lep_eta[i],lep_phi[i],lep_mass[i])
			lj = TLorentzVector()
			lj.SetPtEtaPhiM(lep_pt[j],lep_eta[j],lep_phi[j],lep_mass[j])
			Z = li + lj

			if Z.M() > 0.0 :
				n_Zs+=1
				Z_Z1L_lepindex1.append(i)
				Z_Z1L_lepindex2.append(j)

	# 2 Lepton Opposite Charge Cut
	properLep_ID = False
	Nmm, Nmp, Nem, Nep = 0, 0, 0, 0
	for i in range(0,nLep):
		if   lep_id[i]== 13: Nmp+=1
		elif lep_id[i]==-13: Nmm+=1
		elif lep_id[i]== 11: Nep+=1
		elif lep_id[i]==-11: Nem+=1

	if((Nmp>=1 and Nmm>=1) or (Nep>=1 and Nem>=1)): properLep_ID = True
	if not properLep_ID:
		cut2+=1
		continue

	# Find Best Z Candidate
	minZ1DeltaM=9999.9
	for i in range(0,n_Zs):
		i1, i2 = Z_Z1L_lepindex1[i], Z_Z1L_lepindex2[i]
		# Find highest pt index that's not the Z candidate
		m = np.zeros(lep_pt.size, dtype=bool)
		m[[i1,i2]] = True
		a = np.ma.array(lep_pt, mask=m)
		j1 = np.argmax(a)

		# Define Z
		lep_i1 = TLorentzVector()
		lep_i1.SetPtEtaPhiM(lep_pt[i1],lep_eta[i1],lep_phi[i1],lep_mass[i1])
		lep_i2 = TLorentzVector()
		lep_i2.SetPtEtaPhiM(lep_pt[i2],lep_eta[i2],lep_phi[i2],lep_mass[i2])
		Z1 = lep_i1 + lep_i2
		
		Z1DeltaM = abs(Z1.M()-Zmass)
		Z1_lepindex = [0,0]
		if lep_i1.Pt()>lep_i2.Pt(): Z1_lepindex = [i1,i2]
		else: Z1_lepindex = [i2,i1]

		# Check leading and subleading pT
		if lep_pt[Z1_lepindex[0]] < leadingPtCut or lep_pt[Z1_lepindex[1]] < subleadingPtCut: 
			if debug: print("Failed pT cut: lep1_pt = %f, lep2_pt = %f"%(lep_pt[Z1_lepindex[0]],lep_pt[Z1_lepindex[1]]))
			continue

		# Check dR(li,lj)>0.4 for any i,j
		if deltaR(lep_i1.Eta(),lep_i1.Phi(),lep_i2.Eta(),lep_i2.Phi()) < 0.4: 
			if debug: print("Failed dR cut")
			continue

		# Check M(l+,l-)>4.0 GeV
		if Z1.M() < 4.0: 
			if debug: print("Failed ZMass cut 1")
			continue

		# Check Isolation Cuts
		if lep_iso[i1] > iso_cut or lep_iso[i2] > iso_cut: 
			if debug: print("Failed Iso cut with iso %f and %f"%(lep_iso[i1],lep_iso[i2]))
			continue

		# Check tightId Cut
		if lep_tight[i1] != 1 or lep_tight[i2] != 1: 
			if debug: print("Failed tight cut")
			continue

		# Check Z Mass in Range
		if Z1.M() < mZ1Low or Z1.M() > mZ1High: 
			if debug: print("Failed Z Mass range cut")
			continue

		# Choose Z with closest mass
		if (Z1DeltaM<minZ1DeltaM):
			minZ1DeltaM = Z1DeltaM

			index1 = Z1_lepindex[0]
			index2 = Z1_lepindex[1]

			for lep in range(0,nLep):
				if(lep==index1 or lep==index2): continue
				if(abs(lep_id[lep])==13):
					index3 = lep
					trueL3 = True
					break

			foundZ1LCandidate=True

	if not foundZ1LCandidate:
		cut3+=1
		continue

	lep1 = TLorentzVector()
	lep1.SetPtEtaPhiM(lep_pt[index1],lep_eta[index1],lep_phi[index1],lep_mass[index1])
	lep2 = TLorentzVector()
	lep2.SetPtEtaPhiM(lep_pt[index2],lep_eta[index2],lep_phi[index2],lep_mass[index2])
	lep3 = TLorentzVector()
	lep3.SetPtEtaPhiM(lep_pt[index3],lep_eta[index3],lep_phi[index3],lep_mass[index3])

	threeleps = lep1+lep2+lep3
	Met = TLorentzVector()
	Met.SetPtEtaPhiM(t.MET_sumEt,0,t.MET_phi,0)
	
	ot.idL1[0], ot.idL2[0], ot.idL3[0] = lep_id[index1], lep_id[index2], lep_id[index3]
	ot.pTL1[0], ot.pTL2[0], ot.pTL3[0] = lep1.Pt(), lep2.Pt(), lep3.Pt()
	ot.etaL1[0], ot.etaL2[0], ot.etaL3[0] = lep1.Eta(), lep2.Eta(), lep3.Eta() 
	ot.phiL1[0], ot.phiL2[0], ot.phiL3[0] = lep1.Phi(), lep2.Phi(), lep3.Phi()
	ot.IsoL1[0], ot.IsoL2[0], ot.IsoL3[0] = lep_iso[index1], lep_iso[index2], lep_iso[index3]
	ot.massL1[0], ot.massL2[0], ot.massL3[0] = lep1.M(), lep2.M(), lep3.M()
	ot.tightIdL1[0], ot.tightIdL2[0], ot.tightIdL3[0] = lep_tight[index1], lep_tight[index2], lep_tight[index3]
	ot.medIdL1[0], ot.medIdL2[0], ot.medIdL3[0] = lep_med[index1], lep_med[index2], lep_med[index3]
	ot.dR12[0] = deltaR(lep1.Eta(),lep1.Phi(),lep2.Eta(),lep2.Phi())
	ot.dR13[0] = deltaR(lep1.Eta(),lep1.Phi(),lep3.Eta(),lep3.Phi())
	ot.dR23[0] = deltaR(lep2.Eta(),lep2.Phi(),lep3.Eta(),lep3.Phi())
	ot.met[0], ot.met_phi[0] = t.MET_sumEt, t.MET_phi

	ot.nLep[0] = nLep
	ot.nElectrons[0] = t.nElectron
	ot.nMuons[0] = t.nMuon
	ot.trueL3[0] = trueL3
	ot.m3l[0] = threeleps.M()
	ot.mt[0] = (threeleps+Met).M()

	ot.Run[0] = t.run
	ot.Event[0] = t.event
	ot.LumiSect[0] = t.luminosityBlock

	if isMC=="1":
		ot.genWeight[0] = t.genWeight

	ot.out_tree.Fill()

ot.f_out.Write()
ot.f_out.Close()
File.Close()

# Print out efficiencies
pass1 = nEntries-cut1
pass2 = pass1-cut2
pass3 = pass2-cut3

print("Efficiencies for each cut")
print("=====================================================")
print("Total events before cuts: %i"%(nEntries))
print("Pass 3 lepton cut: %i. Efficiency = %.2f%%"%(pass1,pass1/nEntries*100))
print("Pass opposite charge lepton cut: %i. Efficiency = %.2f%%"%(pass2,pass2/pass1*100))
print("Found Z candidate: %i. Efficiency = %.2f%%"%(pass3,pass3/pass2*100))
print("=====================================================")
print("Total Efficiency = %.2f%%"%(pass3/nEntries*100))
print("Wrote to file %s"%(out_file))
print("")




