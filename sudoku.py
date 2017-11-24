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
test_solution = np.asarray(jsondata["board"])

def grid(sample):
    #this function turns list of rows into list of lists, each of those lists represent a 3x3 grid
    #0 is top left, 1 is top middle, 2 is top right, and so forth
    table = {}
    for i in range(len(sample)):
        index = int(i/3)
        for j in range(len(sample[i])):
            jindex = int(j/3)
            if (index,jindex) in table:
                table[(index,jindex)].append(sample[i][j])
            else:
                table[(index,jindex)] = [sample[i][j]]
    return(table)

def check_solution(finished):
    #ultimately return lists of candidates for a given index
    #within a given row this method will be used to figure out
    #the possible moves to use in the future
    candidates = {}
    grids = grid(finished)
    cols = finished.T
    for i in range(len(finished)):
        row = finished[i]
        #print(col)
        row_total = sum(set(row))
        for j in range(len(row)):
            current_column = cols[j]
            col_total = sum(set(current_column))
            current_grid = grids[int(i/3),int(j/3)]
            grid_total = sum(set(current_grid))
            if(row_total == 45 or col_total == 45 or grid_total == 45):
                print("solved")
            else:
                for item in possible:
                    if item not in row and item not in current_column and item not in current_grid:
                        #print(item)
                        if finished[i,j] == 0:
                            if (i,j) not in candidates:
                                candidates[(i,j)] = [item]
                            else:
                                candidates[(i,j)].append(item)

    '''
    for i in range(len(finished)):
        if(sum(set(finished[i])) == 45):
            print("this row is correct")
        else:
            available_inputs = []
            for item in possible:
                if item not in finished[i] and item not in finished.T[i]:
                    print("bleh")
                    #available_inputs.append(item)
                if item not in finished[i]:
                    available_inputs.append(item)
                if item in finished.T[i]:
            for j in range(len(finished[i])):
                grids = grid(finished)
                if(sum(set(grids[int(i/3),int(j/3)])) == 45):
                    print("hello world")
                else:
                    for item in possible:
                        if item not in finished[i] and item not in finished.T[i] and item not in grids[int(i/3),int(j/3)]:
                            available_inputs.append(item)
                if(finished[i][j] == 0):
                    candidates[(i,j)] = available_inputs
    for i in range(len(finished.T)):
        for j in range(len(finished.T[i])):
            print(finished.T[j])

    '''
    return(candidates)
    
'''
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
'''
#print(grid(test_solution))
#pprint(test_solution)
pprint(check_solution(test_solution))
