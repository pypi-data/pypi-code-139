def encryptFunction (string):
	nonencrypted = string[::-1]
	first_l = [ord(c) for c in nonencrypted]
	swapped_l = []
	if len(first_l) == 2:
		swapped_l = first_l[::-1]
	else:
		for i in range(0, len(first_l)//2):
			if len(first_l)/2 % 2 == 0:
				swapped_l.append(first_l[2*i+1])
				swapped_l.append(first_l[2*i])
			else:
				swapped_l.append(first_l[2*i+1])
				swapped_l.append(first_l[2*i])
		if len(first_l)/2 % 2 != 0:
			swapped_l.append(first_l[int((len(first_l))-1)])
	print (swapped_l)
	j=0
	index=j
	while j < len(swapped_l):
		if swapped_l[j]+(index+1) > 126:

			first = swapped_l[j]+(index+1)-126+33

			swapped_l[j]=first
			second = first + 2*(index+1)

			if second > 126:
				second = second-126+33
			swapped_l.insert(j+1, second)
			third = second + 3*(index+1)

			if third > 126:
				third = third-126+33
			swapped_l.insert(j+2, third)
		else:
			first = swapped_l[j]+(index+1)
			swapped_l[j]=first
			second = first + 2*(index+1)
			print (2*(index+1))
			print (second)
			if second > 126:
				second = second-126+33
			swapped_l.insert(j+1, second)
			third = second + 3*(index+1)
			print (3*(index+1))
			if third > 126:
				third = third-126+33
			swapped_l.insert(j+2, third)
		j += 3
		index+=1
	print (swapped_l)
	encrypted = ""
	for i in swapped_l:
		encrypted = encrypted + chr(i)
	return encrypted


