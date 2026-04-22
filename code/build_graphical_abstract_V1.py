#!/usr/bin/env python3
"""Paper 3 graphical abstract V1 build.

Source: K10_116.0 recovered spec + paper3_main_V65 narrative structure.
Design: 3-layer (2 collapses + forecast | 28-anchor backbone | 6 regime strip).
Axis: piecewise-compressed time (not to scale, explicit in figure).
Palette: Okabe-Ito (colorblind-safe).
Output: paper3_graphical_abstract_V1.pdf + paper3_graphical_abstract_V1.png

NOT-TO-SCALE NOTE: The backbone shape follows the Paper 3 qualitative N(t)
trajectory (two realized collapse dips + long-run super-exponential rise
under the pairwise N^2 law) with axis compression so -70 kyr to 2031.4 fits
a 16:9 canvas. Exact 28-anchor numerical values live in SI V76 Fig. 1 panel;
this is a story-first explanatory graphic per the spec.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Rectangle

# Helvetica/Arial sans-serif per NHB guide
mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]
mpl.rcParams["pdf.fonttype"] = 42  # embed TrueType for vector
mpl.rcParams["ps.fonttype"] = 42

# ---------- Compressed timeline (not to scale) ----------
# Positions on x-axis (monotone; numeric values are visual-weight only)
# 7 tick labels per spec; we insert 2 extra points for collapse dips
tick_positions = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
tick_labels = ["70 kyr BP", "25 kyr BP", "10 kyr BCE",
               "5 kyr BCE", "1963", "2024", "2031.4"]

# ---------- Backbone trajectory (schematic log10 N, N in millions) ----------
# Qualitative anchors aligned with paper narrative:
#   -70kyr: ~0.5 M (upper Paleolithic), H=0 pre-rung
#   -25kyr: ~3 M (post language, H=1 rung on)
#   -10kyr BCE: ~5 M (pre-Neolithic hunter-gatherer ceiling K_HG)
#   -5kyr BCE: ~14 M (post-Neolithic initial climb)
#   Collapse 1 dip inserted between -5kyr and 1963 era
#   1963: ~3200 M (industrial peak entry to long-life regime)
#   Collapse 2 dip in late antiquity region
#   2024: ~8100 M
#   2031.4: ~8500 M (forecast extrapolation)
# Note: compressed timeline — x is visual-weight, not linear calendar time.
# Prehistoric region (tick 0 to 3, x=0..3) spans ~67 kyr in 3 units.
# Ancient+medieval region (x=3 to 3.95) compresses 5 kyr BCE -> 1400 CE.
# Industrial region (x=3.95 to 4.00) very tight (1400 -> 1963).
# Modern region (x=4.00 to 6.00) expanded (1963 -> 2031.4, only 68 yr in 2 units).
x_backbone = np.array([
    0.00, 0.50, 1.00, 1.50, 2.00, 2.50, 3.00,
    3.25, 3.35, 3.50,     # Collapse 1 window (late antiquity)
    3.60, 3.75,
    3.80, 3.88, 3.95,     # Collapse 2 window (14th c Black Death)
    4.00,                  # 1963 (tick 4) — industrial/long-life boundary
    4.40,                  # ~1980
    4.70,                  # ~2000
    5.00,                  # 2024 (tick 5)
    5.50,                  # ~2028
    6.00,                  # 2031.4 (tick 6)
])
y_backbone = np.array([
    np.log10(0.5),    # -70 kyr BP
    np.log10(1.2),    # -25 kyr BP
    np.log10(3.0),    # -10 kyr BCE (near K_HG)
    np.log10(4.2),    # pre-Neolithic climb
    np.log10(5.0),    # K_HG ceiling
    np.log10(8.0),    # early agrarian
    np.log10(14.0),   # -3 kyr (paper anchor: Biraben corrected)
    np.log10(200.0),  # pre-Collapse 1 peak
    np.log10(145.0),  # Collapse 1 trough
    np.log10(180.0),  # post-Collapse 1 rebound
    np.log10(420.0),  # ~1100 CE
    np.log10(460.0),  # pre-Collapse 2
    np.log10(455.0),  # 1300 CE
    np.log10(350.0),  # Collapse 2 trough (Black Death)
    np.log10(440.0),  # post-Black-Death rebound
    np.log10(3200.0), # 1963 (H=6 entry)
    np.log10(4440.0), # ~1980
    np.log10(6140.0), # ~2000
    np.log10(8100.0), # 2024
    np.log10(8300.0), # ~2028
    np.log10(8500.0), # 2031.4
])

# Forecast extension (dashed, beyond the observed anchors)
x_forecast = np.array([6.00, 6.60])
y_forecast = np.array([np.log10(8500.0), np.log10(9200.0)])

# ---------- 6 regime labels + Okabe-Ito palette (colorblind-safe) ----------
regime_labels = ["Language", "Land limit", "Agrarian trap",
                 "Writing / irrig.", "Institutions", "Long-life"]
regime_H = ["H=1", "H=2", "H=3", "H=4", "H=5", "H=6"]
regime_colors = [
    "#56B4E9",  # sky blue
    "#E69F00",  # orange
    "#F0E442",  # yellow
    "#009E73",  # bluish green
    "#0072B2",  # blue
    "#CC79A7",  # reddish purple
]

# ---------- Figure construction ----------
# 16:9 aspect, 180 mm wide vector master
fig_w_in = 180.0 / 25.4   # 7.087 in
fig_h_in = fig_w_in * 9.0 / 16.0  # 3.987 in
fig, ax = plt.subplots(figsize=(fig_w_in, fig_h_in))

# --- Regime bands (background tint in upper 82% zone) ---
# Boundaries align with the 6 realized regimes (H=1..H=6) mapped onto
# the compressed timeline used above:
#   H=1 Language      : x=0.6 .. 1.5  (-65kyr to Still Bay transition)
#   H=2 Land limit    : x=1.5 .. 2.6  (-25kyr to -10kyr BCE, K_HG era)
#   H=3 Agrarian trap : x=2.6 .. 3.3  (PPNB to -3kyr anchor)
#   H=4 Irrig+writing : x=3.3 .. 3.75 (ancient world, through Collapse 1)
#   H=5 Institutions  : x=3.75 .. 4.0 (medieval + industrial, through Collapse 2)
#   H=6 Long-life     : x=4.0  .. 6.6 (1963-2031.4 forecast)
x_regimes = [0.6, 1.5, 2.6, 3.3, 3.75, 4.0, 6.6]
for i, c in enumerate(regime_colors):
    ax.axvspan(x_regimes[i], x_regimes[i + 1], color=c, alpha=0.06, lw=0)

# --- Collapse windows (vermillion semi-transparent, per spec) ---
collapse_windows = [(3.25, 3.50), (3.80, 3.95)]
for x0, x1 in collapse_windows:
    ax.axvspan(x0, x1, color="#D55E00", alpha=0.22, lw=0)

# --- Forecast / falsifier window [2028.4, 2034.4] (bluish green) ---
# 6.00 = 2031.4 center; window edges 2028.4 & 2034.4 scaled to compressed axis
# Use ±0.30 around 6.00 to roughly represent ±3 yr vs. the compressed 5.00->6.00 = 2024->2031.4 span
forecast_x0, forecast_x1 = 5.70, 6.30
ax.axvspan(forecast_x0, forecast_x1, color="#009E73", alpha=0.22, lw=0)

# --- Backbone line (solid, black) + anchors ---
ax.plot(x_backbone, y_backbone, "-", color="black", lw=1.8, zorder=4)
ax.plot(x_backbone, y_backbone, "o", color="black", ms=3.2, zorder=5)

# --- Forecast extension (dashed, blue) ---
ax.plot(x_forecast, y_forecast, "--", color="#0072B2", lw=1.8, zorder=4)

# --- Key annotations (<=5, per spec) ---
ann_fs = 6.8
ax.annotate("Collapse 1",
            xy=(3.35, np.log10(145.0)), xytext=(2.60, 0.75),
            fontsize=ann_fs, ha="center",
            arrowprops=dict(arrowstyle="-", lw=0.6, color="#8B0000"))
ax.annotate("Collapse 2",
            xy=(3.88, np.log10(350.0)), xytext=(3.15, 1.35),
            fontsize=ann_fs, ha="center",
            arrowprops=dict(arrowstyle="-", lw=0.6, color="#8B0000"))
ax.annotate("1963 near-miss,\nenter $H{=}6$",
            xy=(4.00, np.log10(3200.0)), xytext=(4.15, 2.15),
            fontsize=ann_fs, ha="left",
            arrowprops=dict(arrowstyle="-", lw=0.6, color="#444444"))
ax.annotate("2031.4 CE candidate\n$H{=}6{\\to}7$ transition",
            xy=(6.00, np.log10(8500.0)), xytext=(5.00, 3.45),
            fontsize=ann_fs, ha="center",
            arrowprops=dict(arrowstyle="-", lw=0.6, color="#004D80"))
ax.text(6.05, np.log10(8500.0) - 0.18,
        "Falsifier band:\n2028.4 – 2034.4",
        fontsize=6.2, ha="left", va="top",
        color="#005040")

# --- Eq.(2) callout (lower-right, avoiding 2031.4 annotation) ---
callout_text = ("$\\tau_H = \\tau_0\\, q^{\\,H}$ (Eq. 2)\n"
                "Forecast: 2031.4 CE")
ax.text(0.985, 0.40, callout_text,
        transform=ax.transAxes, ha="right", va="top",
        fontsize=6.5, family="sans-serif",
        bbox=dict(boxstyle="round,pad=0.30",
                  facecolor="white", edgecolor="#888888", lw=0.5,
                  alpha=0.92))

# --- Short headline (upper-left) ---
ax.text(0.015, 0.97,
        "Two realized collapses, one near-miss, one dated test",
        transform=ax.transAxes, ha="left", va="top",
        fontsize=8.0, weight="semibold")

ax.text(0.985, 0.02,
        "Compressed time axis — not to scale",
        transform=ax.transAxes, ha="right", va="bottom",
        fontsize=5.8, color="#555555", style="italic")

# --- 6-regime bottom strip (lower 18%) ---
# Use negative-y offset via axes transform
strip_y_top = -0.020     # just below x-axis (in axes coords)
strip_y_bot = -0.150
for i, (name, Hlab, c) in enumerate(zip(regime_labels, regime_H, regime_colors)):
    x_left = x_regimes[i]
    x_right = x_regimes[i + 1]
    rect = Rectangle(
        (x_left, strip_y_bot),
        x_right - x_left,
        strip_y_top - strip_y_bot,
        transform=ax.get_xaxis_transform(),
        color=c, alpha=0.42, lw=0, clip_on=False,
    )
    ax.add_patch(rect)
    x_mid = 0.5 * (x_left + x_right)
    ax.text(x_mid, strip_y_bot + 0.6 * (strip_y_top - strip_y_bot),
            name,
            transform=ax.get_xaxis_transform(),
            ha="center", va="center", fontsize=5.6, clip_on=False)
    ax.text(x_mid, strip_y_top - 0.08 * (strip_y_top - strip_y_bot),
            Hlab,
            transform=ax.get_xaxis_transform(),
            ha="center", va="top", fontsize=5.2,
            color="#333333", clip_on=False)

# --- H=0 faint note on the far left ---
ax.text(-0.02, strip_y_bot + 0.5 * (strip_y_top - strip_y_bot),
        "$H{=}0$",
        transform=ax.get_xaxis_transform(),
        ha="right", va="center", fontsize=5.2, color="#888888",
        clip_on=False)

# --- Axes cosmetics ---
ax.set_xlim(-0.05, 7.20)
ax.set_ylim(-0.5, 4.3)
ax.set_xticks(tick_positions)
ax.set_xticklabels(tick_labels, fontsize=6.8)
ax.set_ylabel("World population $N$ (millions, $\\log_{10}$)", fontsize=7.2)
ax.tick_params(axis="y", labelsize=6.5)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="y", alpha=0.18, lw=0.5)

# Reserve space below for regime strip
plt.subplots_adjust(bottom=0.22, top=0.95, left=0.09, right=0.98)

# ---------- Save vector (PDF) + raster (PNG) ----------
out_dir = "/sessions/ecstatic-beautiful-shannon/mnt/CoWork_加藤方程式/最新論文_P3"
pdf_path = f"{out_dir}/paper3_graphical_abstract_V1.pdf"
png_path = f"{out_dir}/paper3_graphical_abstract_V1.png"

fig.savefig(pdf_path, dpi=300, bbox_inches="tight")
fig.savefig(png_path, dpi=300, bbox_inches="tight")

import os
print(f"PDF written: {pdf_path} ({os.path.getsize(pdf_path)} bytes)")
print(f"PNG written: {png_path} ({os.path.getsize(png_path)} bytes)")
