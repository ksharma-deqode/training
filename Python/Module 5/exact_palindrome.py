import re


text = input()

words = re.findall(r"\w+", text)

pali = []

for w in words:
    if w == w[::-1]:
        pali.append(w)

for p in sorted(pali):
    print(p)