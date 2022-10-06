#!/usr/bin/env python
# coding: utf-8

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
    num_assignments = int(2**(int(num_variables)))
    wff = wff[2:]
    list_wff = [clause.split(",")[:-1] for clause in wff]
    final_wff = [ [int(item) for item in clause] for clause in list_wff]
    num_lit = 0
    
    for clause in final_wff:
        for item in clause:
            num_lit += 1
    
    return problem_number,num_per,satisfiable,num_variables,num_clauses,num_assignments,num_lit,final_wff


def generate_assignments(num_variables):
        
    base = [ [] ]
    values = [0, 1]
    
    if num_variables < 1:
        return base
    
    new_table = generate_assignments(num_variables-1)
    return [ next_row + [value] for next_row in new_table for value in values]


def verify(wff, assignment):
    valid = 1
    
    for clause in wff:
        valid_clause = 0
        clause_tf = []
        for item in clause:
            if item > 0:
                clause_tf.append(1)
            else:
                clause_tf.append(0)
        
        clause_tf_index = 0
        for item in clause:
            if assignment[abs(item) - 1] == clause_tf[clause_tf_index]:
                
                valid_clause = 1
                
            clause_tf_index += 1
                
        if valid_clause == 0:
            valid = 0
        
    return valid
        
    
def check_assignments(wff, assignments_list):
    satisfiable = 0
    assignment_index = 0

    for assignment in assignments_list:
        if (verify(wff, assignment) == 1):
            satisfiable = 1
            return satisfiable,assignment_index
        assignment_index += 1
    
    if satisfiable == 0:
        assignment_index = -1       

    return satisfiable,assignment_index
    

def check_against_answer_key(code_answer, given_answer):
    if code_answer == given_answer:
        return 1

    elif given_answer == '?':
        return 0

    elif code_answer != given_answer:
        return -1
        

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

def last_line_output(answers_list):
    '''
    Generates last line of output
    - Stats about wff solved
    '''
    #Generate last line of output: stats about the wff solved
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


def main():
    input_file = sys.argv[1]
    output_name = sys.argv[1].split('.')[0]+'.csv'
    problems_list = read_problems(input_file)
    test_problems_list = problems_list[:150]

    output = open(output_name, "w")
    answers_list = []

    for problem in test_problems_list:
    
        num_prob, max_per, sat, num_var, num_clause, num_as, num_lit, wff = parse_problem(problem)
        print("Working on problem " + str(num_prob) +" ....")
        time1 = time.time()*1000000

        assignments = generate_assignments(num_var)
        satisfiable, assignment_index = check_assignments(wff, assignments)

        time2 = time.time()*1000000

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