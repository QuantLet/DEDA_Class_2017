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
