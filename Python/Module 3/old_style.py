num = int(input())
sum=0.0
for i in range(num):
    tmp = float(input())
    sum += tmp
    print("{:8.2f}".format(tmp))

print("{:10.3f}".format(sum))    