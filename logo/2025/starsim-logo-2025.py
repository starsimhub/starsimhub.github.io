"""
Circle-virus network with gold asterisk in the middle.

Now with lines.
"""

import numpy as np
import sciris as sc
import matplotlib.pyplot as plt

colkey = 'v2'
color_options = sc.objdict(
    blue = sc.objdict(ast='gold', sh='#47C7F4', spk='#0372A2'),
    green = sc.objdict(ast='gold', sh='tab:green', spk='#C1272D'),
    black = sc.objdict(ast='gold', sh='k', spk='tab:red'),
    hybrid = sc.objdict(ast='gold', sh='#47C7F4', spk='k'),
    lith = sc.objdict(ast='#FDB913', sh='#006A44', spk='#C1272D'),
    ghana = sc.objdict(ast='#FCD20F', sh='#006B3D', spk='#CF0921'),
    sky = sc.objdict(ast='gold', sh='#47C7F4', spk='#47C7F4'),
    inv1 = sc.objdict(ast='#0372A2', sh='#47C7F4', spk='#FDB913'),
    inv2 = sc.objdict(ast='k', sh='tab:green', spk='#C1272D'),
    inv3 = sc.objdict(ast='k', sh='#FDB913', spk='#006A44'),
    v1 = sc.objdict(ast='#004d89', sh='#ffc12f', spk='#30a1f4'),
    v2 = sc.objdict(ast='k', sh='#ffc12f', spk='#135e4a'),
)[colkey]

class Dots(sc.prettyobj):

    def __init__(self, full=False):
        self.seed = 3
        self.cs = 1.8
        self.dsp = 1.0
        self.dsh = 1.0
        self.ms = 640 # Marker size
        self.ang = 0.25
        self.r_ast = 0.25
        self.r_sh = 0.47
        self.r_spk = 0.69
        self.n_ast = 6
        self.n_sh = 12
        self.n_spk = 6
        self.n_out = 18
        self.lw = 5
        self.x = sc.autolist()
        self.y = sc.autolist()
        self.s = sc.autolist()
        self.c = sc.autolist()
        self.lines = sc.autolist()
        self.cols = color_options
        if 'core' not in self.cols:
            self.cols.core = self.cols.ast
        np.random.seed(self.seed)
        self.xy_sp = sc.autolist()
        self.xy_sh = sc.autolist()
        self.make()
        if full:
            self.full()
        else:
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

    def add_line(self, i, j, c=None):
        self.lines.append([i, j, c])
        return

    def make_asterisk(self):
        self.add_dot(0, 0, self.cs, self.cols.core)
        for i in range(self.n_ast):
            ang = i/self.n_ast + self.ang
            x, y = self.p2e(self.r_ast, ang)
            self.add_dot(x, y, self.dsp, self.cols.ast)

        for j in range(1,self.n_ast+1):
            self.add_line(0, j, self.cols.core)

        for path in [
                [1,18],
                [16,6,17],
                [5,15],
                [12,4,14],
                [10,3,11],
                [9,2],
                [8,1],
            ]:
            for k in range(len(path)-1):
                i = path[k]
                j = path[k+1]
                self.add_line(i, j, self.cols.ast)

        return

    def make_spikes(self, perspective=1.0, make=True):
        for j in range(2):
            f = perspective**(j+1)
            reg = self.dsp
            big = self.dsp*f
            sma = self.dsp/f
            sizes = {0:reg, 1:sma, 2:big, 3:reg, 4:big, 5:sma}
            r = [self.r_sh, self.r_spk][j]
            for i in range(self.n_spk):
                ang = i/self.n_spk + self.ang
                x, y = self.p2e(r, ang)
                if make:
                    self.add_dot(x, y, sizes[i], self.cols.spk)
                else:
                    self.xy_sp += (x,y)

        for i,j in [
                [17,34],
                [15,31],
                [13,28],
                [11,25],
                [9,22],
                [7,19],
            ]:
            self.add_line(i, j, self.cols.spk)
        return

    def make_shell(self):
        self.make_spikes(make=False)
        for j in range(2):
            n = [self.n_sh, self.n_out][j]
            r = [self.r_sh, self.r_spk][j]
            for i in range(n):
                ang = i/n + self.ang
                x, y = self.p2e(r, ang)
                size = 0
                if (x,y) not in self.xy_sp:
                    size = self.dsh
                    self.xy_sh += (x,y)
                self.add_dot(x, y, size, self.cols.sh)

        for path in [
                [18,35],
                [33,16,15],
                [30,14,29],
                [14,13,12,26,27],
                [10,24,23,9],
                [7,8,20,7],
            ]:
            for k in range(len(path)-1):
                i = path[k]
                j = path[k+1]
                self.add_line(i, j, self.cols.sh)
        return

    def make(self):
        self.make_asterisk()
        self.make_shell()
        self.make_spikes()
        return

    def logo(self, save=True, debug=False, ax=None):
        if ax is None:
            fig = plt.figure(figsize=[4.5]*2, dpi=100)
            ax = fig.add_axes([0, 0, 1, 1])
        else:
            fig = None
        df = self.df

        # Plot dots
        ax.scatter(df.x, df.y, s=df.s*self.ms, c=df.c)
        used = set()
        if debug:
            for i in range(len(df)):
                x = np.round(df.x[i], 3)
                y = np.round(df.y[i], 3)
                if (x,y) not in used:
                    plt.text(x, y, i, c='w')
                    used.add((x,y))
                print(used)

        # Plot lines
        for line in self.lines:
            i,j,c = line
            ax.plot([df.x[i], df.x[j]], [df.y[i], df.y[j]], c=c, lw=self.lw, zorder=-10)

        ax.set_xlim(left=-1, right=1)
        ax.set_ylim(bottom=-1, top=1)
        ax.axis('off')
        if save:
            fn = f'starsim-logo-2025-{colkey}.png'
            sc.savefig(fn, transparent=True)
            sc.runcommand(f'trim {fn}')
        plt.show()
        return fig

    def full(self, save=True, debug=False):
        """ Full logo, with text """
        # Setup
        fig = plt.figure(figsize=[4.5*4, 4.5], dpi=100)
        ax1 = fig.add_axes([0, 0, 1/4, 1])
        ax2 = fig.add_axes([1/4, 0, 3/4, 1])
        ax2.set_xlim(left=0, right=1)
        ax2.set_ylim(bottom=0, top=1)
        if debug:
            ax1.axhline()
            ax2.axhline(0.5)

        # Make logo
        self.logo(save=False, ax=ax1)

        # Title
        sc.fonts(add='fonts/KumbhSans-ExtraBold.ttf', use=True)
        ax2.text(-0.025, 0.43, 'Starsim', size=230, verticalalignment='center')
        ax2.axis('off')

        if save:
            fn = f'starsim-logo-2025-{colkey}-full.png'
            sc.savefig(fn, transparent=True)
            sc.runcommand(f'trim {fn}')
        plt.show()
        return fig

dots = Dots(full=True)

