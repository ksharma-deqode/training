while True:
    l = input("Enter the command : ").split()
    command = l[0].lower()
    if command == "quit":
        break
    pre_commands = set(["add","sub","mul","div","mod"])

    if command in pre_commands:

        a = int(l[1])
        b = int(l[2])

        match command:
            case "add":
                print(a+b)
            case "sub":
                print(a-b)
            case "mul":
                print(a*b)
            case "div":
                print(a//b)
            case "mod":
                print(a%b)
    else:
        print("unknown")