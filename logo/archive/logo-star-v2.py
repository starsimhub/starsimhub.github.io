"""
Define a star outline
"""

#%% Create the star

import sciris as sc
import numpy as np
from scipy.interpolate import CubicSpline
import pylab as plt
sc.options(dpi=200)

arms = 10
radius1 = 1
radius2 = 0.4
ninterp = 1000

# Function to create rounded star points
def rounded_star_points(arms, radius1, radius2, rounding_factor=0.15):
    points = []
    angle = np.pi / arms
    for i in range(2 * arms):
        r = radius1 if i % 2 == 0 else radius2
        if i % 2 != 0:
            r += rounding_factor
        ia = i*angle
        points.append((np.cos(ia)*r, np.sin(ia)*r))
    return points


def make_splines(arms, radius1, radius2, ninterp):

    # Create star points with rounded inner points
    points = rounded_star_points(arms, radius1, radius2)
    points.append(points[0])  # Close the star shape
    
    # Separate the x and y coordinates
    x, y = zip(*points)
    
    # Create a periodic cubic spline interpolation
    inds = np.arange(ninterp)
    t = np.linspace(0, 1, len(x), endpoint=True)
    cs_x = CubicSpline(t, x, bc_type='periodic')
    cs_y = CubicSpline(t, y, bc_type='periodic')
    t_fine = np.linspace(0, 1, ninterp)
    csf_x = cs_x(t_fine)
    csf_y = cs_y(t_fine)
    
    return inds, csf_x, csf_y

# Plot the smoothed 12-point star with rounded inner points using cubic splines
plot1 = False
if plot1:
    inds, csf_x, csf_y = make_splines(arms, radius1, radius2, ninterp)
    fig1 = plt.figure(figsize=(6, 6))
    plt.fill(csf_x, csf_y, "k")
    plt.axis("equal")
    plt.axis("off")
    plt.show()


#%% Define the points
fig2 = plt.figure(figsize=(6, 6))
np.random.seed(2)
maxpts = 30
for subrad in np.linspace(0.05,1,10):
    subpts = int(np.ceil(subrad*maxpts+5))
    print(subrad, subpts)
    inds, csf_x, csf_y = make_splines(arms, radius1*subrad, radius2*subrad, ninterp)
    r = np.random.randn(subpts)*3
    subi = (np.linspace(0, ninterp-1, subpts)+r).astype(int)
    subi = subi[subi<ninterp]
    subx, suby = csf_x[subi], csf_y[subi]
    s = (1/(0.02+(subx**2+suby**2)**2))*5
    plt.scatter(subx, suby, c='gold', s=s, alpha=0.5)
plt.fill(csf_x, csf_y, 'navy', zorder=-10)
plt.axis("equal")
plt.axis("off")
plt.show()