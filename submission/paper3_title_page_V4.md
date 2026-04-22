# Paper 3 — NHB Portal Title Page V4

## Source
V3 + wave51 graphical abstract V1 build (2026-04-20 wave51 kickoff).
V3 → V4 差分: Display items.Graphical abstract 行に filename 2 本（`paper3_graphical_abstract_V1.pdf` + `paper3_graphical_abstract_V1.png`）を明記、K10_116.0 spec に基づく 16:9 design rationale を 1 行要約。
V2 → V3 差分: (1) SI appendix list に §S-LadderBeyond 追加（V2 が欠けていた 5 本目）、(2) "Final appendix count and ordering to be finalized at V76 integrate" の caveat を "finalized at V76 integrate (2026-04-20)" に確定化、(3) word count / table count の計測手順を V64 → V65 main path に更新。
V1 → V2 差分（履歴参照）: V1 title "...and the Necessity of the H=6→7 Nucleation" は Cover Letter V16 の over-claim framing。V64 main 実体は "...and a Civilizational Ontology of Six Realized Phase Transitions"、V17 Cover Letter と揃えた。

Per K10_116.1 wave48 submission checklist, this is a new blocker (blocker #4) — portal expects a plain-text title page separate from the LaTeX-compiled PDF.

## Target
- **NHB portal step 3**: Title page upload (plain text or separate PDF)
- **Rationale**: NHB portal pre-screens this page before sending to reviewers. Main PDF title page is LaTeX-formatted; portal wants a simple plain-text version for editorial workflow.

## Title Page (plain text — paste into portal)

```
Title:
  After von Foerster: Seventy Thousand Years of Human Coordination on the Kato Ladder, and a Civilizational Ontology of Six Realized Phase Transitions

Short title (≤60 characters including spaces):
  Kato Ladder: Six-Regime Civilizational Ontology

Authors:
  Shota Kato (corresponding author)

Affiliations:
  1. AI and Future Co., Ltd., Tokyo, Japan

Corresponding author:
  Shota Kato
  AI and Future Co., Ltd.
  Tokyo, Japan
  Email: founder@aiandfuture.co.jp

ORCID (if applicable):
  [To be supplied by author]

Keywords (up to 6):
  coordination hierarchy; Kato equation; civilizational ceiling; H=7 nucleation; Humanness theorem; falsifiable forecast

Article type:
  Article

Competing interests:
  The author declares no competing interests.

Funding:
  This research received no external funding.

Data availability:
  All data supporting the findings of this study are available in the Supplementary Information and at Zenodo [DOI to be assigned upon acceptance].

Code availability:
  All code used for the numerical calibrations, figure generation, and sensitivity analyses is deposited at Zenodo [DOI to be assigned upon acceptance].

Word count (main text, excluding abstract, references, methods, and captions):
  [To be counted after V64 integrate]

Display items:
  Figures: 4 (Fig. 1 Kato ladder six-regime schematic; Fig. 2 28-anchor backbone fit; Fig. 3 Eq.(2) rank-2 sensitivity envelope; Fig. 4 seven-axis falsifier battery)
  Tables: [to be counted after V65 integrate — see V4 addendum below]
  Graphical abstract: 1 (16:9 panel, files: paper3_graphical_abstract_V1.pdf [vector master, 180 mm width, Helvetica 5-8 pt] + paper3_graphical_abstract_V1.png [300 dpi fallback]. Three-layer design per K10_116.0 spec: two collapses + 2031.4 CE forecast band [2028.4, 2034.4] | 28-anchor N(t) backbone | 6-regime bottom strip. Okabe-Ito palette, compressed not-to-scale timeline. 150-word caption embedded separately; falsifiability sentence in final line.)

Supplementary Information:
  1 SI document (LaTeX-compiled PDF; paper3_SI_V76.tex, 8412 lines, ~1 appendix index + ~50 appendices), containing wave50-new appendices §S-70ky (Late-Paleolithic-to-Neolithic 70 kyr ladder simulation), §S-Collapse3Routes (three frontier failure routes — Route A/B/C exhaustion leading to the conditional next-rung theorem, Theorem S-Col3.5), §S-LadderFull (Kato Ladder H=0–H=7 full characterization), §S-AIsubstrate (Humanness→AI isomorphism formal target-side conditions — necessary-condition analysis for a non-biological H=7 carrier), §S-LadderBeyond (beyond H=7: open-ended versus closed-sequence reading); pre-existing appendices §S-Falsifier (seven-axis falsifier battery), §S-Eq2-Sensitivity (rank-2 sensitivity panel calibrating [2028.4, 2034.4] CE robustness), the Humanness theorem formal proof with pairwise logical independence against three explicit counter-model societies, and the full species-row Humanness matrix. Appendix count and ordering finalized at V76 integrate (2026-04-20).
```

## Integration checklist

- [ ] Portal step 3: Paste the plain-text block into the portal field (著者手動作業)
- [ ] Fill ORCID (著者判断)
- [ ] Fill word count (after V65 integrate is complete; count via `detex paper3_main_V65.tex.txt | wc -w`)
- [ ] Fill Zenodo DOI (著者 Zenodo account 作成 + dataset upload 後)
- [ ] Remove this V1 file name from the submission-polish blocker list (K10_116.1 blocker #4)

## Placeholders needing 著者 action

1. **ORCID**: 著者 ORCID identifier
2. **Word count**: V65 完成済、`detex paper3_main_V65.tex.txt | wc -w` で計測可能
3. **Zenodo DOI** (data + code): Zenodo account 作成 + dataset/code upload 後の DOI
4. **Table count**: V65 完成済、`grep -c '\\begin{table}' paper3_main_V65.tex.txt` で計測可能

## Version history

- V1 (2026-04-20): Initial draft by 加藤方程式１０－６ (Claude Opus 4.7) based on K10_116.1 wave48 submission checklist blocker #4. Title per Cover Letter V16 (AI-masked form).
- V2 (2026-04-20 16:3X): wave50 V64 main alignment — title shifted to "Civilizational Ontology of Six Realized Phase Transitions" + SI appendix list updated to actual K10_118.1+K10_117.1 names. By 加藤方程式１０－６ (Claude Opus 4.7).
- V3 (2026-04-20 17:2X): V76 SI integrate 完了後の cleanup — §S-LadderBeyond を SI list に追加、caveat "Final appendix count...to be finalized at V76 integrate" を "finalized at V76 integrate (2026-04-20)" に確定化、word count / table count 手順を V65 path に更新。By 加藤方程式１０－６ (Claude Opus 4.7).
- V4 (2026-04-20 18:3X): wave51 graphical abstract V1 build 反映 — Display items.Graphical abstract 行に filename 2 本（paper3_graphical_abstract_V1.pdf + paper3_graphical_abstract_V1.png）+ 3-layer design rationale + 150-word caption memo を統合。K10_116.0 spec integrated. By 加藤方程式１０－６ (Claude Opus 4.7).
