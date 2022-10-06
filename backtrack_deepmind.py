#!usr/bin/env python3

class Stack_Member_Attributes:
    def __init__(self) -> None:
        self.assignment= None
        self.bothTried= False

        
'''
Say we took this example:

    c 1 2 U
    p cnf 4 10
    -2,-3,0
    4,4,0
    -2,-4,0
    4,1,0
    -3,1,0
    -1,-1,0
    -4,-4,0
    2,-4,0
    -3,2,0
    -3,-4,0

    problem_number = 1
    num_per        = 2
    satisfiable    = 'U'
    num_variables  = 4
    num_clauses    = 10

    wff = [[-2, -3], [4, 4], [-2, -4], [4, 1], [-3, 1], [-1, -1], [-4, -4], [2, -4], [-3, 2], [-3, -4] ]




for i in range(num_variables):
    str(i) = Stack_Member_Attributes()


stack = []
possible_solution = [0] * num_variables #Edit this until something gives, then return this


def backtracking(wff, k, num_per, num_clauses, possible_solution):


    for clause in wff: 

        for i in range(num_per): #num_per being the number of  literals per clause

            if abs(clause[i])== int(k): #if we match one of the literals with the current k

                if clause[i] > 0 and k.assignment == 0:
                    
                    possible_solution[k] = 0


'''