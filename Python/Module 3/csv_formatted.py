num = int(input())

for i in range(num):

    value = input()
    value_list = value.split(",")

    name = value_list[0]
    age = value_list[1]
    city = value_list[2]

    print("{:<10}{:<3} {:>15}".format(name,age,city))