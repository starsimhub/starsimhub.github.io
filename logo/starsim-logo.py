#!/usr/bin/env python
"""
Create the Starsim logo: a circular virus-like network
with a black asterisk (for "*sim") in the middle, that also
looks like coordinate axes.

Usage:
    ./starsim-logo.py clean # Clean up all generated files
    ./starsim-logo.py make  # Make all logos

Only works on Linux; requires cairosvg and ImageMagick (for trimming and resizing).
"""

# For StarsimLogo
import numpy as np
import sciris as sc
import matplotlib.pyplot as plt

# For trim_svg
import sys
import io
import re
import cairosvg
from PIL import Image

# Names of packages to make logos for
NAMES = [
    'Starsim',
    'Covasim',
    'FPsim',
    'HPVsim',
    'STIsim',
    'TBsim',
]

# Extensions
EXTS = ['png', 'svg']

# Colors to use
COLORS = sc.objdict(
    light = sc.objdict(ast='k', spk='#135e4a', sh='#ffc12f'),
    mid = sc.objdict(ast='#555555', spk='#1c8a6c', sh='#ffc12f'),
    dark = sc.objdict(ast='#dddddd', spk='#135e4a', sh='#ffc12f'),
)

# Font to use for the logos
FONT = 'fonts/KumbhSans-ExtraBold.ttf'


def trim(fn):
    """ Trim a PNG or SVG file """
    if fn.endswith('.png'):
        sc.runcommand(f'convert "{fn}" -trim "{fn}"')
    elif fn.endswith('.svg'):
        trim_svg(fn)
    else:
        raise ValueError(f'Cannot trim {fn} (not a PNG or SVG)')
    return

class StarsimLogo(sc.prettyobj):

    def __init__(self, colkey='light'):
        self.colkey = colkey
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
        self.lw = 5
        self.x = sc.autolist()
        self.y = sc.autolist()
        self.s = sc.autolist()
        self.c = sc.autolist()
        self.lines = sc.autolist()
        self.xy_sp = sc.autolist()
        self.initialize()
        return
    
    def initialize(self):
        """ Run other tasks to finish initialization """
        sc.fonts(add=FONT, use=True)
        np.random.seed(self.seed)
        self.make(self.colkey)
        return
    
    @property
    def df(self):
        """ Convert to dataframe """
        return sc.dataframe(x=self.x, y=self.y, s=self.s, c=self.c)

    def p2e(self, r, ang):
        """ Convert polar to euclidean coordinates """
        ang *= 2*np.pi
        x = r * np.cos(ang)
        y = r * np.sin(ang)
        return x, y

    def add_dot(self, x, y, s=None, c=None):
        """ Adds a single dot to the list of dots """
        self.x.append(x)
        self.y.append(y)
        self.s.append(s)
        self.c.append(c)
        return

    def add_line(self, i, j, c=None):
        """ Adds a single line to the list of lines """
        self.lines.append([i, j, c])
        return

    def make_asterisk(self):
        """ Make the asterisk in the middle of the logo """
        self.add_dot(0, 0, self.cs, self.cols.core)
        for i in range(self.n_ast):
            ang = i/self.n_ast + self.ang
            x, y = self.p2e(self.r_ast, ang)
            self.add_dot(x, y, self.dsp, self.cols.ast)

        for j in range(1,self.n_ast+1):
            self.add_line(0, j, self.cols.core)

        return

    def make_spikes(self, perspective=1.0, make=True):
        """ Make the spike-like projections from the center """
        for j in range(1):
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

        for path in [
                [2,9],
                [3,11],
                [4,13],
                [5,15],
                [6,17],
            ]:
            for k in range(len(path)-1):
                i = path[k]
                j = path[k+1]
                self.add_line(i, j, self.cols.spk)
        return

    def make_shell(self):
        """" Make the paler dots that the spikes project into """
        self.make_spikes(make=False)
        n = self.n_sh
        r = self.r_sh
        for i in range(n):
            ang = i/n + self.ang
            x, y = self.p2e(r, ang)
            size = 0 if (x,y) in self.xy_sp else self.dsh
            self.add_dot(x, y, size, self.cols.sh)

        for path in [
                [3,10,2],
                [8,1],
                [18,1],
                [12,4,14,13,12],
                [7,8,2],
                [14,5,16,6],
            ]:
            for k in range(len(path)-1):
                i = path[k]
                j = path[k+1]
                self.add_line(i, j, self.cols.sh)
        return

    def set_mode(self, colkey):
        """ Set light or dark mode """
        self.colkey = colkey
        self.cols = COLORS[colkey]
        if 'core' not in self.cols:
            self.cols.core = self.cols.ast
        self.facecolor = 'k' if colkey == 'dark' else 'w'
        self.textcolor = self.cols.core
        return

    def make(self, colkey='light'):
        self.set_mode(colkey)
        self.make_asterisk()
        self.make_shell()
        self.make_spikes()
        return

    def plot_icon(self, save=True, show=None, debug=False, ax=None):
        if ax is None:
            fig = plt.figure(figsize=[4.5]*2, dpi=100, facecolor=self.facecolor)
            ax = fig.add_axes([0, 0, 1, 1])
        else:
            fig = None
        df = self.df

        # Plot dots
        ax.scatter(df.x, df.y, s=df.s*self.ms, c=df.c, marker=None)
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
            base = f'starsim-icon-{self.colkey}'
            print(f'Saving {base}...')
            fns = [f'{base}.{ext}' for ext in EXTS]
            for fn in fns:
                sc.savefig(fn, transparent=True)
                trim(fn)
            if self.colkey == 'light':
                sc.runcommand(f'convert {fns[0]} -resize 32x32 favicon.ico') # Brittle: assumes png is first
            plt.close(fig)
        if show or (show is None and not save):
            plt.show()
        return fig

    def plot_full(self, save=True, show=None, debug=False, names=NAMES):
        """ Full logo, with text """

        for name in names:

            # Setup
            fig = plt.figure(figsize=[4.5*4, 4.5], dpi=100, facecolor=self.facecolor)
            ax1 = fig.add_axes([0, 0, 1/4, 1])
            ax2 = fig.add_axes([1/4, 0, 3/4, 1])
            ax2.set_xlim(left=0, right=1)
            ax2.set_ylim(bottom=0, top=1)
            if debug:
                ax1.axhline()
                ax2.axhline(0.5)

            # Make icon
            fig = self.plot_icon(save=False, show=False, ax=ax1)

            # Title
            ax2.text(-0.055, 0.45, name, size=160, verticalalignment='center', color=self.textcolor)
            ax2.axis('off')

            if save:
                base = f'{name.lower()}-logo-{self.colkey}'
                print(f'Saving {base}...')
                fns = [f'{base}.{ext}' for ext in EXTS]
                for fn in fns:
                    sc.savefig(fn, transparent=True)
                    trim(fn)
                plt.close(fig)
            if show or (show is None and not save):
                plt.show()
                
        return fig

    def make_all(self, save=True, debug=False):
        for colkey in ['light', 'mid', 'dark']:
            sc.heading(f'Working on {colkey}')
            self.make(colkey)
            f1 = self.plot_icon(save=save, debug=debug)
            f2 = self.plot_full(save=save, debug=debug)
        return f1,f2


def trim_svg(input_file, output_file=None, padding=0, scale=4):
    """
    Trim an SVG canvas to the bounds of visible content.

    Args:
        input_file (str|Path): Input SVG file.
        output_file (str|Path|None): Output SVG file. If None, overwrite input_file.
        padding (float): Padding to add around content, in SVG user units.
        scale (float): Render scale for detecting bounds. Higher values are slower but improve accuracy for thin lines

    Returns:
        Path: output path

    Written by ChatGPT
    """
    input_file = sc.path(input_file)
    output_file = sc.path(output_file) if output_file else input_file

    text = input_file.read_text()

    # Read viewBox
    m = re.search(r'viewBox="([^"]+)"', text)
    if not m:
        raise ValueError(f"{input_file}: SVG must contain a viewBox")

    vx, vy, vw, vh = map(
        float,
        m.group(1).replace(",", " ").split()
    )

    # Render to PNG
    png = cairosvg.svg2png(
        bytestring=text.encode(),
        scale=scale
    )

    im = Image.open(io.BytesIO(png)).convert("RGBA")
    bbox = im.getchannel("A").getbbox()

    if not bbox:
        raise ValueError(f"{input_file}: no visible content found")

    l, t, r, b = bbox

    # Pixel → SVG coordinate conversion
    ux = vw / im.width
    uy = vh / im.height

    nx = vx + l * ux - padding
    ny = vy + t * uy - padding
    nw = (r - l) * ux + 2 * padding
    nh = (b - t) * uy + 2 * padding

    new_viewbox = f"{nx:g} {ny:g} {nw:g} {nh:g}"

    # Rewrite root attrs
    text = re.sub(
        r'viewBox="[^"]+"',
        f'viewBox="{new_viewbox}"',
        text,
        count=1,
    )

    text = re.sub(
        r'width="[^"]+"',
        f'width="{nw:g}pt"',
        text,
        count=1,
    )

    text = re.sub(
        r'height="[^"]+"',
        f'height="{nh:g}pt"',
        text,
        count=1,
    )

    output_file.write_text(text)
    return output_file


if __name__ == '__main__':

    T = sc.timer()

    args = sys.argv[1:]

    if 'clean' in args:
        what = '*.png *.svg *.ico'
        files = sc.runcommand(f'ls -1 {what}')
        out = input(f'Clean files? (enter=yes)\n{files}')
        if not out:
            sc.runcommand(f'rm -v {what}', printoutput=True)
    elif 'make' in args:
        sc.options(interactive=False)
        ssl = StarsimLogo()
        ssl.make_all(debug=0)
    else:
        print(__doc__)

    T.toc()

