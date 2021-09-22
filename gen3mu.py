from __future__ import division
import numpy as np
import uproot
import matplotlib.pyplot as plt
from tqdm import tqdm
from ROOT import TLorentzVector

inputPath =  "/cmsuf/data/store/user/t2/users/nikmenendez/signal/NanoAOD/"
masses = [1,4,5,15,30,60]
masses = [4]

for m in range(len(masses)):
	print("Plotting pT for Zp M = "+str(masses[m])+" GeV")
	file = uproot.open(inputPath+"Wto3l_M"+str(masses[m])+".root")
	events = file["Events"]
	
	gen_id = events["GenPart_pdgId"].array()
	gen_eta = events["GenPart_eta"].array()
	gen_pt = events["GenPart_pt"].array()
	gen_phi = events["GenPart_phi"].array()
	gen_mass = events["GenPart_mass"].array()

	genMet = events["GenMET_pt"].array()
	genMet_phi = events["GenMET_phi"].array()

	m3l = []
	m3l_met = []
	for ev in tqdm(range(len(gen_id))):
		muons={"id":np.array([]),"pt":np.array([]),"eta":np.array([]),"phi":np.array([]),"mass":np.array([])}
		gen = np.unique(np.array([gen_id[ev],gen_eta[ev],gen_pt[ev],gen_phi[ev],gen_mass[ev]]), axis=1)
		for i in range(len(gen[0])):
			if (np.abs(gen[0][i])==13.0):
				muons["pt"] = np.append(muons["pt"],gen[2][i])
				muons["eta"] = np.append(muons["eta"],gen[1][i])
				muons["phi"] = np.append(muons["phi"],gen[3][i])
				muons["mass"] = np.append(muons["mass"],gen[4][i])
				muons["id"] = np.append(muons["id"],gen[0][i])
		if len(muons["pt"])<3: continue

		for m1 in range(len(muons["pt"])-2):
			for m2 in range(m1+1,len(muons["pt"])-1):
				for m3 in range(m2+1,len(muons["pt"])):
					if abs(muons["id"][m1] + muons["id"][m2] + muons["id"][m3])!=13: continue
			
					if (muons["pt"][m1]<5) or (muons["pt"][m2]<5) or (muons["pt"][m3]<5): continue

					mu1, mu2, mu3, met = TLorentzVector(), TLorentzVector(), TLorentzVector(), TLorentzVector()
					mu1.SetPtEtaPhiM(muons["pt"][0],muons["eta"][0],muons["phi"][0],muons["mass"][0])
					mu2.SetPtEtaPhiM(muons["pt"][1],muons["eta"][1],muons["phi"][1],muons["mass"][1])
					mu3.SetPtEtaPhiM(muons["pt"][2],muons["eta"][2],muons["phi"][2],muons["mass"][2])
				
					met.SetPtEtaPhiM(genMet[ev],0,genMet_phi[ev],0)

					m3l.append((mu1+mu2+mu3).M())
					m3l_met.append((mu1+mu2+mu3+met).Mt())

					break
				else: continue
				break
			else: continue
			break
	
	# Plot 3mu
	plt.hist(m3l,bins=100,range=[0,100],color='blue',histtype='step',label='3mu Invariant Mass')

	plt.xlim(0,100)
	plt.ylim(bottom=0)
	plt.xlabel("3mu Invariant Mass (GeV)")
	plt.ylabel("Number of Entries (%i total)"%(len(m3l)))
	plt.title("Generator 3mu Invariant Mass Distributions for Wto3l_M"+str(masses[m]))
	plt.legend(loc='best')

	plt.savefig("Plots/3mu_M"+str(masses[m])+".png")
	plt.show()
	plt.clf()

	# Plot 3mu fine
	plt.hist(m3l,bins=10000,range=[0,100],color='blue',histtype='step',label='3mu Invariant Mass')

	plt.xlim(0,100)
	plt.ylim(bottom=0)
	plt.xlabel("3mu Invariant Mass (GeV)")
	plt.ylabel("Number of Entries (%i total)"%(len(m3l)))
	plt.title("Generator 3mu Invariant Mass Distributions for Wto3l_M"+str(masses[m]))
	plt.legend(loc='best')
	
	plt.savefig("Plots/3mu_M"+str(masses[m])+"_fine.png")
	plt.show()
	plt.clf()	

	# Plot 3mu+met
	plt.hist(m3l_met,bins=200,range=[0,200],color='blue',histtype='step',label='3mu+MET Invariant Mass')

	plt.xlim(0,200)
	plt.ylim(bottom=0)
	plt.xlabel("3mu+MET Transverse Mass (GeV)")
	plt.ylabel("Number of Entries (%i total)"%(len(m3l)))
	plt.title("Generator 3mu+MET Transverse Mass Distributions for Wto3l_M"+str(masses[m]))
	plt.legend(loc='best')
	
	plt.savefig("Plots/3mu_M"+str(masses[m])+"_met.png")
	plt.show()
	plt.clf()

