# paper_revision_v2 — Build Instructions & File Descriptions

## Paper: AI-Based Groundwater Depletion Risk Prediction for Mysuru District Using Machine Learning

### Directory Structure

```
paper_revision_v2/
├── main.tex                    # IEEE conference paper (IEEEtran, double-column)
├── references.bib              # BibTeX references (IEEEtran style)
├── figures/
│   ├── fig_regression_scatter_residual.pdf   # Actual vs. predicted + residuals
│   ├── fig_regression_scatter_residual.png   # PNG copy
│   ├── fig_confusion_matrix.pdf              # 4-class confusion matrix (counts + row-norm)
│   ├── fig_confusion_matrix.png
│   ├── fig_class_performance.pdf             # Per-class Precision/Recall/F1
│   ├── fig_class_performance.png
│   ├── fig_feature_importance.pdf            # Permutation importance bar chart
│   ├── fig_feature_importance.png
│   ├── fig_chronological_split.pdf           # Dataset split timeline diagram
│   ├── fig_chronological_split.png
│   ├── fig_baseline_comparison.pdf           # Baseline MAE/RMSE comparison
│   └── fig_baseline_comparison.png
├── verification_report.md      # Verified metrics, data sources, feature leakage checks
├── reviewer_response_matrix.md # Pass/partial/fail checklist for every reviewer concern
├── verify_metrics.py           # Reproducible metric computation from saved artefacts
├── generate_figures.py         # Publication figure generation from verified data
└── README.md                   # This file
```

---

## How to Build the PDF

### Prerequisites

1. **LaTeX distribution**: MiKTeX (Windows) or TeX Live (Linux/macOS)
2. **IEEEtran class**: Included in most LaTeX distributions.
   If missing: `tlmgr install ieeetran` (TeX Live) or install via MiKTeX package manager.
3. **Required packages**: `cite`, `amsmath`, `graphicx`, `booktabs`, `multirow`,
   `array`, `url`, `hyperref`, `balance`, `xcolor` — all standard CTAN packages.

### Build Commands

Run from inside the `paper_revision_v2/` directory:

```bash
# 1. First pass (creates .aux file)
pdflatex main.tex

# 2. Process bibliography
bibtex main

# 3. Second pass (resolves citations)
pdflatex main.tex

# 4. Third pass (resolves cross-references)
pdflatex main.tex
```

### Expected Output

- `main.pdf` — compiled IEEE double-column conference paper
- `main.aux`, `main.bbl`, `main.blg` — LaTeX intermediate files (can be deleted)

### Overleaf Alternative

1. Create a new Overleaf project
2. Upload all files: `main.tex`, `references.bib`, and all PNG files from `figures/`
3. Set compiler to **pdfLaTeX**
4. Click Recompile

---

## Reproducing Metrics and Figures

All metrics are computed from saved model prediction artefacts.
Run from the **project root** (`groundwater-depletion-risk/`):

```bash
# Reproduce all paper metrics
python paper_revision_v2/verify_metrics.py

# Regenerate all figures
python paper_revision_v2/generate_figures.py
```

Both scripts require the `.venv` virtual environment or equivalent with:
- `pandas`, `numpy`, `scikit-learn`, `matplotlib`

---

## Verified Metrics Summary

| Metric | Value | Artefact |
|--------|-------|---------|
| Regression MAE | 1.94 m | `models/test_predictions.csv` |
| Regression RMSE | 2.96 m | `models/test_predictions.csv` |
| Regression R² | 0.547 | `models/test_predictions.csv` |
| Classification Accuracy | 52.82% | `models/risk_test_predictions.csv` |
| Classification Macro F1 | 0.457 | `models/risk_test_predictions.csv` |
| High-risk F1 | 0.33 | `models/risk_test_predictions.csv` |
| Test set size | 657 records | Both artefacts |
| Test date range | 2019-11-11 to 2023-11-05 | Both artefacts |

---

## Important Notes

1. **All figures are generated from actual prediction data** — no invented or
   illustrative charts. Run `generate_figures.py` to verify.

2. **Original project files are NOT modified**. This `paper_revision_v2/` folder
   is isolated from the main project.

3. **PDF compilation not performed** in this environment (no LaTeX installed).
   Use the commands above to compile locally or on Overleaf.

4. **Three citations have unverified DOIs** (marked in `references.bib`).
   Verify these before submission.

5. **Commit SHA for code reference** should be added to the `project_repo`
   entry in `references.bib` before submission.
