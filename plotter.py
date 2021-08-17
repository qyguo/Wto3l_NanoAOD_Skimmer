from __future__ import division
import numpy as np
import uproot
import matplotlib.pyplot as plt
from tqdm import tqdm

inputPath =  "/cmsuf/data/store/user/t2/users/nikmenendez/signal/NanoAOD/"
masses = [1,4,5,15,30,60]

m=5
lead_cut = 12
sublead_cut = 10
trail_cut = 5

for m in range(len(masses)):
	print("Plotting pT for Zp M = "+str(masses[m])+" GeV")
	file = uproot.open(inputPath+"Wto3l_M"+str(masses[m])+".root")
	events = file["Events"]
	
	gen_id = events["GenPart_pdgId"].array()
	gen_eta = events["GenPart_eta"].array()
	gen_pt = events["GenPart_pt"].array()
	
	leading    = np.array([]) #np.zeros(len(gen_id))
	subleading = np.array([]) #np.zeros(len(gen_id))
	trailing   = np.array([]) #np.zeros(len(gen_id))
	npassl, npasss, npasst, npass, inDet = 0,0,0,0,0
	for ev in tqdm(range(len(gen_id))):
		gen = np.unique(np.array([gen_id[ev],gen_eta[ev],gen_pt[ev]]), axis=1)
		pts = np.array([])
		for i in range(len(gen[0])):
			if np.abs(gen[0][i])==13.0 and np.abs(gen[1][i])<2.4:
				pts = np.append(pts,gen[2][i])
		if len(pts)<3: continue
		inDet+=1
		pts = np.sort(pts)
		pts = pts[::-1]
		if len(pts)>0: 
			leading    = np.append(leading,pts[0])
			if leading[-1] > lead_cut: npassl+=1
		if len(pts)>1: 
			subleading = np.append(subleading,pts[1])
			if subleading[-1] > sublead_cut: npasss+=1
		if len(pts)>2: 
			trailing   = np.append(trailing,pts[2])
			if trailing[-1] > trail_cut: npasst+=1
			if leading[-1]>lead_cut and subleading[-1]>sublead_cut and trailing[-1]>trail_cut: npass+=1

		#if leading[-1] > lead_cut: npassl+=1
		#if subleading[-1] > sublead_cut: npasss+=1
		#if trailing[-1] > trail_cut: npasst+=1

		#if leading[-1]>lead_cut and subleading[-1]>sublead_cut and trailing[-1]>trail_cut: npass+=1
	
	ppassl, ppasss, ppasst, ppass = npassl/inDet,npasss/inDet,npasst/inDet,npass/inDet
	
	plt.hist(leading,bins=200,range=[0,100],color='blue',histtype='step',label='Leading, %.2f%% pass'%(ppassl*100))
	plt.hist(subleading,bins=200,range=[0,100],color='orange',histtype='step',label='Subleading, %.2f%% pass'%(ppasss*100))
	plt.hist(trailing,bins=200,range=[0,100],color='green',histtype='step',label='Trailing, %.2f%% pass'%(ppasst*100))
	plt.plot([], [], '', label='Percent where all 3 pass: %.2f%%'%(ppass*100))

	plt.axvline(x=lead_cut,color='blue')
	plt.axvline(x=sublead_cut,color='orange')
	plt.axvline(x=trail_cut,color='green')
	
	plt.xlim(0,100)
	plt.ylim(bottom=0)
	plt.xlabel("Muon pT (GeV)")
	plt.ylabel("Number of Entries")
	plt.title("Generator Muon pT Distributions for Wto3l_M"+str(masses[m]))
	plt.legend(loc='best')

	plt.savefig("Plots/TriMu_12/pTs_M"+str(masses[m])+".png")
	plt.clf()
	#plt.show()
