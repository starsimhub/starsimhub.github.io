"""
Define a star outline
"""

#%% Create the star

import sciris as sc
import numpy as np
from scipy.interpolate import CubicSpline
import pylab as plt
sc.options(dpi=200)

p = sc.objdict()
golden = 1.41421
p.arms1 = 4
p.arms2 = 4
p.npts  = 2000
p.exp1x = 1.0
p.exp1y = 1.0
p.exp2x = 1.2
p.exp2y = 1.2
p.off1  = 0
p.off2  = 0
p.rf1   = 0.23
p.rf2   = 0.21
p.rad1a = 0.6
p.rad1b = 0.0
p.rad2a = 0.6
p.rad2b = 0.0
p.scale1 = 2
p.scale2 = 1.2
p.ratio1 = golden
p.ratio2 = golden
p.zorder = 1
p.c1     = 'k'
p.c2     = 'w'

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

def exp_stretch(x, y, expx, expy, scale, ratio):
    sign_x = np.sign(x)
    sign_y = np.sign(y)
    newx = np.abs(x)**expx
    newy = np.abs(y)**expy
    newx *= sign_x*scale
    newy *= sign_y*scale*ratio
    return newx, newy

# Plot the smoothed 12-point star with rounded inner points using cubic splines
plot1 = True
if plot1:
    fig1 = plt.figure(figsize=(6, 6))

    inds, csf_x, csf_y = make_splines(p.arms1, p.rad1a, p.rad1b, p.npts, rf=p.rf1, off=p.off1*np.pi/p.arms1)
    x,y = exp_stretch(csf_x, csf_y, p.exp1x, p.exp1y, p.scale1, p.ratio1)
    plt.fill(x, y, p.c1)

    inds, csf_x, csf_y = make_splines(p.arms2, p.rad2a, p.rad2b, p.npts, rf=p.rf2, off=p.off2*np.pi/p.arms2)
    x,y = exp_stretch(csf_x, csf_y, p.exp2x, p.exp2y, p.scale2, p.ratio2)
    plt.fill(x, y, p.c2, zorder=p.zorder)

    plt.axis("equal")
    # plt.axis("off")
    plt.show()

    sc.savefig('starsim-logo-v8.png')