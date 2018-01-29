"""
Description:
 -
 -

Usage:

Author:
 - Junjie Hu, hujunjie@hu-berlin.de
Last modified date: 09-12-2017
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
ax.plot(np.arange(1, 21), A, 'mu')  # Plot the dots, using circle
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
image_output.show()
