import sys
n = int(sys.argv[1])
a,b = 0,1
while n-1>0:
	print(a)
	a, b = b , a+b
	n-=1
