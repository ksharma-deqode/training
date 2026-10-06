from decimal import Decimal, getcontext
n = int(input())
ds = input().split(" ")
op = input()
pv = int(input())

getcontext().prec = pv

result = Decimal("0")

for i in range(n):
    num = Decimal(ds[i])

    match op:
        case "+":
            result+=num
        case "-":
            result -=num
        case "*":
            result *=num
        case "/":
            result /=num


print("{:.0f}".format(result))