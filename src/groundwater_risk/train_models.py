from pathlib import Path
import warnings

import joblib
import numpy as np
import pandas as pd

from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import (
    ExtraTreesRegressor,
    HistGradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
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

MODELS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def print_section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def evaluate_model(model_name, model, X, y):
    """
    Evaluate a trained regression model.
    """

    predictions = model.predict(X)

    mae = mean_absolute_error(y, predictions)

    rmse = np.sqrt(
        mean_squared_error(y, predictions)
    )

    r2 = r2_score(y, predictions)

    print(f"\n{model_name}")
    print(f"MAE:  {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"R²:   {r2:.4f}")

    return {
        "model": model_name,
        "mae": mae,
        "rmse": rmse,
        "r2": r2,
    }


# ============================================================
# LOAD DATA
# ============================================================

print_section("LOADING TRAINING DATASET")

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Training dataset not found:\n{DATA_PATH}"
    )

df = pd.read_csv(DATA_PATH)

print(f"\nRecords loaded: {len(df)}")
print(f"Columns loaded: {len(df.columns)}")


# ============================================================
# CONVERT DATE
# ============================================================

print("\nConverting monitoring dates...")

df["Monitoring Date"] = pd.to_datetime(
    df["Monitoring Date"],
    errors="coerce"
)

invalid_dates = df["Monitoring Date"].isna().sum()

print(f"Invalid dates: {invalid_dates}")

if invalid_dates > 0:
    df = df.dropna(
        subset=["Monitoring Date"]
    ).copy()

if len(df) == 0:
    raise ValueError(
        "No valid records remain after date conversion."
    )


# ============================================================
# SORT DATA
# ============================================================

print("\nSorting data by date and station...")

df = df.sort_values(
    ["Monitoring Date", "Station"]
).reset_index(drop=True)


# ============================================================
# DEFINE TARGET
# ============================================================

TARGET_COLUMN = "next_groundwater_level"

if TARGET_COLUMN not in df.columns:
    raise ValueError(
        f"Target column '{TARGET_COLUMN}' not found."
    )


# ============================================================
# CHECK REQUIRED COLUMNS
# ============================================================

print_section("CHECKING FEATURE COLUMNS")


# Columns that must NEVER be used as predictors.
#
# These columns contain future information or are targets derived
# from the future observation.
#

LEAKAGE_COLUMNS = [
    "next_groundwater_level",
    "next_groundwater_change",
    "depletion_direction",
    "depletion_risk",
    "days_to_next_observation",
    "next_monitoring_date",
]


# Identifier / date columns.
#
# Monitoring Date is converted into time features such as
# year, month and quarter, so the raw datetime itself is excluded.

IDENTIFIER_COLUMNS = [
    "Monitoring Date",
]


# Keep all remaining columns as possible features.

excluded_columns = (
    LEAKAGE_COLUMNS
    + IDENTIFIER_COLUMNS
)

feature_columns = [
    column
    for column in df.columns
    if column not in excluded_columns
]


# Remove target explicitly as an extra safety check.

feature_columns = [
    column
    for column in feature_columns
    if column != TARGET_COLUMN
]


if len(feature_columns) == 0:
    raise ValueError(
        "No feature columns available for training."
    )


print("\nTarget column:")
print(TARGET_COLUMN)

print("\nNumber of features:")
print(len(feature_columns))

print("\nFeature columns:")

for column in feature_columns:
    print(f" - {column}")


# ============================================================
# REMOVE INVALID TARGET VALUES
# ============================================================

print_section("CLEANING TARGET DATA")

df[TARGET_COLUMN] = pd.to_numeric(
    df[TARGET_COLUMN],
    errors="coerce"
)

invalid_targets = df[TARGET_COLUMN].isna().sum()

print(
    f"Records with invalid target values: "
    f"{invalid_targets}"
)

df = df.dropna(
    subset=[TARGET_COLUMN]
).copy()

print(
    f"Records remaining: {len(df)}"
)


# ============================================================
# DEFINE CATEGORICAL AND NUMERIC FEATURES
# ============================================================

print_section("IDENTIFYING FEATURE TYPES")

X = df[feature_columns].copy()
y = df[TARGET_COLUMN].copy()


categorical_columns = [
    column
    for column in X.columns
    if X[column].dtype == "object"
    or str(X[column].dtype) == "category"
]


numeric_columns = [
    column
    for column in X.columns
    if column not in categorical_columns
]


print("\nCategorical features:")

if categorical_columns:
    for column in categorical_columns:
        print(f" - {column}")
else:
    print("None")


print("\nNumeric features:")

for column in numeric_columns:
    print(f" - {column}")


# ============================================================
# ENSURE NUMERIC COLUMNS ARE NUMERIC
# ============================================================

for column in numeric_columns:
    X[column] = pd.to_numeric(
        X[column],
        errors="coerce"
    )


# ============================================================
# CREATE CHRONOLOGICAL DATA SPLIT
# ============================================================

print_section("CREATING CHRONOLOGICAL DATA SPLIT")


# Use unique monitoring dates.
#
# This prevents the same monitoring date from appearing in
# different train/validation/test sets.

unique_dates = np.sort(
    df["Monitoring Date"]
    .dropna()
    .unique()
)


if len(unique_dates) < 10:
    raise ValueError(
        "Not enough unique dates to create a chronological split."
    )


train_end_index = int(
    len(unique_dates) * 0.70
)

validation_end_index = int(
    len(unique_dates) * 0.85
)


train_end_date = unique_dates[
    train_end_index - 1
]

validation_end_date = unique_dates[
    validation_end_index - 1
]


train_mask = (
    df["Monitoring Date"]
    <= train_end_date
)

validation_mask = (
    (df["Monitoring Date"] > train_end_date)
    &
    (df["Monitoring Date"] <= validation_end_date)
)

test_mask = (
    df["Monitoring Date"]
    > validation_end_date
)


X_train = X.loc[train_mask].copy()
y_train = y.loc[train_mask].copy()

X_validation = X.loc[
    validation_mask
].copy()

y_validation = y.loc[
    validation_mask
].copy()

X_test = X.loc[test_mask].copy()
y_test = y.loc[test_mask].copy()


print(f"\nTrain end date: {train_end_date}")
print(
    f"Validation end date: "
    f"{validation_end_date}"
)


print("\nDataset split sizes:")

print(f"Train:      {len(X_train)}")
print(
    f"Validation: {len(X_validation)}"
)
print(f"Test:       {len(X_test)}")


print("\nTrain date range:")

print(
    df.loc[
        train_mask,
        "Monitoring Date"
    ].min(),
    "to",
    df.loc[
        train_mask,
        "Monitoring Date"
    ].max()
)


print("\nValidation date range:")

print(
    df.loc[
        validation_mask,
        "Monitoring Date"
    ].min(),
    "to",
    df.loc[
        validation_mask,
        "Monitoring Date"
    ].max()
)


print("\nTest date range:")

print(
    df.loc[
        test_mask,
        "Monitoring Date"
    ].min(),
    "to",
    df.loc[
        test_mask,
        "Monitoring Date"
    ].max()
)


# ============================================================
# PREPROCESSING
# ============================================================

print_section("CREATING PREPROCESSING PIPELINE")


# Numeric preprocessing.
#
# Median imputation handles occasional missing numerical values.

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


# Categorical preprocessing.
#
# IMPORTANT:
# sparse_output=False creates a DENSE matrix.
#
# HistGradientBoostingRegressor does not support sparse matrices.

categorical_transformer = Pipeline(
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


transformers = []


if numeric_columns:
    transformers.append(
        (
            "numeric",
            numeric_transformer,
            numeric_columns,
        )
    )


if categorical_columns:
    transformers.append(
        (
            "categorical",
            categorical_transformer,
            categorical_columns,
        )
    )


preprocessor = ColumnTransformer(
    transformers=transformers,
    remainder="drop",
    sparse_threshold=0,
)


# ============================================================
# DEFINE MODELS
# ============================================================

print_section("DEFINING MODELS")


models = {


    "Random Forest": RandomForestRegressor(
        n_estimators=500,
        max_depth=None,
        min_samples_split=4,
        min_samples_leaf=2,
        max_features=0.8,
        n_jobs=-1,
        random_state=RANDOM_STATE,
    ),


    "Extra Trees": ExtraTreesRegressor(
        n_estimators=600,
        max_depth=None,
        min_samples_split=3,
        min_samples_leaf=1,
        max_features=0.9,
        n_jobs=-1,
        random_state=RANDOM_STATE,
    ),


    "HistGradientBoosting": HistGradientBoostingRegressor(
        learning_rate=0.05,
        max_iter=500,
        max_leaf_nodes=31,
        min_samples_leaf=10,
        l2_regularization=0.1,
        random_state=RANDOM_STATE,
    ),
}


# ============================================================
# TRAIN MODELS
# ============================================================

print_section("TRAINING MODELS")


results = []

trained_models = {}


for model_name, model in models.items():

    print(f"\nTraining: {model_name}")


    pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                clone(preprocessor),
            ),
            (
                "model",
                clone(model),
            ),
        ]
    )


    pipeline.fit(
        X_train,
        y_train,
    )


    predictions = pipeline.predict(
        X_validation
    )


    mae = mean_absolute_error(
        y_validation,
        predictions,
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_validation,
            predictions,
        )
    )

    r2 = r2_score(
        y_validation,
        predictions,
    )


    print(
        f"Validation MAE:  {mae:.4f}"
    )

    print(
        f"Validation RMSE: {rmse:.4f}"
    )

    print(
        f"Validation R²:   {r2:.4f}"
    )


    results.append(
        {
            "model": model_name,
            "mae": mae,
            "rmse": rmse,
            "r2": r2,
        }
    )


    trained_models[
        model_name
    ] = pipeline


# ============================================================
# MODEL COMPARISON
# ============================================================

print_section("VALIDATION MODEL COMPARISON")


results_df = pd.DataFrame(
    results
).sort_values(
    by="rmse",
    ascending=True,
).reset_index(
    drop=True
)


print(
    results_df.to_string(
        index=False
    )
)


best_model_name = results_df.loc[
    0,
    "model"
]


print(
    f"\nBest validation model: "
    f"{best_model_name}"
)


# ============================================================
# SAVE VALIDATION RESULTS
# ============================================================

results_path = (
    MODELS_DIR
    / "validation_results.csv"
)


results_df.to_csv(
    results_path,
    index=False,
)


print(
    f"\nValidation results saved to:"
)

print(results_path)


# ============================================================
# FINAL TRAINING
# ============================================================

print_section(
    "RETRAINING BEST MODEL ON TRAIN + VALIDATION DATA"
)


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


best_model = models[
    best_model_name
]


final_pipeline = Pipeline(
    steps=[
        (
            "preprocessor",
            clone(preprocessor),
        ),
        (
            "model",
            clone(best_model),
        ),
    ]
)


print(
    f"\nRetraining: "
    f"{best_model_name}"
)


final_pipeline.fit(
    X_train_final,
    y_train_final,
)


# ============================================================
# FINAL TEST EVALUATION
# ============================================================

print_section("FINAL TEST EVALUATION")


test_predictions = final_pipeline.predict(
    X_test
)


test_mae = mean_absolute_error(
    y_test,
    test_predictions,
)


test_rmse = np.sqrt(
    mean_squared_error(
        y_test,
        test_predictions,
    )
)


test_r2 = r2_score(
    y_test,
    test_predictions,
)


print(
    f"\nBest model: {best_model_name}"
)

print(
    f"Test MAE:  {test_mae:.4f}"
)

print(
    f"Test RMSE: {test_rmse:.4f}"
)

print(
    f"Test R²:   {test_r2:.4f}"
)


# ============================================================
# SAVE MODEL
# ============================================================

print_section("SAVING FINAL MODEL")


model_path = (
    MODELS_DIR
    / "groundwater_prediction_model.joblib"
)


joblib.dump(
    final_pipeline,
    model_path,
)


print(
    f"\nModel saved to:"
)

print(model_path)


# ============================================================
# SAVE FEATURE INFORMATION
# ============================================================

feature_info = {
    "target": TARGET_COLUMN,
    "features": feature_columns,
    "numeric_features": numeric_columns,
    "categorical_features": categorical_columns,
    "best_model": best_model_name,
}


feature_info_path = (
    MODELS_DIR
    / "feature_info.joblib"
)


joblib.dump(
    feature_info,
    feature_info_path,
)


print(
    f"\nFeature information saved to:"
)

print(feature_info_path)


# ============================================================
# SAVE TEST PREDICTIONS
# ============================================================

test_output = df.loc[
    test_mask,
    [
        "Station",
        "Monitoring Date",
        "groundwater_level_m",
        TARGET_COLUMN,
    ],
].copy()


test_output[
    "predicted_next_groundwater_level"
] = test_predictions


test_output[
    "prediction_error"
] = (
    test_output[
        "predicted_next_groundwater_level"
    ]
    -
    test_output[
        TARGET_COLUMN
    ]
)


test_predictions_path = (
    MODELS_DIR
    / "test_predictions.csv"
)


test_output.to_csv(
    test_predictions_path,
    index=False,
)


print(
    f"\nTest predictions saved to:"
)

print(test_predictions_path)


# ============================================================
# FINAL SUMMARY
# ============================================================

print_section("MODEL TRAINING COMPLETE")


print(
    f"\nBest model: "
    f"{best_model_name}"
)


print("\nFINAL TEST PERFORMANCE")

print(
    f"MAE:  {test_mae:.4f}"
)

print(
    f"RMSE: {test_rmse:.4f}"
)

print(
    f"R²:   {test_r2:.4f}"
)


print("\nTraining records:")
print(
    len(X_train_final)
)


print("\nTest records:")
print(
    len(X_test)
)


print("\nNumber of input features:")
print(
    len(feature_columns)
)


print("\nSaved files:")

print(
    f"1. Model:\n{model_path}"
)

print(
    f"\n2. Feature information:\n"
    f"{feature_info_path}"
)

print(
    f"\n3. Validation results:\n"
    f"{results_path}"
)

print(
    f"\n4. Test predictions:\n"
    f"{test_predictions_path}"
)

print("\n" + "=" * 60)