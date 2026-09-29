num = int(input())

for i in range(num):

    value = input()
    value_list = value.split(",")

    item = value_list[0]
    price = value_list[1]

    print("{:<15} {:>10}".format(item,price))