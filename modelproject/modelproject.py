from scipy import optimize
import numpy as np
import sympy as sm
import matplotlib.pyplot as plt
from types import SimpleNamespace
import ipywidgets as widgets

class OLG_Model:
    def __init__(self): #OBS: IKKE ÆNDRET ENDNU!!!
        """setup model"""

        self.par = SimpleNamespace()
        self.setup()

    def setup(self):
        """Define parameters"""
        par = self.par
        
        #Setting up parameters for the utility function
        par.c1t = sm.symbols('c_1t')
        par.c2t = sm.symbols('c_{2t+1}')
        par.beta = sm.symbols('beta')

        #Setting up parameters for the production function
        par.Kt = sm.symbols('K_t')
        par.Kt1 = sm.symbols('K_{t+1}')
        par.Lt = sm.symbols('L_t')
        par.Lt1 = sm.symbols('L_{t+1}')
        par.A = sm.symbols('A')
        par.Ut = sm.symbols('U_t')
        par.alpha = sm.symbols('alpha')
        par.kt = sm.symbols('k_t')
        par.kt1 = sm.symbols('k_{t+1}')
        par.kst = sm.symbols('k^*')

        #Setting up parameters for the budget constraint
        par.rt = sm.symbols('r_t')
        par.rt1 = sm.symbols('r_{t+1}')
        par.wt = sm.symbols('w_t')
        par.wt1 = sm.symbols('w_{t+1}')
        par.dt1 = sm.symbols('d_{t+1}')
        par.n = sm.symbols('n')
        par.tau = sm.symbols('tau')
        par.st = sm.symbols('s_t')
        par.lamb = sm.symbols('lambda')
    
    def utility(self):
        """Define the utility function"""
        par = self.par
        return sm.log(par.c1t)+par.beta*sm.log(par.c2t)
    
    def BC(self): #BC=BudgetConstraint
        """Define the budget constraint"""
        