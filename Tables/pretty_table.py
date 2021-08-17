from prettytable import from_csv
with open("Tables/cut_list.txt") as fp:
	cuttable = from_csv(fp)
with open("Tables/GoodMu_list.txt") as fp:
	mutable = from_csv(fp)
with open("Tables/ZpCandidate_list.txt") as fp:
	zptable = from_csv(fp)

print("Efficiencies of Cuts")
print(cuttable)
print("")
print("Bad Muons cut due to:")
print(mutable)
print("")
print("No Z' Candidate because of:")
print(zptable)

