import sys
from ROOT import TFile, TTree, TLorentzVector

File = TFile("/cmsuf/data/store/user/t2/users/nikmenendez/2017_MC_bkg/ZpX/WZTo3LNu.root","READ")
t = File.Get("Events")
nEntries = t.GetEntries()

for ev in (range(nEntries)):
	t.GetEntry(ev)

	for i in range(len(t.GenPart_pt)):
		if(abs(t.GenPart_pdgId[i])==13 and t.GenPart_status[i]==1):
			print(t.GenPart_pt[i])

