"""
SIR-based Starsim logo
"""

import numpy as np
import matplotlib.pyplot as plt
import sciris as sc

n = 800
x = np.arange(n)

S = [0.998]
I = [0.002]
R = [0]
beta = 0.03
gamma = 0.004
cols = ['black', 'gold', 'red']

for j in range(n-1):
    inf = beta*I[j]*S[j]
    rec = I[j]*gamma
    s = S[j] - inf
    i = I[j] + inf - rec
    r = R[j] + rec
    S.append(s)
    I.append(i)
    R.append(r)


mindist = 0.1
res = sc.objdict()
for k,v in dict(S=S, I=I, R=R).items():
    res[k] = sc.objdict()
    r = res[k]
    r.x = [x[0]]
    r.y = [v[0]]
    for i in range(1, len(v)):
        lastx = r.x[-1]
        lasty = r.y[-1]
        thisx = x[i]
        thisy = v[i]
        dist = np.sqrt(((thisx - lastx)/n)**2 + (thisy - lasty)**2)
        if dist > mindist:
            print('Appending', thisx, dist)
            r.x.append(thisx)
            r.y.append(thisy)
        else:
            print('Skipping', thisx, dist)


sc.options(dpi=200)

fig = plt.figure(figsize=(6,6))
kw = dict(lw=0, s=800, alpha=0.8)
plt.scatter(res.R.x, res.R.y, c=[cols[2]], **kw)
plt.scatter(res.I.x, res.I.y, c=[cols[1]], **kw)
plt.scatter(res.S.x, res.S.y, c=[cols[0]], **kw)
plt.axis('off')
sc.figlayout()
plt.show()
