"""Verification script for all paper metrics."""
import pandas as pd
import numpy as np
from sklearn.metrics import (
    accuracy_score, f1_score, classification_report,
    confusion_matrix, mean_absolute_error, mean_squared_error, r2_score
)
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ============================================================
# REGRESSION METRICS
# ============================================================
print("=" * 60)
print("REGRESSION TEST METRICS")
print("=" * 60)

reg_preds = pd.read_csv(ROOT / "models" / "test_predictions.csv")
reg_preds = reg_preds.dropna(subset=["next_groundwater_level", "predicted_next_groundwater_level"])

actual_r = reg_preds["next_groundwater_level"]
pred_r = reg_preds["predicted_next_groundwater_level"]
persist_r = reg_preds["groundwater_level_m"]

mae = mean_absolute_error(actual_r, pred_r)
rmse = np.sqrt(mean_squared_error(actual_r, pred_r))
r2 = r2_score(actual_r, pred_r)

mean_base_mae = mean_absolute_error(actual_r, np.full(len(actual_r), actual_r.mean()))
persist_mae = mean_absolute_error(actual_r, persist_r)
mean_base_rmse = np.sqrt(mean_squared_error(actual_r, np.full(len(actual_r), actual_r.mean())))
persist_rmse = np.sqrt(mean_squared_error(actual_r, persist_r))

print(f"Test records: {len(reg_preds)}")
print(f"Date range: {reg_preds['Monitoring Date'].min()} to {reg_preds['Monitoring Date'].max()}")
print(f"Model MAE:   {mae:.4f} m")
print(f"Model RMSE:  {rmse:.4f} m")
print(f"Model R2:    {r2:.4f}")
print(f"Mean-target baseline MAE:  {mean_base_mae:.4f} m, RMSE: {mean_base_rmse:.4f} m")
print(f"Persistence baseline MAE:  {persist_mae:.4f} m, RMSE: {persist_rmse:.4f} m")

# ============================================================
# CLASSIFICATION METRICS
# ============================================================
print()
print("=" * 60)
print("CLASSIFICATION TEST METRICS")
print("=" * 60)

CLASS_ORDER = ["No Depletion", "Low", "Moderate", "High"]

cls_preds = pd.read_csv(ROOT / "models" / "risk_test_predictions.csv")
cls_preds = cls_preds.dropna(subset=["depletion_risk", "predicted_depletion_risk"])

actual_c = cls_preds["depletion_risk"]
pred_c = cls_preds["predicted_depletion_risk"]

acc = accuracy_score(actual_c, pred_c)
macro_f1 = f1_score(actual_c, pred_c, average="macro", labels=CLASS_ORDER)
weighted_f1 = f1_score(actual_c, pred_c, average="weighted", labels=CLASS_ORDER)

print(f"Test records: {len(cls_preds)}")
print(f"Date range: {cls_preds['Monitoring Date'].min()} to {cls_preds['Monitoring Date'].max()}")
print(f"Accuracy:    {acc:.4f}")
print(f"Macro F1:    {macro_f1:.4f}")
print(f"Weighted F1: {weighted_f1:.4f}")
print()
print("Classification Report:")
print(classification_report(actual_c, pred_c, labels=CLASS_ORDER))

cm = confusion_matrix(actual_c, pred_c, labels=CLASS_ORDER)
cm_df = pd.DataFrame(cm, index=[f"Actual_{c}" for c in CLASS_ORDER],
                     columns=[f"Pred_{c}" for c in CLASS_ORDER])
print("Confusion Matrix:")
print(cm_df)

# Baselines
majority_class = actual_c.value_counts().idxmax()
maj_pred = [majority_class] * len(actual_c)
maj_acc = accuracy_score(actual_c, maj_pred)
maj_macro = f1_score(actual_c, maj_pred, average="macro", labels=CLASS_ORDER, zero_division=0)
print(f"\nMajority baseline ({majority_class}): Acc={maj_acc:.4f}, Macro F1={maj_macro:.4f}")

np.random.seed(42)
class_probs = actual_c.value_counts(normalize=True)
strat_pred = np.random.choice(class_probs.index, size=len(actual_c), p=class_probs.values)
strat_acc = accuracy_score(actual_c, strat_pred)
strat_macro = f1_score(actual_c, strat_pred, average="macro", labels=CLASS_ORDER, zero_division=0)
print(f"Stratified dummy (seed=42): Acc={strat_acc:.4f}, Macro F1={strat_macro:.4f}")

# ============================================================
# SPLIT INFO FROM TRAINING DATASET
# ============================================================
print()
print("=" * 60)
print("DATASET SPLIT VERIFICATION")
print("=" * 60)

df = pd.read_csv(ROOT / "data" / "processed" / "mysore_training_dataset.csv", low_memory=False)
df["Monitoring Date"] = pd.to_datetime(df["Monitoring Date"], errors="coerce")
df = df.dropna(subset=["Monitoring Date", "next_groundwater_level"]).sort_values("Monitoring Date")

unique_dates = np.sort(df["Monitoring Date"].dropna().unique())
train_end_idx = int(len(unique_dates) * 0.70)
val_end_idx = int(len(unique_dates) * 0.85)

train_end = unique_dates[train_end_idx - 1]
val_end = unique_dates[val_end_idx - 1]

train = df[df["Monitoring Date"] <= train_end]
val = df[(df["Monitoring Date"] > train_end) & (df["Monitoring Date"] <= val_end)]
test = df[df["Monitoring Date"] > val_end]

print(f"Total records: {len(df)}")
print(f"Unique stations: {df['Station'].nunique()}")
print(f"Train end date: {pd.Timestamp(train_end).date()}")
print(f"Val end date:   {pd.Timestamp(val_end).date()}")
print(f"Train: {len(train)} records, {df[df['Monitoring Date'] <= train_end]['Monitoring Date'].min().date()} to {pd.Timestamp(train_end).date()}")
print(f"Val:   {len(val)} records")
print(f"Test:  {len(test)} records")
print()
print("Depletion risk distribution (full dataset):")
print(df["depletion_risk"].value_counts())
print()
print("Prediction horizon (days_to_next_observation):")
print(df["days_to_next_observation"].describe())
print()
print("Feature importance (top 10):")
fi = pd.read_csv(ROOT / "reports" / "feature_importance.csv")
print(fi.head(10).to_string(index=False))
