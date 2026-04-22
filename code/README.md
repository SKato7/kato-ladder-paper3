# Code directory — Paper 3 (Kato Ladder)

This directory contains Python scripts to regenerate every figure in Paper 3 and to reproduce the MCMC and Laplace posteriors for the four-anchor calibration of Eq.(2).

## Requirements

Python ≥ 3.10 with:
- numpy ≥ 1.24
- scipy ≥ 1.10
- matplotlib ≥ 3.7

Install via:
```bash
pip install -r requirements.txt
```

## Scripts

### `build_graphical_abstract_V1.py`
Builds the graphical abstract (`../figures/paper3_graphical_abstract_V1.pdf` + `.png`). Outputs a 180 mm width, 16:9 single-panel figure with:
- Main layer: two collapse windows + [2028.4, 2034.4] CE forecast band + 1963 H=6 entry arrow
- Base layer: 21 qualitative anchor backbone line with dashed forecast extension
- Bottom strip: 6 Okabe-Ito colored regime bands (Language / Land limit / Agrarian trap / Writing+irrig. / Institutions / Long-life)

```bash
python3 build_graphical_abstract_V1.py
```

### `gen_fig3_col3_sensitivity.py`
Fig. 3: Eq.(2) rank-2 sensitivity envelope calibrating the [2028.4, 2034.4] CE robustness.

### `gen_fig4_arrhenius_ladder.py`
Fig. 4: seven-axis falsifier battery.

### `mcmc_m4_posterior_final.py`
Four-anchor MCMC posterior for Eq.(2) (τ_0, q) calibration. Emcee-based, 4 chains × 5000 samples × 20 walkers. Outputs `mcmc_m4_chains.npz`.

### `laplace_m4_posterior.py`
Laplace approximation of the same posterior. Cross-check for MCMC convergence.

## Reproducibility note

All scripts use fixed random seeds (see top of each file). Running them twice produces bit-identical outputs on the same matplotlib version.

## License

Apache-2.0. See the root `LICENSE-CODE` file.
