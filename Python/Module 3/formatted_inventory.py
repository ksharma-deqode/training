import sys
import json

def process():
    try:
        raw_input = sys.stdin.read()
        data = json.loads(raw_input)
        
        for item in data:
            id = item.get("id")
            name = item.get("name")
            price = float(item.get("price"))
            quantity = int(item.get("quantity"))

            print("{:>05d}{:<15s}{:>8.2f}{:>5d}".format(id,name,price,quantity))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    process()