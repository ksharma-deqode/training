class InvalidOperandError(Exception):
    """Operand must be numeric"""

class DivisionByZeroError(Exception):
    """Cannot divide by zero"""

no = int(input())
for _ in range(no):
        inputs = input().split(" ")
        nume = inputs[0]
        deno = inputs[1]
        try: 
    
            try:
                flt_num = float(nume)
                flt_den = float(deno)
            except ValueError:
                err = InvalidOperandError("Operand must be numeric")
                raise err
            if flt_den == 0.0:
                err = DivisionByZeroError("Cannot divide by zero")
                raise err

            result = flt_num / flt_den

        except (InvalidOperandError, DivisionByZeroError)  as e:
            exception_name = type(e).__name__
            print(f"{exception_name}: {e}")

        else:
            print(f"{result:.2f}")

        finally:
            print("Operation processed.")
