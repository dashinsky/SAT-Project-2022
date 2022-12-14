#!usr/bin/env python3

import time
import sys
import random

def read_problems(filename):
    '''
    Reads in the correct input format
    '''
    with open(filename) as ksat:
        lines = ksat.read()
        split = lines.split('c ')

    wffs = []
    for line in split:
        wffs.append(line.split('\n'))

    for wff in wffs:
        while("" in wff):
            wff.remove("")
    wffs = [wff for wff in wffs if wff != []]
    
    return wffs


def parse_problem(wff):
    '''
    Parses through the list of problems
    '''
    problem_info = wff[0].split()
    problem_number = int(problem_info[0])
    num_per = int(problem_info[1])
    
    if len(problem_info) == 3:
        satisfiable = problem_info[2]
    else:
        satisfiable = "NA"

    cnf_info = wff[1].split()
    num_variables = int(cnf_info[2])
    num_clauses = int(cnf_info[3])
    wff = wff[2:]
    list_wff = [clause.split(",")[:-1] for clause in wff]
    final_wff = [ [int(item) for item in clause] for clause in list_wff]
    num_lit = 0
    
    for clause in final_wff:
        for item in clause:
            num_lit += 1
    
    return problem_number,num_per,satisfiable,num_variables,num_clauses,num_lit,final_wff   


def format_output(num_prob, num_var, num_clause, max_per, num_lit, satisfiable, result, completion_time, assignment): 
    '''
    Creates the output according to the format
    '''
    answer = [str(num_prob),str(num_var),str(num_clause),str(max_per),str(num_lit)]
    
    sat_string = ''
    if satisfiable == 1:
        sat_string = 'S'
    elif satisfiable == -1:
        sat_string = 'U'
        
    answer.append(sat_string)
    answer.append(str(result))
    answer.append(str(completion_time))
    
    for value in assignment:
        answer.append(str(value))
                
    return ','.join(answer)


def last_line_output(answers_list):
    '''
    Generates last line of output: Stats about wff solved
    '''
    total_wffs = 0
    satisfiable_wffs = 0
    answers_provided  = 0
    num_correct_answered = 0
    file_name = sys.argv[1].split('.')[0]

    for entry in answers_list:
        total_wffs += 1

        entry_list = entry.split(',')
        print(entry_list)
    
        if entry_list[5] == 'S':
            satisfiable_wffs += 1
        if entry_list[6] != 0:
            answers_provided += 1
        if entry_list != -1 and entry_list[6] != 0:
            num_correct_answered += 1
        
    unsatisfiable_wffs = total_wffs - satisfiable_wffs

    return ','.join([str(file_name), 'deepmind', str(total_wffs), str(satisfiable_wffs), str(unsatisfiable_wffs), str(answers_provided), str(num_correct_answered)])


def count_sat_clauses(wff, stack):
    '''
    Returns the number of clauses that are satisfied
    '''
    curr_assignment = {}
    count = 0

    for var in stack:
        curr_assignment[var[0]] = var[1]

    for clause in wff:
        for literal in clause:
            if literal in curr_assignment.keys() and curr_assignment[literal] == 1:
                count += 1
                break
            elif literal < 0 and (-literal in curr_assignment.keys()) and curr_assignment[-literal] == 0:
                count += 1
                break
    
    return count


def optimize_stack(wff, stack):
    curr_assignment = {}
    count = 0

    for var in stack:
        curr_assignment[var[0]] = var[1]

    for clause in wff:
        p = clause[0]
        q = clause[1]

        # Case when first literal is false and the other has no assignment
        if ((p in curr_assignment.keys() and curr_assignment[p] == 0) or (-p in curr_assignment.keys() and curr_assignment[-p] == 1)) and (q not in curr_assignment):
            if q < 0:
                stack.append([-q, 0, True])
            else:
                stack.append([q, 1, True])

        # Case when second literal is false and the other has no assignment
        if ((q in curr_assignment.keys() and curr_assignment[q] == 0) or (-q in curr_assignment.keys() and curr_assignment[-q] == 1)) and (p not in curr_assignment):
            if p < 0:
                stack.append([-p, 0, True])
            else:
                stack.append([p, 1, True])
        

def check_false_clause(wff, stack):
    curr_assignment = {}

    for var in stack:
        curr_assignment[var[0]] = var[1]

    for clause in wff:
        p = clause[0]
        q = clause[1]
        if p in check_


def check_against_answer_key(found, given):
    '''
    Checks the computer answer against the answer key
    '''
    if found == given:
        return 1
    elif given == '?':
        return 0
    elif found != given:
        return -1


def twosat_solver(wff, num_var, num_clauses):
    global stack
    stack.append([num_var, 1])
    sat_clauses = count_sat_clauses(wff, stack)
    false_clauses = check_false_clause(wff, stack)

    while sat_clauses < num_clauses and false_clauses == 0:
        optimize_stack(wff, stack)
        new_sat_clauses = count_sat_clauses(wff, stack)

        if new_sat_clauses == sat_clauses:
            # pick random variable to assign to 0 or 1



def backtracking_sat(wff, num_var, num_clause):
    '''
    flag - represents the state where:
    1 - satisfiable, 0 - continue, -1 - unsatisfiable
    '''
    global stack

    # Base cases
    if not stack:
        return -1

    if num_var <= 0:
        return 0

    if count_sat_clauses(wff, stack) == num_clause:
        return 1

    # Recursive cases
    if [num_var - 1, 1, ]
    stack.append([num_var - 1, 1, False])
    optimize_stack(wff, stack)
    flag = backtracking_sat(wff, num_var-1, num_clause)

    while True:
        if flag == 1 or flag == -1:
            return flag

        elif flag == 0:
            if stack[-1][-1] == True:
                stack.pop()
                if len(stack) == 0:
                    return -1
            else:
                stack[-1][1] = 0
                stack[-1][-1] = True
                flag = backtracking_sat(wff, stack[-1][0], num_clause)


def generate_assignment(stack, num_var):
    '''Generates the full assignment based on the stack (partial assignment that SATs)'''
    assignment = []
    for line in stack:
        assignment.append(line[1])
    for i in range(num_var - len(stack)):
        assignment.append(0)
    assignment.reverse()

    return assignment


# Global Variables
stack = []

def main():
    global stack
    input_file = sys.argv[1]
    output_name = sys.argv[1].split('.')[0]+'_backtrack.csv'
    problems_list = read_problems(input_file)

    test_problems_list = problems_list[:20]

    output = open(output_name, "w")
    answers_list = []

    for problem in test_problems_list:
        num_prob, max_per, sat, num_var, num_clause, num_lit, wff = parse_problem(problem)
        time1 = time.time()*1000000
    
        # returns whether the wff is satisfiable
        # stack - assignment (empty if UNSAT)
        stack = [[num_var, 1, False]]
        satisfiable = backtracking_sat(wff, num_var, num_clause)

        time2 = time.time()*1000000
        completion_time = time2-time1
        
        assignment = generate_assignment(stack, num_var) if satisfiable == 1 else []

        if satisfiable == 1:
            satisfiable_string = 'S'
        elif satisfiable == -1:
            satisfiable_string = 'U'
        
        #Check if program matches answer key
        test_result = check_against_answer_key(satisfiable_string, sat)
    
        #Generate answer string
        problem_answer = format_output(num_prob, num_var, num_clause, max_per, num_lit, satisfiable, test_result, completion_time, assignment)
    
        #Write answer string to file
        output.write(problem_answer+'\n')
        answers_list.append(problem_answer)

    output.write(last_line_output(answers_list)+'\n')
    output.close()

if __name__ == "__main__":
    main()