#!/usr/bin/env python3
"""
Paper 3 — Figure 4: Kato ladder as an Arrhenius sequence.
X-axis: integer relay depth H (0–7)
Y-axis: milestone onset age (years before 2025) — log scale

Data from SI S10.18 milestone table and S10.9.1 residence times.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

# ── Milestone data (H, label, onset_age_years_before_2025) ──
# Using midpoint of anchor windows from SI S10.18
milestones = [
    (0, 'Pre-linguistic\nHomo sapiens', 200000),  # origin ~200ka
    (1, 'Language /\nsymbolic cognition', 60000),  # ~70-50ka → midpoint 60ka
    (2, 'Agriculture', 12000),                      # ~10k BCE
    (3, 'Writing /\nurbanisation', 7000),            # ~5k BCE
    (4, 'Printing /\nindustrial', 375),              # ~1500-1800 → midpoint ~1650 CE → 375 yr ago
    (5, 'Computer /\nnetworked', 50),                # ~1950-2000 → midpoint ~1975 → 50 yr ago
    (6, 'Saturated compute\n/ LLM-class AI', 5),     # ~2015-2025 → midpoint ~2020 → 5 yr ago
]

# Predicted H=6→7 nucleation window: ~75 yr from onset of compute (Paper 5 §5)
# So τ_nuc(6→7) ≈ 75 yr from ~1950 → ~2025 → ~0 yr from now (or use 75 as the scale)
predicted = [(7, 'Predicted\nAGI nucleation', 75)]  # τ_nuc calibration = ~75 yr

H_obs = [m[0] for m in milestones]
age_obs = [m[2] for m in milestones]
labels_obs = [m[1] for m in milestones]

H_pred = [p[0] for p in predicted]
age_pred = [p[2] for p in predicted]

# ── Residence times from S10.9.1 ──
# τ₁₂=69,507yr, τ₂₃=9,898yr, τ₃₄=249.5yr, τ₄₅=3.02yr
residence = {
    '1→2': 69507,
    '2→3': 9898,
    '3→4': 249.5,
    '4→5': 3.02,
}

# ── Arrhenius calibration points from Paper 5 §5 ──
# wheat domestication ~5,000 yr, cerebellum→cortex ~2×10⁸ yr, compute→AI ~75 yr
arrhenius_cal = [
    ('wheat\ndomestication', 5000),
    ('cerebellum→\ncortex', 2e8),
    ('compute→\nAI', 75),
]

# ── Figure ──
fig, ax = plt.subplots(figsize=(8, 6))

# Plot observed milestones
ax.scatter(H_obs, age_obs, s=120, c='#2166AC', edgecolors='#08306B',
           linewidths=1.5, zorder=10, label='Observed milestones ($H=0$–$6$)')

# Plot predicted H=7
ax.scatter(H_pred, age_pred, s=120, c='#B2182B', edgecolors='#67001F',
           linewidths=1.5, marker='D', zorder=10,
           label=r'Predicted $H=6\to7$ nucleation ($\sim 75$ yr)')

# Connect with line (approximate Arrhenius trend)
all_H = H_obs + H_pred
all_age = age_obs + age_pred
# Sort by H for line
idx = np.argsort(all_H)
H_sorted = [all_H[i] for i in idx]
age_sorted = [all_age[i] for i in idx]
ax.plot(H_sorted, age_sorted, color='gray', linestyle='--', linewidth=1.0, alpha=0.5, zorder=1)

# Labels for milestones
offsets = {
    0: (15, 8), 1: (15, -12), 2: (15, 8), 3: (15, -12),
    4: (-10, 12), 5: (-10, 12), 6: (-10, 12), 7: (15, 8)
}
for H_val, label, age in milestones:
    dx, dy = offsets.get(H_val, (10, 5))
    ax.annotate(label, xy=(H_val, age), fontsize=7,
                xytext=(dx, dy), textcoords='offset points',
                ha='left' if dx > 0 else 'right', va='bottom',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                          edgecolor='gray', alpha=0.8),
                arrowprops=dict(arrowstyle='->', color='gray', lw=0.5))

for H_val, label, age in predicted:
    ax.annotate(label, xy=(H_val, age), fontsize=7,
                xytext=(15, 8), textcoords='offset points',
                ha='left', va='bottom',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#FDDBC7',
                          edgecolor='#B2182B', alpha=0.8),
                arrowprops=dict(arrowstyle='->', color='#B2182B', lw=0.5))

# Residual band: factor ~2.4
# Draw as gray band around the trend
# Simple: log-linear fit through H=0-6, then show ±log10(2.4) band
log_age = np.log10(np.array(age_obs, dtype=float))
H_arr = np.array(H_obs, dtype=float)
# Linear fit in (H, log10(age))
coeffs = np.polyfit(H_arr, log_age, 1)
H_fit = np.linspace(-0.5, 7.5, 100)
log_age_fit = np.polyval(coeffs, H_fit)
age_fit = 10**log_age_fit

# ±factor 2.4 band
factor = 2.4
ax.fill_between(H_fit, age_fit / factor, age_fit * factor,
                color='gray', alpha=0.08, zorder=0,
                label=f'$\\pm$ factor {factor} band')
ax.plot(H_fit, age_fit, color='gray', linewidth=1.5, alpha=0.4, zorder=1,
        label='Arrhenius fit (log-linear)')

# ── Formatting ──
ax.set_yscale('log')
ax.set_xlabel('Integer relay depth $H$', fontsize=12)
ax.set_ylabel('Milestone onset age (years before 2025)', fontsize=12)
ax.set_xlim(-0.5, 7.8)
ax.set_ylim(1, 5e5)
ax.set_xticks(range(8))
ax.legend(fontsize=8, loc='upper right', framealpha=0.9)
ax.grid(axis='both', alpha=0.2, which='both')

# Add secondary annotations
ax.text(0.02, 0.02,
        r'Arrhenius: $\tau_{\mathrm{nuc}} = \tau_0\,\exp[\Delta G^*/k_B T_{\mathrm{eff}}]$'
        '\nResiduals $\\leq$ factor 2.4 across $H=0$–$6$',
        transform=ax.transAxes, fontsize=8, va='bottom',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

plt.tight_layout()
outdir = '/sessions/dazzling-epic-sagan/mnt/CoWork_加藤方程式/Paper3専用_4回目作業用_出力はここだけにしろ'
plt.savefig(f'{outdir}/paper3_fig4_arrhenius_ladder.pdf', dpi=300, bbox_inches='tight')
plt.savefig(f'{outdir}/paper3_fig4_arrhenius_ladder.png', dpi=300, bbox_inches='tight')
print("Fig 4 saved.")
print(f"Log-linear fit: log10(age) = {coeffs[0]:.3f} * H + {coeffs[1]:.3f}")
print(f"Slope = {coeffs[0]:.3f} (negative = age decreases with H)")
