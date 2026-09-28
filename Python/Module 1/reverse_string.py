import sys

if len(sys.argv) > 1:

	sentance = " ".join(sys.argv[1:])
	reversed_string = sentance[::-1]
	print(reversed_string)
else:
	print("Empty Input Provided")
