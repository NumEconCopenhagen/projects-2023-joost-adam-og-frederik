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
    
    def solve(self):
        """ solve model continously """
        par = self.par
        sol = self.sol
        opt = SimpleNamespace()
        def obj(x):
            return - self.utility_A(x[0])
        res = optimize.minimize(obj, x0=1, method="Nelder-Mead")
        opt.c_mark = res.x[0]
        return opt
    
    def solve_p_vec(self):
        sol = self.sol
        par = self.par
        for it, p in enumerate(par.p_vec):
            par.p = p
            res = self.solve()
            sol.c_mark_vec[it] = res.c_mark
        return
    


