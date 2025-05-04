"""
SIR-based Starsim logo
"""

import numpy as np
import matplotlib.pyplot as plt
import sciris as sc

n = 5000
x = np.arange(n)

S = [1]
I = [0]
R = [0]
beta = 0.01
gamma = 0.005
cols = sc.gridcolors(3)

for j in range(n-1):
    inf = beta*S[j]
    rec = I[j]*gamma
    s = S[j] - inf
    i = I[j] + inf - rec
    r = R[j] + rec
    S.append(s)
    I.append(i)
    R.append(r)


sc.options(dpi=200)
fig = plt.figure(figsize=(12,3))
kw = dict(lw=10, alpha=0.8)
plt.plot(x, R, c=cols[2], **kw)
plt.plot(x, I, c=cols[1], **kw)
plt.plot(x, S, c=cols[0], **kw)
plt.axis('off')
sc.figlayout()
plt.show()
