import sys 


for line in sys.stdin.readlines():
	line = line.strip()
	if line == '': 
		print(line)
		continue
	
	if line.count('\t') == 9:
		row = line.split('\t')
			
		if row[5] != '_':
			feats = row[5].split('|')
			feats = list(set(feats))
			feats.sort()
			row[5] = '|'.join(feats)
			# double features not allowed, Emp pronouns are by definition Prs in Bambara
			row[5] = row[5].replace('PronType=Emp|PronType=Prs', 'PronType=Emp')
			line = '\t'.join(row)	

	print(line)

print()
