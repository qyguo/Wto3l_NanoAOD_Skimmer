from __future__ import division
import numpy as np
import uproot
import sys
from ROOT import TLorentzVector
from tqdm import tqdm
import concurrent.futures
import matplotlib.pyplot as plt

executor = concurrent.futures.ThreadPoolExecutor()

sets = ["DYJetsToLL_M1To10","DYJetsToLL_M10To50","DYJetsToLL_M50"]
vars_in = ["nMuon","Muon_pt","Muon_pdgId","Muon_eta","Muon_phi","Muon_mass"]#,"GenPart_pdgId","GenPart_eta","GenPart_pt","GenPart_phi","GenPart_mass"]
sumW = {}
weight = {}
xs = {sets[0]:2037.0,sets[1]:18610.0,sets[2]:6077.22}
counts = {sets[0]:[],sets[1]:[],sets[2]:[]}
bins = {sets[0]:[],sets[1]:[],sets[2]:[]}

for x in sets:
	file_in = "/cmsuf/data/store/user/t2/users/nikmenendez/2017_MC_bkg/NanoAOD/"+x+".root"
	print("Getting diMu masses for %s"%(x))
	file_root = uproot.open(file_in)
	events = file_root["Events"]
	runs = file_root["Runs"]

	SumWeights = runs["genEventSumw"].array()
	sumW[x] = (np.sum(SumWeights))
	diMu_masses = []

	data = events.arrays(vars_in,executor=executor)
	nEntries = len(data["nMuon"])
	
	selection = data["nMuon"] >= 3

	for ev in tqdm(range(nEntries)):
		if not selection[ev]: continue
		#gen = np.unique(np.array([data["GenPart_pdgId"][ev],data["GenPart_pt"][ev],data["GenPart_eta"][ev],data["GenPart_phi"][ev],data["GenPart_mass"][ev]]))
		#muons = {"id":[],"pt":[],"eta":[],"phi":[],"mass":[]}
		#for p in (range(len(gen[0]))):
		#	if abs(gen[0][i]==13):
		#		muons["id"].append(gen[0])
		#		muons["pt"].append(gen[1])
		#		muons["eta"].append(gen[2])
		#		muons["phi"].append(gen[3])
		#		muons["mass"].append(gen[4])

		for i in range(data["nMuon"][ev]-1):
			for j in range(i,data["nMuon"][ev]):
				if data["Muon_pdgId"][ev][i] + data["Muon_pdgId"][ev][j] == 0:
					mu1, mu2 = TLorentzVector(), TLorentzVector()
					mu1.SetPtEtaPhiM(data["Muon_pt"][ev][i],data["Muon_eta"][ev][i],data["Muon_phi"][ev][i],data["Muon_mass"][ev][i])
					mu2.SetPtEtaPhiM(data["Muon_pt"][ev][j],data["Muon_eta"][ev][j],data["Muon_phi"][ev][j],data["Muon_mass"][ev][j])
					diMu_masses.append((mu1+mu2).M())

	counts[x], bins[x] = np.histogram(diMu_masses, bins=range(100))
	weight[x] = xs[x]/sumW[x]

print("Plotting masses")
for x in sets:
	plt.hist(bins[x][:-1], bins[x], weights=counts[x]*weight[x], alpha=0.5, label=x)
plt.legend(loc='best')
plt.savefig("Plots/diMu_masses.png")

#///////////////////////////////
