"""
Simulation of Generalized Wiener Process

Author: Junjie Hu
Python Version: 3.7

"""


import numpy as np
np.random.seed(1124)

num = 10000
dt = 1/60

# A basic Wiener Process
"""
Markov Process with mean change=0, variance rate=1 
"""
epsilon = np.random.normal(loc=0, scale=1, size=num) # Standard normal distribution
d_W = epsilon * np.sqrt(dt)



# Generalized form of Wiener Process




