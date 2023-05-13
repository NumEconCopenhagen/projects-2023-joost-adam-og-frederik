from types import SimpleNamespace
import numpy as np
import sympy as sm 
import matplotlib.pyplot as plt

#We did not have time to finsh this

#We define the OLG model
class OLGmodelclass(): 
    def __init__(self):
        "Creating namespace for parameters"
        self.par = SimpleNamespace()
        self.setup()

    def setup(self):
        
        self.par = SimpleNamespace()
        par=self.par
        #Define parameters and variables 
        par.alpha = sm.symbols('alpha')
        par.k_t = sm.symbols('k_t')
        par.k_t1 = sm.symbols('k_{t+1}')
        par.A = sm.symbols('A')
        par.w_t = sm.symbols('w_t')
        par.w_t1 = sm.symbols('w_{t+1}') 
        par.r_t1 = sm.symbols('r_{t+1}')
        par.s_t = sm.symbols('s_t') 
        par.tau = sm.symbols('tau')
        par.c_1t = sm.symbols('c_1t') 
        par.c_2t = sm.symbols('c_{2t+1}') 
        par.rho = sm.symbols('rho') 
        par.lambdaa = sm.symbols('lambda')
 


    def utility_func(self): 
        #Defining utility function
        par = self.par

        return sm.log(par.c_1t)+1/(1+par.rho)*sm.log(par.c_2t)
    
    def budget_constraints(self):
       #combine the budget constraints for Euler equation 
        par = self.par
        bud_con_1 = sm.Eq(par.c_1t+par.s_t, (1-par.tau)*par.w_t)
        bud_con_2 = sm.Eq(par.c_2t, (1+par.r_t1)*par.s_t+(1+par.n)*par.tau*par.w_t1)

        # Isolate s_t in bud_con_2 and then combine it with bud_con_1
        bud_con_2_iso = sm.solve(bud_con_2, par.s_t)
        comb = bud_con_1.subs(par.s_t, bud_con_st2_sub[0])

        return sp.solve(lifetimeconstraint, (1-par.tau)*par.w_t)[0]-(1-par.tau)*par.w_t






        
        











