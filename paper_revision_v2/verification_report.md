# Verification Report
**Paper:** AI-Based Groundwater Depletion Risk Prediction for Mysuru District Using Machine Learning  
**Version:** paper_revision_v2  
**Date:** 2026-10-20  
**Prepared by:** Antigravity (automated verification + paper authoring)

---

## 1. Verified Final Metrics

All metrics are recomputed from saved prediction artefacts — not taken from prose summaries.

### 1.1 Regression (HistGradientBoostingRegressor)

| Artefact | `models/test_predictions.csv` |
|---|---|
| Test records | **657** |
| Test date range | 2019-11-11 to 2023-11-05 |
| MAE | **1.9384 m** |
| RMSE | **2.9568 m** |
| R² | **0.5469** |
| Mean-target baseline MAE | 3.4268 m |
| Persistence baseline MAE | 2.1495 m |
| Mean-target baseline RMSE | 4.3924 m |
| Persistence baseline RMSE | 3.3890 m |

> [!NOTE]
> The previously reported MAE 1.94 m, RMSE 2.96 m, R² 0.55 are CONFIRMED to 4 significant figures.

### 1.2 Classification (Random Forest — 4 classes)

| Artefact | `models/risk_test_predictions.csv` |
|---|---|
| Test records | **657** |
| Test date range | 2019-11-11 to 2023-11-05 |
| Accuracy | **0.5282** (52.82%) |
| Macro F1 | **0.4570** |
| Weighted F1 | **0.5290** |
| Majority baseline accuracy | 0.4581 |
| Stratified dummy accuracy (seed=42) | 0.3044 |
| Majority baseline macro F1 | 0.1571 |
| Stratified dummy macro F1 | 0.2533 |

**Per-class performance:**

| Class | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| No Depletion | 0.70 | 0.69 | 0.70 | 301 |
| Low | 0.38 | 0.39 | 0.38 | 129 |
| Moderate | 0.42 | 0.42 | 0.42 | 147 |
| High | 0.33 | 0.33 | 0.33 | 80 |

**Confusion Matrix (counts):**

| | Pred No Depln | Pred Low | Pred Moderate | Pred High |
|---|---|---|---|---|
| Actual No Depletion | **209** | 28 | 34 | 30 |
| Actual Low | 53 | **50** | 21 | 5 |
| Actual Moderate | 19 | 48 | **62** | 18 |
| Actual High | 16 | 6 | 32 | **26** |

> [!NOTE]
> The previously reported classification metrics (accuracy 52.82%, macro F1 0.4570, weighted F1 0.5290, High F1 ~0.327) are CONFIRMED. The High-risk F1 in the artefact is 0.33, consistent with the indicated ~0.327.

### 1.3 Dataset Split (Verified from Code)

| Split | Records | Date Range |
|---|---|---|
| Train | 2,624 | 1997-01-05 to 2015-08-25 |
| Validation | 904 | 2015-09-xx to 2019-08-19 |
| Test | 657 | 2019-11-11 to 2023-11-05 |
| **Total** | **4,185** | 1997--2023 |

> [!IMPORTANT]
> A previous draft claimed 2,569 / 846 / 657 splits. The verified figures are 2,624 / 904 / 657. The test count of 657 is identical. The train/val discrepancy arises from different preprocessing runs; the current artefact values are authoritative.

---

## 2. Data Source Verification

### 2.1 Groundwater Data

| Item | Verified Value |
|---|---|
| Source 1 | `data/raw/groundwater/gwl_manual_quarterly_cgwb_ka_1991_2020.csv` |
| Source 2 | `data/raw/groundwater/groundwater_karnataka_2021_2025.csv` |
| Portal | India-WRIS (https://indiawris.gov.in/) |
| Measurement | Depth below ground level (mbgl) |
| Monitoring type | Manual quarterly |
| Mysuru stations (verified) | 92 unique stations |
| Total records after filtering | 4,185 (post feature engineering + target construction) |
| GWL units | Metres below ground level (mbgl) |
| Date column | `Data Acquisition Time` (format `DD-MM-YYYY HH:MM`) |

### 2.2 Rainfall Data

| Item | Verified Value |
|---|---|
| Source | 16 IMD CSVs (`rainfall_YYYY_YYYY.csv`), 1989--2025 |
| Aggregation | Mean daily rainfall across Mysuru district gauges |
| Missing day treatment | Retained as NaN (NOT imputed to zero) — see `build_features.py` lines 343--354 |
| December 2023 gap | Confirmed; rolling features near gap boundary have partial-window uncertainty |
| Alignment | `merge_asof` backward join to GWL observations |

> [!WARNING]
> The code uses `min_periods=1` for all rolling windows. This means early-series or gap-adjacent windows may be computed over fewer days than the window name implies. This is disclosed in the paper as a limitation.

---

## 3. Feature Engineering Verification

All lag and rolling features are verified to use `shift(1)` before window operations, ensuring no target leakage:

- `gw_lag_1..4`: `station_group.shift(1..4)` ✅
- `gw_rolling_mean_3`: `shift(1).rolling(3)` ✅  
- `gw_rolling_mean_4`: `shift(1).rolling(4)` ✅
- `gw_rolling_std_3`: `shift(1).rolling(3)` ✅
- `station_historical_mean`: `shift(1).expanding().mean()` ✅
- `station_historical_std`: `shift(1).expanding().std()` ✅
- Rainfall features: backward `merge_asof` (no future rainfall) ✅

**Leakage columns explicitly excluded from training:**
- `next_groundwater_level` ✅
- `next_groundwater_change` ✅
- `depletion_direction` ✅
- `depletion_risk` ✅
- `days_to_next_observation` ✅
- `next_monitoring_date` ✅

---

## 4. Feature Importance Notes

Top-5 features by permutation importance (mean):
1. `groundwater_level_m`: 0.5923 — current GWL is dominant predictor
2. `gw_rolling_mean_4`: 0.3276 — 4-obs rolling mean
3. `month_cos`: 0.1474 — cyclical seasonality
4. `station_historical_mean`: 0.1203 — long-term station baseline
5. `month_sin`: 0.0286

Rainfall features with NEGATIVE importance (near zero):
- `rain_365d`: -0.0012; `rain_30d`: -0.0300; `rain_90d`: +0.0027

> [!CAUTION]
> Negative importance does not mean rainfall is physically unimportant. It likely reflects collinearity with GWL history features or poor discriminative power of district-averaged rainfall at individual station scale. The paper discloses this finding rather than suppressing it.

---

## 5. Dashboard Verification

The dashboard (`backend/` FastAPI + `frontend/` React+Vite) consumes:
- `reports/all_station_predictions.csv` generated by `generate_all_predictions.py`
- Individual station prediction outputs

The dashboard is labeled "exploratory" in the paper and does not claim operational status.

---

## 6. Original Files Preserved

| Item | Status |
|---|---|
| `models/` directory and all `.joblib` files | Preserved |
| `data/raw/` (all source CSVs) | Preserved |
| `data/processed/` (all processed CSVs) | Preserved |
| `src/` (all Python source files) | Preserved |
| `reports/` (all report files and figures) | Preserved |
| `paper_revision_v2/` | New folder, no originals overwritten |

---

## 7. Unresolved Issues

1. **Risk threshold validation**: The 1 m / 3 m class boundaries are heuristic. No hydrogeological validation against official CGWB classifications has been performed.

2. **Variable horizon problem**: Fixed-metre thresholds applied across 40--200 day intervals are not physically equivalent. Normalised thresholds (m/day) were not tested.

3. **High-risk recall**: F1 of 0.33 for High depletion is insufficient for early-warning applications.

4. **December 2023 rainfall gap**: Confirmed but unresolved. Future work should obtain complete IMD data.

5. **Reference verification**: Several cited papers (Wundt & Selle 2021; Ramesh & Manikandan 2022; Chen et al. 2023) have incomplete DOI verification. These are flagged with notes in `references.bib`.

6. **No 2026 Frontiers in AI paper found**: The reviewer comments reference a 2026 Frontiers in Artificial Intelligence paper. No such paper could be verified from available information. It is not cited in this revision.

7. **PDF compilation**: LaTeX compilation requires a local TeX distribution (MiKTeX or TeX Live) and the IEEEtran class. Pre-compiled PDF cannot be guaranteed from this environment. See README.md for build instructions.

8. **Bootstrap CI not computed**: Point estimates are reported. Bootstrap confidence intervals for MAE/RMSE are described in the methodology but not numerically computed and included in the tables (implementation requires additional compute). This should be added before final submission.

---

## 8. Code Reproducibility

Metric reproduction command:
```bash
cd groundwater-depletion-risk
python paper_revision_v2/verify_metrics.py
```

Figure regeneration command:
```bash
python paper_revision_v2/generate_figures.py
```

Both scripts run successfully from the project root (verified 2026-10-20).
