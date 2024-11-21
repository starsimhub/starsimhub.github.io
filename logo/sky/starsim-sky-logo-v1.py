"""
Ugly.

Do a star as a network, black and green nodes/edges, with a larger gold node
in the middle.
"""

import numpy as np
import sciris as sc
import matplotlib.pyplot as plt

class Dots(sc.prettyobj):

    def __init__(self):
        self.seed = 1
        self.npts = 10
        self.niter = 200
        self.v_center = 1e-2
        self.v_neigh = 1e-1

        np.random.seed(self.seed)
        self.x = np.random.uniform(-1, 1, size=self.npts)
        self.y = np.random.uniform(-1, 1, self.npts)
        self.step = 0
        return

    def xy(self):
        return self.x, self.y

    def all_dists(self, i):
        x,y = self.xy()
        return ((x-x[i])**2 + (y-y[i])**2)**0.5

    def min_dist(self, i):
        x,y = self.xy()
        dists = self.all_dists(i)
        ind = np.argmin(dists)
        return sc.dictobj(ind=ind, dist=dists[ind], x=x[ind], y=y[ind])

    def diff2vec(self, i, x1, y1, x2, y2, sign=1):
        xdiff = x2 - x1
        ydiff = y2 - y1
        mag = 1.0#(xdiff**2 + ydiff**2)**0.5
        xcomp = xdiff/mag*sign
        ycomp = ydiff/mag*sign
        # print(f'{self.step=}, {i=}, {x2=}, {y2=}, {xdiff=}, {ydiff=}, {mag=}, {xcomp=}, {ycomp=}')
        return xcomp, ycomp

    def to_center(self):
        x,y = self.xy()
        npts = self.npts
        dx = np.zeros(npts)
        dy = np.zeros(npts)
        for i in range(npts):
            dx[i], dy[i] = self.diff2vec(i, 0, 0, x[i], y[i], sign=-1)
        print(dx, dy)
        self.x += dx*self.v_center
        self.y += dy*self.v_center
        return

    def run(self, animate=0.1):
        fig = None
        for i in range(self.niter):
            self.step += 1
            self.to_center()
            if animate:
                fig = self.plot(fig, animate)
        return

    def plot(self, fig=None, pause=None):
        if fig is None:
            fig = plt.figure(dpi=300)
        else:
            plt.clf()
        plt.scatter(self.x, self.y, s=150)
        plt.axis('square')
        plt.xlim(left=-1, right=1)
        plt.ylim(bottom=-1, top=1)
        plt.axis('off')
        plt.title(f'Step {self.step}')
        plt.tight_layout()
        plt.show()
        if pause:
            plt.pause(pause)
        return fig


dots = Dots()
dots.run()


