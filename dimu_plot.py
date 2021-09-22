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
#vars_in = ["nMuon","Muon_pt","Muon_pdgId","Muon_eta","Muon_phi","Muon_mass"]#,"GenPart_pdgId","GenPart_eta","GenPart_pt","GenPart_phi","GenPart_mass"]
#vars_in = ["nMuon","GenPart_pdgId","GenPart_eta","GenPart_pt","GenPart_phi","GenPart_mass","genWeight"]
#sumW = {}
#weight = {}
#xs = {sets[0]:2037.0,sets[1]:18610.0,sets[2]:6077.22}
#counts = {sets[0]:[],sets[1]:[],sets[2]:[]}
#bins = {sets[0]:[],sets[1]:[],sets[2]:[]}
#
#for x in sets:
#	if x==sets[0]:
#		file_in = "/cmsuf/data/store/user/t2/users/nikmenendez/2017_MC_bkg/NanoAOD/"+x+".root"
#	else:
#		file_in = "/cmsuf/data/store/user/t2/users/nikmenendez/2017_MC_bkg/NanoAOD/DiMu/"+x+".root"
#	print("Getting diMu masses for %s"%(x))
#	file_root = uproot.open(file_in)
#	events = file_root["Events"]
#	runs = file_root["Runs"]
#
#	SumWeights = runs["genEventSumw"].array()
#	sumW[x] = (np.sum(SumWeights))
#	diMu_masses, genWeights = [],[]
#
#	data = events.arrays(vars_in,executor=executor)
#	nEntries = len(data["nMuon"])
#	
#	selection = data["nMuon"] >= 2
#
#	for ev in tqdm(range(nEntries)):
#		if not selection[ev]: continue
#		gen = np.unique(np.array([data["GenPart_pdgId"][ev],data["GenPart_pt"][ev],data["GenPart_eta"][ev],data["GenPart_phi"][ev],data["GenPart_mass"][ev]]),axis=1)
#		muons = {"id":[],"pt":[],"eta":[],"phi":[],"mass":[]}
#		for p in (range(len(gen[0]))):
#			if abs(gen[0][p])==13:
#				muons["id"].append(gen[0][p])
#				muons["pt"].append(gen[1][p])
#				muons["eta"].append(gen[2][p])
#				muons["phi"].append(gen[3][p])
#				muons["mass"].append(gen[4][p])
#
#		if len(muons["pt"]) < 2: continue
#		for i in range(len(muons["pt"])-1):
#			for j in range(i,len(muons["pt"])):
#				if muons["id"][i] + muons["id"][j] == 0:
#					mu1, mu2 = TLorentzVector(), TLorentzVector()
#					mu1.SetPtEtaPhiM(muons["pt"][i],muons["eta"][i],muons["phi"][i],muons["mass"][i])
#					mu2.SetPtEtaPhiM(muons["pt"][j],muons["eta"][j],muons["phi"][j],muons["mass"][j])
#					diMu_masses.append((mu1+mu2).M())
#					genWeights.append(data["genWeight"][ev])
#
#		#for i in range(data["nMuon"][ev]-1):
#		#	for j in range(i,data["nMuon"][ev]):
#		#		if data["Muon_pdgId"][ev][i] + data["Muon_pdgId"][ev][j] == 0:
#		#			mu1, mu2 = TLorentzVector(), TLorentzVector()
#		#			mu1.SetPtEtaPhiM(data["Muon_pt"][ev][i],data["Muon_eta"][ev][i],data["Muon_phi"][ev][i],data["Muon_mass"][ev][i])
#		#			mu2.SetPtEtaPhiM(data["Muon_pt"][ev][j],data["Muon_eta"][ev][j],data["Muon_phi"][ev][j],data["Muon_mass"][ev][j])
#		#			diMu_masses.append((mu1+mu2).M())
#
#		
#
#	counts[x], bins[x] = np.histogram(diMu_masses, bins=range(120), weights=genWeights)
#	weight[x] = xs[x]/sumW[x]
#	np.savez('Plots/arrays_%s.npz'%(x),counts=counts[x],bins=bins[x],weight=weight[x])

masses, counts, bins, weight, sumW = {}, {}, {}, {}, {}

sumW = {sets[0]: 24227000, sets[1]: 78994955, sets[2]: 3782668437151}
for x in sets:
	data = np.load('Plots/arrays_%s.npz'%(x))
	counts[x] = data['counts']
	bins[x] = data['bins']
	weight[x] = data['weight']

for x in sets:
	if x==sets[0]:
		s_weight = counts[x]*weight[x]
	else:
		s_weight += counts[x]*weight[x]
#k_factor = {sets[0]: s_weight[13]/s_weight[9], sets[1]: 1, sets[2]: s_weight[49]/s_weight[51]}
k_factor = {sets[0]: 2, sets[1]: 1, sets[2]: s_weight[49]/s_weight[51]}
for x in sets:
	weight[x] = weight[x]*k_factor[x]
	print("%s k factor = %.3f"%(x,k_factor[x]))

print("Plotting masses")
for x in sets:
	plt.hist(bins[x][:-1], bins[x], weights=counts[x]*weight[x], alpha=0.5, label=x)
plt.legend(loc='best')
plt.savefig("Plots/test_diMu_masses_gen.png")

plt.yscale('log', nonposy='clip')
plt.savefig("Plots/test_diMu_masses_gen_log.png")
#///////////////////////////////

plt.clf()
plt.hist([bins[sets[0]][:-1],bins[sets[1]][:-1],bins[sets[2]][:-1]], bins[sets[0]], weights=[counts[sets[0]]*weight[sets[0]],counts[sets[1]]*weight[sets[1]],counts[sets[2]]*weight[sets[2]]],stacked=True,density=True,label=[sets[0],sets[1],sets[2]])
plt.legend(loc='best')
plt.savefig("Plots/diMu_masses_gen_stacked.png")
plt.show()
plt.clf()
plt.hist([bins[sets[0]][:-1],bins[sets[1]][:-1],bins[sets[2]][:-1]], bins[sets[0]], weights=[counts[sets[0]]*weight[sets[0]],counts[sets[1]]*weight[sets[1]],counts[sets[2]]*weight[sets[2]]],stacked=True,density=True,label=[sets[0],sets[1],sets[2]])
plt.legend(loc='best')
plt.yscale('log', nonposy='clip')
plt.savefig("Plots/diMu_masses_gen_stacked_log.png")
plt.show()
