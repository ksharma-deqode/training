import textwrap

w = int(input())
i = input()
text = input()


result = textwrap.TextWrapper(
    width=w, initial_indent=i, subsequent_indent=i,break_long_words=False,
).wrap(text=text)

for word in result:
    print(word)