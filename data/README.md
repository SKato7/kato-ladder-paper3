# Data directory — Paper 3 (Kato Ladder)

This directory contains the numerical data necessary to reproduce every figure and numerical claim in Paper 3. All files are plain CSV with UTF-8 encoding and header rows.

## Files

### `backbone_28anchor.csv`
Twenty-eight qualitative anchor points of log world population spanning ~70 kyr BP to 2031.4 CE projection. Columns:
- `anchor_id` (1–28)
- `epoch_label` (string, e.g. "Upper Paleolithic (-70 kyr BP)")
- `t_yr_BP` (numeric, years before present; positive = past; future = negative)
- `log10_N` (log-10 of world population estimate)
- `regime_id` (0–6, ladder level H)
- `notes` (textual citation pointer to `paper3_refs_V13.bib`)

### `collapse_windows.csv`
Two historically realized collapse windows rendered as vermilion bands in the graphical abstract. Columns:
- `window_id` (1, 2)
- `label` (string, e.g. "Late antiquity collapse")
- `t_start_yr_BP`
- `t_end_yr_BP`
- `pre_collapse_log10_N`
- `trough_log10_N`
- `duration_years`

### `eq2_rank2_sensitivity_envelope.csv`
Output of the rank-2 sensitivity analysis on Eq.(2) τ_H = τ_0 q^H. Columns:
- `param_name` (τ_0, q, H baseline, etc.)
- `baseline_value`
- `perturbation_pct` (−20, −10, 0, +10, +20)
- `forecast_year_lower`
- `forecast_year_upper`
- `jacobian_kappa`

The envelope columns collapse into the forecast band [2028.4, 2034.4] CE under the default baseline + ±10% joint perturbations on (τ_0, q).

### `falsifier_seven_axis.csv`
Seven independent rejection criteria for the candidate H=6→7 transition. Columns:
- `axis_id` (1–7)
- `axis_name` (e.g. "demographic transition rate")
- `null_hypothesis`
- `test_statistic`
- `rejection_threshold`
- `current_observed_value`
- `status` (one of: observed, pending, unfalsifiable)

## Provenance and citation

All anchor points and regime labels trace back to peer-reviewed sources cited in `paper3_refs_V13.bib`. When using these CSVs in derivative analyses, cite both the Zenodo deposit (see root README.md) and the original sources listed in the `notes` column.

## License

CC-BY-4.0. See the root `LICENSE` file.
