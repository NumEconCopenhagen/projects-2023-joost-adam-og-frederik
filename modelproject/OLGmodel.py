from types import SimpleNamespace
import time
import numpy as np
from scipy import optimize

class OLG_Class():

    def __init__(self,do_print=True):
        """ create the model """

        if do_print: print('initializing the model:')

        self.par = SimpleNamespace()
        self.sim = SimpleNamespace()

        if do_print: print('calling .setup()')
        self.setup()

        if do_print: print('calling .allocate()')
        self.allocate()
    
    def setup(self):
        """ baseline parameters """

        par = self.par

        par.alpha = 0.3
        par.rho = 0.25
        par.tau = 0.2
        par.n = 0.02
        par.A = 10

        # d. misc
        par.k_lag_ini = 1.0 # initial capital stock
        par.simT = 50 # length of simulation

    def allocate(self):
        """ allocate arrays for simulation """
        
        par = self.par
        sim = self.sim

        # a. list of variables
        household = ['C1','C2']
        firm = ['k','k_lag']
        prices = ['w','r']

        # b. allocate
        allvarnames = household + firm + prices
        for varname in allvarnames:
            sim.__dict__[varname] = np.nan*np.ones(par.simT)

    def simulate(self,do_print=True):
        """ simulate model """

        t0 = time.time()

        par = self.par
        sim = self.sim
        
        # a. initial values
        sim.k_lag[0] = par.k_lag_ini

        # Set an initial value for s
        s = 0.41

        # b. iterate
        for t in range(par.simT):
            
            # i. simulate before s
            simulate_before_s(par, sim, t, s)

            if t == par.simT-1: continue          

            # i. find bracket to search
            s_min,s_max = find_s_bracket(par,sim,t)

            # ii. find optimal s
            obj = lambda s: calc_euler_error(s,par,sim,t=t)
            result = optimize.root_scalar(obj,bracket=(s_min,s_max),method='bisect')
            s = result.root

            # iii. simulate after s
            simulate_after_s(par,sim,t,s)

        if do_print: print(f'simulation done in {time.time()-t0:.2f} secs')

def find_s_bracket(par,sim,t,maxiter=500,do_print=False):
    """ find bracket for s to search in """

    # a. maximum bracket
    s_min = 0.0 + 1e-8 # save almost nothing
    s_max = 1.0 - 1e-8 # save almost everything

    # b. saving a lot is always possible 
    value = calc_euler_error(s_max,par,sim,t)
    sign_max = np.sign(value)
    if do_print: print(f'euler-error for s = {s_max:12.8f} = {value:12.8f}')

    # c. find bracket      
    lower = s_min
    upper = s_max

    it = 0
    while it < maxiter:
                
        # i. midpoint and value
        s = (lower+upper)/2 # midpoint
        value = calc_euler_error(s,par,sim,t)

        if do_print: print(f'euler-error for s = {s:12.8f} = {value:12.8f}')

        # ii. check conditions
        valid = not np.isnan(value)
        correct_sign = np.sign(value)*sign_max < 0
        
        # iii. next step
        if valid and correct_sign: # found!
            s_min = s
            s_max = upper
            if do_print: 
                print(f'bracket to search in with opposite signed errors:')
                print(f'[{s_min:12.8f}-{s_max:12.8f}]')
            return s_min,s_max
        elif not valid: # too low s -> increase lower bound
            lower = s
        else: # too high s -> increase upper bound
            upper = s

        # iv. increment
        it += 1

    raise Exception('cannot find bracket for s')

def calc_euler_error(s,par,sim,t):
    """ target function for finding s with bisection """

    # a. simulate forward
    simulate_after_s(par,sim,t,s)
    simulate_before_s(par,sim,t+1,s) # next period

    # c. Euler equation
    LHS = sim.C1[t]
    RHS = sim.C2[t+1]*(par.rho+1)/(sim.r[t+1]+1)

    return LHS-RHS

def simulate_before_s(par,sim,t,s):
    """ simulate forward """

    if t > 0:
        sim.k_lag[t] = sim.k[t-1]

    # ii. factor prices
    sim.r[t] = par.alpha * sim.k_lag[t]**(par.alpha-1) * (1.0)**(1-par.alpha)
    sim.w[t] = (1-par.alpha) * sim.k_lag[t]**(par.alpha) * (1.0)**(-par.alpha)

    #capital
    sim.k[t]=(1-par.alpha)*(1-par.tau)*par.alpha/((2+par.rho)*par.alpha+(1+par.rho)*(1-par.alpha)*par.tau)*par.A*sim.k_lag[t]**par.alpha

    # c. consumption
    sim.C2[t] = (1+sim.r[t])*s+sim.w[t]*par.tau


def simulate_after_s(par,sim,t,s):
    """ simulate forward """

    # a. consumption of young
    sim.C1[t] = (1-par.tau)*sim.w[t]-s

    





        
        











