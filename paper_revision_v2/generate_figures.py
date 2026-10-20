"""
Generate all publication figures for paper_revision_v2.
Run from: groundwater-depletion-risk/ (project root)
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
from sklearn.metrics import (
    confusion_matrix, mean_absolute_error, mean_squared_error, r2_score
)
from pathlib import Path

# ---- Paths --------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
FIG_OUT = ROOT / "paper_revision_v2" / "figures"
FIG_OUT.mkdir(parents=True, exist_ok=True)

# Style
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
})

CLASS_ORDER = ["No Depletion", "Low", "Moderate", "High"]

# ---- Load data ----------------------------------------------------
reg = pd.read_csv(ROOT / "models" / "test_predictions.csv")
reg = reg.dropna(subset=["next_groundwater_level", "predicted_next_groundwater_level"])
actual_r = reg["next_groundwater_level"].values
pred_r = reg["predicted_next_groundwater_level"].values
persist_r = reg["groundwater_level_m"].values

cls = pd.read_csv(ROOT / "models" / "risk_test_predictions.csv")
cls = cls.dropna(subset=["depletion_risk", "predicted_depletion_risk"])
actual_c = cls["depletion_risk"].values
pred_c = cls["predicted_depletion_risk"].values

fi = pd.read_csv(ROOT / "reports" / "feature_importance.csv")

mae = mean_absolute_error(actual_r, pred_r)
rmse = np.sqrt(mean_squared_error(actual_r, pred_r))
r2 = r2_score(actual_r, pred_r)

# ==================================================================
# FIGURE 1: Actual vs Predicted scatter + residual (regression)
# ==================================================================
fig, axes = plt.subplots(1, 2, figsize=(6.5, 3.0))

# Scatter
ax = axes[0]
ax.scatter(actual_r, pred_r, alpha=0.35, s=8, color="#1a6faf", edgecolors="none")
lim_min = min(actual_r.min(), pred_r.min()) - 0.5
lim_max = max(actual_r.max(), pred_r.max()) + 0.5
ax.plot([lim_min, lim_max], [lim_min, lim_max], "k--", lw=0.8, label="y = x")
ax.set_xlabel("Actual GWL (mbgl)")
ax.set_ylabel("Predicted GWL (mbgl)")
ax.set_title(f"(a) Actual vs. Predicted\nMAE={mae:.2f} m, RMSE={rmse:.2f} m, R²={r2:.3f}")
ax.legend(fontsize=7)
ax.set_xlim(lim_min, lim_max)
ax.set_ylim(lim_min, lim_max)

# Residuals
ax2 = axes[1]
residuals = pred_r - actual_r
ax2.scatter(pred_r, residuals, alpha=0.35, s=8, color="#c94040", edgecolors="none")
ax2.axhline(0, color="k", lw=0.8, ls="--")
ax2.set_xlabel("Predicted GWL (mbgl)")
ax2.set_ylabel("Residual (Predicted − Actual, m)")
ax2.set_title("(b) Residual Plot")
# Annotate stats
ax2.text(0.02, 0.97, f"Mean residual: {residuals.mean():.3f} m\nStd: {residuals.std():.3f} m",
         transform=ax2.transAxes, fontsize=7, va="top",
         bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gray", alpha=0.8))

fig.tight_layout()
fig.savefig(FIG_OUT / "fig_regression_scatter_residual.pdf")
fig.savefig(FIG_OUT / "fig_regression_scatter_residual.png")
plt.close(fig)
print("Saved fig_regression_scatter_residual")

# ==================================================================
# FIGURE 2: Confusion matrix (classification)
# ==================================================================
cm = confusion_matrix(actual_c, pred_c, labels=CLASS_ORDER)
cm_norm = cm.astype(float) / cm.sum(axis=1, keepdims=True)

fig, axes = plt.subplots(1, 2, figsize=(6.5, 3.0))

for ax_idx, (data, title, fmt) in enumerate([
    (cm, "(a) Counts", "d"),
    (cm_norm, "(b) Row-normalised", ".2f")
]):
    ax = axes[ax_idx]
    im = ax.imshow(data, cmap="Blues", vmin=0)
    ax.set_xticks(range(len(CLASS_ORDER)))
    ax.set_yticks(range(len(CLASS_ORDER)))
    ax.set_xticklabels(["No\nDepln.", "Low", "Mod.", "High"], fontsize=8)
    ax.set_yticklabels(CLASS_ORDER, fontsize=8)
    ax.set_xlabel("Predicted class")
    ax.set_ylabel("Actual class")
    ax.set_title(title)
    threshold = data.max() / 2.0
    for i in range(len(CLASS_ORDER)):
        for j in range(len(CLASS_ORDER)):
            val = f"{data[i, j]:{fmt}}"
            color = "white" if data[i, j] > threshold else "black"
            ax.text(j, i, val, ha="center", va="center", fontsize=7.5, color=color)
    fig.colorbar(im, ax=ax, shrink=0.8)

fig.suptitle("Random Forest Confusion Matrix — Test Set (N=657)", fontsize=9, y=1.01)
fig.tight_layout()
fig.savefig(FIG_OUT / "fig_confusion_matrix.pdf")
fig.savefig(FIG_OUT / "fig_confusion_matrix.png")
plt.close(fig)
print("Saved fig_confusion_matrix")

# ==================================================================
# FIGURE 3: Per-class classification performance bar chart
# ==================================================================
from sklearn.metrics import precision_score, recall_score, f1_score

prec_vals = precision_score(actual_c, pred_c, labels=CLASS_ORDER, average=None)
rec_vals = recall_score(actual_c, pred_c, labels=CLASS_ORDER, average=None)
f1_vals = f1_score(actual_c, pred_c, labels=CLASS_ORDER, average=None)
support = [np.sum(actual_c == c) for c in CLASS_ORDER]

x = np.arange(len(CLASS_ORDER))
width = 0.25

fig, ax = plt.subplots(figsize=(5.5, 3.0))
b1 = ax.bar(x - width, prec_vals, width, label="Precision", color="#1a6faf")
b2 = ax.bar(x, rec_vals, width, label="Recall", color="#c94040")
b3 = ax.bar(x + width, f1_vals, width, label="F1-Score", color="#2ca02c")

ax.set_xticks(x)
ax.set_xticklabels([f"{c}\n(n={s})" for c, s in zip(CLASS_ORDER, support)], fontsize=8)
ax.set_ylim(0, 1.0)
ax.set_ylabel("Score")
ax.set_title("Per-Class Classification Performance — Test Set")
ax.legend(loc="upper right", fontsize=7)
ax.axhline(0.5, color="gray", lw=0.5, ls=":")

for bars in [b1, b2, b3]:
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{h:.2f}", xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 2), textcoords="offset points",
                    ha="center", va="bottom", fontsize=6)

fig.tight_layout()
fig.savefig(FIG_OUT / "fig_class_performance.pdf")
fig.savefig(FIG_OUT / "fig_class_performance.png")
plt.close(fig)
print("Saved fig_class_performance")

# ==================================================================
# FIGURE 4: Feature Importance (top 15, positive only)
# ==================================================================
fi_pos = fi[fi["importance_mean"] > 0].nlargest(15, "importance_mean")
labels = fi_pos["feature"].values
vals = fi_pos["importance_mean"].values
errs = fi_pos["importance_std"].values

fig, ax = plt.subplots(figsize=(5.5, 3.5))
colors = ["#1a6faf" if i < 5 else "#7ab3d9" for i in range(len(labels))]
bars = ax.barh(range(len(labels)), vals, xerr=errs, capsize=2,
               color=colors, error_kw={"elinewidth": 0.7})
ax.set_yticks(range(len(labels)))
ax.set_yticklabels(labels, fontsize=8)
ax.invert_yaxis()
ax.set_xlabel("Permutation Importance (mean ± std)")
ax.set_title("Top-15 Feature Importances (Regression Model)")
ax.axvline(0, color="black", lw=0.5)
fig.tight_layout()
fig.savefig(FIG_OUT / "fig_feature_importance.pdf")
fig.savefig(FIG_OUT / "fig_feature_importance.png")
plt.close(fig)
print("Saved fig_feature_importance")

# ==================================================================
# FIGURE 5: Chronological split diagram
# ==================================================================
fig, ax = plt.subplots(figsize=(6.5, 1.8))
ax.set_xlim(0, 10)
ax.set_ylim(-0.5, 2.5)
ax.axis("off")

# Timeline bar
timeline_y = 1.0
ax.annotate("", xy=(9.8, timeline_y), xytext=(0.2, timeline_y),
            arrowprops=dict(arrowstyle="->", color="black", lw=1.2))

# Segments
# Train: 0.2 to 4.9 (1997-2015-08)
# Val: 4.9 to 7.3 (2015-08-2019-08)
# Test: 7.3 to 9.8 (2019-08-2023-11)
segs = [
    (0.3, 4.9, "#2166ac", "Train\n2,624 records\n1997-01-05 to 2015-08-25", 2.0),
    (4.9, 7.3, "#4dac26", "Validation\n904 records\n2015-09 to 2019-08-19", 2.0),
    (7.3, 9.7, "#d6604d", "Test\n657 records\n2019-11 to 2023-11-05", 2.0),
]

for x0, x1, color, label, txt_y in segs:
    ax.barh(timeline_y, x1 - x0, left=x0, height=0.35, color=color, alpha=0.85)
    ax.text((x0 + x1) / 2, 1.65, label,
            ha="center", va="bottom", fontsize=7.0, color=color)

# Boundary lines
for xb, lbl in [(4.9, "2015-08-25\n(train|val)"), (7.3, "2019-08-19\n(val|test)")]:
    ax.axvline(xb, color="black", lw=0.8, ls="--", ymin=0.35, ymax=0.75)
    ax.text(xb, 0.35, lbl, ha="center", va="top", fontsize=7)

ax.text(0.2, timeline_y, "1991", ha="center", va="center", fontsize=7, fontweight="bold")
ax.text(9.8, timeline_y, "2024", ha="center", va="center", fontsize=7, fontweight="bold")
ax.set_title("Chronological Dataset Split — Regression Model (N=4,185 total)", fontsize=9)

fig.tight_layout()
fig.savefig(FIG_OUT / "fig_chronological_split.pdf")
fig.savefig(FIG_OUT / "fig_chronological_split.png")
plt.close(fig)
print("Saved fig_chronological_split")

# ==================================================================
# FIGURE 6: Baseline comparison bar chart
# ==================================================================
models_names = ["Mean Target", "Persistence", "HistGBT (ours)"]
mae_vals = [3.4268, 2.1495, 1.9384]
rmse_vals = [4.3924, 3.3890, 2.9568]

x = np.arange(len(models_names))
width = 0.35

fig, axes = plt.subplots(1, 2, figsize=(5.5, 2.8))

colors = ["#aec7e8", "#aec7e8", "#1a6faf"]
axes[0].bar(x, mae_vals, width=0.6, color=colors)
axes[0].set_xticks(x)
axes[0].set_xticklabels(models_names, fontsize=8)
axes[0].set_ylabel("MAE (m)")
axes[0].set_title("(a) MAE Comparison")
for i, v in enumerate(mae_vals):
    axes[0].text(i, v + 0.05, f"{v:.2f}", ha="center", fontsize=7.5)

axes[1].bar(x, rmse_vals, width=0.6, color=colors)
axes[1].set_xticks(x)
axes[1].set_xticklabels(models_names, fontsize=8)
axes[1].set_ylabel("RMSE (m)")
axes[1].set_title("(b) RMSE Comparison")
for i, v in enumerate(rmse_vals):
    axes[1].text(i, v + 0.05, f"{v:.2f}", ha="center", fontsize=7.5)

fig.suptitle("Regression Baseline Comparison — Test Set (N=657)", fontsize=9)
fig.tight_layout()
fig.savefig(FIG_OUT / "fig_baseline_comparison.pdf")
fig.savefig(FIG_OUT / "fig_baseline_comparison.png")
plt.close(fig)
print("Saved fig_baseline_comparison")

print("\nAll figures generated successfully in:", FIG_OUT)
