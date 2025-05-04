"""
Logistic-based Starsim logo
"""

import numpy as np
import matplotlib.pyplot as plt
import sciris as sc

n = 100
x = np.linspace(-1, 1, n)
cols = ['navy', 'black']

f = 10
sp = 0.3

r = 0.5
I = sc.cat(
    -np.sqrt(r**2 - x[n//2:]**2),
    np.sqrt(r**2 - x[:n//2]**2)
)
R = I+0.2

# I = -1 / (1 + np.exp(f*(x+sp)))
# R = -1 / (1 + np.exp(f*(x-sp)))

mindist = 0.1
res = sc.objdict()
for k,v in dict(I=I, R=R).items():
    res[k] = sc.objdict()
    r = res[k]
    r.x = [x[0]]
    r.y = [v[0]]
    for i in range(1, len(v)):
        lastx = r.x[-1]
        lasty = r.y[-1]
        thisx = x[i]
        thisy = v[i]
        dist = np.sqrt(((thisx - lastx))**2 + (thisy - lasty)**2)
        if dist > mindist:
            print('Appending', thisx, dist)
            r.x.append(thisx)
            r.y.append(thisy)
        else:
            print('Skipping', thisx, dist)


sc.options(dpi=200)

fig = plt.figure(figsize=(6,6))
kw = dict(lw=0, s=800, alpha=0.8)
plt.scatter(res.R.x, res.R.y, c=[cols[1]], **kw)
plt.scatter(res.I.x, res.I.y, c=[cols[0]], **kw)
plt.axis('off')
sc.figlayout()
plt.show()
