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
        self.seed = 3
        self.npts = 50
        self.niter = 1000
        self.mindist = 0.25
        self.v_center = 1e-3
        self.v_neighbor = 1e-2
        self.temp = 0.2

        np.random.seed(self.seed)
        self.x = np.random.uniform(-1, 1, size=self.npts)
        self.y = np.random.uniform(-1, 1, self.npts)
        self.step = 0
        self.trim()
        return

    def xy(self):
        return self.x, self.y

    def trim(self):
        x,y = self.xy()
        r = x**2+y**2
        valid = r<=1.0
        self.x = self.x[valid]
        self.y = self.y[valid]
        self.npts = valid.sum()
        return

    def all_dists(self, i):
        x,y = self.xy()
        return ((x-x[i])**2 + (y-y[i])**2)**0.5

    def nearest(self, i):
        x,y = self.xy()
        dists = self.all_dists(i)
        dists[i] = np.inf
        assert dists.min() > 0
        ind = np.argmin(dists)
        return sc.dictobj(ind=ind, dist=dists[ind], x=x[ind], y=y[ind])

    def diff2vec(self, i, x1, y1, x2, y2):
        xdiff = x2 - x1
        ydiff = y2 - y1
        return -xdiff, -ydiff

    def noise(self, arg):
        return arg*sc.perturb(len(arg), span=self.temp, randseed=self.seed)

    def to_center(self):
        x,y = self.xy()
        npts = self.npts
        dx = np.zeros(npts)
        dy = np.zeros(npts)
        for i in range(npts):
            dx[i], dy[i] = self.diff2vec(i, 0, 0, x[i], y[i])
        self.x += self.noise(dx*self.v_center)
        self.y += self.noise(dy*self.v_center)
        return

    def push_neighbor(self):
        x,y = self.xy()
        npts = self.npts
        dx = np.zeros(npts)
        dy = np.zeros(npts)
        for i in range(npts):
            near = self.nearest(i)
            # print(near.dist)
            if near.dist < self.mindist:
                # print('YES', i)
                dx[i], dy[i] = self.diff2vec(i, near.x, near.y, x[i], y[i])
        self.x += self.noise(-dx*self.v_neighbor)
        self.y += self.noise(-dy*self.v_neighbor)
        return

    def run(self, animate=0):
        fig = None
        for i in range(self.niter):
            self.step += 1
            self.to_center()
            self.push_neighbor()
            if animate:
                fig = self.plot(fig, animate)
        return

    def plot(self, fig=None, pause=None):
        if fig is None:
            fig = plt.figure(dpi=300)
        else:
            plt.clf()
        # plt.scatter([0], [0], c='k', s=300)
        plt.scatter(self.x, self.y, s=800)
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
dots.plot()


