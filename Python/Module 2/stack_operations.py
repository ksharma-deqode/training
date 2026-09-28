no_of_commands = int(input("Enter the number of commands : "))
st = []

def push(x):
    st.append(x)
    print(f"{x} is pushed to the Stack")

def pop():
    if len(st) == 0:
        print("empty")
    else:
        x  = st.pop()
        print(f"{x} is poped from stack")


for no in range(no_of_commands):
    prompt = input("Enter the command : ").split()
    command = prompt[0].lower()


    match command:
        case "push":
            push(prompt[1])
        case "pop":
            pop()
        case "top":
            if len(st) == 0:
                print("empty")
            else:
                print(st[len(st)-1])
        case "size":
            print(len(st))
        case "empty":
            if len(st) == 0:
                print("true")
            else:
                print("false")
        case _:
            print("Invalid Operation")