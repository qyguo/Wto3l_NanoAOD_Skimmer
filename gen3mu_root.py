import sys
from ROOT import TFile, TTree, TLorentzVector
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

#File = TFile("/cmsuf/data/store/user/t2/users/nikmenendez/2017_MC_bkg/ZpX/WZTo3LNu.root","READ")
File = TFile("/cmsuf/data/store/user/t2/users/nikmenendez/signal/NanoAOD/Wto3l_M5.root","READ")
t = File.Get("Events")
nEntries = t.GetEntries()

pTs, in10, uniques = [], [], []
for ev in tqdm(range(nEntries)):
	t.GetEntry(ev)

	#for i in range(len(t.GenPart_pt)):
	#	if(abs(t.GenPart_pdgId[i])==13 and t.GenPart_status[i]==1):
	#		pTs.append(t.GenPart_pt[i])
	#		if t.GenPart_pt[i] >=10 and t.GenPart_pt[i] <= 11:
	#			in10.append(t.GenPart_pt[i])
	#			if t.GenPart_pt[i] not in uniques:
	#				uniques.append(t.GenPart_pt[i])

	for i in range(len(t.Muon_pt)):
		pTs.append(t.Muon_pt[i])
		if t.Muon_pt[i] >= 10 and t.Muon_pt[i] <= 11:
			in10.append(t.Muon_pt[i])
			if t.Muon_pt[i] not in uniques:
				uniques.append(t.Muon_pt[i])

print(in10)
print("Number of unique entries between 10 and 11: %i"%(len(uniques)))

plt.hist(pTs,bins=200,range=(10,11))
plt.xlim(10,11)
plt.xlabel('Gen Muon pT (GeV)')
plt.ylabel('Count')
plt.show()
plt.clf()
