import math
exceptions = []
no = int(input())

for _ in range(no):
    op = input().split(" ")
    task = op[0]
    try:
        
        match task:
            case "div":
                x = float(op[1])
                y = float(op[2])
                result = x/y

            case "sqrt":
                x = float(op[1])
                result = math.sqrt(x)
    except Exception as e:
      exceptions.append(e)

if exceptions:
    try:
        raise ExceptionGroup(
                  "error",
                  exceptions
                )
    except* ZeroDivisionError as ex:
      for e in ex.exceptions:
        print(f"{type(e).__name__}: {e}")

    except* ValueError as ex:
      for e in ex.exceptions:
        print(f"{type(e).__name__}: {e}")
      
    except* TypeError as ex:
      for e in ex.exceptions:
        print(f"{type(e).__name__}: {e}")
      
else:
  print("No errors")
