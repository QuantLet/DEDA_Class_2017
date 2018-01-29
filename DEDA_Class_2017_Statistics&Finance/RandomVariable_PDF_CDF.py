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
plt.figure(figsize=figsize)
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
