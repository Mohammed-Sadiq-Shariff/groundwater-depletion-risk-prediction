from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BACKEND_DIR.parent

DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "reports"


MODEL_DATASET_PATH = (
    PROCESSED_DATA_DIR / "mysore_model_dataset.csv"
)

GROUNDWATER_DATA_PATH = (
    PROCESSED_DATA_DIR / "mysore_groundwater_1991_2025.csv"
)

RAINFALL_DATA_PATH = (
    PROCESSED_DATA_DIR / "mysore_rainfall_1991_2025.csv"
)


PREDICTION_MODEL_PATH = (
    MODELS_DIR / "groundwater_prediction_model.joblib"
)

RISK_MODEL_PATH = (
    MODELS_DIR / "groundwater_depletion_risk_model.joblib"
)

FEATURE_INFO_PATH = (
    MODELS_DIR / "feature_info.joblib"
)

RISK_FEATURE_INFO_PATH = (
    MODELS_DIR / "risk_feature_info.joblib"
)


LATEST_PREDICTION_PATH = (
    REPORTS_DIR / "latest_station_prediction.csv"
)

ALL_PREDICTIONS_PATH = (
    REPORTS_DIR / "all_station_predictions.csv"
)

FEATURE_IMPORTANCE_PATH = (
    REPORTS_DIR / "feature_importance.csv"
)

MODEL_EVALUATION_PATH = (
    REPORTS_DIR / "model_evaluation_summary.csv"
)
