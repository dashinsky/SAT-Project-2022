#!/usr/bin/env python
# coding: utf-8

#Test comment and github!

# In[283]:


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
        


# In[284]:


#Test function execution
#problems_list = read_problems('kSAT.cnf')


# In[285]:


#Function to read in a particular problem in a usable format

def parse_problem(wff):
    
    #Split the "c" line so we can parse 
    problem_info = wff[0].split()
    
    #Get problem number
    problem_number = int(problem_info[0])
    
    #TEST
    #print("Problem number: " + str(problem_number))
    
    #Get max num literals per clause
    num_per = int(problem_info[1])
    
    #TEST
    #print("Max literals per clause: " + str(num_per))
    
    #If included, get whether known to be satisfiable or unsatisfiable (test cases)
    if len(problem_info) == 3:
        satisfiable = problem_info[2]
    else:
        satisfiable = "NA"
    #print(satisfiable)
    
    #TEST
    #print("Satisfiable: " + str(satisfiable))
    
    #After we've done this, parse the p line
    cnf_info = wff[1].split()
    
    #Get total num variables
    num_variables = int(cnf_info[2])
    
    #TEST
    #print("Number of variables: " + str(num_variables))
    
    #Get total num clauses
    num_clauses = int(cnf_info[3])
    
    #TEST
    #print("Number of clauses: " + str(num_clauses))
    
    
    #From number of variables, generate number of possible assignment combos
    num_assignments = int(2**(int(num_variables)))
    
    #TEST
    #print("Number of possible assignments: " + str(num_assignments))
    
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
        
    #TEST
    #print("Total number of literals: " + str(num_lit))
    
    #TEST
    #print(final_wff)
    
    return problem_number,num_per,satisfiable,num_variables,num_clauses,num_assignments,num_lit,final_wff


# In[286]:


#Test parse function's execution
#Argument: a member of the list of wffs (read in from original file)
#Unpack tuple into variables

#prob_num, max_per, sat, num_var, num_clause, num_as, num_lit, wff = parse_problem(problems_list[2])


# In[287]:


#Function to generate all possible assignments for a given number of variables
def generate_assignments(num_variables):
        
    base = [ [] ]
    values = [0, 1]
    
    if num_variables < 1:
        return base
    
    #recursive call
    new_table = generate_assignments(num_variables-1)
    return [ next_row + [value] for next_row in new_table for value in values]
    


# In[288]:


#assignments = generate_assignments(num_var)

#TEST
#print(assignments)


# In[289]:


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
        
        


# In[290]:


#TEST
#wff is whichever wff is run through the parse program above
#assignments[index] is whichever assignment generated above you would like to test
#satisfiable = verify(wff, assignments[2])


# In[291]:


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
    


# In[292]:


#TEST 
#is_wff_satisfiable, assignment = check_assignments(wff, assignments)

#TEST
#print(is_wff_satisfiable)


# In[293]:


def check_against_answer_key(code_answer, given_answer):
        
    #If they agree  
    if code_answer == given_answer:
        return 1

    #accounts for the case where there is no answer key
    elif given_answer == '?':
        return 0

    elif code_answer != given_answer:
        return -1
        


# In[300]:


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



# In[ ]:


import time
import sys

#Execution: run all functions on the first several wff problems

#0 parse command line argument
input_file = sys.argv[1]

#1: Read in the problems from the file
problems_list = read_problems(input_file)

#1.1: (for testing): select only the first 10 problems to try
test_problems_list = problems_list[:50]

#1.2: Open output file
output = open("answer.csv", "a")


#2: Loop through the problems
for problem in problems_list:
    
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
    
    #Print answer string
    #print(problem_answer)

    #Write answer string to file
    output.write(problem_answer+'\n')

