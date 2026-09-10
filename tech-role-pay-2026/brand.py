"""Skillenai chart branding + dataviz-skill compliance.

Palettes validated with the dataviz skill's validate_palette.js (light, surface #FBFCFE):
  RUNG  #9AD9E8 #35A0D8 #2E63C4 #2B2E8C  ordered/sequential; CVD dE 14.1 deutan, normal 15.8 PASS,
                                          lightness monotone 0.848->0.365. Contrast WARN on the
                                          lightest step is discharged by legend + data table.
  CAT2  #22C1DA #7A3FD1                   categorical; ALL CHECKS PASS, CVD dE 25.3 deutan.
  Brand indigo #4B54C6 and violet #7A3FD1 must NEVER both carry identity in one discrete
  encoding - they collapse to dE 2.0 under deuteranopia.
NOTE: Inter's latin subset has no arrow glyph - write "to", never an arrow.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.image import imread
from matplotlib.ticker import FuncFormatter

DS = "/Users/jrand/git-repos/skillenai-ds/work/comp-vs-flow"
for w in (400, 500, 600, 700):
    fm.fontManager.addfont(f"{DS}/fonts/Inter-{w}.ttf")

CYAN="#22C1DA"; BLUE="#2E7FD1"; INDIGO="#4B54C6"; VIOLET="#7A3FD1"; DEEP="#3B2A9A"
BG="#FBFCFE"; INK="#16233F"; GRID="#DAE0EC"; MUTE="#8A93A6"
RUNG=["#9AD9E8","#35A0D8","#2E63C4","#2B2E8C"]     # ordered: Entry, Mid, Senior, Staff+
CAT2=[CYAN, VIOLET]                                 # two-series categorical
SKN=LinearSegmentedColormap.from_list("skn",[CYAN,BLUE,INDIGO,VIOLET])
STAMP=imread(f"{DS}/logo_stamp.png")
K=FuncFormatter(lambda v,_: f"${v/1000:,.0f}K")

plt.rcParams.update({
    "font.family":"Inter","figure.facecolor":BG,"axes.facecolor":BG,
    "axes.edgecolor":GRID,"text.color":INK,"axes.labelcolor":INK,
    "xtick.color":INK,"ytick.color":INK,"xtick.labelsize":9,"ytick.labelsize":9,
    "axes.grid":False,"legend.frameon":False,
})

def header(fig, title, subtitle, x=0.0, y=1.0, dy=0.030, ts=16.0, ss=9.8):
    """Title + subtitle only. No logo, no gradient bar (house rule)."""
    fig.text(x, y, title, fontsize=ts, weight="bold", color=INK, va="top", ha="left")
    fig.text(x, y-dy, subtitle, fontsize=ss, color=MUTE, va="top", ha="left", linespacing=1.5)

def footer(fig, note, x=0.0, y=-0.004):
    """Methodology / source note, bottom-LEFT."""
    fig.text(x, y, note, fontsize=7.8, color=MUTE, va="top", ha="left", linespacing=1.55)

def stamp(fig, x=0.905, y=-0.010, h=0.030):
    """Grayscale spiral + 'Skillenai' wordmark, bottom-RIGHT. Title-case, never uppercase."""
    fw,fh=fig.get_size_inches(); w=h*fh/fw
    bx=fig.add_axes([x,y,w,h]); bx.axis("off"); bx.imshow(STAMP)
    fig.text(x+w+0.006, y+h/2, "Skillenai", fontsize=10.5, weight="semibold",
             color=MUTE, va="center", ha="left")

def tidy(ax, xgrid=True, spines=("top","right","left")):
    if xgrid: ax.grid(axis="x", color=GRID, alpha=0.75, lw=0.7, ls="-")
    ax.set_axisbelow(True)
    for sp in spines: ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(length=0)

def save(fig, path):
    fig.savefig(path, dpi=150, bbox_inches="tight", pad_inches=0.28, facecolor=BG)
    plt.close(fig); print("wrote", path)

def layout(fig, header_in=0.98, footer_in=0.82, left_in=None):
    """Reserve exact inches for the header block and the footer/stamp band, then
    tight_layout the axes into what's left. Returns (top_frac, bottom_frac) in
    figure coords so header()/footer()/stamp() can anchor without dead space."""
    fw, fh = fig.get_size_inches()
    top = 1.0 - header_in/fh
    bot = footer_in/fh
    rect = [0, bot, 1, top]
    fig.tight_layout(rect=rect)
    return top, bot

def save_exact(fig, path):
    """No bbox expansion - layout() already reserved the margins."""
    fig.savefig(path, dpi=150, facecolor=BG)
    plt.close(fig); print("wrote", path)
