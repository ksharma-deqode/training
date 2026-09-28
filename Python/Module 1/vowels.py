import sys
line = sys.argv[1]
vowels = ['a','e','i','o','u']
v =0
c = 0
for w in line:
	if w in vowels:
		v+=1
	else:
		c+=1

print(v,c)
