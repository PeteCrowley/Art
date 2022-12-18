import numpy as np
import matplotlib.pyplot as plt

DETAIL = 2_000
M_DEPTH = 200
SAVE_IMAGE = True
SAVE_FILE_NAME = "test"
my_dpi = 100

# Create a grid of complex numbers
x = np.linspace(-1.9, 0.5, DETAIL)  # Not the full range and domain of the set, but it is enough
y = np.linspace(-1.3, 1.3, DETAIL)  # for all the points we will be able to see
xx, yy = np.meshgrid(x, y)      # Creating R^2, the cartesian coordinate system
complex_plane = xx + 1j * yy    # Multiplying y values by sqrt(-1) to make them complex
# z is now the complex plane


# The Mandelbrot function
def mandelbrot(z, max_iter):
    c = z
    for n in range(max_iter):
        if abs(z) > 2:
            return n    # Return the number of iterations it takes to diverge
        z = z ** 2 + c
    return max_iter     # Return max_iter if it never diverges


# Generate a matrix of the Mandelbrot values
mandelbrot_values = np.vectorize(mandelbrot)(complex_plane, M_DEPTH)

# Generate a contour plot of the Mandelbrot set
plt.figure(figsize=(800 / my_dpi, 600 / my_dpi), dpi=my_dpi)
cp = plt.contourf(xx, yy, mandelbrot_values)
plt.colorbar(cp)
if SAVE_IMAGE:
    plt.savefig("Images/Mandelbrot/" + SAVE_FILE_NAME + ".png", bbox_inches="tight", dpi=my_dpi * 7)
plt.show()
