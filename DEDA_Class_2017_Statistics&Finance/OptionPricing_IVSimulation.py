"""
Copyright: This code is from "Python for finance, analyze big financial data", Yves Hilpisch
It is a highly recommended book for Python novices

Python Version: 3.7

"""

# Monte Carlo valuation of European call option
import numpy as np

np.random.seed(123)

# Parameter Values
S0 = 100.  # initial index level
K = 105.  # strike price
T = 1.0  # time-to-maturity
mu = 0.05  # risk-free short-term rate
sigma = 0.2  # volatility
n = 100000  # number of simulations

# Valuation Algorithm
z = np.random.standard_normal(n)  # A random vector with normal distribution
# Geometric Brownian Motion simulation of price at time T
ST = S0 * np.exp((mu - 0.5 * sigma ** 2) * T + sigma * z)

# index values at maturity
hT = np.maximum(ST - K, 0)  # Option values at maturity
C0 = np.exp(-mu * T) * np.sum(hT) / n  # Discount average option values to time 0

# Result Output
print("Simulation value of the European Call Option {:1.5f}".format(C0))


# Valuation of European call options in Black-Scholes-Merton model
# incl. Vega function and implied volatility estimation
# bsm_functions.py

# Black-Scholes-Merton model

# Analytical Black-Scholes-Merton (BSM) Formula

def bsm_call_value(S0, K, T, r, sigma):
    ''' Valuation of European call option in BSM model.
    Analytical formula.

    Parameters
    ==========
    S0 : float
        initial stock/index level
    K : float
        strike price
    T : float
        maturity date (in year fractions)
    r : float
        constant risk-free short rate
    sigma : float
        volatility factor in diffusion term

    Returns
    =======
    bs_call : float
        present bs_call of the European call option
    '''
    from math import log, sqrt, exp
    from scipy import stats

    S0 = float(S0)
    d1 = (log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    d2 = (log(S0 / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    bs_call = (S0 * stats.norm.cdf(x=d1, loc=0.0, scale=1.0) - K * exp(-r * T) * stats.norm.cdf(d2, 0.0, 1.0))
    # stats.norm.cdf --> cumulative distribution function
    #                    for normal distribution
    return bs_call


bs_call = bsm_call_value(S0, K, 1, mu, sigma)
print("B-S model for the European Call Option {:1.5f}".format(bs_call))


# Vega function
def bsm_vega(S0, K, T, r, sigma):
    ''' Vega of European option in BSM model.

    Parameters
    ==========
    S0 : float
        initial stock/index level
    K : float
        strike price
    T : float
        maturity date (in year fractions)
    r : float
        constant risk-free short rate
    sigma : float
        volatility factor in diffusion term

    Returns
    =======
    vega : float
        partial derivative of BSM formula with respect
        to sigma, i.e. Vega
    '''
    from math import log, sqrt
    from scipy import stats

    S0 = float(S0)
    d1 = (log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    vega = S0 * stats.norm.pdf(d1, 0.0, 1.0) * sqrt(T)
    return vega


# Implied volatility function
def bsm_call_imp_vol(S0, K, T, r, C0, sigma_est, it=100):
    ''' Implied volatility of European call option in BSM model.

    Parameters
    ==========
    S0 : float
        initial stock/index level
    K : float
        strike price
    T : float
        maturity date (in year fractions)
    r : float
        constant risk-free short rate
    sigma_est : float
        estimate of impl. volatility
    it : integer
        number of iterations

    Returns
    =======
    simga_est : float
        numerically estimated implied volatility
    '''
    for i in range(it):
        sigma_est -= ((bsm_call_value(S0, K, T, r, sigma_est) - C0) / bsm_vega(S0, K, T, r, sigma_est))
    return sigma_est

import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt

S0 = 17.6639  # asset price
r = 0.01  # interest rate
tol = 0.5  # tolerance level for moneyness

# Read VSTOXX futures and options data
futures_data = pd.read_hdf('DEDA_Class_2017_Statistics&Finance/source/vstoxx_data.h5', key='futures_data', mode='r')
options_data = pd.read_hdf('DEDA_Class_2017_Statistics&Finance/source/vstoxx_data.h5', key='options_data', mode='r')

# Altering timestamp to datetime
futures_data['DATE'] = futures_data['DATE'].apply(lambda x: dt.datetime.fromtimestamp(x / 1e9))
futures_data['MATURITY'] = futures_data['MATURITY'].apply(lambda x: dt.datetime.fromtimestamp(x / 1e9))

options_data['DATE'] = options_data['DATE'].apply(lambda x: dt.datetime.fromtimestamp(x / 1e9))
options_data['MATURITY'] = options_data['MATURITY'].apply(lambda x: dt.datetime.fromtimestamp(x / 1e9))

options_data[['DATE', 'MATURITY', 'TTM', 'STRIKE', 'PRICE']].head()
options_data['IMP_VOL'] = 0.0  # new column for implied volatilities

for num, option in options_data.iterrows():
    print(num)
    print(option)
    # iterating over all options quotes
    forward = futures_data[futures_data['MATURITY'] == option['MATURITY']]['PRICE'].values[0]
    # picking the right futures value
    if (forward * (1 - tol) < option['STRIKE'] < forward * (1 + tol)):
        # only for options with moneyness within tolerance
        imp_vol = bsm_call_imp_vol(
            S0=S0,  # VSTOXX value
            K=option['STRIKE'],
            T=option['TTM'],
            r=r,
            C0=option['PRICE'],
            sigma_est=2.,  # estimate for implied volatility
            it=100)
        options_data.loc[num, 'IMP_VOL'] = imp_vol

plot_data = options_data[options_data['IMP_VOL'] > 0]

maturities = sorted(set(options_data['MATURITY']))
trade_date = options_data['DATE'].values[0]

plt.figure(figsize=(16, 7))
for maturity in maturities:
    data = plot_data[options_data.MATURITY == maturity]
    # select data for this maturity
    plt.plot(data['STRIKE'], data['IMP_VOL'], label=f'{(maturity - trade_date).days}-days TTM', lw=1.5)
    plt.plot(data['STRIKE'], data['IMP_VOL'], 'r.', label='')
plt.xlabel('Strike Price', fontsize=16)
plt.ylabel('Implied Volatility', fontsize=16)
plt.legend()
plt.tight_layout()
plt.show()
plt.savefig('DEDA_Class_2017_Statistics&Finance/IV_Strike.png', dpi=300)
