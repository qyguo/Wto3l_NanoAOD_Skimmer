import sys
from ROOT import TFile, TTree
from array import array

# Define branches of output tree

Run			= array('L', [0])
Event		= array('L', [0])
LumiSect	= array('L', [0])
nLep		= array('i', [0])
nMuons		= array('i', [0])
nElectrons	= array('i', [0])
nbJets		= array('i', [0])
pTL1		= array('f', [0.])
pTL2		= array('f', [0.])
pTL3		= array('f', [0.])
idL1		= array('f', [0.])
idL2		= array('f', [0.])
idL3		= array('f', [0.])
etaL1		= array('f', [0.])
etaL2		= array('f', [0.])
etaL3		= array('f', [0.])
phiL1		= array('f', [0.])
phiL2		= array('f', [0.])
phiL3		= array('f', [0.])
IsoL1		= array('f', [0.])
IsoL2		= array('f', [0.])
IsoL3		= array('f', [0.])
Iso_chgL1	= array('f', [0.])
Iso_chgL2	= array('f', [0.])
Iso_chgL3	= array('f', [0.])
Iso_MiniL1  = array('f', [0.])
Iso_MiniL2  = array('f', [0.])
Iso_MiniL3  = array('f', [0.])
Iso_MinichgL1   = array('f', [0.])
Iso_MinichgL2   = array('f', [0.])
Iso_MinichgL3   = array('f', [0.])
ip3dL1		= array('f', [0.])
ip3dL2		= array('f', [0.])
ip3dL3		= array('f', [0.])
sip3dL1		= array('f', [0.])
sip3dL2		= array('f', [0.])
sip3dL3		= array('f', [0.])
tightIdL1	= array('f', [0.])
tightIdL2	= array('f', [0.])
tightIdL3	= array('f', [0.])
medIdL1   	= array('f', [0.])
medIdL2   	= array('f', [0.])
medIdL3   	= array('f', [0.])
massL1		= array('f', [0.])
massL2		= array('f', [0.])
massL3		= array('f', [0.])
maxdxy		= array('f', [0.])
maxdz		= array('f', [0.])
dR12		= array('f', [0.])
dR13		= array('f', [0.])
dR23		= array('f', [0.])
trueL3		= array('b', [False])
m3l			= array('f', [0.])
mt			= array('f', [0.])
met			= array('f', [0.])
met_phi		= array('f', [0.])
genWeight	= array('f', [0.])
passedDiMu1 = array('i', [0])
passedDiMu2 = array('i', [0])
passedTriMu = array('i', [0])

dataset = str(sys.argv[1])
sort_by = str(sys.argv[2])
isSignal = 0
isMC = 1
if "To3l_M" in sys.argv[1] or "to3l_M" in sys.argv[1]:
    isSignal = 1
if "Muon" in sys.argv[1]:
	isMC = 0

if isSignal==1:
	out_file = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/signal/signal_sel/"+sort_by+"/"+dataset+".root"
elif isMC==1:
	out_file = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/background/signal_sel/"+sort_by+"/"+dataset+".root"
else:
	out_file = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/data/signal_sel/"+sort_by+"/"+dataset+".root"
f_out = TFile(out_file,'RECREATE')
out_tree = TTree("passedEvents","Events that passed skimmer")

out_tree.Branch("Run",Run,"Run/L");
out_tree.Branch("Event",Event,"Event/L");
out_tree.Branch("LumiSect",LumiSect,"LumiSect/L");
out_tree.Branch("nLeptons",nLep,"nLeptons/I");
out_tree.Branch("nMuons",nMuons,"nMuons/I");
out_tree.Branch("nElectrons",nElectrons,"nElectrons/I");
out_tree.Branch("nbJets",nbJets,"nbJets/I");
out_tree.Branch("pTL1",pTL1,"pTL1/F");
out_tree.Branch("pTL2",pTL2,"pTL2/F");
out_tree.Branch("pTL3",pTL3,"pTL3/F");
out_tree.Branch("idL1",idL1,"idL1/F");
out_tree.Branch("idL2",idL2,"idL2/F");
out_tree.Branch("idL3",idL3,"idL3/F");
out_tree.Branch("etaL1",etaL1,"etaL1/F");
out_tree.Branch("etaL2",etaL2,"etaL2/F");
out_tree.Branch("etaL3",etaL3,"etaL3/F");
out_tree.Branch("phiL1",phiL1,"phiL1/F");
out_tree.Branch("phiL2",phiL2,"phiL2/F");
out_tree.Branch("phiL3",phiL3,"phiL3/F");
out_tree.Branch("IsoL1",IsoL1,"IsoL1/F");
out_tree.Branch("IsoL2",IsoL2,"IsoL2/F");
out_tree.Branch("IsoL3",IsoL3,"IsoL3/F");
out_tree.Branch("Iso_chgL1",Iso_chgL1,"Iso_chgL1/F");
out_tree.Branch("Iso_chgL2",Iso_chgL2,"Iso_chgL2/F");
out_tree.Branch("Iso_chgL3",Iso_chgL3,"Iso_chgL3/F");
out_tree.Branch("Iso_MiniL1",Iso_MiniL1,"Iso_MiniL1/F");
out_tree.Branch("Iso_MiniL2",Iso_MiniL2,"Iso_MiniL2/F");
out_tree.Branch("Iso_MiniL3",Iso_MiniL3,"Iso_MiniL3/F");
out_tree.Branch("Iso_MinichgL1",Iso_MinichgL1,"Iso_MinichgL1/F");
out_tree.Branch("Iso_MinichgL2",Iso_MinichgL2,"Iso_MinichgL2/F");
out_tree.Branch("Iso_MinichgL3",Iso_MinichgL3,"Iso_MinichgL3/F");
out_tree.Branch("ip3dL1",ip3dL1,"ip3dL1/F");
out_tree.Branch("ip3dL2",ip3dL2,"ip3dL2/F");
out_tree.Branch("ip3dL3",ip3dL3,"ip3dL3/F");
out_tree.Branch("sip3dL1",sip3dL1,"sip3dL1/F");
out_tree.Branch("sip3dL2",sip3dL2,"sip3dL2/F");
out_tree.Branch("sip3dL3",sip3dL3,"sip3dL3/F");
out_tree.Branch("tightIdL1",tightIdL1,"tightIdL1/F");
out_tree.Branch("tightIdL2",tightIdL2,"tightIdL2/F");
out_tree.Branch("tightIdL3",tightIdL3,"tightIdL3/F");
out_tree.Branch("medIdL1",medIdL1,"medIdL1/F");
out_tree.Branch("medIdL2",medIdL2,"medIdL2/F");
out_tree.Branch("medIdL3",medIdL3,"medIdL3/F");
out_tree.Branch("massL1",massL1,"massL1/F");
out_tree.Branch("massL2",massL2,"massL2/F");
out_tree.Branch("massL3",massL3,"massL3/F");
out_tree.Branch("maxdxy",maxdxy,"maxdxy/F");
out_tree.Branch("maxdz",maxdz,"maxdz/F");
out_tree.Branch("dR12",dR12,"dR12/F");
out_tree.Branch("dR13",dR13,"dR13/F");
out_tree.Branch("dR23",dR23,"dR23/F");
out_tree.Branch("trueL3",trueL3,"trueL3/O");
out_tree.Branch("m3l",m3l,"m3l/F");
out_tree.Branch("mt",mt,"mt/F");
out_tree.Branch("met",met,"met/F");
out_tree.Branch("met_phi",met_phi,"met_phi/F");
out_tree.Branch("genWeight",genWeight,"genWeight/F");
out_tree.Branch("passedDiMu1",passedDiMu1,"passedDiMu1/I");
out_tree.Branch("passedDiMu2",passedDiMu2,"passedDiMu2/I");
out_tree.Branch("passedTriMu",passedTriMu,"passedTriMu/I");
