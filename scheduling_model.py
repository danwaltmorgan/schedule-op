# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 17:13:02 2020

@author: ltdan
"""

from ortools.sat.python import cp_model
import numpy as np

def main():
    
    #define the variables
    residents = 3
    weeks = 2
    days = 7
    shifts = 3
    num_res = range(residents)
    num_weeks = range(weeks)
    num_days = range(days)
    num_shift = range(shifts)
    
    shift_requests = np.random.randint(2, size = (residents, weeks, days, shifts))
    
    min_per_shift = 1
    max_per_shift = 2
    
        
    
    #create the model
    shift_model = cp_model.CpModel()


    #Decision Variables
    
    x = {}
    for r in num_res:
        for w in num_weeks:
            for d in num_days:
                for s in num_shift:
                    x[(r, w, d, s)] = shift_model.NewBoolVar('x_r%iw%id%is%i' % (r, w, d, s))
    
    
    #Contraints
    
    # min and max per shift
    
    for w in num_weeks:
        for d in num_days:
            for s in num_shift:
                shift_model.Add(sum(x[r,w,d,s] for r in num_res) >= min_per_shift)
                shift_model.Add(sum(x[r,w,d,s] for r in num_res) <= min_per_shift)
    
   
    # max shifts per week
    for r in num_res:
        for w in num_weeks:
            shift_model.Add(sum(x[r, w, d, s] 
                                for d in num_days
                                for s in num_shift) <= 10)
        
    #max days per week
    for r in num_res:
        for w in num_weeks:
            shift_model.Add(sum(x[r, w, d, s] for d in num_res) <= 6)
    

    #Opjective
    
    shift_model.Maximize(
        sum(shift_requests[r][w][d][s] * x[(r, w, d, s)] 
            for r in num_res
            for w in num_weeks
            for d in num_days
            for s in num_shift))
   
    #Solver
    solver = cp_model.CpSolver()
    solver.Solve(shift_model)
    
    for r in num_res:
        total_shifts = 0
        print('Resident %i' % r )
        for w in num_weeks:
            week_shifts = 0
            print("Week %i" % w)
            for d in num_days:
                week_shifts += 1
                print("Day %i" % d)
                for s in num_shift:
                    if solver.Value(x[(r, w, d, s)]) == 1:
                        total_shifts += 1
                        if shift_requests[r][w][d][s] == 1:
                            print("Resident %i works shift %i, (requested)" % (r, s))
                        else:
                            print("Resident %i works shift %i, (no requested)" % (r, s))
                print()
            print("Week shift: ", week_shifts)
            print()
        print("Total shifts: ", total_shifts)
        print()
        
    #Stats
    num_shift_req = 0 
    
    for r in num_res:
        for w in num_weeks:
            for d in num_days:
                for s in num_shift:
                    num_shift_req += shift_requests[r][w][d][s]
    
    print()
    print('Statistics')
    print('Number of requests met = %i' % solver.ObjectiveValue(),
          '(out of %i)' % num_shift_req)
    print("Walltime: %f s" %solver.WallTime())
    

if __name__ == '__main__':
    main()

