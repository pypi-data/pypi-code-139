def naive_exact_match (sequence,pattern):
	positions = []
	for i in range(0, len(sequence) - len(pattern) + 1):
		if sequence[i:i+len(pattern)] == pattern:
			positions.append(i)
	return positions

def hamming_dist (S1,S2):
	dist = 0
	for i,j in zip(S1,S2):
		if i != j:
			dist = dist + 1
	return dist
#print(hamming_dist('ATCGA','ATGCA'))

def reverse_complement (S):
	comp_bases = {'A':'T','C':'G','G':'C','T':'A'}
	rev_comp = []
	for base in S:
		rev_comp.append(comp_bases[base])
	return ''.join(rev_comp)[::-1]	
							
def naive_with_mismatch (sequence,pattern):
	positions = []
	for i in range(0, len(sequence) - len(pattern) + 1):
		if sequence[i:i+len(pattern)] == pattern:
			positions.append(i)
		elif hamming_dist (sequence[i:i+len(pattern)],pattern) <= 2:
			positions.append(i)
		elif reverse_complement (pattern) == sequence[i:i+len(pattern)]:
			positions.append(i)
		elif hamming_dist (pattern, reverse_complement (sequence[i:i+len(pattern)])) <= 2:
			positions.append(i) 
	return positions

