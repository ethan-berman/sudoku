import json
import time
from pprint import pprint
from random import *
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
def vectorize(options):
    #this function takes in all of the possible inputs for a cell and returns a binary representation
    #for example: vectorize(board_options[(0,0)]) would return binary representation of candidates for that cell
    inputs = [0]*len(possible)
    for number in options:
        inputs[number-1] = 1
    return inputs
board_options = check_solution(test_solution)
#print(vectorize(board_options[(0,1)]))

def sigmoid(x, deriv=False):
    if deriv:
        return(x*(1-x))
    return 1/1+np.exp(-1)
def think(cell, neurons, numlayers, alpha, dropout, dp):
    outputs = [0] * len(possible)
    #create a neural network based on any random inputs, make a list of synaptic weight
    layers = range(numlayers)
    layers[0] = vectorize(cell)
    syn = []
    for i in range(numlayers):
        if i==0:
            syn.append(np.random.random((len(layers[0]),neurons))*2-1)
            layers.append(sigmoid(np.dot(layers[i],syn[i])))
        elif i > 0 and i < numlayers-1:
            #for as many hidden layers there are, in a non deep learning network then this would iterate once
            syn.append(np.random.random((neurons, len(syn[i-1])))*2-1)
            layers.append(sigmoid(np.dot(layers[i],syn[i])))
        elif i == numlayers - 1:
            #synaptic weights that lead to the outputting value
            syn.append(np.random.random((len(syn[i-1]),9))*2-1)
            layers.append(sigmoid(np.dot(layers[i],syn[i])))
            print(layers[i])
    #print(syn)
    outputs[layers[numlayers -1]+1] = 1
    #print(layers)
    return outputs

class species(object):
    start_time = 0
    neurons = 0
    numlayers = 0
    alpha = 0
    dropout = False
    dp = 0

    def __init__(self,neurons,numlayers,alpha,dropout,dp):
        self.start_time = time.time()
        self.neurons = neurons
        self.numlayers = numlayers
        self.alpha = alpha
        self.dropout = dropout
        self.dp = dp
exampleGenus = species(20,2,3,True,95)
print(exampleGenus.start_time)
def predict(cell):
    #call this method like predict(board_options[(0,1)]), and it will return what number should go in that cell
    layer0 = vectorize(cell)
    outputs = [0]*len(layer0)
    choices = []
    for item in layer0:
        if item == 1:
            choices.append(item)
    guess_index = random() * len(choices)
    answer = choices[int(guess_index)]
    '''
    syn0 = np.random.random((9,20))*2-1
    syn1 = np.random.random((1,9))*2-1
    layer1 = sigmoid(np.dot(layer0,syn0))
    layer2 = sigmoid(np.dot(layer1,syn1))
    '''
    outputs[int(answer)-1] = 1
    return outputs
    #print(predict(board_options[(2,2)]))
#print(think(board_options[(0,0)],exampleGenus.neurons,exampleGenus.numlayers,exampleGenus.alpha,exampleGenus.dropout,exampleGenus.dp))
#now that we are generating guesses, attempt to solve a sudoku with an example genus
def solve_attempt(problem, test_species):
    #this is the method where we cook with gas
    possibilities = check_solution(problem)
    #pprint(possibilities)
    while(check_solution(problem) is not None):
        options = check_solution(problem)
        #pprint(options)
        counter = 0
        for row in problem:
            for cell in row:
                if cell == 0:
                   counter+= 1
        if counter == 0:
            return(problem)
        for item in options:
            #print(item)
            #this checks for mistakes, if any empty cell has no options for solutions, kill this phenotype
            #print(item)
            #print(options[item])
            if options[item] == []:
                print("trying to fail")
                return [[0]*9]*9
                
            else:
                #this makes a guess in a given cell then it reiterates based on the given information
                cell_solution = think(options[item],test_species.neurons,test_species.numlayers,test_species.alpha,test_species.dropout,test_species.dp)
                tile_value = -1
                for i in range(len(cell_solution)):
                    if cell_solution[i] == 1:
                        tile_value = i+1 
                if(tile_value == -1):
                    print("ruh-roh")
                #print(tile_value)
                pprint(problem)
                problem[item[0]][item[1]] = tile_value                
                #print(problem[item[0]][item[1]])
                #think about a solution for this tile
                
        #until we have found a perfect solution iterate through
        possibilities = options
    return problem
print(solve_attempt(test_solution, exampleGenus))
#print(grid(test_solution))
#pprint(test_solution)
#pprint(check_solution(test_solution))
#pprint(board_options)
