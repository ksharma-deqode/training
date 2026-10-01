def fib(n):
    a, b = 0,1
    for _ in range(n):
        yield a
        a,b = b, a+b


def get_fib(n):
    if n<0:
        print("Invalid Input " )
        return

    fib_num = list(fib(n))

    print(*(fib_num))

    sum_fib = sum(x**2 for x in fib_num)

    print(sum_fib)
no = int(input())

get_fib(no)