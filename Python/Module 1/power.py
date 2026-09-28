import sys
base = 0
exp = 0
arg_len = len(sys.argv)



def power(base, expo = 2):

	"""Compute base to the power exponent.If exponent not provided,use 2"""
	return(base ** expo)

if arg_len < 2:
	print("Usage: python3 ./script.py base [exponent]")
elif arg_len <3:
	base = int(sys.argv[1])
	print(power(base))
	print(power.__doc__)
else:
	base = int(sys.argv[1])
	exp = int(sys.argv[2])
	print(power(base,exp))
	print(power.__doc__)

