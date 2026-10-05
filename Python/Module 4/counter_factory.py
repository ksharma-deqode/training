global_count = 0

def make_counter():
    count = 0
    def counter():
        nonlocal count 
        global global_count

        count +=1
        global_count +=1

        return count
    return counter


c1 = make_counter()
c2 = make_counter()

for i in range(5):
    c1()

for i in range(7):
    c2()

print("Counter 1: ", c1())
print("Counter 2: ", c2())