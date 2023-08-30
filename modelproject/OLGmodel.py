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
        par.k_PAYG_lag_ini = 1.0 # initial capital stock
        par.k_FF_lag_ini = 1.0 # initial capital stock
        par.simT = 50 # length of simulation

    def allocate(self):
        """ allocate arrays for simulation """
        
        par = self.par
        sim = self.sim

        # a. list of variables
        household = ['C1','C2']
        firm = ['k_PAYG', 'k_PAYG_lag', 'k_FF' , 'k_FF_lag']
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
        sim.k_PAYG_lag[0] = par.k_PAYG_lag_ini
        sim.k_FF_lag[0] = par.k_FF_lag_ini

        # Set an initial value for s
        s = 0.41

        # b. iterate
        for t in range(par.simT):
            
            # i. simulate before s
            simulate_1(par, sim, t, s)

            if t == par.simT-1: continue          

            # iii. simulate after s
            simulate_2(par,sim,t,s)

        if do_print: print(f'simulation done in {time.time()-t0:.2f} secs')

def simulate_1(par,sim,t,s):
        """ simulate forward """

        if t > 0:
            sim.k_PAYG_lag[t] = sim.k_PAYG[t-1]
            sim.k_FF_lag[t] = sim.k_FF[t-1]

        # ii. factor prices
        sim.r[t] = par.alpha * sim.k_PAYG_lag[t]**(par.alpha-1) * (1.0)**(1-par.alpha)
        sim.w[t] = (1-par.alpha) * sim.k_PAYG_lag[t]**(par.alpha) * (1.0)**(-par.alpha)

        #capital
        sim.k_PAYG[t]=(1-par.alpha)*(1-par.tau)*par.alpha/((2+par.rho)*par.alpha+(1+par.rho)*(1-par.alpha)*par.tau)*par.A*sim.k_PAYG_lag[t]**par.alpha
        sim.k_FF[t]=((1-par.rho*par.tau-2*par.tau)/(2+par.rho))*(1-par.alpha)*par.A*sim.k_FF_lag[t]**par.alpha+par.tau*(1-par.alpha)*par.A*sim.k_FF_lag[t]**par.alpha

        # c. consumption
        sim.C2[t] = (1+sim.r[t])*s+sim.w[t]*par.tau    


def simulate_2(par,sim,t,s):
        """ simulate forward """

        # a. consumption of young
        sim.C1[t] = (1-par.tau)*sim.w[t]-s
    





        
        











