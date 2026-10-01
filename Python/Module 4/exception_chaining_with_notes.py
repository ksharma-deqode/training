
class DivisionError(Exception):
    """Raised when an error occurs during a division operation."""
    pass

def process_division(num1_str, num2_str):
    try:
        numerator = float(num1_str)
        denominator = float(num2_str)
        
        try:
            result = numerator / denominator
            print(f"Result: {round(result, 2)}")
            
        except ZeroDivisionError as ze:
            ze.add_note("Denominator was zero")
            raise DivisionError("Division failed due to an invalid denominator") from ze

    except DivisionError as de:
        print(f"Caught Exception Type: {type(de).__name__}")
        
        de_notes = getattr(de, '__notes__', [])
        print(f"Caught Exception Note: {de_notes[0] if de_notes else 'None'}")
        
        cause = de.__cause__
        if cause:
            print(f"Cause Exception Type: {type(cause).__name__}")
            cause_notes = getattr(cause, '__notes__', [])
            print(f"Cause Exception Note: {cause_notes[0] if cause_notes else 'None'}")
        else:
            print("Cause Exception Type: None")
            print("Cause Exception Note: None")


no = int(input())

for i in range(no):

    num_1 = input()
    num_2 = input()
    process_division(num_1,num_2)