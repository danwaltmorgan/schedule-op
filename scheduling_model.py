# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 17:13:02 2020

@author: ltdan
"""

from ortools.sat.python import cp_model

def main():
    
    #define the variables
    residents = 3
    shifts = 21
    days = 7
    weeks = 1
    total_residents = range(residents)
    total_shifts = range(shifts)
    total_days = range(days)
    total_weeks = range(weeks)
    shift_requests = [[0, 1, 0, 0, 1, 0, 1, 
                       1, 0, 0, 1, 0, 1, 1,
                       0, 1, 1, 0, 1, 0, 1],
                      [0, 1, 0, 0, 1, 0, 1, 
                       1, 0, 0, 1, 0, 1, 1,
                       0, 1, 1, 0, 1, 0, 1],
                      [0, 1, 0, 0, 1, 0, 1, 
                       1, 0, 0, 1, 0, 1, 1,
                       0, 1, 1, 0, 1, 0, 1],]
    
        
    min_per_shift = 1
    max_per_shift = 2

    num_shifts_req = 0
    
    for r in total_residents:
        for s in total_shifts:
            num_shifts_req += shift_requests[r][s]


    
    #create the model
    shift_model = cp_model.CpModel()


    x = {}
    for r in total_residents:
        for s in total_shifts:
            x[(r,s)] = shift_model.NewBoolVar('x_r%is%i' % (r,s))
            
    
    
    #Contraints
    
    #Every shift must have at least min_per_shift residents and less
    ##than max_per_shift
    for s in total_shifts:
       shift_model.Add(sum(x[r,s] for r in total_residents) >= min_per_shift)
       shift_model.Add(sum(x[r,s] for r in total_residents) <= max_per_shift)
      
                
    #for r in total_residents:
        #for w in total_weeks:
    
    for r in total_residents:
        if(r == 1):
            shift_model.Add(sum(x[r, s] for s in total_shifts) <= 1)

        
    
    

    #Opjective
    shift_model.Maximize(
        sum(shift_requests[r][s] * x[(r,s)] for r in total_residents
            for s in total_shifts))
    
    #Solver
    solver = cp_model.CpSolver()
    solver.Solve(shift_model)
    
    for r in total_residents:
        print('Resident ', r)
        for s in total_shifts:
            if solver.Value(x[(r,s)]) == 1:
                if shift_requests[r][s] == 1:
                    print('Resident ', r, ' works shift ', s, ' (requested)' )
                else:
                    print('Resident ', r, ' works shift ', s, ' (not requested)')
        print()
        
    #Stats
    print()
    print('Statistics')
    print('Number of requests met = %i' % solver.ObjectiveValue(),
          '(out of %i)' % num_shifts_req)
    
    print(x[r,s])
    

if __name__ == '__main__':
    main()

