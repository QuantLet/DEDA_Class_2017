
[<img src="https://github.com/QuantLet/Styleguide-and-FAQ/blob/master/pictures/banner.png" width="888" alt="Visit QuantNet">](http://quantlet.de/)

## [<img src="https://github.com/QuantLet/Styleguide-and-FAQ/blob/master/pictures/qloqo.png" alt="Visit QuantNet">](http://quantlet.de/) **Digital Economy and Decision Analytics** [<img src="https://github.com/QuantLet/Styleguide-and-FAQ/blob/master/pictures/QN2.png" width="60" alt="Visit QuantNet 2.0">](http://quantlet.de/)

```yaml

Name of Quantlet : DEDA_Class_2017_Statistics&Finance
Published in : Digital Economy and Decision Analytics
Description :
- Demonstrate Linear Opearation and Fourier Transform Using Nympy
- Draw plot normal distributed random variables and sample's PDF and CDF using Matplotlib
- Demonstrate different kernel density estimations
- Use Black-Scholes Model to price options
- Simulate implied volatility and plot volatility smile  

Keywords :
- Python
- Teaching
- Numpy
- Scipy
- Matplotlib
- PDF/CDF
- KDE
- Black-Scholes
- Implied Volatility

Author : Junjie Hu, Yves Hilpisch

```

### Python Code:
```python

"""
### Please note: This file is not for execution ###
### Special thanks to Mr. Yves Hilpisch's public code from his book "Python for finance, analyze big financial data" 
"""

import numpy as np

"""
Generating numbers in numpy array
"""

# Giving the seed of random number generator
np.random.seed(1)
# Generate a 20*20 matrix with uniform distributed random integers between 0 to 50
A = np.random.randint(low=0, high=50, size=(20, 20))
print(A)

import matplotlib.pyplot as plt

fig = plt.figure()  # Create a window to draw
ax = plt.axes()  # Create axes
ax.plot(A, 'o')  # Plot the dots, using circle
ax.set_title('Random Number Plotting')  # Set figure title
plt.show()
# Save figure to a high quality
fig.savefig('random_scatter.png', dpi=300)
fig.clear()  # clear the figure

# Another scatter plot
x = np.random.randn(1000)
# plt also provide a quick way to draw
plt.plot(x, '.')
plt.title('Normal Distribution Scatter Plotting')
plt.xlabel('X')
plt.ylabel('Y')
plt.draw()
plt.savefig('normal_dis_scatter.png', dpi=300)

"""
Matrix operations
"""

# Inverse matrix
A_inv = np.linalg.inv(A)

# Matrix times operation
dot_result = np.dot(A, A_inv)
print(dot_result)
# Generate a 20*20 identity matrix
idn_matrix = np.identity(20)
print(idn_matrix)
# Using .allclose() function to evaluate two matrices are equal within tolerance
np.allclose(dot_result, np.eye(20))  # True

from PIL import Image
from numpy.fft import fft, ifft

# Open then image by using Python Imaging Library(PIL)
image_before = Image.open('berlin_view.jpg')
# Decoding and encoding image to float number
image_int = np.fromstring(image_before.tobytes(), dtype=np.int8)
# Processing Fourier transform
fft_transformed = fft(image_int)
# Filter the lower frequency
fft_transformed = np.where(np.absolute(fft_transformed) < 9e4, 0, fft_transformed)
# Inverse Fourier transform
fft_transformed = ifft(fft_transformed)
# Keep the real part
fft_transformed = np.int8(np.real(fft_transformed))
# Output the image
image_output = Image.frombytes(image_before.mode, image_before.size, fft_transformed)
image_output.draw()


"""
Random Variables PDF CDF
"""

import scipy.stats as ss
import matplotlib.pyplot as plt
import numpy as np

# Generate a normal distributed random variable
# First, generate x axis from 0.1% - 99.9% of quantile
# The random variable with mean=10, sigma=3
parameters = {'loc': 10, 'scale': 3}
x = np.linspace(ss.norm.ppf(0.001, **parameters), ss.norm.ppf(0.999, **parameters), 10000)

# Calculate the pdf
norm_pdf = ss.norm.pdf(x, **parameters)
# Then, Calculate the CDF
norm_cdf = ss.norm.cdf(x, **parameters)

# Plot the cdf and pdf in 1 figure
figsize = (10, 8)
fig = plt.figure(figsize=figsize)
# upper plot is pdf
plt.subplot(2, 1, 1)  # (rows, columns, which one)
plt.plot(x, norm_pdf, '-', alpha=1)
plt.xlabel('X')
plt.ylabel('PDF')
plt.legend(['Probability Density Function'])
# lower plot is cdf
plt.subplot(2, 1, 2)
plt.plot(x, norm_cdf, '-', alpha=1)
plt.xlabel('X')
plt.legend(['Cumulative Density Function'])
plt.ylabel('CDF')
# Save
plt.savefig('normal_pdf_cdf.png', dpi=300)
plt.show()


"""
CDF of Normal distributions
"""

import scipy as sc
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab


def plot_normal(mu, sigma, size):
    # Create a function to receive normal distribution parameters
    normal_data = sc.random.normal(loc=mu, scale=sigma, size=size)
    plt.axes()
    # The hist() method not only draw the histogram
    # but also return the info of the drawing
    n, bins, patchs = plt.hist(normal_data, bins=100, normed=1)
    # Use bins returned from hist() to draw a wrap line
    y = mlab.normpdf(bins, mu, sigma)
    plt.plot(bins, y, '-')
    plt.draw()
    return plt


mus = (0, 10, 20)
sigmas = (1, 1.5, 3)
sizes = (10000, 10000, 10000)

# Draw 3 plots with different parameters in the same figure
plot = [plot_normal(mu, sigma, size) for mu, sigma, size in zip(mus, sigmas, sizes)][0]

# Set the legend of the figure
plot.legend(['$\mu=0, \sigma=1$',  # Like LATEX, Use $ and \to mark mathematical symbols
             '$\mu=10, \sigma=1.5$',
             '$\mu=20, \sigma=3$'])
plot.ylabel('Frequency')
plot.title('Normal Distributions Histogram')
plot.savefig('histogram_normal.png', dpi=300)
plot.show()


"""
Kernel Density Estimation
"""

import scipy as sc
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab


def plot_normal(mu, sigma, size):
    # Create a function to receive normal distribution parameters
    normal_data = sc.random.normal(loc=mu, scale=sigma, size=size)
    plt.axes()
    # The hist() method not only draw the histogram
    # but also return the info of the drawing
    n, bins, patchs = plt.hist(normal_data, bins=100, normed=1)
    # Use bins returned from hist() to draw a wrap line
    y = mlab.normpdf(bins, mu, sigma)
    plt.plot(bins, y, '-')
    plt.draw()
    return plt


mus = (0, 10, 20)
sigmas = (1, 1.5, 3)
sizes = (10000, 10000, 10000)

# Draw 3 plots with different parameters in the same figure
plot = [plot_normal(mu, sigma, size) for mu, sigma, size in zip(mus, sigmas, sizes)][0]

# Set the legend of the figure
plot.legend(['$\mu=0, \sigma=1$',  # Like LATEX, Use $ and \to mark mathematical symbols
             '$\mu=10, \sigma=1.5$',
             '$\mu=20, \sigma=3$'])
plot.ylabel('Frequency')
plot.title('Normal Distributions Histogram')
plot.savefig('histogram_normal.png', dpi=300)
plot.show()


"""
Copyright: This code is from "Python for finance, analyze big financial data", Yves Hilpisch
It is a highly recommended book for Python novices
"""
# Monte Carlo valuation of European call option
# in Black-Scholes-Merton model
# bsm_mcs_euro.py
#
import numpy as np

# Parameter Values
S0 = 100.  # initial index level
K = 105.  # strike price
T = 1.0  # time-to-maturity
r = 0.05  # riskless short rate
sigma = 0.2  # volatility
I = 100000  # number of simulations

# Valuation Algorithm
z = np.random.standard_normal(I)  # pseudorandom numbers
ST = S0 * np.exp((r - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * z)
# index values at maturity
hT = np.maximum(ST - K, 0)  # inner values at maturity
C0 = np.exp(-r * T) * np.sum(hT) / I  # Monte Carlo estimator

# Result Output
print("Value of the European Call Option %5.3f" % C0)


#
# Valuation of European call options in Black-Scholes-Merton model
# incl. Vega function and implied volatility estimation
# bsm_functions.py
#

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
    value : float
        present value of the European call option
    '''
    from math import log, sqrt, exp
    from scipy import stats

    S0 = float(S0)
    d1 = (log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    d2 = (log(S0 / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    value = (S0 * stats.norm.cdf(d1, 0.0, 1.0)
             - K * exp(-r * T) * stats.norm.cdf(d2, 0.0, 1.0))
    # stats.norm.cdf --> cumulative distribution function
    #                    for normal distribution
    return value


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
        sigma_est -= ((bsm_call_value(S0, K, T, r, sigma_est) - C0)
                      / bsm_vega(S0, K, T, r, sigma_est))
    return sigma_est


import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt

V0 = 17.6639
r = 0.01
tol = 0.5  # tolerance level for moneyness

h5 = pd.HDFStore('./DEDA_Class_2017_Statistics&Finance/source/vstoxx_data.h5', 'r')
futures_data = h5['futures_data']  # VSTOXX futures data
options_data = h5['options_data']  # VSTOXX call option data
h5.close()

futures_data['DATE'] = futures_data['DATE'].apply(lambda x: dt.datetime.fromtimestamp(x / 1e9))
futures_data['MATURITY'] = futures_data['MATURITY'].apply(lambda x: dt.datetime.fromtimestamp(x / 1e9))

options_data['DATE'] = options_data['DATE'].apply(lambda x: dt.datetime.fromtimestamp(x / 1e9))
options_data['MATURITY'] = options_data['MATURITY'].apply(lambda x: dt.datetime.fromtimestamp(x / 1e9))

options_data[['DATE', 'MATURITY', 'TTM', 'STRIKE', 'PRICE']].head()
options_data['IMP_VOL'] = 0.0  # new column for implied volatilities

for option in options_data.index:
    # iterating over all option quotes
    forward = futures_data[futures_data['MATURITY'] == options_data.loc[option]['MATURITY']]['PRICE'].values[0]
    # picking the right futures value
    if (forward * (1 - tol) < options_data.loc[option]['STRIKE'] < forward * (1 + tol)):
        # only for options with moneyness within tolerance
        imp_vol = bsm_call_imp_vol(
            V0,  # VSTOXX value
            options_data.loc[option]['STRIKE'],
            options_data.loc[option]['TTM'],
            r,  # short rate
            options_data.loc[option]['PRICE'],
            sigma_est=2.,  # estimate for implied volatility
            it=100)
        options_data.ix[option, 'IMP_VOL'] = imp_vol

plot_data = options_data[options_data['IMP_VOL'] > 0]

maturities = sorted(set(options_data['MATURITY']))

plt.figure(figsize=(8, 6))
for maturity in maturities:
    data = plot_data[options_data.MATURITY == maturity]
    # select data for this maturity
    plt.plot(data['STRIKE'], data['IMP_VOL'],
             label=maturity.date(), lw=1.5)
    plt.plot(data['STRIKE'], data['IMP_VOL'], 'r.', label='')
plt.grid(True)
plt.xlabel('strike')
plt.ylabel('implied volatility of volatility')
plt.legend()
plt.show()
plt.savefig('./DEDA_Class_2017_Statistics&Finance/IV_Strike.png', dpi=300)


```



