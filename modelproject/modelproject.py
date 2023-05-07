from scipy import optimize
import numpy as np
import matplotlib.pyplot as plt
from types import SimpleNamespace
import ipywidgets as widgets

class IS_LM_Solver:
    def __init__(self):
        """setup model"""

        par = self.par = SimpleNamespace()

        # Variables for the IS/LM Model
        par.Y = 2800  # Initial guess for output, 2,800 billion DKK as of 2022 for Denmark
        par.r = 0.03  # Initial guess for interest rate, current rate from Nationalbanken
        par.C = lambda Y: 50 + 0.25 * Y  # Consumption function guess
        par.T = 1200  # Taxes, Denmark 2022
        par.I = lambda r: 1500 - 50 * r  # Investment function guess
        par.G = 620  # Government spending, Denmark 2022
        par.L = lambda Y, r: 0.5 * Y - 20 * r  # Money demand function
        par.M = 140  # Money supply, guess of 5 percent of total output
        par.P = 5  # Price level guess

    def IS_equation(self):
        """IS curve equation"""
        par = self.par
        IS_curve = par.Y - par.C(par.Y - par.T) - par.I(par.r) - par.G
        return IS_curve
    
    def evaluate_IS(self):
        """Evaluate IS equation at initial values"""
        result_IS = self.IS_equation()
        print("Result of IS equation:", result_IS)
        
    def LM_equation(self):
        """LM curve equation"""
        par = self.par
        LM_curve = par.L(par.Y, par.r) - par.M/par.P
        return LM_curve
    
    def evaluate_LM(self):
        """Evaluate LM equation at initial values"""
        result_LM = self.LM_equation()
        print("Result of LM equation:", result_LM)
    
    def solve_model(self):
        """Solve the IS/LM model"""
        par = self.par
        
        # Defines a function that returns the residuals (i.e. the difference between the IS and LM equations) for a given value of Y and r
        def equations(x):
            Y, r = x
            eq1 = par.Y - par.C(Y - par.T) - par.I(r) - par.G - Y
            eq2 = par.L(Y, r) - par.M / par.P
            return [eq1, eq2]
        
        # We use scipy.optimize.root to find the values of Y and r that satisfy the equations
        solution = optimize.root(equations, [par.Y, par.r])
        
        # Store the solution values in the par namespace
        par.Y, par.r = solution.x
    