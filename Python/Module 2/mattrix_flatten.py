rnc = input().split()


r = int(rnc[0])
c = int(rnc[1])

mattrix = []
final = ""
for i in range(0,r):
    emp = []
    for j in range(c):
        
        e = int(input())
        emp.append(e)
    mattrix.append(emp[::-1])

filtered = []
for i in range(0,r):
    for j in range(c):
       if(mattrix[i][j]>0 and mattrix[i][j]%2 ==0):
           filtered.append(mattrix[i][j])

for ele in filtered:
    
    final = final + str(ele) + " "
if(len(final)==0):
    print("empty")
        
else:
    print(final)
