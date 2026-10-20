from pathlib import Path
import warnings

import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import (
    RandomForestClassifier,
    ExtraTreesClassifier,
    HistGradientBoostingClassifier,
)
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


# ============================================================
# CONFIGURATION
# ============================================================

warnings.filterwarnings("ignore")

RANDOM_STATE = 42

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "mysore_training_dataset.csv"
)

MODELS_DIR = PROJECT_ROOT / "models"

MODELS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# HELPER FUNCTION
# ============================================================

def print_section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


# ============================================================
# LOAD DATA
# ============================================================

print_section("LOADING DEPLETION RISK TRAINING DATA")


if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Training dataset not found:\n{DATA_PATH}"
    )


df = pd.read_csv(DATA_PATH)


print(
    f"\nRecords loaded: {len(df)}"
)

print(
    f"Columns loaded: {len(df.columns)}"
)


# ============================================================
# DATE PREPARATION
# ============================================================

print_section("PREPARING DATA")


df["Monitoring Date"] = pd.to_datetime(
    df["Monitoring Date"],
    errors="coerce",
)


invalid_dates = (
    df["Monitoring Date"]
    .isna()
    .sum()
)


print(
    f"\nInvalid monitoring dates: {invalid_dates}"
)


df = df.dropna(
    subset=[
        "Monitoring Date",
        "depletion_risk",
    ]
).copy()


df = df.sort_values(
    [
        "Monitoring Date",
        "Station",
    ]
).reset_index(
    drop=True
)


# ============================================================
# TARGET
# ============================================================

TARGET_COLUMN = "depletion_risk"

# Ensure target-observation dates are datetime values
df["next_monitoring_date"] = pd.to_datetime(
    df["next_monitoring_date"],
    errors="coerce"
)


print_section("DEPLETION RISK TARGET")


print(
    "\nRisk distribution:"
)


print(
    df[TARGET_COLUMN]
    .value_counts()
)


# ============================================================
# DEFINE FEATURES
# ============================================================

print_section("SELECTING MODEL FEATURES")


# IMPORTANT:
# Do not include future information or target-related columns.

EXCLUDED_COLUMNS = [
    "Monitoring Date",
    "next_monitoring_date",
    "next_groundwater_level",
    "next_groundwater_change",
    "days_to_next_observation",
    "depletion_direction",
    "depletion_risk",
]


FEATURE_COLUMNS = [
    column
    for column in df.columns
    if column not in EXCLUDED_COLUMNS
]


print(
    f"\nNumber of input features: "
    f"{len(FEATURE_COLUMNS)}"
)


print("\nFeature columns:")


for feature in FEATURE_COLUMNS:
    print(
        f" - {feature}"
    )


X = df[
    FEATURE_COLUMNS
].copy()


y = df[
    TARGET_COLUMN
].copy()


# ============================================================
# IDENTIFY CATEGORICAL AND NUMERIC FEATURES
# ============================================================

print_section("IDENTIFYING FEATURE TYPES")


CATEGORICAL_FEATURES = [
    column
    for column in FEATURE_COLUMNS
    if not pd.api.types.is_numeric_dtype(X[column])
]


NUMERIC_FEATURES = [
    column
    for column in FEATURE_COLUMNS
    if pd.api.types.is_numeric_dtype(X[column])
]


print(
    "\nCategorical features:"
)


for feature in CATEGORICAL_FEATURES:
    print(
        f" - {feature}"
    )


print(
    "\nNumeric features:"
)


for feature in NUMERIC_FEATURES:
    print(
        f" - {feature}"
    )


# ============================================================
# CHRONOLOGICAL SPLIT
# ============================================================

print_section(
    "CREATING CHRONOLOGICAL DATA SPLIT"
)


unique_dates = np.sort(
    df[
        "Monitoring Date"
    ]
    .unique()
)


train_end_index = int(
    len(unique_dates) * 0.70
)


validation_end_index = int(
    len(unique_dates) * 0.85
)


train_end_date = (
    unique_dates[
        train_end_index - 1
    ]
)


validation_end_date = (
    unique_dates[
        validation_end_index - 1
    ]
)


train_mask = (
    (df["Monitoring Date"] <= train_end_date)
    & (df["next_monitoring_date"] <= train_end_date)
)


validation_mask = (
    (df["Monitoring Date"] > train_end_date)
    & (df["Monitoring Date"] <= validation_end_date)
    & (df["next_monitoring_date"] <= validation_end_date)
)


test_mask = (
    df["Monitoring Date"] > validation_end_date
)


X_train = X.loc[
    train_mask
].copy()


y_train = y.loc[
    train_mask
].copy()


X_validation = X.loc[
    validation_mask
].copy()


y_validation = y.loc[
    validation_mask
].copy()


X_test = X.loc[
    test_mask
].copy()


y_test = y.loc[
    test_mask
].copy()


print(
    f"\nTrain records:      {len(X_train)}"
)

print(
    f"Validation records: {len(X_validation)}"
)

print(
    f"Test records:       {len(X_test)}"
)


print(
    "\nTrain date range:"
)


print(
    df.loc[
        train_mask,
        "Monitoring Date"
    ].min(),
    "to",
    df.loc[
        train_mask,
        "Monitoring Date"
    ].max(),
)


print(
    "\nValidation date range:"
)


print(
    df.loc[
        validation_mask,
        "Monitoring Date"
    ].min(),
    "to",
    df.loc[
        validation_mask,
        "Monitoring Date"
    ].max(),
)


print(
    "\nTest date range:"
)


print(
    df.loc[
        test_mask,
        "Monitoring Date"
    ].min(),
    "to",
    df.loc[
        test_mask,
        "Monitoring Date"
    ].max(),
)


# ============================================================
# PREPROCESSING
# ============================================================

print_section(
    "CREATING PREPROCESSING PIPELINES"
)


numeric_transformer = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(
                strategy="median"
            ),
        )
    ]
)


categorical_transformer_sparse = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(
                strategy="most_frequent"
            ),
        ),
        (
            "onehot",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
        ),
    ]
)


categorical_transformer_dense = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(
                strategy="most_frequent"
            ),
        ),
        (
            "onehot",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False,
            ),
        ),
    ]
)


preprocessor_sparse = ColumnTransformer(
    transformers=[
        (
            "numeric",
            numeric_transformer,
            NUMERIC_FEATURES,
        ),
        (
            "categorical",
            categorical_transformer_sparse,
            CATEGORICAL_FEATURES,
        ),
    ]
)


preprocessor_dense = ColumnTransformer(
    transformers=[
        (
            "numeric",
            numeric_transformer,
            NUMERIC_FEATURES,
        ),
        (
            "categorical",
            categorical_transformer_dense,
            CATEGORICAL_FEATURES,
        ),
    ],
    sparse_threshold=0,
)


# ============================================================
# DEFINE MODELS
# ============================================================

print_section(
    "DEFINING CLASSIFICATION MODELS"
)


models = {
    "Random Forest": Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor_sparse,
            ),
            (
                "model",
                RandomForestClassifier(
                    n_estimators=400,
                    min_samples_leaf=2,
                    class_weight="balanced",
                    random_state=RANDOM_STATE,
                    n_jobs=-1,
                ),
            ),
        ]
    ),

    "Extra Trees": Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor_sparse,
            ),
            (
                "model",
                ExtraTreesClassifier(
                    n_estimators=400,
                    min_samples_leaf=2,
                    class_weight="balanced",
                    random_state=RANDOM_STATE,
                    n_jobs=-1,
                ),
            ),
        ]
    ),

    "HistGradientBoosting": Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor_dense,
            ),
            (
                "model",
                HistGradientBoostingClassifier(
                    max_iter=300,
                    learning_rate=0.05,
                    max_leaf_nodes=31,
                    random_state=RANDOM_STATE,
                ),
            ),
        ]
    ),
}


# ============================================================
# TRAIN MODELS
# ============================================================

print_section(
    "TRAINING RISK CLASSIFICATION MODELS"
)


validation_results = []


for model_name, model_pipeline in models.items():

    print(
        f"\nTraining: {model_name}"
    )


    model_pipeline.fit(
        X_train,
        y_train,
    )


    validation_predictions = (
        model_pipeline.predict(
            X_validation
        )
    )


    accuracy = accuracy_score(
        y_validation,
        validation_predictions,
    )


    macro_f1 = f1_score(
        y_validation,
        validation_predictions,
        average="macro",
        zero_division=0,
    )


    weighted_f1 = f1_score(
        y_validation,
        validation_predictions,
        average="weighted",
        zero_division=0,
    )


    print(
        f"Validation Accuracy:    "
        f"{accuracy:.4f}"
    )


    print(
        f"Validation Macro F1:    "
        f"{macro_f1:.4f}"
    )


    print(
        f"Validation Weighted F1: "
        f"{weighted_f1:.4f}"
    )


    validation_results.append(
        {
            "model": model_name,
            "accuracy": accuracy,
            "macro_f1": macro_f1,
            "weighted_f1": weighted_f1,
        }
    )


# ============================================================
# MODEL COMPARISON
# ============================================================

print_section(
    "VALIDATION MODEL COMPARISON"
)


validation_results_df = pd.DataFrame(
    validation_results
)


validation_results_df = (
    validation_results_df
    .sort_values(
        "macro_f1",
        ascending=False,
    )
    .reset_index(
        drop=True
    )
)


print(
    validation_results_df.to_string(
        index=False
    )
)


validation_results_path = (
    MODELS_DIR
    / "risk_validation_results.csv"
)


validation_results_df.to_csv(
    validation_results_path,
    index=False,
)


best_model_name = (
    validation_results_df.iloc[0]["model"]
)


print(
    f"\nBest validation model: "
    f"{best_model_name}"
)


# ============================================================
# RETRAIN BEST MODEL
# ============================================================

print_section(
    "RETRAINING BEST MODEL"
)


best_model = models[
    best_model_name
]


X_train_final = pd.concat(
    [
        X_train,
        X_validation,
    ],
    axis=0,
)


y_train_final = pd.concat(
    [
        y_train,
        y_validation,
    ],
    axis=0,
)


print(
    f"\nRetraining {best_model_name}"
)


print(
    f"Training records: "
    f"{len(X_train_final)}"
)


best_model.fit(
    X_train_final,
    y_train_final,
)


# ============================================================
# FINAL TEST EVALUATION
# ============================================================

print_section(
    "FINAL TEST EVALUATION"
)


test_predictions = (
    best_model.predict(
        X_test
    )
)


test_accuracy = accuracy_score(
    y_test,
    test_predictions,
)


test_macro_f1 = f1_score(
    y_test,
    test_predictions,
    average="macro",
    zero_division=0,
)


test_weighted_f1 = f1_score(
    y_test,
    test_predictions,
    average="weighted",
    zero_division=0,
)


print(
    f"\nBest model: "
    f"{best_model_name}"
)


print(
    f"Test Accuracy:    "
    f"{test_accuracy:.4f}"
)


print(
    f"Test Macro F1:    "
    f"{test_macro_f1:.4f}"
)


print(
    f"Test Weighted F1: "
    f"{test_weighted_f1:.4f}"
)


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

print_section(
    "CLASSIFICATION REPORT"
)


risk_classes = [
    "No Depletion",
    "Low",
    "Moderate",
    "High",
]


print(
    classification_report(
        y_test,
        test_predictions,
        labels=risk_classes,
        zero_division=0,
    )
)


# ============================================================
# CONFUSION MATRIX
# ============================================================

print_section(
    "CONFUSION MATRIX"
)


conf_matrix = confusion_matrix(
    y_test,
    test_predictions,
    labels=risk_classes,
)


confusion_df = pd.DataFrame(
    conf_matrix,
    index=[
        f"Actual_{risk}"
        for risk in risk_classes
    ],
    columns=[
        f"Predicted_{risk}"
        for risk in risk_classes
    ],
)


print(
    confusion_df
)


confusion_matrix_path = (
    MODELS_DIR
    / "risk_confusion_matrix.csv"
)


confusion_df.to_csv(
    confusion_matrix_path
)


# ============================================================
# SAVE TEST PREDICTIONS
# ============================================================

prediction_results = df.loc[
    test_mask,
    [
        "Station",
        "District",
        "Latitude",
        "Longitude",
        "Monitoring Date",
        "groundwater_level_m",
        TARGET_COLUMN,
    ],
].copy()


prediction_results[
    "predicted_depletion_risk"
] = test_predictions


prediction_results_path = (
    MODELS_DIR
    / "risk_test_predictions.csv"
)


prediction_results.to_csv(
    prediction_results_path,
    index=False,
)


# ============================================================
# SAVE MODEL
# ============================================================

print_section(
    "SAVING FINAL RISK MODEL"
)


risk_model_path = (
    MODELS_DIR
    / "groundwater_depletion_risk_model.joblib"
)


joblib.dump(
    best_model,
    risk_model_path,
)


risk_feature_info = {
    "best_model": best_model_name,
    "features": FEATURE_COLUMNS,
    "target": TARGET_COLUMN,
    "categorical_features": CATEGORICAL_FEATURES,
    "numeric_features": NUMERIC_FEATURES,
    "risk_classes": risk_classes,
    "test_accuracy": test_accuracy,
    "test_macro_f1": test_macro_f1,
    "test_weighted_f1": test_weighted_f1,
}


risk_feature_info_path = (
    MODELS_DIR
    / "risk_feature_info.joblib"
)


joblib.dump(
    risk_feature_info,
    risk_feature_info_path,
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print_section(
    "DEPLETION RISK MODEL TRAINING COMPLETE"
)


print(
    f"\nBest model: "
    f"{best_model_name}"
)


print(
    "\nFINAL TEST PERFORMANCE"
)


print(
    f"Accuracy:    "
    f"{test_accuracy:.4f}"
)


print(
    f"Macro F1:    "
    f"{test_macro_f1:.4f}"
)


print(
    f"Weighted F1: "
    f"{test_weighted_f1:.4f}"
)


print(
    "\nSaved files:"
)


print(
    "\n1. Risk model:"
)


print(
    risk_model_path
)


print(
    "\n2. Risk feature information:"
)


print(
    risk_feature_info_path
)


print(
    "\n3. Validation comparison:"
)


print(
    validation_results_path
)


print(
    "\n4. Confusion matrix:"
)


print(
    confusion_matrix_path
)


print(
    "\n5. Test predictions:"
)


print(
    prediction_results_path
)


print("\n" + "=" * 60)


