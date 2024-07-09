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
center = (0, 0)

# Function to create rounded star points
def rounded_star_points(center, arms, radius1, radius2, rounding_factor=0.15):
    points = []
    angle = np.pi / arms
    for i in range(2 * arms):
        r = radius1 if i % 2 == 0 else radius2
        if i % 2 != 0:
            r += rounding_factor
        points.append((
            center[0] + np.cos(i * angle) * r,
            center[1] + np.sin(i * angle) * r
        ))
    return points

# Create star points with rounded inner points
points = rounded_star_points(center, arms, radius1, radius2)
points.append(points[0])  # Close the star shape

# Separate the x and y coordinates
x, y = zip(*points)

# Create a periodic cubic spline interpolation
t = np.linspace(0, 1, len(x), endpoint=True)
cs_x = CubicSpline(t, x, bc_type='periodic')
cs_y = CubicSpline(t, y, bc_type='periodic')
t_fine = np.linspace(0, 1, 1000)
csf_x = cs_x(t_fine)
csf_y = cs_y(t_fine)

# Plot the smoothed 12-point star with rounded inner points using cubic splines
fig1 = plt.figure(figsize=(6, 6))
# plt.fill(csf_x, csf_y, "k")
plt.axis("equal")
plt.axis("off")
plt.show()


#%% Define the points

def is_inside(x, y, csf_x, csf_y):
    """
    Check if a point (x, y) is inside the shape defined by csf_x and csf_y.
    
    Args:
    - x (float): The x-coordinate of the point.
    - y (float): The y-coordinate of the point.
    - csf_x (np.array): The x-coordinates of the shape's boundary.
    - csf_y (np.array): The y-coordinates of the shape's boundary.
    
    Returns:
    - bool: True if the point is inside the shape, False otherwise.
    """
    n = len(csf_x)
    inside = False

    p1x, p1y = csf_x[0], csf_y[0]
    for i in range(n+1):
        p2x, p2y = csf_x[i % n], csf_y[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside


npts = 1000
p = sc.objdict()
for k in ['x', 'y']:
    p[k] = np.random.rand(npts)*2-1
p.s = (1/(0.02+(p.x**2+p.y**2)**2))*5

isin = []
for ind,(ix,iy) in enumerate(zip(p.x,p.y)):
    inside = is_inside(ix, iy, csf_x, csf_y)
    if inside:
        isin.append(ind)
isin = np.array(isin)
notin = np.setdiff1d(np.arange(npts), isin)

plt.scatter(p.x[isin], p.y[isin], c='k', s=p.s[isin], alpha=0.5)
# plt.scatter(px[notin], py[notin], c='b')


