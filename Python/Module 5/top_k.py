import re

k = int(input())

text = input()

words = re.findall(r"\w+",text)
seen = []

count = {}
for w in words:
    if w in seen:
        count[w] += 1
    else:
        seen.append(w)
        count[w] = 1

result = sorted(count.items(), key= lambda x: (-x[1], x[0]))

for word,freq in result[:k]:
    print(word)