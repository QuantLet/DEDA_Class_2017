
[<img src="https://github.com/QuantLet/Styleguide-and-FAQ/blob/master/pictures/banner.png" width="888" alt="Visit QuantNet">](http://quantlet.de/)

## [<img src="https://github.com/QuantLet/Styleguide-and-FAQ/blob/master/pictures/qloqo.png" alt="Visit QuantNet">](http://quantlet.de/) **Digital Economy and Decision Analytics** [<img src="https://github.com/QuantLet/Styleguide-and-FAQ/blob/master/pictures/QN2.png" width="60" alt="Visit QuantNet 2.0">](http://quantlet.de/)

```yaml

Name of Quantlet : DEDA_Class_2017_Statistics&Finance
Published in : Digital Economy and Decision Analytics
Description : 
- Demonstrate Linear Opearation and Fourier Transform Using Nympy
- Draw plot normal distributed random variables and sample's PDF and CDF using Matplotlib
- Demonstrate different kernel density estimations 
 
Keywords :
- Python
- Teaching
- Numpy
- Scipy
- Matplotlib
- PDF/CDF
- KDE

Author : Junjie Hu

```

### Python Code:
```python

"""
### Please note: This file is not for execution ###
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



```



