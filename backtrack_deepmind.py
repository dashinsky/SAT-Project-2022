#!usr/bin/env python3

import time
import sys

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
    elif satisfiable == 0:
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
    file_name = sys.argv[1].split('.')[0]
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

'''
def solve_sat(problem):
    num_prob, max_per, sat, num_var, num_clause, num_lit, wff = parse_problem(problem)
    time1 = time.time()*1000000
    satisfiable, assignment = backtracking_sat(wff, max_per, num_var, num_clause, num_lit, [[num_var, 1, False]])
    time2 = time.time()*1000000
    completion_time = time2-time1

    result = check_against_answer_key(satisfiable, sat)
    problem_answer = format_output(num_prob, num_var, num_clause, max_per, num_lit, satisfiable, result, completion_time, assignment)
'''

def backtracking_sat(wff, num_var, num_clause):
    '''
    flag - represents the state where:
    1 - satisfiable, 0 - continue, -1 - unsatisfiable
    '''
    global stack

    # Base cases
    if not stack:
        return -1

    if count_sat_clauses(wff, stack) == num_clause:
        return 1

    if num_var <= 0:
        return 0

    # Recursive cases
    stack.append([num_var - 1, 1, False])
    flag = backtracking_sat(wff, num_var-1, num_clause)

    while True:
        if flag == 1 or flag == -1:
            return flag

        elif flag == 0:
            if stack[-1][-1] == True:
                if len(stack) == 1:
                    return -1
                stack.pop()
            else:
                stack[-1][1] = 0
                stack[-1][-1] = True
                flag = backtracking_sat(wff, num_var-1, num_clause)

# Global Variables
stack = []

def main():
    global stack
    input_file = sys.argv[1]
    output_name = sys.argv[1].split('.')[0]+'_backtrack.csv'
    problems_list = read_problems(input_file)

    test_problems_list = problems_list[:150]

    output = open(output_name, "w")
    answers_list = []

    for problem in test_problems_list:
        num_prob, max_per, sat, num_var, num_clause, num_lit, wff = parse_problem(problem)
        time1 = time.time()*1000000
    
        # returns whether the wff is satisfiable and the assignment that works
        # if unsatisfiable => assignment = []
        stack = [[num_var, 1, False]]
        satisfiable = backtracking_sat(wff, num_var, num_clause)
        assignment = stack

        time2 = time.time()*1000000
        completion_time = time2-time1
           
        #Convert numerical t/f to 'S' or 'S'  
        '''
        if sat == 'U':
            sat_num = 0
        elif sat == 'S':
            sat_string = 1
        '''
        
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