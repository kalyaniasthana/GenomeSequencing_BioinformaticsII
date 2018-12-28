
from __future__ import division
from collections import Counter


def reverseComplement(string):
	myStr = []
	for i in range(0, len(string)):
		if string[i] == 'A':
			myStr.append('T')
		elif string[i] == 'T':
			myStr.append('A')
		elif string[i] == 'G':
			myStr.append('C')
		elif string[i] == 'C':
			myStr.append('G')

	myStr = myStr[::-1]
	myStr = "".join(myStr)
	return myStr

def CodonDictionary():
	file = '../Downloads/RNA_codon_table_1.txt'
	d = {}
	with open(file) as f:
		for line in f:
			line = line.strip('\n')
			l = line.split(' ')
			if l[0] not in d:
				d[l[0]] = l[1]

	return d

def IntergerMassDictionary():
	file = '../Downloads/integer_mass_table.txt'
	d ={}
	with open(file) as f:
		for line in f:
			line = line.strip('\n')
			l = line.split(' ')
			if l[0] not in d:
				d[l[0]] = l[1]

	return d


def ProteinTranslation(rna):
	pattern = []
	d = CodonDictionary()
	rnaCodons = [rna[i:i+3] for i in range(0, len(rna), 3)]
	for codon in rnaCodons:
		pattern.append(d[codon])
	pattern = ''.join(pattern)
	return pattern

def SubstringEncodingAminoAcid(rna, aminoAcid):
	substrings = []
	substringLen = len(aminoAcid)*3
	for i in range(0, len(rna) - substringLen + 1):
		substrings.append(rna[i:i+substringLen])
	encoders = []
	for sub in substrings:
		reverse = reverseComplement(sub)
		reverseTranslated = reverse.replace('T','U')
		translated = sub.replace('T','U')
		if ProteinTranslation(translated) == aminoAcid or ProteinTranslation(reverseTranslated) == aminoAcid:
			encoders.append(sub)
	return encoders


def NumberOfSubpeptides(n):
	return n*(n-1)

def SubpeptidesLinear(n):
	return n*(n+1)/2 + 1

def LinearSpectrum(peptide):
	integer_mass_dict = IntergerMassDictionary()
	peptide = list(peptide)
	PrefixMass = [0 for i in range(len(peptide) + 1)]
	for i in range(1, len(peptide) + 1):
		PrefixMass[i] = PrefixMass[i - 1] + int(integer_mass_dict[peptide[i - 1]])

	LinearSpectrum = []
	LinearSpectrum.append(0)

	for i in range(0, len(PrefixMass) - 1):
		for j in range(i + 1, len(PrefixMass)):
			LinearSpectrum.append(PrefixMass[j] - PrefixMass[i])

	LinearSpectrum.sort()

	return LinearSpectrum

def CircularSpectrum(peptide):
	integer_mass_dict = IntergerMassDictionary()
	peptide = list(peptide)
	PrefixMass = [0 for i in range(len(peptide) + 1)]
	for i in range(1, len(peptide) + 1):
		PrefixMass[i] = PrefixMass[i - 1] + int(integer_mass_dict[peptide[i - 1]])

	peptideMass = PrefixMass[len(PrefixMass) - 1]

	CyclicSpectrum = []
	CyclicSpectrum.append(0)

	for i in range(0, len(PrefixMass) - 1):
		for j in range(i + 1, len(PrefixMass)):
			CyclicSpectrum.append(PrefixMass[j] - PrefixMass[i])
			if i > 0 and j < len(PrefixMass) - 1:
				CyclicSpectrum.append(peptideMass - PrefixMass[j] + PrefixMass[i])

	CyclicSpectrum.sort()

	return CyclicSpectrum

def Expand(peptide):
	p = ['G', 'A', 'S', 'P', 'V', 'T', 'C', 'I', 'L', 'N', 'D', 'K', 'Q', 'E', 'M', 'H', 'F', 'R', 'Y', 'W']
	q = []
	if len(peptide) == 0:
		return p
	else:
		for pep in p:
			for pep_ in peptide:
				q.append(pep + pep_)
		return q

def PeptideMass(peptide):
	d = IntergerMassDictionary()
	peptide = list(peptide)
	mass = 0
	for pep in peptide:
		mass += int(d[pep])

	return mass

def PeptideMassString(peptide):
	d = IntergerMassDictionary()
	peptide = list(peptide)
	mass = []
	for pep in peptide:
		mass.append(d[pep])

	mass = '-'.join(mass)
	return mass

def CyclopeptideSequencing(spectrum):
	peptides = ['']
	result = []
	d = IntergerMassDictionary()
	while len(peptides) != 0:
		peptides = Expand(peptides)
		for peptide in peptides[:]:
			if PeptideMass(peptide) == spectrum[len(spectrum) - 1]:
				if Counter(CircularSpectrum(peptide)) == Counter(spectrum):
					m = PeptideMassString(peptide)
					if m not in result:
						result.append(m)
				peptides.remove(peptide)

			else:
				l = LinearSpectrum(peptide)
				for mass in l:
					if mass not in spectrum:
						peptides.remove(peptide)
						break
	result = ' '.join(result)
	return result



#n = 24460
#print NumberOfSubpeptides(n)

#rna = 'GTTACCGTAGCCTCGTTCGGTCTTTATGATTAACAAAAACTTCGTGACCCGAGGGGCCGTCCACGCTCGTGTATTTTCGTGTACTGTCACCCCCACGGCAACATTGTTGAGATTAAAATACGGAGCATCTGAGCACGGGTAGTGAGATCTATTAGCAATCGATAGTATCTCGCGCGAAGGTTGCGATTTCTCTTTAGCCGAAGTCGCCTACGTTCCGGTTGAACTAGATGTGAAGCCAGGGTGGACCAGGTTCATACAGGGGAGGCGAGATAAATCGAAAAATTAGTCCCCAAGAGCGAGTACACCAAGTTCCTGAGTATCCAAGAACTGACCGCTCGATTCACCGAACACGAATGCTAACTTTTTATGGCGTCATTTCCGGGGGTGATTTCTACACATGGTAAACCTTCACACCATAGATGAGTCGAGTACGTCAACGTTTGGTGCGCGCGTGACGCACAGACGGTTCGGAATAAACTCAATGCCAGTCCCTATGGAAGGGTAACAACTCGTGAGGGCAGGAGATATCTGGTTCTCATAAAATATTACGGCCTCGATACGTAATCAGGCGAGTGATCTCGGGTGTGGTCACCGCATAATAGCAGTTCTGCATTATCCGCGAATTTTTCGGTTGATAGTGCTGGGTACGAAATGACCTGGCAGAATCGTAACTCACCGCTGTGGAAGGACTGGAACCCTGCACTATGGGATAGCCGCGGAGCCCTAGCTCGTTTGTCCAACCAGGTCATACAGCAGTCATCTGCCCTTCCGTATTCATAAGGCCTCTAGCGCATGGCGCTAGCGCAGCTTACCGGACTTTAGGCATAAACAATCGAAAGAACTTAGTTTCGTTACGACGATCCGCGATCGTACGGGATTTTGTCATAGATGGTAGGAAGTCCCGCACTCATGGCAGTTAATGATCGACCGATCGTCGTGGACGGACGGCACGGCTGGTCTGCCTTGATCGGATCAACTCTATGCCCGTTCCAATGCGGTTTCGAGCCAACCGAACAGTGAGGGAACTTGGCCGTGCAACCGTCAGTGATGGATCCAGCAAGCATAATCACCCTTGTGAGCTGGAAGCCAGTTCGGGCCTCGCTGGAAGGTCATACTCCGGCCCAGGTACAATTTGGCTCGATTCACTACGGTACTCGTTCGTGAGCTCTAGACCTAAGAACTCAGCTGATCTCCACGTCCTCCATACCGCGAAGCGCGTGATAGGCCTGAGAAGCAGTAGCGCCACTCTTAAGTGTGCGTAAATTGCTATTGGCACCCGTCAGCGAATAAGGTAATATGTCGGACCCTGAAACGGAGCTTTAACGACTTCTGGTCGATGTTGGTTGTGAAACTCTATTTTTTCTTGGTTCAGCTGAAACCAAACCTAGCCGGGTACCGTCAGGCGGCACTTGACTACTTGTACGCGATACCTTGGGGTCAGGTTACAGCAGTGTAAGGACCCCGCGAAGTGCAGGTGGAGGAGCCCAAGTTACCGCTCGCGACCATAAGATGGGCGTAGCGAACCCATCTATGATAGCTCCCGCGATTTCAATTTGTGCTCTTTATGAGCCTTACCCAGTCCACCGCAGGGGCTTACCGAGTTCTCGCAGATAGGCAAAATAATTGGGGGGCAATTAATTTTACGATAAATACATGCCTTCGCGGAGTCTGTGGGATCGCAGCAATGCTCACTACACCAGTCTTGCCTGCCTGGGCGAGAATGCGTGGGTGACGATATATTGAGCACCACACTATCGAGCATCGCCGCGATTTTGCCGTGTGGCGGACTGCTCCGAGATCGGGACCGGAAAAGTGGTTGTCCTCTAGATGTCGCACCTACGAGCGCCGCATTGGCACCGGCATACTGTTAATAGTGCATTATGGAAGAATAAGCAGCTATACTCCAGACTTGTGCACTTCCTATAGGGAGTATTTATGGCCGGACCGTAACCCATAGGGACCGGCATACTATTGATATCTCAACTAAACTTGCCACCTAAACCCCCACAAGGCTACATTAAAAACATGGGGCCACAGATGTATTGCATTATGTTTGCAGCAGTAACAGTGGGCGTTCTGGCGCAGTCCAGGTAACTAATGATAGTCATTAGCGGATAGTCACACAGCATATACCTCGACTGCTAAAGGTTACCCTACCGTTGTTTTAAATATCGGACCGGAACCTGCTGTGGTAAAACGCCCAATTACAGCTTAAGTCAATAGGGCATTAATAGTATGCCCGTACCAATGGCGCAACGGTGGGCGTGTGCGGTTAGCAAGGTATCGTTGCAGCTTCTTCAGATCTGATTGGAGTGTCGTCCCCAAAAAATTCATCCGTTTGGGCGATGACAACGGTCCAACAAAGCTTCTCGCGTCCGTAAGAGATTGGATTCAACTCGAGGAACTTTTGACCTAAGATGACCGCACCCAGTACCAATAAAGTGGATCAGTCCTAGTTACTACGGATAAGTGGGGACCACCCAATCAGTACGGACACTTCGACAAGTATAAGAGCACATGCCATGTTACCGATGTGATCCTATAGCGGGCTTAACCCTGTGGCGCCTACTATAAGCGGCATTCTCCGAGGTGCCATGATTTGGATTACCGGCGGTGCGCGGATCTTGGCCAACGGCAGCACGCAAAATACACCTTCCCGTGAAATGCAGGGATACTCATATACGGAGAACACGCATCCCGCACGATATATCTCGGTAGAAAGCAATGGGGCTGGGCAGTAAGCCCGATATTTATCGCACCTCCCCAAGGCAAGTCTAGTCATTCAAATCATACCGCCGTTTACTCTCCACACGCTGTACGGTTTATACCATGATGGTCGGTATGATACAGGGTCGCCTTCTGCTATTACGAACAGCGCGTAGTAATTTTGGAAGATAAATGCGCACAAATGAGATTTCTTGAGCTGGAACCTGGTCCCAAGGTCAGTGCCCCACTGGTGATCATGTATTAGTGAGGAGCCTATTTTCGCACGAGTCACAAGTGGTGACCTAGTGGTCCCTCGCGTTGTTACGCTGGTATCTCAGAGGAAATCCCTCACATTGCTACCGGGGGTGTGCTGCTCTGGCCCCGTGAGTGGCATCAATTCCATGCCCGTACCAATGTTTCGCACCGATCTCATGGGGACTGGCATAGAATTAATTTTCGGCTTTGGGCATTAGAAGCCGATGCAGACATTAACTAAAAAGACGATCCAGCAAGAGTTGGGTTGATACAGATACTAATTCCATAAGAGAAGACGTATCCCCCTTTCGCCAGCGTCTGCAAACTAATAGTCATCACTTGGACCAGTGAGTAGCCCAGGTAGTATTTTACGAGAGTTCGGGGAAAGGTCCTTCTGACACGTCCAGACTCAGTTTTCGCATAAGGTTCAAATCTATGGGTTTCCCTGACTGCTAGGGCCAGGGGTGACTCACGCGTCTTTCCTGATCCTCAGCCCTTTACCCTTCCAGACTACTGAATGACATCGGTACTGGCATTGAGTTAATAGGCGGGTCATACGTATGAGCTCCTTCCCTGGATAGCTATGATCTCTGACGGTCCGACAGGTAGAAGTGATGGGGGGCCCTGCCGCTTCGATGAAGCCAGTAGCTCGGCGGAAGACAATCACCCGTAAGTTGTCTTCCCTGATCGCGGTTCTGTCACCCCGGCCACTGCGGCTAGACGCAATGAGAAACCGCTCTGTCCCAGTTCGATAGCAATAAACAAATACGAACAGCGCACCGGGATTATGGCCCGCGCGCCTTCGGCACCTATAACATCGAGTGAATGCATGGACTACAGGCCTGGGCACCCTATTTGAGACCATCGACGTTTAAGTGAGAGGTGCCAAATTCATCCGGAGCGTGGCTTCCCGGAACTAACCCACAGTCGGCTAATTGAAATGAGATCGTCGACCTGTCTATGACTTAGACATGGCCCTCCAAGGGCCCCGATCTCCATCGCACACCACCTCGAAATTTGTTGGAATTAATTCTATGCCAGTTCCCATGTTTACCGCTTGTGTCCAGCTGATGCCGACTCCCCGTGGTCCAGTGTAATCTATGTGCCCACGAGACCTATAAGTGTCCTTGTACACTAATCCGAGTGCGATTATCGACACACAGCAGGCGGGAGGGGCTGGAAAGCATCTCCTTTCGGTCATTTAGTGAGTATCGTCGTTCATACTGGCTTCCGGTCCATGGTCCTCGCTATGCGAGGGCCTTCAACTATTCAGGTAACCCTATCGCCGCAGAGAAAGTGCAATGCGAACCAAACGATTGAACTATCTAACCTAGGCGGTGAGAACCGCCAGGGTTCATGGCGGATCAGCTAGTTCACCAACTCGCTTGACTCATTAGTCGGCTGCGGACTGTCTAGTACACCCGAAACCGCCATTGGTACAGGCATGGAGTTAATTGTGAGGAAGTCCGAATTAGAAGCGTATGTTGCGCCTGCATATGTCACCACTCCAAACTGTTTTGTTCAGTAACGGTTATGTTACTTGCCAGTACGCTGCGCGGTGACTTTAAACGGATCCTGCGTCAAGGGTTAGGAGTACTTCTGTACGATAACCCATAAACAGATTAGTGGAAGCATCCTGTTTAAGATTCCGCGGTGTTCGAACCGCCCGATGCGTCGAGGGTTCAGGTACACGCCAATAGCCCCATGGGCCATATGCTCGAAACTATTTCGTGTGTTGGTGTGCCAGTGATAACGTTATACAGCCAGTGTCTAAAGACCACGTTTCATTCCCCCGGCGGCCTCTGCGTTGCGAGCCCATAGGATCCTAGTTGCGCGACTCGTAGCCCAAGCGCGTGCTACTCGCTATGACTCCGTGATTCAATTTAATGCCATAGGAGACTGCAGGCACATCCTCGCTGAATCTGATCTCCGACCTGAAGGACGATTCTATGCTCACCTTGTCGTCTATAAGTTGGTGCATTAGTCTAACCGTCGCTAAATCGCTGCGGGACGCTTCCTCTCGCATAGGCACGCGCTCACTCTGTAACCATGGTATTTGATGCTCTAGCGTACATCAATAGCATGCCGGTGCCCATGGAAATGCATACGTCGAGCCGCATCGGGGTACGGAGCCTACACGTTGCTGCGCCCCGCGTCGTATTTACCACTGGCCCGAGTCGAAGGATTGTTTTAGCTGCGACAAGGATGGTCAGGTGGACATTGGCACGGGCATGGAGTTAATTTCCCTCTCACTTTTCACACGAAGTGGACAGCCAACGGGTTCATTGGGACCGGCATGCTGTTAATCGTTGCTTCATGGTTCTGATCATGACCCTTTCGGCTCTAGCCTACAGTCAAAGGCATGTGGTGCGTCACTCAGATTCACATTAGGATTGTTTTTTAAGCAGGATTCTAGTCTCGATTTTTGAGCAGCATTTAGTGTTCTGTGGCTTGCGGGCCAAGAATAGTTAAACTAGTAACAATGGGCAGGTGGAGGGAAGCGTATCTATCGTAGGGAATGTCGTATCCGAGTTGTACCTATCTGAGCCTCTCTCCCAATCCTAACGGCTGGTAACAAACCGCCAACAAGCGGTCTCAGTTTCTATGACTTCTTCAGCCCTGCAGTGTCTAAATTCTTCGGCTTGGTCATGCCAGCCTCTCCTGTGCGCGGTCAAAGCTCCTTACCCGAATATCGCAGACCGGTGTCCTACAGAGTTCAGGATAGTGTGTTACTGATTATCAGATAGGCGGCACCACTGACCGCAGGCTACGACGCGATAAGAAGAAGATGGCGGGGCCCTGCATATCGGCCCTGGCATGATTATCTGATACCCGTAGGTTCCTTCTAGCGTAGGTAAATTACTTCATACACGACCCTGTTTTTAGCACCACCCGCTTGATTGCGGGCGATCAATTCAATGCCGGTCCCTATGAGTTAATGTTTTATGTTCCCCATGTAGGGCAGGGATGTGCAATCACTGGCATAAGAGCAATGTCTTTCCCATAATCTCATATCCCTAACTACAGACTGCAAACATTAAGGGACAATTACCCTTATAAGACAGGTGATCTGATCGATCCGGCTTCAGATATGGTATGATGGTCTGCGTATTATTGCTGCCAACCCGCCAAATACAGTTCTCCCTCACGGGGACGGCGGGTTTGGGATAATGATTGAGTCACAGAAGTATTCGCTTTGCCTGCTTAAAACACCCGAGTTCGACACTGCTACTTTGACAACTCTGGGAATTGAAGCGTACGGCACGTACAGCCCCAATTTAGCGTCGTACATACGGTCCTTACATAGATATTCTGGGTACTCCAAACGGTCCGATGCCGCAAAAACATTAGCGGGCGCTCCGGTAATGTTCCGAAACATAGGCCTGGTAGACGTGCTCAAGCGTCACGCATTGGTACGGGCATCGAATTTATATTCTAAGCGCCCTAGGGCACATTAAAGCCCAATTGATAGATGCACGCGTAAGACATCCCAGCCCAGTTGCGCCAACGGACGCTGACTGAATATTGTAAAGTGCCTACAAACTATACTGCTTGCCAACTGTCTTCTAAGATTTAGGGAAGAAAGAGGATAGGGGAGTCTATAACCGGAGGATACATATAAACTCTATGCCGGTACCAATGTCAGAATATTTGCCCCGTGTGTTTGGATATTAGGTTTTCGTCCATGGTGAGCTGCGGTGTATTAGGGGGGCATCCGCACCGGCATGAAGTGTCCTCATACAAGACAAGCTGATCCAGACTACCCCATGCGTGTCTATTACGCTGGAGCAGCACAGCCCCTAATCCGTGGGGTATGTGACGTCTCCTGTAAAGTTCCCGCTAAGTGGACTCGTTAGTGCATCAGACGCGAGTGCCCGTACCACCGAAGCCTGACTCCCTTGGCTCTTTCACCTTTCCCAATTGGAGTTTGTTGTCCGATAAATACAAAATCAGGCCTATTTGTCGAATTAGAAAGGGGCAGAAAATCCATGAGGGTTTGCGGTACCCCGCTACGACCAATAAAGGTAGGTAGGGCCTCGGCGATCGTAGATTAAACTTGGTGGGTGTGTCGACAGTCCGCTCTGATCTGGCCGTAACAGATAAGCTGTGGGATGCACGCAGGACAGGGGCTGCGAGGTCACACCGATGCGATCACCGTCTTGGGCGTGTGGAGGAGCATAAAGGATTGGGAACAGAGGGTCTTGGGCAGAAATCTGTCATCGCCAGCCCAGAAGGTCGAATGTTCTCCGCGACAGGTGCCGTGAATGAGATGGGACTGGAATTCAGATTATGCGCCTGGTAAGAACTCACTAAAATTCGAAAATGTTTCCAGTATTACCTCGGACCAATGTGCTGACTAACGGCAGTGGTGCGAACTCTGAACGTCAGTAGTGCTCCAGGATCTCCACAACGACATCACGATCCATCACAGGGGCTCATGTCGGTTGTGATACAGTGACCAAACATACCTCCAGGGCGTGCCACCGGTGGACGCTCGCTGACGTAGGGTGGGTAGGTTAATCGCTCACGTATCCTCAGATTAATACGCCATCAGGCCGCTCTCTTTGTCATAAATTCGATGCCGGTGCCGATGCGATGCTCGTAGCTACTGGAGTCGGACGTACATATTGTATGCTATTGGTGGAGGTACCACTAGCAGTGCGGAATAGCACTAAGGACGAAGATATAAGCGATAATGCATACCTCCACGGTGACGCTCAATCCTGGTTCTATAAAACGTTGTGGATCCAAATATGGCAAGAAGGCTAATAAGTAAGGGCGACTCGCCATCTTATCAACTCCATGCCCGTCCCTATGCCCTGGTAGGCTGTATCATAGCCCCCCCGAAAACAACAGAGAATTTTCGGATGCAAAAACTAGTTTGCCTGACCGAATCCGTCCGAAGGCGGTCTGGGACGCCGCGACCTGTTTACAATGTGTCCAAGAGCCTAGGGATTGCGCACCGAGTGCGTGTTTCACGATCTCGAGGTCGAGCGTTTGTGGATCAACAGTATGCCTGTGCCGATGAGAGGAAATTGTCTATTGGCGAACCACATTCCCAACAATCTGTGCGTGGATGCTCATGGGTATGGTGACCGGGGTTGTCGCTGTATAAGCGCCTGTGACGGTTCCTGCTAGCTAGTAGTGGCTACAACCTCGCATGCTGTCTTGGAGGCCTGGGGGATCACCTCGCAAG'
#aminoAcid = 'INSMPVPM'
#encoders = SubstringEncodingAmninoAcid(rna, aminoAcid)
#for encoder in encoders:
#	print encoder

#rna = 'AUGUAUGGCAAUGCUAUAUGCUUACUGUGCAACCCCUUACACGCCUUAGUACUCAGGGUGCUAUGCGCCCAGUCGGGCGAGCGCUAUUACUAUGGUAUCUUUAAGAAUCACUAUCCAAUGCAUUUUACCUUCUUAAAGACCGGGACCUGUCCGACGUACAAUCAAGUCUCAAGCACCCGUAUUUCAAAAGAAACAAUAGCACUUGUCUGGCCCACUACGCGGAAGCAACAUCGAACCGAUCUUAGAUCUUUUCUCACUAAAGUCGUAUACAGGGCGUAUCAUCAUCGGGCCUCUGCUGUCACUUGCAGUCUACUUAAGAUGUUGGAGCCAGUGGUCCAGGCCGCCGAGGUCUUCCUACCUUGGAAAGGUCCUAUUUUCGCACCGGUGGAGAGUGGAACUUUGUCUAACUUCUUCUUAACGCAGCUUUGGAUUUGUGGCCGCUUACAACGUAAAUUGGUCAUAGAGAUGUACGCUGAAAGAGGAUUAAUCCGGAAGGCCCCAACCAGCCUCUCUCGCAGAUUAAAAUGUGAUAGUGACUCAUUCUACCCAGGUUUUAUGAAAUUCGACACUAAGGUUGCCGAUCGGAAUCGGCCUAAGAAGGAAGAGACGAUCUCCACCACCCUCGACGGCGUGUCGUCUUUGCCAGUCUCCUCCCCAAUCAUAGAUAUCUAUGGCAGAAGCGUCAAGGUUUUGAACUGUGUGACCAAGCAUAUCGUUAUCGGGCGAAAGACUCUAAAGCGCGUUAAGUAUGCAAGACAACUUUCAUGCGUCCUGGUAUGCUGCGCAUCGGAGCUGUUAGACUAUAUUAACCGUACCUAUUCAAUACCGCAAAUCGGUGGGACCAAGGGGCGAAAGAGCGGACUUAGUGGUUAUGCUGUUAAUAUUGGUGCUAACACUACCACCGCGGAUCUGUUCACUUCUGUGAAGACGCCAGAGCUAUUUAGGGAGUGGGUUAACACAAGGAAAACUUACAUCCUUCCCCGGCAUUUUUUACGUAGGAGGUGGUUAGCUCAACGCCUCCCGUGUGGACAUAUCUCUAGUAAAUGUAAGACCGGGGGGCAUCUUCUAGGUUCCAACUCGGUCCCUUGGCAUCUGAAAGCCAGCCACGGCAGCCGCGACAGAAUUAGUCUUCUCUCUAGGUUCGCCGUUCGGUACAAAAUGCUGGGUAGGGUCAGGGAGCCCUACUCGCUACUUCUCCGAGUGCUUUUUCCCCCUAAGAUUCGAACUGUGAUCCUCCGGCAAUGCUCUGUGAAGGUCUUGUCCGUCGGCAGGUUCACACGUAAGGCAACGUUAUCGGCCCGGAAUGAUCCGGUGACCCUGAUCGCGCCCCUAAAACAGCAUGUAGCCUCUAAUAUCACCGUUUCCUACUCCAUGUUGAGGAGAUCUGAUCAGAAAGCCAUUCGCUGCGCCCGCGCGCAGUGCCCCCGCCGCGAACUAUGCGAUAGGUUGAACGCAUUCCCAAGGCCCUCCUCCCUAUGGCCUUAUACGCAGGCCUUGACAUAUCAGGUCCCUGUCGCAGAGCGAUACUUGUCCCACAGCUUGUGGACCGUUGGGGAUAAAUUGUAUAAAACAAUCACAUUAGUGUUAAACUGGGCCGCAUUAUCGUAUCACCUCCUCAGGGGUCAUUAUGCUGAUACUGCUUGGUUACCUAGGAUCUGUGUUCGCACCGGGGCCUUCCACUAUGGACCGCUCAGGGGUCAUCAUUAUUGCUCCCCGAAGUUACAACGAGCCCGCGUUGGACUGUGGAUUACUGACUACCCCAGAUCUUCUAACCUAAAGAGUACCCAUCGAUACCACCGGGAAGUUUUUAUGUCUAGAGCGUUGGGACACUCCAAACGGCCCGGGCGACCUCUGAGCCCAAGAAUGCUAAUCGGCGAUUAUGAAUCACCCUGCUAUUGCAGAGGCUGCAGAGGUAUCAAAUCCUAUAGCGGGAUAAAACCGACUGUCCAGCUAGCUAGAUGUGGCGCGCGGCGAGAGAUACCUUCGAUGCCUAUCUGCCCAGCACCAUUGCCACGGUUUAUGUACAAUGUCACCAUAGCUGCGGUAGCCUCUUCUACCAAUCGGUAUGUAUGCAUCAAUAUAGUGGCUCCGAGUGUUCGAGAGGGGGACGGGAGGAUCCUGUUACAGCUUAUCCGACAGACACCUUCUAAUGGUCCCAGAAGUAUAUCUCGUAACGAAGUAGCGCGGCAUUUGUGGGACGCUCCACCGCACUCACACAUUUUGGAUAAAACAGCAUACUUAUCAGCUUCACCCGGUAGCGACCGUAAUACCGGACGUUUUCUAUCCUUUGUCCCAGUCUACGCUUACCCAGCGACCGGGAUCCAAGCAAAGCUAUGUUGCUUGAAACCAAUGAUUCUACACUGCUUCCUAGGCAAGAUGGUUGAGGAUUCACAAGGGUACUACGGCUUUCUGCGGACGGCACUCAUGCGUGGUAACAGGAGGUUCAGUAUUCCGAGGUACCACACGGCGCUUAAUACCAAGGUACCCCUUCUGGAAAUCAAAAAAGCGUGCUUCUCGGCAUACAAUUCCGGGCGAGCGGAGAGAGACGUCAAGGUAAUUAGCGCAUCCUGUGGAAAUCAAUCUCUUAUUUAUGUUAGCAGGUGCGCCAAAAAGUGUUACCGCGGCGUACCAAGUUGGCUUGCAGGACGGAUCUCUCUCUUAUAUUCCCUGCUUCCUGCGCUCGCUCCACUCGUGAAUGCCGUUCGUACAAGGAAGGGGAAAGACGGCGGGAACUAUUUACAUUGCCACACCUAUUCGGGCGGGUCUCUGACCCAAAAAAAUCGCCCACAGCCUGACUGUACGUCCACAGCGGCUAUCGCUGAAAAGCGACAAAACAUCGCCACUUUAGUCUAUGUUAUACUAGUUCGGUCGCCCCUAGCGAAGGAGUGUGAGAGUAGAACCGGCAAACGCGCUAUGCUGAGCUACAUAAAACUAGCAUCCAAGUUUUUACCCCGGAACCAUGGACGGCGUAGAACCCACCUGGCACCUACGCGACGUGUGGGGAUGGACGUCAGCAGAGGGAAAGGGAGAGGCACUACGCGGGUAGACCACCGGAAAGCCAACCCGUCCCAUUGCACUCUUCGGCCUAUGCCACUGGGGUUUAGAGCCAUAUGUUCUGCUCUCAGGUCGGUACACGCUUGUGAAGAUCUAAACCUUCUCGGUUACGAAGUGGUUACAAUGAGAAGAACGCUGGGCUGCCAGUUCCUGAACUACCUGCCAGGAAGCAGCAGAUGUUCUCUACUUUAUGGAUUGGCUAAUUUGAACGCUUACCUAACACGUCCCCGACCCGCCGUAAAUACAGCGCUCCUGGUUUGGCAGAGUGUCUACCCUUACUUGCACUUCGUCGUCGGGCCAUACGAGGUCCGCUCAUCUCACUUUCCGGAUUACUUGGUUAUCCCCAAGAUCCCAGUUCGUACUCUUGUGCGUCCAUCAUUUAAAGGGUGCUGGAUCGCGAUUCAGGUGGAUUUACUUUUACUGAACCCUUACCGCAGCGCUCACGUCGGCCGGGCCGUAAGUAGACAACGGCUGAAAUAUCAACACCUCAUCGUCCAGCCCCCGGGAACUUCAGGAACUGUGCGAAUCAGGCUAUAUGCGCCUUUUAAGUUGCUCAGGACUGACACUACGAUAUGUCGCUGUGGCCAGGUCGUAGCUAUUCCCUCGCAGAGGCCAACGGAACUUGAGCGGCUACCCAGUCGCGUAAUCGAUCGUGCACGUAGAGAACGACUAGGGGAAUGUAAGAUUCCCCUUGCCCGGACUUUUGCUAUUGAGUCGACUUUGAGCACUGUCGCAUUCCGUUUGGGUAGUUUAAAUAUCUGCGAAAGAGUAUAUAUAAAAUCUGAUAGGUUCUUCGGAACAGAUGUGGACGCCUGGGUGCAACGAGUUGGAGAUGGGCGUAGUUGGGAACCACGCCCGUUGGUCCAUACAGCCACCCUUAGAGUCGUCAUGUGCCCCGUACAUUUGUUUCCGGCAGUCCAUGGUACUCAAUUCACGCGGCGAGGUAAGGGUGUUUCGAAGGUCCCAAAGAAAACAUACAGACGUGAGGACGAAUCCCCUUGCUUAUUGAACUCCUACAAUCCCUGUGCGGCAACUGUGCCGGCCAGGACAGAAUUAUUUGGUAUGUGGAGUGCUGCCCGCCGCGGUCUGGACUCUCACCAUAGGACGGCUGAAUGUUCUAGAUUCAGCCGCAGGUUGGAAGUGACGGGAUUGACCGUAAUCUUAGACUCCAGGACACCGAUCCCACCAUUUUUUGCGCAGGCAGCGGUUCGUAGUCCACUUACUAGUGUGCUUCAAUUUGAGGCACUAUCAUCGUUUCGCAGGCAUGAUCCGGUGGGUAGGACGGCUAGGGCUAGAUGCUUCGGCGUUGCUGUGACGCCUAGUGGCCCGACGCGCACGGUUUGCAAAGCAGAACCAGUACCUUACCUUGUUACGGUCAGCGCAGCUUCGGUGAGAUCUCCCUGGUGCGGGCUGCCAAAGUCUGUGCGACCCUGCAUGCCUUGCAGGCAUCAAUCUAAAGGAUAUCGACAAUGGAAUUGGUAUCAUGAGGCAUUCAGUCCUGGAUACGCCCGGAUAUGUUUAGAGUGCAGCAUAUGUUCGCAUACAGAAUUCAAUACCGAGACUAUGCCUCUAUCGUCGGAUAGUCCUCCGGGCAACGAGGGACAUACCCCACACCUUUAUCAGCGUUCCCAACUUAGUUCAGGUAUGCAGGCUCAAAUGAGUCUCCGGGAAUCGCAGUGCGGCCUUACGGGCCGGGUAAGCAUACAUUUCGUAGAGCUGUUUUUCCAGGACUUGGCCCUCACCGGCCAGCAAGACCUACUUCAGUCCUUAGGGAAUCCGAAUCUUGUAAACACUCGCUGUGAUCCAGUGGGUAUGCGUGAUAUACACCUGAGGCGUCCCGCUAUUAAGCGCCGGUCGAGGUAUGUGGUCCAAGAUAGUGUACCUAAUAAAGAUAUGUCAUUGACGCUGACUCCCGCUAAAACAGCAGGCGUCCACCUCGGUAGCAUGAGCGUUGAGCCUACCCGAUGUUCAGCUUCUCCCACUCGGGUUAACUCGUUUAAGCACAGACACUGGUCUUGCCGACUUAUUCGUGGUCGCACGUCUGAUCGUCAACACUACCUUGCUUACUUCCGGGGACAGUAUUGCCUAGGGGAAGGCGUCGAGCGGCUUCACCUAGUCCCCACUCUUCUGCUAGUUCCAGCAUUUCUAACUGCGAAACCGAGGGCCCGUACAGGGAGCUCGAAAUCGGGAUCACCCGUAACUGAGGGGCUAGAUAAUAUUGGCUUUUAUGAUCUGUUGUCAGAUAACCGUACAAACUCCGACGGAGGUUCACGUCGCUGCCGGGUGAAUAAGAUUGAAUUUAUACACAUCCCAUAUGUCUCAAAAAAACAGCUAAAGAUUUUACAUCCCGGGGGUUGGACUCUUAACAUAGGCAAUGGGUUGCGUUUGCAGUUCCGAGGUUCUUCAUGUAUCCAUCCGGACUGGCUCGAACUGAUGUAUCCCUAUACGCGCAGGCAAAAGCGCCGCGAAAUUAUAACCCUGCGAGCUCGGUGCAAGUACAGUUUCCGACUUACUUAUGCUUGUAAGAAUCGGCGCGCUUCCUUCUAUGCUUUUCAGAGAUCUGUUUCAAUUACGACGCGGACUUUCCUUCCCGUCGAGAGCGAAGUUACUCAUCUAACUUUCGGCAAGAGCUCGAGGCGUGCCGGUAUGGGGCAUUUUAUACCACGAUUGCAUUCGACAUUUGUCCUGGAUGUAGCGUCCCACAGCGCUCAUACCAGUUCCUGUGUUUUUCAAUCCAGGAUGGAUGCUCCCUGUAACAGGGCAAACUCCGCUACUUACUUAUGUAAAUUGCCCGCCCCGCAUGUUGUGUUCUUGGGAAGGUAUCAAUGCACCCCACUCGAGUCAUUAACCGCAGUUUUUGUCUCGUCCCCAGAUCGCGAGGCUUUUUACGACCAGAACAUCGCAGUAUUUUCACGUGCUUUAGUGGAAAGUGAAGACACAGCACAGACCUCUACUUUUUCUCCCAGGGCGGCCCCCGACGCUAAAUUCUACUCAUGGAAAAUCCACGGUAUAUUUCGCUUUGAAAUGAGAGGAAAUCUCGAAUAUUUUAGCUGUAUCACACCACGACAGUCUACACAGUACACCGCCCUUAGAAAGGAAGAAGUUUUCUGGGUUUGCCCCUUACACGUCAUUCAGCCAAAUUCGAUAUUAAUUGAAGCAAUACCACUGAUGAAGGUUAGGGUGGUUACAUAUGAGGUAUUAGCAGUCCGUGUGUCCAGCCGAGAUUUGCCAGAGCCUAUCACUCAUUUAUAUUCUAGUAGGGCUCUCCCAGCGCUUUCUGGUGACCGGAGUAAAGAGAUCACAAGACCUUGGCUAUCCGAGCUCAGAGACGGAAUGUUACUGCGCGUGGGCGGCAUUUCGGGGUCCUACCAAGUUCAGCUUUCUUAUAGACACGGUGUUUCGGCCCUUAACGCUGCUAUCACAAAGCUUGCUGGGUCGCCCGAUGGGAAUCUGACACCGUUAUCGAUCGCGUUGAACCGCCCUCAGUUGCCUUGCCCAGCGUCGCUACGACUGAGGAUCAGCCGCGACCUGCCAGAUUGGCAGGCUGGCUCUUGGAAUCGCUUCGAAGAAAACAUACACUCCGGAUCCGUAGACUUAAGUCCAGGUGUCUCCAUCCAGUGCCCCCGCCCCCUAGUAUUCUACUCUAGUGCAAGCGUUCACGUAAGUAGUGGUGAACGCCGUGGUACAGGCGUAGGUUCUUUAAUAGAGGGUUGGCUCAGGAUACGCGGAAAACUCAAGAACACUUGGGAAGCUCCCAGAGACUAUUGGGUAGUUAAGCUAAUGUCAUGGCGGCACAUCUUGAUGGGGAAUUCAAUUCAACCCGGGUGGACAACCAGGCGGGUGGUCAAACUAGCCAUGAUGUUUUGUCUUAAGUCGGUUGACCGCUUUGGUAAGAGCUCUAUUUGCUACGGGAAAUACACGCACUUGAAUGACAGCAAUUUAAGAUUAGGUAUAGGCUCCACUACCCGUUGUUCAAUUCACCUAAUUCUACUACCGUGGCGGAGGCCCGCGCUGAUGGACACCCAGUUCCCAAAAGCUCGAUCCUCUCUUGGUGCGUGUACCCCUAGGGUACCAAAACCGGUAUUUUAUCCAUGUGCUAUGGCAGCUUCAUCUCAGCAUUGCAUUUGUGGACAUUAUGUAAGUUCUGAAAUAGCUACGUUAUCGCCGGGCCGCCUAACUGCCAAUAAUCUGAAGUCGCUACGUCCUUCGUGGAGCGACUCAAACACACCAAUUGGAUCAUUUUGGGUUUUACUUGGGCACCCACUGUCCCCUCAAGCCUCUCACUUCACAGUUGGCCCCCACCACGACGUAUUACUGCACUUAAUCCAGCUUCCCUGCUGGUCUAUAACGGAUGGUCCCAUUGUGGCCGGCCGGGAAACACGCUGGUAUACAGUGCAGACUGCUAUGCUGGCUCAGCGUACCUAUAUGAACUGGGGCUGCAGUCUAGUGACAUGCCAUGUGGCUACGACCGUGUGUAGUAUAACUCGCAGAACUUACUGUGCGACGCGAAAGCGAAGACGCAGAUCAGAAAGCCCAUCUCUCAUCUCAGUUCACCCUUCAUGGUGUAUUAGAUUUAUACCCCCGGGACGAUAUUGCUUCGCUUCGCGGUUGGGCGCAGACACAAGGGACCCCCAAACGGGGGCCGGUCCGGGAAAGGAGGUCCGCAACCACGUUGCUAGCGGGGUAGUUGACGACUUGAGAUUCUUAACGAUAAUCGGAGCGAGUGUCAAUGCGAUGCAAAGGGAUGGAGUGAUGUUAAGAGAUCCAAACGCCAAAUGGUCAAUCUGCUCCAACCCGGCUCCUAGCAAUGAUAGCUCCGGUGCGUUAUACGUUGGUCUUAAUCCGGCCCCGACGGCCGCUGUUUGCCAAUUUAAUUUCCCCACGCACCCGUCUUUCUCCCCCUGGCGUAGGUCACUAAAACUCCACACAAUCGCUAUUACAGUUCAGAGUCAGCGAUGCGCCCCGCGUCAGUACGCUCUAACAGUUGCUAGGGGGGCUUCGCAACCUGAAGAACGAAUACUCGGGAUGCGUUCUUUGGCUGCAGACCAAGAUUCUCCUUGCCACGGGAGGACUAGGUCGAGGGGAGGAUCAAAAUUUGUCUUGUGGGAAGGAGUAUUAUUCACCUGCGUCUGCGGACGGAGAAAGAACUUUUGCGAGAACAGUUGGCGUGACCCAGCACUGGCGCGAUGCCACGCCGCUGAUAGUCGCUAUCCCUCUACACAUUCGGGAUUCGGCAAUGCGGCAGCCUCAUUCAUUUGCGACUUGAAGAGAGCCGGGGUCCGACCGACGGGAGUCUUAGGAAUGGCCCACGCCUUAAUGAGGCAGAAAGGUCACGUCGCGAUUGAAUUAACAACGUACGCUAAGGACUUCCCGUUAAGCCGGUGCGGAAGCGGGGGCUCGAGUGUGAUCUUGUGUACUCACGGCCAGCGUAUUUAUGAUUCUGUUGUUGCGCAGGCUGAGAGAUUUUAUGUUGGCUGUUGGAAGCUAUGCAUAGACUUGGGGAGGCUCCUGCCUAGAGCGGGGAUAUUAAUUCUCAUUGCUUUUCUCAUAGUGCAGGUAGCUGCUGGUUACUUCUCUAGAGUACGAAAUGGCUCUAAUCUCGUGGUCAGUUACCACCCUGAAUGCUCGAUUCCACGGUUUGCGAGGGCGGAACGAAUGGUUGAGGGUAAGCUGGAAGGGCUUCGGGCCUUCUAUCAUCUCCCAGAGAGGUGGUAUUGGCAUCGGGAGAACACAGCGUUGUCGGCUACAGGUAUAACUUGCGAGAGACACCUACACUUCACAUUCCUUACAUCGACAUACCAGAAUUGGACUUUUGUCGCCCACAUCGCCGCACCGGUGCCGCUGUUAAACAUCAGACGUAAUGACCCGUCUCCCGAUUCCAGUGGGCUCAUUCUACGGGCAGACCGUUCGAUGUUGUGCCCAGUUCGGGCGUUUGGUGUACGCCCCGCUUGUGUGAAACGAGGCCCAUACGAUGUCAUCAAGUUGUUGCCCCUAGCAUCGGGCAAAUUAUUUCCUGCUCAGCCGUCACCCGUCUAUUCCUGUUCCAAAUUAGAGAAUCAGUUGAGCAUAGCUGAGAAGGGUCUCAUAGGUAGGGUGGCCGCGGCCUUAAAUGAUCACCGAAGGUUUCCUUCGUACGUGUGUCGACUUGGCUGGUUGCCUUGUCGCUCAACAAGGACGAACUUCAUAGUUUUAGUUAUAAAACAGCCGAGCCUUUUAAGGAGGCGGGGCAGACGCAGUGGGGACUGGUUGCACAGCCUUGGGGGACAGGGGAACACGAUUGAUAAGUCCGUCAGGUGUAACGUACGACGAAGUUACGGUGACUGCUGGAAGCCAACUUCAAUCAGGGGAGUGGAGUCGCCCGAGGGUUCCCUAGGACGAAGCAUCUGGUCAAGAAGACACGUUCUUCAGUCUCCCAAUACGAUCGCCGAUCUACAUUUCGAAUGCGAUAAGGUGCGUGGCAUAAGAGUCUUAACCGAGAUCGUGGAAAAGACCGCACAACAUAGGCCAGACGCGGCCUGGGAGAGCCACACAUUCCACCCAUGUGCACUUCACAUCAUCCGGAUUAGACUGCUCUAUCGGGUAAAACUCCCGCUAGAUGUCUCCUCGAACUUGGCGGGAGAUGAUAUUAGCACGACCUCCGAUGGAUUUAAACUCACAUGGCGGGUAAUGACACCAGGGAGGGUGCCGAUUCCGUACCUGUAUGGAUAUCAGAGUGCCUGUUCCCAGGCUAGCGCCUCGAAUUGA'
#print ProteinTranslation(rna)

#integer_mass_dict = IntergerMassDictionary()
#peptide = 'MPILEINAWWLLWS'
#l =  CircularSpectrum(peptide, integer_mass_dict)
#l = ' '.join(map(str, l))
#print l

file = '../Downloads/dataset_100_6.txt'
spectrum = []
with open(file) as f:
	for line in f:
		line = line.strip('\n')
		l = line.split(' ')
		for element in l:
			spectrum.append(int(element))

print CyclopeptideSequencing(spectrum)







