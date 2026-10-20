from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    message: str


class OverviewResponse(BaseModel):
    monitoring_stations: int
    total_observations: int
    historical_coverage_years: float
    high_risk_stations: int


class StationSummary(BaseModel):
    station: str
    district: Optional[str] = None
    tehsil: Optional[str] = None
    block: Optional[str] = None
    village: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    records: int


class StationPrediction(BaseModel):
    station: str
    district: Optional[str] = None
    tehsil: Optional[str] = None
    block: Optional[str] = None
    village: Optional[str] = None
    monitoring_date: Optional[str] = None

    current_groundwater_level: Optional[float] = None
    predicted_groundwater_level: Optional[float] = None
    predicted_change: Optional[float] = None

    predicted_risk: Optional[str] = None

    no_depletion_probability: Optional[float] = None
    low_probability: Optional[float] = None
    moderate_probability: Optional[float] = None
    high_probability: Optional[float] = None


class PredictionRequest(BaseModel):
    station: str


class PredictionResponse(BaseModel):
    station: str
    current_groundwater_level: float
    predicted_groundwater_level: float
    predicted_change: float
    predicted_risk: str
    probabilities: Dict[str, float]


class DashboardResponse(BaseModel):
    overview: Dict[str, Any]
    stations: List[Dict[str, Any]]
    predictions: List[Dict[str, Any]]
