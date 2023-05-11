
from types import SimpleNamespace

import numpy as np
from scipy import optimize

import pandas as pd 
import matplotlib.pyplot as plt

class HouseholdSpecializationModelClass:

    def __init__(self):
        """ setup model """

        # a. create namespaces
        par = self.par = SimpleNamespace()
        sol = self.sol = SimpleNamespace()

        # b. preferences
        par.rho = 2.0
        par.nu_M = 0.001
        par.nu_F = 0.001
        par.epsilon_M = 1.0
        par.epsilon_F = 1.0
        par.omega = 0.5 

        # c. household production
        par.alpha = 0.5
        par.sigma = 1.0

        # d. wages
        par.wM = 1.0
        par.wF = 1.0
        par.wF_vec = np.linspace(0.8,1.2,5)

        # e. targets
        par.beta0_target = 0.4
        par.beta1_target = -0.1

        # f. solution
        sol.LM_vec = np.zeros(par.wF_vec.size)
        sol.HM_vec = np.zeros(par.wF_vec.size)
        sol.LF_vec = np.zeros(par.wF_vec.size)
        sol.HF_vec = np.zeros(par.wF_vec.size)

        sol.beta0 = np.nan
        sol.beta1 = np.nan

    def calc_utility(self,LM,HM,LF,HF):
        """ calculate utility """

        par = self.par
        sol = self.sol

        # a. consumption of market goods
        C = par.wM*LM + par.wF*LF

        # b. home production
        if par.sigma == 0:
            H = min(HM, HF)
        elif par.sigma == 1:
            H = HM**(1-par.alpha)*HF**par.alpha
        else:
            H = (
                (1-par.alpha)*HM**((par.sigma - 1)/par.sigma) \
                + (par.alpha)*HF**((par.sigma - 1)/par.sigma)
            )**(par.sigma/(par.sigma - 1))

        # c. total consumption utility
        Q = C**par.omega*H**(1-par.omega)
        utility = np.fmax(Q,1e-8)**(1-par.rho)/(1-par.rho)

        # d. disutlity of work
        epsilon_F_ = 1+1/par.epsilon_F
        epsilon_M_ = 1+1/par.epsilon_M
        TM = LM+HM
        TF = LF+HF
        disutility = par.nu_M*(TM**epsilon_M_/epsilon_M_)+par.nu_F*(TF**epsilon_F_/epsilon_F_)
        
        return utility - disutility

    def solve_discrete(self,do_print=False):
        """ solve model discretely """
        
        par = self.par
        sol = self.sol
        opt = SimpleNamespace()
        
        # a. all possible choices
        x = np.linspace(0,24,49)
        LM,HM,LF,HF = np.meshgrid(x,x,x,x) # all combinations
    
        LM = LM.ravel() # vector
        HM = HM.ravel()
        LF = LF.ravel()
        HF = HF.ravel()

        # b. calculate utility
        u = self.calc_utility(LM,HM,LF,HF)
    
        # c. set to minus infinity if constraint is broken
        I = (LM+HM > 24) | (LF+HF > 24) # | is "or"
        u[I] = -np.inf
    
        # d. find maximizing argument
        j = np.argmax(u)
        
        opt.LM = LM[j]
        opt.HM = HM[j]
        opt.LF = LF[j]
        opt.HF = HF[j]

        # e. print
        if do_print:
            for k,v in opt.__dict__.items():
                print(f'{k} = {v:6.4f}')

        return opt

    def solve(self,do_print=False):
        """ solve model continously """
        par = self.par
        sol = self.sol
        opt = SimpleNamespace()
        def obj(x):
            return - self.calc_utility(x[0],x[1],x[2],x[3])
        res = optimize.minimize(obj, x0=[6]*4, method="Nelder-Mead")
        opt.LM = res.x[0]
        opt.HM = res.x[1]
        opt.LF = res.x[2]
        opt.HF = res.x[3]
        return opt
          

    def solve_wF_vec(self,discrete=False):
        """ solve model for vector of female wages """
        sol = self.sol
        par = self.par
        for it, w in enumerate(par.wF_vec):
            par.wF = w
            if discrete== True:
                res = self.solve_discrete()
            else:
                res = self.solve()
            sol.LM_vec[it] = res.LM
            sol.LF_vec[it] = res.LF
            sol.HM_vec[it] = res.HM
            sol.HF_vec[it] = res.HF
        pass

    def run_regression(self):
        """ run regression """

        par = self.par
        sol = self.sol

        x = np.log(par.wF_vec / par.wM)
        y = np.log(sol.HF_vec/sol.HM_vec)
        A = np.vstack([np.ones(x.size),x]).T
        sol.beta0,sol.beta1 = np.linalg.lstsq(A,y,rcond=None)[0]
    


    def estimate(self,alpha=None,sigma=None):
        """ estimate alpha and sigma """

        par = self.par
        sol = self.par
        opt = SimpleNamespace()

        
        #We make a new function, which defines the dif "different"
        def dif(x):
            par = self.par
            sol = self.sol
            par.alpha = x[0]
            par.sigma = x[1]
            self.solve_wF_vec()
            self.run_regression()
            dif = (par.beta0_target - sol.beta0)**2 + (par.beta1_target - sol.beta1)**2 
            return dif
        
        #We try to minimize the dif function with respect to alpha and sigma
        result = optimize.minimize(dif, [alpha,sigma], bounds=[(0.01,0.99),(0.01,5)], method='Nelder-Mead')
        opt.alpha = result.x[0]
        opt.sigma = result.x[1]
       
        return opt
    
    def estimate_q5(self,sigma=None,epsilon_M=None,epsilon_F=None,extend=True):
        par = self.par
        sol = self.par
        opt = SimpleNamespace()

        if extend==True:
            #We make a new function, which defines the dif "different"
            def dif(x):
                par = self.par
                sol = self.sol
                par.sigma = x[0]
                par.epsilon_M = x[1]
                par.epsilon_F = x[2]
                self.solve_wF_vec()
                self.run_regression()
                dif = (sol.beta0 - par.beta0_target)**2 +(sol.beta1 - par.beta1_target)**2 
                return dif
        
            result = optimize.minimize(dif, [sigma,epsilon_F,epsilon_M], bounds=[(0.01,2.0),(0.01,2),(0.01,2)], method='Nelder-Mead')
            opt.sigma = result.x[0]
            opt.epsilon_M = result.x[1]
            opt.epsilon_F = result.x[2]

            return opt
        
        elif extend==False:
            def dif(x):
                par = self.par
                sol = self.sol
                par.sigma = x[0]
                self.solve_wF_vec()
                self.run_regression()
                dif = (sol.beta0 - par.beta0_target)**2 +(sol.beta1 - par.beta1_target)**2 
                return dif
        
            result = optimize.minimize(dif, [sigma], bounds=[(0.01,0.5)], method='Nelder-Mead')
            opt.sigma = result.x[0]

            return opt
        
        return opt


