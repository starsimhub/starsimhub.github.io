"""
Circle-virus network with gold asterisk in the middle.
"""

import numpy as np
import sciris as sc
import matplotlib.pyplot as plt

class Dots(sc.prettyobj):

    def __init__(self):
        self.seed = 3
        self.ms = 800 # Marker size
        self.ang = 0.25
        self.r_ast = 0.25
        self.r_in = 0.48
        self.r_out = 0.7
        self.r_spk = 0.95
        self.n_ast = 5
        self.n_shell = 20
        self.x = sc.autolist()
        self.y = sc.autolist()
        self.s = sc.autolist()
        self.c = sc.autolist()
        self.cols = sc.objdict(k='k', y='gold', r='red', g='g', b='navy')
        np.random.seed(self.seed)
        self.make()
        self.logo()
        return

    @property
    def df(self):
        return sc.dataframe(x=self.x, y=self.y, s=self.s, c=self.c)

    def p2e(self, r, ang):
        """ Convert polar to euclidean coordinates """
        ang *= 2*np.pi
        x = r * np.cos(ang)
        y = r * np.sin(ang)
        return x, y

    def e2p(self, x=None, y=None):
        """ Convert euclidean to polar coordinates """
        if x is None:
            x = self.x
        if y is None:
            y = self.y
        r = np.sqrt(x**2 + y**2)
        ang = np.arctan2(y, x) / (2*np.pi)
        return r, ang

    def xy(self):
        return self.x, self.y

    def add_dot(self, x, y, s=None, c=None):
        self.x.append(x)
        self.y.append(y)
        self.s.append(s)
        self.c.append(c)
        return

    def make_asterisk(self):
        self.add_dot(0, 0, 1.5, self.cols.y)
        for i in range(self.n_ast):
            ang = i/self.n_ast + self.ang
            x, y = self.p2e(self.r_ast, ang)
            self.add_dot(x, y, 1.0, self.cols.y)
        return

    def make_circle(self):
        for r in [self.r_in, self.r_out]:
            n = int(self.n_shell*r)
            for i in range(n):
                ang = i/n + self.ang
                x, y = self.p2e(r, ang)
                self.add_dot(x, y, 0.8, self.cols.k)
        return

    def make_spikes(self):
        n = int(self.n_shell*self.r_out)//2
        for i in range(n):
            ang = i/n + self.ang
            x, y = self.p2e(self.r_spk, ang)
            self.add_dot(x, y, 0.8, self.cols.r)
        return

    def make(self):
        self.make_asterisk()
        self.make_circle()
        self.make_spikes()
        return

    def logo(self, save=True):
        fig = plt.figure(dpi=300)
        df = self.df
        plt.scatter(df.x, df.y, s=df.s*self.ms, c=df.c)

        plt.axis('square')
        plt.xlim(left=-1, right=1)
        plt.ylim(bottom=-1, top=1)
        plt.axis('off')
        plt.tight_layout()
        if save:
            sc.savefig('starsim-sky-logo-v2.png')
        plt.show()
        return fig

dots = Dots()

