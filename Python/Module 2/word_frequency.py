def print_frequncy(f):
    for i in range(len(f)):
        print(f"{f[i][0]} {f[i][1]}")
frequency = {}
while True:
    try:
        word = input()
       
        if word in frequency:
            frequency[word] = frequency[word]+1
        else:
            frequency[word] = 1
    except EOFError:
        sorted_frequency = sorted(frequency.items(), key= lambda x: (-x[1], x[0]))
        print_frequncy(sorted_frequency)
        break
