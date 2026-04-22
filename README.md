# kato-ladder-paper3

Reproducibility archive for **Paper 3**:

> *After von Foerster: Seventy Thousand Years of Human Coordination on the Kato Ladder, and a Civilizational Ontology of Six Realized Phase Transitions*
> — Shota Kato, AI and Future Co., Ltd., Tokyo (NHB initial submission snapshot).

This repository bundles the manuscript, Supplementary Information, reference bibliography, figures, data, and code necessary to reproduce every numerical and figural claim in the paper. A snapshot release (`v1.0-submission`) is tagged for Zenodo DOI minting.

## Repository layout

```
kato-ladder-paper3/
├── README.md                # this file
├── LICENSE                  # CC-BY-4.0 for prose, figures, data
├── LICENSE-CODE             # Apache-2.0 for source code
├── .gitignore
├── .zenodo.json             # Zenodo deposit metadata
│
├── paper3_main_V65.tex      # main manuscript (latex source)
├── paper3_SI_V76.tex        # Supplementary Information (latex source)
├── paper3_refs_V13.bib      # shared bibliography
│
├── submission/              # NHB portal submission artifacts
│   ├── paper3_cover_letter_V17.md
│   ├── paper3_significance_statement_V1.md
│   └── paper3_title_page_V4.md
│
├── figures/                 # camera-ready figures
│   ├── paper3_fig3_col3_sensitivity.pdf
│   ├── paper3_fig4_arrhenius_ladder.pdf
│   ├── paper3_graphical_abstract_V1.pdf
│   ├── paper3_graphical_abstract_V1.png
│   └── fig_S3a.pdf          # SI Fig. S3a
│
├── data/                    # reproducibility data
│   ├── README.md
│   ├── backbone_28anchor.csv               # 28-anchor compressed-timeline backbone
│   ├── collapse_windows.csv                # two historically realized collapse windows
│   ├── eq2_rank2_sensitivity_envelope.csv  # Eq.(2) calibration output
│   └── falsifier_seven_axis.csv            # seven-axis falsifier battery
│
└── code/                    # build and analysis scripts
    ├── README.md
    ├── build_graphical_abstract_V1.py      # matplotlib build for Fig. graphical abstract
    ├── gen_fig3_col3_sensitivity.py        # Fig. 3 Eq.(2) rank-2 sensitivity envelope
    ├── gen_fig4_arrhenius_ladder.py        # Fig. 4 seven-axis falsifier battery
    ├── mcmc_m4_posterior_final.py          # four-anchor posterior via MCMC
    └── laplace_m4_posterior.py             # four-anchor posterior via Laplace approx
```

## Core claims reproduced by this repository

1. **21 qualitative anchor + 28-anchor quantitative backbone fit** of log world population over ~70 kyr (`data/backbone_28anchor.csv`, Fig. 1 / Fig. 2)
2. **Two realized collapse windows** (late antiquity and Black Death era) rendered as vermilion bands in the graphical abstract (`data/collapse_windows.csv`)
3. **Eq.(2) rank-2 sensitivity envelope** yielding the [2028.4, 2034.4] CE forecast window (`data/eq2_rank2_sensitivity_envelope.csv`, Fig. 3)
4. **Seven-axis falsifier battery** providing seven independent rejection criteria for the H=6→7 candidate transition (`data/falsifier_seven_axis.csv`, Fig. 4)
5. **Graphical abstract** as a three-layer single-panel visual (collapses+forecast band | 28-anchor backbone | 6-regime bottom strip) built from `code/build_graphical_abstract_V1.py`

## Quick reproduction

```bash
git clone https://github.com/SKato7/kato-ladder-paper3.git
cd kato-ladder-paper3
pip install -r code/requirements.txt  # numpy, scipy, matplotlib
python3 code/build_graphical_abstract_V1.py    # regenerates graphical abstract PDF + PNG
python3 code/gen_fig3_col3_sensitivity.py      # regenerates Fig. 3
python3 code/gen_fig4_arrhenius_ladder.py      # regenerates Fig. 4
```

## LaTeX compilation

```bash
pdflatex paper3_main_V65.tex
bibtex   paper3_main_V65
pdflatex paper3_main_V65.tex
pdflatex paper3_main_V65.tex

pdflatex paper3_SI_V76.tex
bibtex   paper3_SI_V76
pdflatex paper3_SI_V76.tex
pdflatex paper3_SI_V76.tex
```

## Citation

If you use this data or code, please cite:

```
Kato, S. (2026). Kato Ladder: Seventy Thousand Years of Human Coordination and a
Civilizational Ontology of Six Realized Phase Transitions — Paper 3 submission
snapshot [Data set]. Zenodo. https://doi.org/10.5281/zenodo.XXXXXXX
```

(Replace `XXXXXXX` with the minted versioned DOI after Release publish.)

## License

- **Manuscript, Supplementary Information, figures, and data**: [CC-BY-4.0](LICENSE)
- **Source code (Python scripts)**: [Apache License 2.0](LICENSE-CODE)

## Deposit mode note

This repository is built to support both **1-deposit** and **2-deposit** Zenodo workflows:

- **1-deposit mode (single DOI for data + code)** — push the full tree as-is to a single GitHub repository and toggle Zenodo integration. Paper 5 of this series (`kato-ladder-paper5`) uses this mode.
- **2-deposit mode (separate data DOI + code DOI)** — split `data/` into `kato-ladder-paper3-data` and `code/` into `kato-ladder-paper3-code`, push separately, and toggle Zenodo integration for each. Author decides at push time.

See `submission/paper3_title_page_V4.md` §Data availability and §Code availability for DOI placeholder locations that need post-Release sed-replace.

## Contact

Shota Kato, AI and Future Co., Ltd., Tokyo, Japan
Email: founder@aiandfuture.co.jp
