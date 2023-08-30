from types import SimpleNamespace

import numpy as np
from scipy import optimize

import pandas as pd 
import matplotlib.pyplot as plt

class opg2_class:
    def __init__(self):
        """ setup model """

        par = self.par = SimpleNamespace()
        sol = self.sol = SimpleNamespace()

        par.epsilon = 10.0
        par.e_A = 10
        par.e_B = 10
        par.eta = 10

        par.p_vec = np.linspace(1,2,10000)

        sol.c_mark_vec = np.zeros(par.p_vec.size)
        sol.c_mark_q3 = 0  # Initialize c_mark_q3
        sol.p_star = 0  # Initialize p_star

    def utility_A(self,c_mark):
        par = self.par
        sol = self.sol
        U_A = par.e_A - par.p*c_mark + (c_mark**(1-1/par.epsilon))/(1-1/par.epsilon)
        return U_A
    
    def solve_U_A(self):
        par = self.par
        sol = self.sol
        opt = SimpleNamespace()
        def obj_A(x):
            return - self.utility_A(x[0])
        res = optimize.minimize(obj_A, x0=1, method="Nelder-Mead")
        opt.c_mark = res.x[0]
        return opt
    
    def solve_p_vec(self):
        sol = self.sol
        par = self.par
        for it, p in enumerate(par.p_vec):
            par.p = p
            res = self.solve_U_A()
            sol.c_mark_vec[it] = res.c_mark

        return sol.c_mark_vec


    #Analytical method
    def utility_B(self,p):
        par = self.par
        sol = self.sol
        U_A = par.e_A - p**(-par.epsilon) + (p*p**(-par.epsilon))**(1-1/par.epsilon)/(1-1/par.epsilon)
        return U_A
    
    def solve_U_B(self):
        par = self.par
        sol = self.sol
        opt = SimpleNamespace()
        def obj_B(x):
            return - self.utility_B(x[0])
        res = optimize.minimize(obj_B, x0=1, method="Nelder-Mead")
        opt.p = res.x[0]
        return opt
    


    #Question 3
    def utility_A_q3(self, c_mark_q3, p):
        par = self.par
        U_A_q3 = (par.e_A - p * c_mark_q3)**(1 - 1 / par.eta) / (1 - 1 / par.eta) + c_mark_q3**(1 - 1 / par.epsilon) / (1 - 1 / par.epsilon)
        return U_A_q3
    
    def solve_U_A_q3(self):
        par = self.par
        sol = self.sol
        opt = SimpleNamespace()
        def obj_A_q3(x):
            return -self.utility_A_q3(sol.c_mark_q3, x[0])
        res_first = optimize.minimize(obj_A_q3, x0=1, method="Nelder-Mead")
        sol.c_mark_q3 = res_first.x[0]
        return sol
    
    def utility_B_q3(self, c_mark_q3, p):
        par = self.par
        sol = self.sol
        U_B_q3 = (par.e_B - p * c_mark_q3)**(1 - 1 / par.eta) / (1 - 1 / par.eta) + c_mark_q3**(1 - 1 / par.epsilon) / (1 - 1 / par.epsilon)
        return U_B_q3
    
    def solve_U_B_q3(self):
        par = self.par
        sol = self.sol
        opt = SimpleNamespace()
        def obj_B_q3(x):
            return -self.utility_B_q3(sol.c_mark_q3, x[0])
        
        # Find optimal p that maximizes U_B_q3 given c_mark_q3
        res_last = optimize.minimize(obj_B_q3, x0=1, method="Nelder-Mead")
        sol.p_star = res_last.x[0]
        return sol


