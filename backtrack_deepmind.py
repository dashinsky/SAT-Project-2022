#!usr/bin/env python3

import time
import sys

def read_problems(filename):
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
    answer = [str(num_prob),str(num_var),str(num_clause),str(max_per),str(num_lit)]
    
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
            if literal in curr_assignment and curr_assignment[literal] == 1:
                count += 1
                break
            elif literal < 0 and (-literal) in curr_assignment and curr_assignment[literal] == 0:
                count += 1
                break
    
    return count


def check_answer_key(found, given):
    if found == given:
        return 1
    elif given == '?':
        return 0
    elif found != given:
        return -1


def solve_sat(problem):
    num_prob, max_per, sat, num_var, num_clause, num_lit, wff = parse_problem(problem)
    time1 = time.time()*1000000
    satisfiable, assignment = backtracking_sat(wff, max_per, num_var, num_clause, num_lit, [[num_var, 1, False]])
    time2 = time.time()*1000000
    completion_time = time2-time1

    result = check_answer_key(satisfiable, sat)
    problem_answer = format_output(num_prob, num_var, num_clause, max_per, num_lit, satisfiable, result, completion_time, assignment)



def backtracking_sat(wff, max_per, num_var, num_clause, num_lit, stack):
    '''
    Flow of the function:
        - assign the value to num_var 
            - start with 1, push to stack
            - if we have to go back assign it to 0 and change the stack accordingly ()
            - if both values tried, pop it from the stack
        - after each new assignment, check the number of clauses that satisfy (check_assignment function based on the stack)
            - if number = num_clause return => we found an assignment that satisfies
        - if stack is empty

    '''
    # Base cases
    if not stack:
        return False, []

    if count_sat_clauses(wff, stack) == num_clause:
        return True, stack

    if num_var <= 0:
        return False, stack

    # Recursive case
    stack.append([num_var - 1, 1, False])
    flag, path = backtracking_sat(wff, max_per, num_var-1, num_clause, num_lit, stack)

    if flag == True:
        return True, path

    elif flag == False:
        if stack[-1][-1] == False:
            stack[-1][1] = 0
            stack[-1][-1] = True
            backtracking_sat(wff, max_per, num_var-1, num_clause, num_lit, stack)
        else:
            stack.pop()
        return False, stack


def main():
    input_file = sys.argv[1]
    output_name = sys.argv[1].split('.')[0]+'.csv'
    problems_list = read_problems(input_file)
    test_problems_list = problems_list[:150]

    output = open(output_name, "w")
    answers_list = []

    for problem in test_problems_list:
        solve_sat(problem)
        # num_prob, max_per, sat, num_var, num_clause, num_lit, wff = parse_problem(problem)
        #time1 = time.time()*1000000

        #assignments = generate_assignments(num_var)
        #satisfiable, assignment_index = check_assignments(wff, assignments)

        # time2 = time.time()*1000000

        '''
        completion_time = time2-time1
    
        if assignment_index == -1:
            valid_assignment = []
        else:
            valid_assignment = assignments[assignment_index]

        if sat == 'U':
            sat_num = 0
        elif sat == 'S':
            sat_string = 1
        
        if satisfiable == 1:
            satisfiable_string = 'S'
        elif satisfiable == 0:
            satisfiable_string = 'U'
        
        test_result = check_against_answer_key(satisfiable_string, sat)
    
        problem_answer = format_output(num_prob, num_var, num_clause, max_per, num_lit, satisfiable, test_result, completion_time, valid_assignment)
    
        output.write(problem_answer+'\n')
        answers_list.append(problem_answer)

    last_line_csv = last_line_output(answers_list)

    output.write(last_line_csv+'\n')
    output.close()
    '''

if __name__ == "__main__":
    main()