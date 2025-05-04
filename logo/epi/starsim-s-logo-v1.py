"""
Ugly.

Do a star as a network, black and green nodes/edges, with a larger gold node
in the middle.
"""

import numpy as np
import sciris as sc
import matplotlib.pyplot as plt

def mkcurve(xoff=0, dist=0.1):
    dx = 0.001
    f = 4.0
    xp = sc.inclusiverange(-1, 1, dx)
    yp = np.tanh(f*xp)
    r = 1.0
    x1 = sc.inclusiverange(-1, 0, dx)
    x2 = sc.inclusiverange(0, 1-dx, dx)
    x_ = sc.cat((x1+1), (x2-1))
    y1 = np.sqrt(r**2-x1**2)
    y2 = np.sqrt(r**2-x2**2)
    y_ = sc.cat(y1, -y2)
    inds = np.argsort(x_)
    x_ = x_[inds]
    y_ = y_[inds]

    xf = xp
    yf = (yp + y_)/2
    mid = len(xp)//2
    xf = sc.cat(xf[:mid], xf[mid+1:])
    yf = sc.cat(yf[:mid], yf[mid+1:])

    npts = len(xf)
    pts = sc.autolist(0)
    xlist = sc.autolist(xf[0])
    ylist = sc.autolist(yf[0])
    for i in range(1,npts):
        newx = xf[i]
        newy = yf[i]
        thisdist = ((newx-xlist[-1])**2+(newy-ylist[-1])**2)**0.5
        print(thisdist, dist)
        if thisdist > dist:
            pts += i
            xlist += newx
            ylist += newy

    x = sc.cat(xlist)
    y = sc.cat(ylist)

    print(f'Keeping {len(xlist)} of {npts}')

    x += xoff
    # xf = xf[::stride]
    # yf = yf[::stride]

    return x,y



sc.options(dpi=300)

plt.figure()
a = 0.2
af = 0.8
x1,y1 = mkcurve(xoff=-0.5, dist=0.45)
x2,y2 = mkcurve(xoff=0.5, dist=0.45)
plt.plot(x1,y1, lw=5, c='gold')
plt.plot(x2,y2, lw=5, c='gold')
plt.scatter(x1,y1, s=500, c='k', zorder=10)
plt.scatter(x2,y2, s=500, c='green', zorder=10)
r1 = np.random.choice(len(x1), size=10)
r2 = np.random.choice(len(x1), size=10)
for ir,jr in zip(r1, r2):
    rx1 = x1[ir]
    rx2 = x2[jr]
    ry1 = y1[ir]
    ry2 = y2[jr]
    plt.plot([rx1, rx2], [ry1, ry2])


plt.axis('square')
plt.ylim(bottom=-1.5)
plt.axis('off')
sc.figlayout()
plt.show()
