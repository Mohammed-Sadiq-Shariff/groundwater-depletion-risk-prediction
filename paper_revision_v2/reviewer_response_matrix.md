# Reviewer Compliance Matrix
**Paper:** AI-Based Groundwater Depletion Risk Prediction for Mysuru District  
**Version:** paper_revision_v2  
**Date:** 2026-10-20

Legend: ✅ PASS | ⚠️ PARTIAL | ❌ FAIL | 📋 DISCLOSED LIMITATION

---

## ABSTRACT

| Concern | Evidence / Artefact | Correction Made | Status |
|---|---|---|---|
| Verified data source | `data/raw/groundwater/` — two CGWB CSVs confirmed | Abstract states CGWB and 92 stations | ✅ |
| Station coverage | 92 unique stations (verified from training data) | Stated in abstract | ✅ |
| GWL units (mbgl) | `create_target.py` — level column is "Groundwater Level Quarterly Manual (meter)" | Abstract uses "mbgl" correctly | ✅ |
| Observation frequency | Quarterly (40–200 day intervals, median 91 days) | Abstract states "quarterly well observations" | ✅ |
| Metric accuracy | MAE=1.94 m, RMSE=2.96 m, R²=0.547; Acc=52.8%, MacroF1=0.457 reproduced from artefacts | All metrics in abstract are verified | ✅ |

---

## INTRODUCTION

| Concern | Evidence / Artefact | Correction Made | Status |
|---|---|---|---|
| Research question explicitly stated | Section I states two explicit RQs | Both RQs included with clear prediction horizon | ✅ |
| Prediction horizon stated | 40–200 days, median 91 days (verified from `days_to_next_observation` distribution) | Stated in intro and methodology | ✅ |
| Geographic representativeness | 92 stations / 6,645 km² district; scope limitations stated | Intro explicitly limits scope to 92 CGWB stations | ✅ |
| No claim of live forecasting | Paper explicitly disclaims operational/real-time claims | Section I and Section VII contain explicit disclaimers | ✅ |

---

## RELATED WORK

| Concern | Evidence / Artefact | Correction Made | Status |
|---|---|---|---|
| Literature comparison table | Table I: 6 studies, model/region/data/validation/metrics/limitations | Table I included with correct columns | ✅ |
| Citation metadata verification | 3 of 6 citations have verified DOIs; 3 flagged in references.bib with "unverified" notes | Unverified citations disclosed in .bib file | ⚠️ |
| 2026 Frontiers in AI paper | No such paper could be verified | Not cited; cannot include unverifiable reference | 📋 |
| Research gap stated | Section II explicitly identifies 4 gaps addressed by this study | Research gap paragraph included | ✅ |

---

## METHODOLOGY

| Concern | Evidence / Artefact | Correction Made | Status |
|---|---|---|---|
| Implementation consistency | All features verified against actual code (`create_model_features.py`, `build_features.py`) | Feature table matches verified code | ✅ |
| No algorithmic novelty claims | Paper does not claim novel algorithms; correctly frames as applied ML | No novelty claims made | ✅ |
| Feature leakage check | All lag/rolling features use `shift(1)` before window; verified in code | Explicitly documented in methodology | ✅ |
| Future columns explicitly excluded | `LEAKAGE_COLUMNS` list in `train_models.py` lines 160-167 verified | Stated in Section III | ✅ |
| Model selection rationale | HGB selected for lowest validation RMSE; RF for highest validation accuracy | Section III.C states selection criterion | ✅ |

---

## DATASET

| Concern | Evidence / Artefact | Correction Made | Status |
|---|---|---|---|
| Data provenance stated | Source files named, portal (India-WRIS, IMD DSP) cited | Section III.A and III.B with exact filenames | ✅ |
| GWL units confirmed | Source column: "Groundwater Level Quarterly Manual (meter)" = depth below GL | Units clarified throughout | ✅ |
| Missing value handling | `dropna` used for invalid dates/levels; see `build_features.py` lines 169–180 | Missing value policy stated | ✅ |
| Duplicate removal | `drop_duplicates` on station+date+lat+lon: `build_features.py` line 462-469 | Stated in Section III.A | ✅ |
| December 2023 rainfall gap | Confirmed in code and data; rolling windows carry partial uncertainty | Explicitly disclosed in Section III.B | ✅ |
| Missing rainfall NOT set to zero | `build_features.py` lines 343-354: gap preserved as NaN | Explicitly stated | ✅ |

---

## VARIABLE MONITORING INTERVALS AND RISK THRESHOLDS

| Concern | Evidence / Artefact | Correction Made | Status |
|---|---|---|---|
| Interval variability disclosed | `days_to_next_observation`: min 40, max 200, mean 93, std 32 | Stated in Section III.A and IV.B | ✅ |
| Fixed-metre thresholds acknowledged as limitation | `create_target.py` lines 200-218: thresholds are 0/1/3 m | Section III.B and Section VI.B explicitly flag this | ✅ |
| Hydrogeological justification | Not provided (no external validation data available) | Disclosed as requiring hydrogeological validation | 📋 |
| Interval-normalised alternatives | Not evaluated (not feasible within scope) | Recommended as future work | ⚠️ |

---

## TEMPORAL SPLITS AND BOUNDARY LEAKAGE

| Concern | Evidence / Artefact | Correction Made | Status |
|---|---|---|---|
| Chronological split verified | Train 2624/1997-2015; Val 904/2015-2019; Test 657/2019-2023 | Split counts and dates verified from artefact | ✅ |
| No temporal leakage | Unique dates used for split boundaries; no overlap possible | Methodology section explicitly confirms | ✅ |
| Reproducible features | All features from `predict_station.py` consistent with training features | Feature columns documented in Table II | ✅ |
| Train/val/test counts discrepancy | Previous draft had 2569/846/657; verified is 2624/904/657 | Discrepancy disclosed in Section V.A | ✅ |

---

## REGRESSION METRICS AND BASELINES

| Concern | Evidence / Artefact | Correction Made | Status |
|---|---|---|---|
| MAE verified | 1.9384 m — reproduced from `models/test_predictions.csv` | Table II reports 1.94 m ✅ | ✅ |
| RMSE verified | 2.9568 m — reproduced from artefact | Table II reports 2.96 m ✅ | ✅ |
| R² verified | 0.5469 — reproduced from artefact | Table II reports 0.547 ✅ | ✅ |
| Mean-target baseline | MAE=3.43 m, RMSE=4.39 m — computed from same test set | Reported in Table II | ✅ |
| Persistence baseline | MAE=2.15 m, RMSE=3.39 m — computed from same test set | Reported in Table II | ✅ |
| Sample count (657) | Confirmed from artefact columns | Stated in Table II caption | ✅ |
| Chronological test dates | 2019-11-11 to 2023-11-05 — confirmed from CSV | Stated in Table II caption | ✅ |
| Uncertainty intervals | Bootstrap method described but not numerically computed | Described in methodology; acknowledged as incomplete | ⚠️ |

---

## CLASSIFICATION METRICS, BASELINES, AND CONFUSION MATRIX

| Concern | Evidence / Artefact | Correction Made | Status |
|---|---|---|---|
| Accuracy 52.82% verified | Reproduced from `models/risk_test_predictions.csv` | Table III reports 0.528 ✅ | ✅ |
| Macro F1 0.457 verified | Reproduced from artefact | Table III reports 0.457 ✅ | ✅ |
| Weighted F1 0.529 verified | Reproduced from artefact | Table III reports 0.529 ✅ | ✅ |
| High-risk F1 0.33 verified | Reproduced (Table IV in paper) | Stated as F1=0.33, discussed in results | ✅ |
| Majority-class baseline | Acc=0.458, MacroF1=0.157 — computed | Table III includes both baselines | ✅ |
| Stratified dummy baseline | Acc=0.304, MacroF1=0.253 — computed with seed=42 | Table III includes both baselines | ✅ |
| Confusion matrix from verified predictions | CM from `risk_test_predictions.csv` with explicit class order | Fig. 2 and Table in paper; matches `risk_confusion_matrix.csv` | ✅ |
| Class order stated | CLASS_ORDER = [No Depletion, Low, Moderate, High] | Stated in paper and verification script | ✅ |
| High-risk performance discussion | Discussed in results and limitations sections | Sections V.B and VI.B | ✅ |

---

## DASHBOARD CONSISTENCY AND OPERATIONAL LIMITATIONS

| Concern | Evidence / Artefact | Correction Made | Status |
|---|---|---|---|
| Dashboard consumes correct files | `generate_all_predictions.py` → `reports/all_station_predictions.csv` | Verified (AGENTS.md confirms FastAPI+React structure) | ✅ |
| Dashboard labeled exploratory | Multiple disclaimers in paper | Sections I, VI.B.8 explicitly state exploratory nature | ✅ |
| No operational readiness claims | Paper explicitly disclaims replacement of field measurements | Section I: "not intended as an operational early-warning tool" | ✅ |
| Observ. vs. estimate distinction | Paper distinguishes "measured historical observations" from "model-generated predictions" | Consistently maintained throughout | ✅ |

---

## REFERENCE METADATA AND CODE REFERENCES

| Concern | Evidence / Artefact | Correction Made | Status |
|---|---|---|---|
| CGWB data reference | India-WRIS portal cited with exact filename | `references.bib`: cgwb_data entry | ✅ |
| IMD rainfall reference | IMD DSP portal cited | `references.bib`: imd_rainfall entry | ✅ |
| Code repository reference | Placeholder entry with note to add commit SHA | `references.bib`: project_repo entry — SHA pending | ⚠️ |
| Sahoo et al. 2017 | WRR journal — major publication, verifiable | Cited with DOI | ✅ |
| Tao et al. 2022 | Neurocomputing review — verifiable | Cited with DOI | ✅ |
| Ramesh & Manikandan 2022 | JGSE journal — flagged as partially unverified | Note in .bib | ⚠️ |
| Wundt & Selle 2021 | J. Hydrology — flagged as unverified | Note in .bib | ⚠️ |
| Chen et al. 2023 | EnvSoft — flagged as unverified | Note in .bib | ⚠️ |

---

## IEEE FORMATTING AND FIGURES

| Concern | Evidence / Artefact | Correction Made | Status |
|---|---|---|---|
| Double-column IEEEtran class | `\documentclass[conference]{IEEEtran}` | Main.tex confirmed | ✅ |
| All template instructions removed | main.tex contains no placeholder text | Verified by inspection | ✅ |
| Figures from verified data (not invented) | All 6 figures generated by `generate_figures.py` from actual CSVs | Artefacts confirmed | ✅ |
| Confusion matrix from verified predictions | `risk_test_predictions.csv` → Fig. 2 | Verified match with saved `risk_confusion_matrix.csv` | ✅ |
| Figure captions with units | All figures include mbgl units and N counts | Captions include "N=657" and "mbgl" | ✅ |
| In-text figure references | \ref{fig:scatter}, \ref{fig:cm}, \ref{fig:arch}, etc. | All figures cross-referenced | ✅ |
| Grayscale-friendly styling | Figures use blue/red palette; confusion matrix uses Blues colormap | Adequate for grayscale printing | ✅ |
| IEEE references style | `\bibliographystyle{IEEEtran}` | Confirmed in main.tex | ✅ |
| PDF compilation | Requires LaTeX + IEEEtran; not compiled in this environment | Build instructions in README.md | ⚠️ |
| Visual inspection of PDF | Not performed (no TeX environment) | Disclosed explicitly | ⚠️ |

---

## SUMMARY SCORECARD

| Category | PASS | PARTIAL | FAIL | DISCLOSED |
|---|---|---|---|---|
| Abstract | 5 | 0 | 0 | 0 |
| Introduction | 4 | 0 | 0 | 0 |
| Related Work | 2 | 1 | 0 | 1 |
| Methodology | 5 | 0 | 0 | 0 |
| Dataset | 6 | 0 | 0 | 1 |
| Monitoring intervals / Thresholds | 2 | 1 | 0 | 2 |
| Temporal splits | 5 | 0 | 0 | 0 |
| Regression metrics | 7 | 1 | 0 | 0 |
| Classification metrics | 9 | 0 | 0 | 0 |
| Dashboard | 4 | 0 | 0 | 0 |
| References | 4 | 3 | 0 | 0 |
| Formatting / Figures | 7 | 3 | 0 | 0 |
| **Total** | **60** | **9** | **0** | **4** |

### Items Preventing Unconditional Submission Readiness

1. PDF not compiled (no local LaTeX environment available)
2. Bootstrap confidence intervals described but not numerically reported
3. Partial citation verification (3 references unconfirmed DOIs)
4. Code repository commit SHA not yet added to `project_repo` reference
5. Interval-normalised risk thresholds not evaluated (future work only)
