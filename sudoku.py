import json
from pprint import pprint
import numpy as np
board = []
for i in range(0,10):
    row = []
    for j in range(0,10):
        row.append(0)
    board.append(row)

pprint(board)

f = open("test.json", "r")
data = f.read()
jsondata = json.loads(data)
pprint(jsondata["board"])

possible = [1,2,3,4,5,6,7,8,9]
problem = jsondata["board"]
test_solution = np.asarray(jsondata["board1"])
def check_solution(finished):
    #ultimately return lists of candidates for a given index
    #within a given row this method will be used to figure out
    #the possible moves to use in the future
    candidates = {}
    for i in range(len(finished)):
        for j in range(len(finished[i])):

    for row, rindex in enumerate(finished):
        if ((sum(set(row))) == 45):
            print("this row is correct")
        else:
            available_inputs = []
            for item in possible:
                if item not in row:
                    available_inputs.append(item)
            for col, cindex in enumerate(row):
                candidates[(rindex,cindex)] = available_inputs
            pprint(row)
            print(sum(row))
            print(sum(set(row)))
    for row in finished.T:
        if sum(set(row)) == 45:
            print("this column is correct")
        else:
            print(row)
            print(sum(row))


check_solution(test_solution)
