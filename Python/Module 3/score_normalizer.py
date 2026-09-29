import sys
import json

def solution():
    try:
        raw_input = sys.stdin.read()

        data = json.loads(raw_input)
        sorted_data = sorted(data, key=lambda x:x['name'])
        # print(sorted_data)

        for records in sorted_data:
            name = records['name']
            score = records['score']

            print("{:s}{:.2f}".format(name,score))

    except Exception as e:
        print(e)


if __name__ == "__main__":
    solution()