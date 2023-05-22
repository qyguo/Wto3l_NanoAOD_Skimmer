

in_file = "/cmsuf/data/store/user/t2/users/nikmenendez/skimmed/NanoAOD/2017/background/Zpeak/UL/sumW/"

sumW = 0.0
for i in range(10):
	print("Reading %s/DYJetsToLL_M50_%i.txt"%(in_file,i))
	file = open("%s/DYJetsToLL_M50_%i.txt"%(in_file,i),"r")
	sumW += float(file.read())
file.close()

print("Writing to %s/DYJetsToLL_M50.txt"%(in_file))
file_out = open("%s/DYJetsToLL_M50.txt"%(in_file),"w")
file_out.write(str(sumW))
file_out.close()
