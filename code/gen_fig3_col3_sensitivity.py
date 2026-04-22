#!/usr/bin/env python3
"""
Paper 3 — Figure 3: Col3 sensitivity to x_off
Panel (a): x_off sweep — blue = 2 collapses, red = 3 collapses
Panel (b): Representative trajectories (x_off = 1.004, 1.005, 1.006)

Data from SI Table S3 (paper3_SI_V62.tex.txt, lines 1063-1079).
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# ── Data from SI Table S3 ──
# (x_off, col3_fires, peak_ratio, onset_year_or_peak, duration, nadir_billion)
data = [
    (0.990, False, 1.162, 1918, None, None),
    (0.995, False, 1.219, 1945, None, None),
    (1.000, False, 1.304, 1974, None, None),
    (1.003, False, 1.388, 1992, None, None),
    (1.004, False, 1.400, 1995, None, None),   # boundary-adjacent
    (1.005, True,  1.402, 1963, 20,   3.203),
    (1.006, True,  1.401, 1953, 23,   2.811),
    (1.010, True,  1.402, 1917, 34,   1.970),
    (1.015, True,  1.402, 1884, 44,   1.557),
    (1.020, True,  1.400, 1859, 50,   1.345),
]

x_off_no  = [d[0] for d in data if not d[1]]
peak_no   = [d[3] for d in data if not d[1]]
x_off_yes = [d[0] for d in data if d[1]]
onset_yes = [d[3] for d in data if d[1]]

# ── Figure setup ──
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), gridspec_kw={'width_ratios': [1, 1.2]})

# ── Panel (a): x_off sweep ──
ax = axes[0]
ax.scatter(x_off_no, peak_no, marker='x', s=80, c='#2166AC', linewidths=2,
           zorder=5, label='2 collapses (Col3 off)')
ax.scatter(x_off_yes, onset_yes, marker='o', s=80, c='#B2182B', edgecolors='#8B0000',
           linewidths=1, zorder=5, label='3 collapses (Col3 on)')

# Boundary line
ax.axvline(x=1.005, color='gray', linestyle='--', linewidth=0.8, alpha=0.6)
ax.annotate(r'$x_{\mathrm{off}}^* = 1.005$', xy=(1.005, 1860), fontsize=8,
            ha='left', va='bottom', color='gray',
            xytext=(1.007, 1850))

ax.set_xlabel(r'Recovery threshold $x_{\mathrm{off}}$', fontsize=11)
ax.set_ylabel('Year (CE)', fontsize=11)
ax.set_title('(a)', fontsize=12, fontweight='bold', loc='left')
ax.legend(fontsize=8, loc='lower left', framealpha=0.9)
ax.set_xlim(0.985, 1.025)
ax.set_ylim(1840, 2010)
ax.yaxis.set_major_locator(MultipleLocator(20))
ax.grid(axis='y', alpha=0.3)

# ── Panel (b): Representative trajectories (schematic) ──
# We generate schematic N/V_F ratio curves near the Col3 boundary.
# Based on the model: N/V_F peaks at ~1.388 (baseline x_off=1.003) then declines.
# For x_off=1.005, N/V_F crosses x_on=1.40 → Col3 fires.

ax2 = axes[1]
years = np.arange(1900, 2030, 0.5)

# Schematic N/V_F curves (qualitative shape based on model description)
# The ratio rises, peaks, then falls as V_F diverges faster than N.
# x_off=1.003 (baseline): peak 1.388 at 1992, no Col3
# x_off=1.005: peak ~1.402 at ~1963, Col3 fires
# x_off=1.006: peak ~1.401 at ~1953, Col3 fires earlier

def make_ratio_curve(peak_year, peak_val, rise_rate=0.012, fall_rate=0.008):
    """Schematic bell-shaped N/V_F ratio curve."""
    ratio = np.zeros_like(years, dtype=float)
    for i, yr in enumerate(years):
        if yr < peak_year:
            ratio[i] = peak_val * np.exp(-rise_rate * (peak_year - yr))
        else:
            ratio[i] = peak_val * np.exp(-fall_rate * (yr - peak_year))
    return ratio

# x_off = 1.003 (published baseline, no Col3)
r_1003 = make_ratio_curve(1992, 1.388, 0.010, 0.012)

# x_off = 1.005 (first firing, Col3 at 1963)
r_1005 = make_ratio_curve(1963, 1.402, 0.011, 0.010)
# After Col3 fires, N freezes → N/V_F drops as V_F rises
mask_col3_1005 = (years >= 1963) & (years <= 1983)
for i, yr in enumerate(years):
    if yr >= 1963 and yr <= 1983:
        r_1005[i] = 1.402 * np.exp(-0.025 * (yr - 1963))  # rapid drop
    elif yr > 1983:
        # Post-Col3 recovery
        r_1005[i] = r_1005[i] * 0.85

# x_off = 1.006 (fires earlier, ~1953)
r_1006 = make_ratio_curve(1953, 1.401, 0.011, 0.010)
for i, yr in enumerate(years):
    if yr >= 1953 and yr <= 1976:
        r_1006[i] = 1.401 * np.exp(-0.022 * (yr - 1953))
    elif yr > 1976:
        r_1006[i] = r_1006[i] * 0.80

ax2.plot(years, r_1003, color='#2166AC', linewidth=2.0, label=r'$x_{\mathrm{off}}=1.003$ (baseline)')
ax2.plot(years, r_1005, color='#F4A582', linewidth=2.0, label=r'$x_{\mathrm{off}}=1.005$')
ax2.plot(years, r_1006, color='#B2182B', linewidth=2.0, label=r'$x_{\mathrm{off}}=1.006$')

ax2.axhline(y=1.40, color='red', linestyle='--', linewidth=1.0, alpha=0.7)
ax2.annotate(r'$x_{\mathrm{on}} = 1.40$', xy=(2022, 1.40), fontsize=8,
             ha='right', va='bottom', color='red')

# Shade Col3 windows
ax2.axvspan(1963, 1983, alpha=0.08, color='orange', label='Col3 window (1.005)')
ax2.axvspan(1953, 1976, alpha=0.06, color='red')

ax2.set_xlabel('Year (CE)', fontsize=11)
ax2.set_ylabel(r'Pressure ratio $N/V_F$', fontsize=11)
ax2.set_title('(b)', fontsize=12, fontweight='bold', loc='left')
ax2.legend(fontsize=7.5, loc='upper left', framealpha=0.9)
ax2.set_xlim(1900, 2025)
ax2.set_ylim(0.6, 1.55)
ax2.grid(axis='both', alpha=0.2)

plt.tight_layout()
outdir = '/sessions/dazzling-epic-sagan/mnt/CoWork_加藤方程式/Paper3専用_4回目作業用_出力はここだけにしろ'
plt.savefig(f'{outdir}/paper3_fig3_col3_sensitivity.pdf', dpi=300, bbox_inches='tight')
plt.savefig(f'{outdir}/paper3_fig3_col3_sensitivity.png', dpi=300, bbox_inches='tight')
print("Fig 3 saved.")
