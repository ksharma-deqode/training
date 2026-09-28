import sys
found_even = False
try:
	numbers = [int(x) for x in sys.argv[1:]]
except ValueError:
	print("Please enter only Integers")
for i in numbers:
	if i%2 ==0:
		print(i)
		found_even = True
		break
if found_even==False:
	print("No even Numbers")
