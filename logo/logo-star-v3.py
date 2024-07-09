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
rf = 0.15

# Function to create rounded star points
def rounded_star_points(arms, radius1, radius2, rf, off=0):
    points = []
    angle = (np.pi / arms)
    for i in range(2 * arms):
        r = radius1 if i % 2 == 0 else radius2
        if i % 2 != 0:
            r += rf
        ia = i*angle + off
        points.append((np.cos(ia)*r, np.sin(ia)*r))
    return points


def make_splines(arms, radius1, radius2, ninterp, **kw):

    # Create star points with rounded inner points
    points = rounded_star_points(arms, radius1, radius2, **kw)
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
plot1 = True
if plot1:
    inds, csf_x, csf_y = make_splines(arms, radius1, radius2, ninterp, rf=rf)
    fig1 = plt.figure(figsize=(6, 6))
    plt.fill(csf_x, csf_y, "k")
    inds, csf_x, csf_y = make_splines(arms, 0.6, 0.1, ninterp, rf=0.07, off=np.pi/arms)
    plt.fill(csf_x, csf_y, "w")
    plt.axis("equal")
    plt.axis("off")
    plt.show()