#!/usr/bin/env python

import sys
import time
# coding: utf-8




#Read in CNF DIMACS file, and separate each problem into its own list
def read_problems(filename):
    #Open the file
    with open(filename) as ksat:
    
        #Read the file
        lines = ksat.read()
    
        #Split into problems by looking for c
        split = lines.split('c ')

    
    #Split by newline
    wffs = []
    for line in split:
        wffs.append(line.split('\n'))

    #Remove empty strings, and empty lists left over
    for wff in wffs:
        while("" in wff):
            wff.remove("")
    wffs = [wff for wff in wffs if wff != []]

    #Print to check formatting (can be taken out in performance run)
    #for line in wffs:
        #print(line)
        
    return wffs
        


#Function to read in a particular problem in a usable format

def parse_problem(wff):
    
    #Split the "c" line so we can parse 
    problem_info = wff[0].split()
    
    #Get problem number
    problem_number = int(problem_info[0])
    
    
    #Get max num literals per clause
    num_per = int(problem_info[1])
    
    
    #If included, get whether known to be satisfiable or unsatisfiable (test cases)
    if len(problem_info) == 3:
        satisfiable = problem_info[2]
    else:
        satisfiable = "NA"

    
    #After we've done this, parse the p line
    cnf_info = wff[1].split()
    
    #Get total num variables
    num_variables = int(cnf_info[2])
    
    
    #Get total num clauses
    num_clauses = int(cnf_info[3])

        
    #From number of variables, generate number of possible assignment combos
    num_assignments = int(2**(int(num_variables)))

    
    #After parsing the p line, remove the c and p lines so we just have the clauses
    wff = wff[2:]
    
    
    #Transform each clause to a list, getting rid of zeros
    
    #Convert strings of clauses to list format, removing zeros
    list_wff = [clause.split(",")[:-1] for clause in wff]
       
    #Convert individual variables from strings to ints
    final_wff = [ [int(item) for item in clause] for clause in list_wff]
    
    #Count total number of literals
    num_lit = 0
    for clause in final_wff:
        for item in clause:
            num_lit += 1
        
    
    return problem_number,num_per,satisfiable,num_variables,num_clauses,num_assignments,num_lit,final_wff




#Function to generate all possible assignments for a given number of variables
def generate_assignments(num_variables):
        
    base = [ [] ]
    values = [0, 1]
    
    if num_variables < 1:
        return base
    
    #recursive call
    new_table = generate_assignments(num_variables-1)
    return [ next_row + [value] for next_row in new_table for value in values]
    



def verify(wff, assignment):
    
    valid = 1
    
    
    #Big for loop
    #Default of valid_clause = 0 for EACH CLAUSE
    #Create an array going from 1 to num variables
    #Set each to its zero or one value
    #Cycle through clause and look at each literal
    #Determine its t/f value (e.g. seeing -4 gives 0)
    #Compare its value with assignment value (given by assignment[abs(literal) - 1])
    #E.g. continuing above example, the assignment value for the variable 4 would be 
    #assignment[abs(-4) -1] (the 4th entry in the assignment list)
    #If one such assignment matches in a clause, then switch the for loop 
    #flag variable to 1 (since one literal in the clause matching makes the clause valid)
    
    for clause in wff:
        #set default to zero (the clause is not satisfied by the assignment)
        valid_clause = 0
        
        #Collect whether each value in the clause is true or false
        clause_tf = []
        for item in clause:
            if item > 0:
                clause_tf.append(1)
            else:
                clause_tf.append(0)
                
        
        clause_tf_index = 0
        
        #Check each variable's t/f value against its assignment
        for item in clause:
            if assignment[abs(item) - 1] == clause_tf[clause_tf_index]:
                
                #If they are the same, then the clause is valid
                valid_clause = 1
                
            #Increment to check next literal
            clause_tf_index += 1
                
        

        #If no valid match has been found, the clause fails and is unsatisfiable with the given assignment
        if valid_clause == 0:
            valid = 0
        
    return valid
        
        




#Loop through the possible assignments, and see if any of them satisfy the wff
def check_assignments(wff, assignments_list):
    satisfiable = 0
    
    #Check if either value assignment matches in the clause, and keep 
    #track of which assignment satisfies
    
    assignment_index = 0
    for assignment in assignments_list:
        if (verify(wff, assignment) == 1):
            satisfiable = 1
            
            #Return satisfiable with the assignment that satisfies
            return satisfiable,assignment_index
        
        assignment_index += 1
    
    #If no assignment found, set assignment_index to -1
    if satisfiable == 0:
        assignment_index = -1       

    return satisfiable,assignment_index
    



def check_against_answer_key(code_answer, given_answer):
        
    #If they agree
    
    if code_answer == given_answer:
        return 1
    elif given_answer == '?':
        return 0
    elif code_answer != given_answer:
        return -1
        



#Output function: takes the relevant variables and formats the output into CSV
def format_output(num_prob, num_var, num_clause, num_per, num_lit, sat, test_result, completion_time, values):
    
    answer = [str(num_prob),str(num_var),str(num_clause),str(num_per),str(num_lit)]
    
    sat_string = ''
    if sat == 1:
        sat_string = 'S'
    elif sat == 0:
        sat_string = 'U'
        
        
    answer.append(sat_string)
    
    answer.append(str(test_result))
    
    answer.append(str(completion_time))
    
    for value in values:
        answer.append(str(value))
                  
    
        
    return ','.join(answer)






import time

#Execution: run all functions on the first several wff problems

#1: Read in the problems from the file
input_file = sys.argv[1]

output_name = sys.argv[1].split('.')[0]+'.csv'

problems_list = read_problems(input_file)


#1.1: (for testing): select only the first xx problems to try
test_problems_list = problems_list[:150]

#1.2 open output file
output = open(output_name, "w")
answers_list = []

#2: Loop through the problems
for problem in test_problems_list:
    
    #Parse the problem for relevant variables
    num_prob, max_per, sat, num_var, num_clause, num_as, num_lit, wff = parse_problem(problem)
    
    
    
    #Start time check for wff
    time1 = time.time()*1000000
    
    #Generate the possible assignments for the problem
    assignments = generate_assignments(num_var)
     
    #check each assignment to find a valid one (if it exists)
    satisfiable, assignment_index = check_assignments(wff, assignments)
    #print(satisfiable)
    
    #End time check for wff
    time2 = time.time()*1000000
    
    #Calculate total time elapsed
    completion_time = time2-time1
    
    #Get the matching assignment, if one exists
    if assignment_index == -1:
        valid_assignment = []
    else:
        valid_assignment = assignments[assignment_index]
           
    #Convert numerical t/f to 'S' or 'S'    
    if sat == 'U':
        sat_num = 0
    elif sat == 'S':
        sat_string = 1
        
    if satisfiable == 1:
        satisfiable_string = 'S'
    elif satisfiable == 0:
        satisfiable_string = 'U'
        
    #Check if program matches answer key
    test_result = check_against_answer_key(satisfiable_string, sat)
    
    #Generate answer string
    problem_answer = format_output(num_prob, num_var, num_clause, max_per, num_lit, satisfiable, test_result, completion_time, valid_assignment)
    
    
    #Write answer string to file
    output.write(problem_answer+'\n')
    answers_list.append(problem_answer)
    
file_name = sys.argv[1].split('.')[0]

#Generate last line of output: stats about the wff solved
total_wffs = 0

satisfiable_wffs = 0
answers_provided  = 0
num_correct_answered = 0

for entry in answers_list:
    total_wffs += 1

    entry_list = entry.split(',')
   
    
    if entry_list[5] == 'S':
        satisfiable_wffs += 1
    if entry_list[6] != 0:
        answers_provided += 1
    if entry_list != -1 and entry_list[6] != 0:
        num_correct_answered += 1
        
unsatisfiable_wffs = total_wffs - satisfiable_wffs

last_line_list = [str(file_name), 'deepmind', str(total_wffs), str(satisfiable_wffs), str(unsatisfiable_wffs), str(answers_provided), str(num_correct_answered)]

last_line_csv = ','.join(last_line_list)

#Write last line to file
output.write(last_line_csv+'\n')

 
#Close output file
output.close()
    
    
    
        

