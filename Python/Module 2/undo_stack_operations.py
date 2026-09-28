no_of_commands = int(input("Enter the number of commands : "))
main_stack = []
logs_stack = []


def push(x):
    main_stack.append(x)
    logs_stack.append(("pushed", x))
    display()
def pop():
    if len(main_stack) == 0:
        print("empty")
    else:
        x  = main_stack.pop()
        logs_stack.append(("poped", x))
        display()

def undo():
    if len(logs_stack) ==0:
        print("nothing to undo")
    else:
        undo_op = logs_stack.pop()
        match undo_op:
            case ("pushed", x):
                main_stack.pop()
            case ("poped", x):
                main_stack.append(x)
        display()
def display():
    if len(main_stack) == 0:
        print("empty")
    else:    
        val = ""
        for i in range(len(main_stack)-1,-1,-1):
            val = val + str(main_stack[i]) + " "
        print(val)
        

for no in range(no_of_commands):
    prompt = input("Enter the command : ").split()
    command = prompt[0].lower()
    

    match command:
        case "push":
            push(prompt[1])
            
        case "pop":
            pop()
        case "undo":
            undo()
        case _:
            print("Invalid Operation")

