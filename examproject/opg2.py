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
        par.p = 1
        par.eta = np.linspace(1000, 10, 990)
        par.eta_ = (1-1/par.eta)

        par.p_vec = np.linspace(1,2,10000)

        self.combined_list = []

        sol.c_mark_vec = np.zeros(par.p_vec.size)

    def utility_A(self,c_mark):
        par = self.par
        sol = self.sol
        U_A = par.e_A - par.p*c_mark + c_mark**(1-1/par.epsilon)/(1-1/par.epsilon)
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

        self.combined_list = [(p, num) for p, num in zip(par.p_vec, sol.c_mark_vec)]

        return sol.c_mark_vec
    
    #list forsog
    def utility_B_list(self):
        par = self.par
        sol = self.sol
        for p_val, num in self.combined_list:
            p = p_val
            c_mark = num
            U_B = par.e_B - p * c_mark + c_mark**(1 - 1 / par.epsilon) / (1 - 1 / par.epsilon)
            sol.U_B[p_val] = U_B
        return sol.U_B


    #Numerical 
    # Numerical utility function for B
    def utility_B_num(self):
        par = self.par
        sol = self.sol
        U_B = par.e_B - sol.c_mark_vec + (par.p_vec * sol.c_mark_vec)**(1 - 1 / par.epsilon) / (1 - 1 / par.epsilon)
        return U_B

    # Solve for optimal p using numerical optimization
    def solve_U_B_num(self):
        par = self.par
        sol = self.sol
        opt = SimpleNamespace()
        
        def obj_B_num(p):
            par.p_vec = p
            return -self.utility_B_num()

        result = optimize.minimize(obj_B_num, method="Nelder-Mead", bounds=[(1, 2)])
        opt.p = result.x
        return opt



    #Analytical
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
    

    def utility_q3(self,c_mark_q3):
        par = self.par
        sol = self.sol
        U_A_q3 = (par.e_A - par.p*c_mark_q3)**par.eta_/par.eta_ + c_mark_q3**(1-1/par.epsilon)/(1-1/par.epsilon)
        return U_A_q3
    
    def solve_U_A_q3(self):
        par = self.par
        sol = self.sol
        opt = SimpleNamespace()
        def obj_A(x):
            return - self.utility_A(x[0])
        res = optimize.minimize(obj_A, x0=1, method="Nelder-Mead")
        opt.c_mark = res.x[0]
        return opt


