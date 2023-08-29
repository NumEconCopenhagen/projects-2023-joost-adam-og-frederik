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

        par.p_vec = np.linspace(1,2)

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
        return sol.c_mark_vec
    
    #Numerical 
    def utility_B_num(self):
        par = self.par
        sol = self.sol
        opt = SimpleNamespace()
        self.solve_U_A()
        self.solve_p_vec()
        U_B = par.e_B - sol.c_mark_vec + (par.p_vec*sol.c_mark_vec)**(1-1/par.epsilon)/(1-1/par.epsilon)
        return U_B
    
    def solve_U_B_num(self):
        par = self.par
        sol = self.sol
        opt = SimpleNamespace()
        def obj_B_num(x):
            par.p_vec = x[0]
            return - self.utility_B_num(x[0])
        result = optimize.minimize(obj_B_num, x0=1.5, method="Nelder-Mead", bounds=(1,2))
        opt.p = result.x[0]
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


