from __future__ import division
import numpy as np
import uproot
import matplotlib.pyplot as plt
from tqdm import tqdm
from ROOT import TLorentzVector
import os

inputPath =  "/cmsuf/data/store/user/t2/users/nikmenendez/signal/NanoAOD/"
masses = [1,4,5,15,30,60]
masses = [4]

triggers = ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8","HLT_TripleMu_12_10_5","HLT_TripleMu_10_5_5_DZ"]

for m in range(len(masses)):
	print("Plotting pT for Zp M = "+str(masses[m])+" GeV")
	file = uproot.open(inputPath+"Wto3l_M"+str(masses[m])+".root")
	#file = uproot.open("/cmsuf/data/store/user/t2/users/nikmenendez/2017_MC_bkg/ZpX/WZTo3LNu.root")
	events = file["Events"]
	
	gen_id = events["GenPart_pdgId"].array()
	gen_eta = events["GenPart_eta"].array()
	gen_pt = events["GenPart_pt"].array()
	gen_phi = events["GenPart_phi"].array()
	gen_mass = events["GenPart_mass"].array()
	gen_mom = events["GenPart_genPartIdxMother"].array()
	gen_stat = events["GenPart_status"].array()

	#genMet = events["GenMET_pt"].array()
	#genMet_phi = events["GenMET_phi"].array()

	t1 = events[triggers[0]].array()
	t2 = events[triggers[1]].array()
	t3 = events[triggers[2]].array()

	selection = (t1==1) | (t2==1) | (t3==1)

	m3l = []
	m3l_met = []
	W = {"mass":[],"pt":[],"eta":[],"phi":[],"status":[]}
	mu = {"mass":[],"pt":[],"eta":[],"phi":[],"status":[]}
	for ev in tqdm(range(len(gen_id))):
		#if not selection[ev]: continue
		muons={"id":np.array([]),"pt":np.array([]),"eta":np.array([]),"phi":np.array([]),"mass":np.array([]),"mom":np.array([])}
		#gen = np.unique(np.array([gen_id[ev],gen_eta[ev],gen_pt[ev],gen_phi[ev],gen_mass[ev],gen_mom[ev]]), axis=1)
		gen = np.array([gen_id[ev],gen_eta[ev],gen_pt[ev],gen_phi[ev],gen_mass[ev],gen_mom[ev],gen_stat[ev]])
		found = False
		for i in range(len(gen[0])):
			if (np.abs(gen[0][i])==13.0 and gen[6][i]==1):
				muons["pt"] = np.append(muons["pt"],gen[2][i])
				muons["eta"] = np.append(muons["eta"],gen[1][i])
				muons["phi"] = np.append(muons["phi"],gen[3][i])
				muons["mass"] = np.append(muons["mass"],gen[4][i])
				muons["id"] = np.append(muons["id"],gen[0][i])
				mom = gen_id[ev][(gen[5][i]).astype(int)]
				muons["mom"] = np.append(muons["mom"],mom)

				mu["mass"].append(gen[4][i])
				mu["eta"].append(gen[1][i])
				mu["pt"].append(gen[2][i])
				mu["phi"].append(gen[3][i])
				mu["status"].append(gen[6][i])
			if (np.abs(gen[0][i])==24.0) and (gen[6][i]<25) and not found:
				W["mass"].append(gen[4][i])
				W["eta"].append(gen[1][i])
				W["pt"].append(gen[2][i])
				W["phi"].append(gen[3][i])
				W["status"].append(gen[6][i])
				#found = True
		if len(muons["pt"])<3: continue

		order = muons["pt"].argsort()
		for key in muons:
			muons[key] = muons[key][order[::-1]]

		for m1 in range(len(muons["pt"])-2):
			for m2 in range(m1+1,len(muons["pt"])-1):
				for m3 in range(m2+1,len(muons["pt"])):
					#if abs(muons["id"][m1] + muons["id"][m2] + muons["id"][m3])!=13: continue

					#moms = np.array([(muons["mom"][m1]),(muons["mom"][m2]),(muons["mom"][m3])])
					#nW = np.count_nonzero(np.abs(moms)==24)
					#nZp = np.count_nonzero(np.abs(moms)==999888)
					#if nZp!=2 or nW!=1: continue

					np.set_printoptions(suppress=True)
					if muons["pt"][m1]<muons["pt"][m2]:
						print("")
						print(muons)

					#if (muons["pt"][m1]<5) or (muons["pt"][m2]<5) or (muons["pt"][m3]<5): continue
					#if (muons["eta"][m1]>2.5) or (muons["eta"][m2]>2.5) or (muons["eta"][m3]>2.5): continue

					mu1, mu2, mu3, met = TLorentzVector(), TLorentzVector(), TLorentzVector(), TLorentzVector()
					mu1.SetPtEtaPhiM(muons["pt"][m1],muons["eta"][m1],muons["phi"][m1],muons["mass"][m1])
					mu2.SetPtEtaPhiM(muons["pt"][m2],muons["eta"][m2],muons["phi"][m2],muons["mass"][m2])
					mu3.SetPtEtaPhiM(muons["pt"][m3],muons["eta"][m3],muons["phi"][m3],muons["mass"][m3])
				
					#met.SetPtEtaPhiM(genMet[ev],0,genMet_phi[ev],0)

					m3l.append((mu1+mu2+mu3).M())
					#m3l_met.append((mu1+mu2+mu3+met).Mt())

					break
				else: continue
				break
			else: continue
			break

	out_dir = "output/base/"
	if not os.path.exists(out_dir): os.mkdir(out_dir)
	# Plot 3mu
	plt.hist(m3l,bins=100,range=[0,100],color='blue',histtype='step',label='3mu Invariant Mass')

	plt.xlim(0,100)
	plt.ylim(bottom=0)
	plt.xlabel("3mu Invariant Mass (GeV)")
	plt.ylabel("Number of Entries (%i total)"%(len(m3l)))
	plt.title("Generator 3mu Invariant Mass Distributions for Wto3l_M"+str(masses[m]))
	plt.legend(loc='best')

	plt.savefig(out_dir+"3mu_M"+str(masses[m])+".png")
	#plt.show()
	plt.clf()

	# Plot 3mu fine
	plt.hist(m3l,bins=10000,range=[0,100],color='blue',histtype='step',label='3mu Invariant Mass')

	plt.xlim(0,100)
	plt.ylim(bottom=0)
	plt.xlabel("3mu Invariant Mass (GeV)")
	plt.ylabel("Number of Entries (%i total)"%(len(m3l)))
	plt.title("Generator 3mu Invariant Mass Distributions for Wto3l_M"+str(masses[m]))
	plt.legend(loc='best')
	
	plt.savefig(out_dir+"3mu_M"+str(masses[m])+"_fine.png")
	#plt.show()
	plt.clf()	

	# Plot 3mu+met
	#plt.hist(m3l_met,bins=200,range=[0,200],color='blue',histtype='step',label='3mu+MET Invariant Mass')

	#plt.xlim(0,200)
	#plt.ylim(bottom=0)
	#plt.xlabel("3mu+MET Transverse Mass (GeV)")
	#plt.ylabel("Number of Entries (%i total)"%(len(m3l)))
	#plt.title("Generator 3mu+MET Transverse Mass Distributions for Wto3l_M"+str(masses[m]))
	#plt.legend(loc='best')
	#
	#plt.savefig(out_dir+"3mu_M"+str(masses[m])+"_met.png")
	#plt.show()
	#plt.clf()

	# Plot gen W Mass
	print("Number of unique W masses = %i"%(len(set(W["mass"]))))
	plt.hist(W["mass"],bins=1000,range=[75,85],color='blue',histtype='step',label='Gen W Mass')
	
	plt.xlim(75,85)
	plt.ylim(bottom=0)
	plt.xlabel("Gen W Mass (GeV)")
	plt.ylabel("Number of Entries (%i total)"%(len(m3l)))
	plt.title("Generator W Mass Distributions for Wto3l_M"+str(masses[m]))
	plt.legend(loc='best')
	
	plt.savefig(out_dir+"massW_M"+str(masses[m])+".png")
	#plt.show()
	plt.clf()

	# Plot mu pTs

	for i in range(len(mu["pt"])):
		if mu["pt"][i] > 104 and mu["pt"][i] < 105: print(mu["pt"][i])

	plt.hist(mu["pt"],bins=1000,range=[104,105],color='blue',histtype='step',label='Muon pT')
	
	plt.xlim(104,105)
	plt.ylim(bottom=0)
	plt.xlabel("Gen Muon pT (GeV)")
	plt.ylabel("Number of Entries (%i total)"%(len(m3l)))
	plt.title("Generator Muon pT Distribution for Wto3l_M"+str(masses[m]))
	plt.legend(loc='best')
	
	plt.savefig(out_dir+"mupT_M"+str(masses[m])+".png")
	plt.show()
	plt.clf()

	print("For Generated ZpM%i:"%(masses[m]))
	print("****************************")
	print("Number of unique W masses: %i"%(len(set(W["mass"]))))
	print("Number of unique W pts: %i"%(len(set(W["pt"]))))
	print("Number of unique W etas: %i"%(len(set(W["eta"]))))
	print("Number of unique W phis: %i"%(len(set(W["phi"]))))
	print("****************************")
	print("Number of unique mu masses: %i"%(len(set(mu["mass"]))))
	print("Number of unique mu pts: %i"%(len(set(mu["pt"]))))
	print("Number of unique mu etas: %i"%(len(set(mu["eta"]))))
	print("Number of unique mu phis: %i"%(len(set(mu["phi"]))))
	print("****************************")
	print("Number of unique 3 muon invariant masses: %i"%(len(set(m3l))))
	#print("Number of unique 3 muon+MET invariant masses: %i"%(len(set(m3l_met))))
	print("")

	## Plot mu Status
	#plt.hist(mu["status"],bins=51,range=[0,50],color='blue',histtype='step',label='Muon pT')
	#
	#plt.xlim(0,50)
	#plt.ylim(bottom=0)
	#plt.xlabel("Gen Muon pT (GeV)")
	#plt.ylabel("Number of Entries (%i total)"%(len(m3l)))
	#plt.title("Generator Muon pT Distribution for Wto3l_M"+str(masses[m]))
	#plt.legend(loc='best')
	#
	##plt.savefig(out_dir+"mupT_M"+str(masses[m])+".png")
	#plt.show()
	#plt.clf()
	#
	#plt.hist(W["status"],bins=51,range=[0,50],color='blue',histtype='step',label='Muon pT')
	#
	#plt.xlim(0,50)
	#plt.ylim(bottom=0)
	#plt.xlabel("Gen Muon pT (GeV)")
	#plt.ylabel("Number of Entries (%i total)"%(len(m3l)))
	#plt.title("Generator Muon pT Distribution for Wto3l_M"+str(masses[m]))
	#plt.legend(loc='best')
	#
	##plt.savefig(out_dir+"mupT_M"+str(masses[m])+".png")
	#plt.show()
	#plt.clf()
