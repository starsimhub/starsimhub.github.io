"""
SIR-based Starsim logo
"""

import numpy as np
import matplotlib.pyplot as plt
import sciris as sc

n = 800
x = np.arange(n)

S = [0.995]
I = [0.005]
R = [0]
beta = 0.04
gamma = 0.004
cols = sc.gridcolors(3)

for j in range(n-1):
    inf = beta*I[j]*S[j]
    rec = I[j]*gamma
    s = S[j] - inf
    i = I[j] + inf - rec
    r = R[j] + rec
    S.append(s)
    I.append(i)
    R.append(r)


stride = 20
res = sc.objdict()
for k,v in dict(x=x, S=S, I=I, R=R).items():
    res[k] = v[::stride]

sc.options(dpi=200)

fig = plt.figure(figsize=(6,6))
kw = dict(s=500, alpha=0.8, marker='o')
plt.scatter(res.x, res.R, c=cols[2], **kw)
plt.scatter(res.x, res.I, c=cols[1], **kw)
plt.scatter(res.x, res.S, c=cols[0], **kw)
plt.axis('off')
sc.figlayout()
plt.show()
