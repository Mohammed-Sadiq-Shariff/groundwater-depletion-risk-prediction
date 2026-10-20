export type Risk = "No Depletion" | "Low" | "Moderate" | "High";

export interface StationTelemetry {
  name: string;
  district: string;
  tehsil: string;
  block: string;
  village: string;
  latitude: number;
  longitude: number;
  monitoringDate: string;
  current: number;
  predicted: number;
  change: number;
  risk: Risk;
  probabilities: {
    no: number;
    low: number;
    moderate: number;
    high: number;
  };
  history?: Array<{ date: string; level: number }>;
}

export interface OverviewMetrics {
  monitoring_stations: number;
  total_observations: number;
  historical_coverage_years: number;
  high_risk_stations: number;
}

export interface TalukSummary {
  block: string;
  taluk_name: string;
  station_count: number;
  avg_current_depth_m: number;
  avg_predicted_depth_m: number;
  dominant_risk: Risk;
  classification_color: string;
  risk_counts: {
    high: number;
    moderate: number;
    low: number;
    no_depletion: number;
  };
  center: [number, number];
}

export interface FeatureImportance {
  name: string;
  score: number;
}

export interface MapClassificationReport {
  district: string;
  state: string;
  total_taluks: number;
  total_monitoring_stations: number;
  generated_timestamp: string;
  taluk_classifications: TalukSummary[];
}

export interface UploadResult {
  success: boolean;
  filename: string;
  total_rows: number;
  high_risk_count: number;
  moderate_risk_count: number;
  low_risk_count: number;
  no_depletion_count: number;
  warnings: string[];
  predictions: Array<{
    station: string;
    district: string;
    tehsil: string;
    block: string;
    village: string;
    latitude: number;
    longitude: number;
    monitoring_date: string;
    current_groundwater_level: number;
    predicted_groundwater_level: number;
    predicted_change: number;
    predicted_risk: Risk;
    no_depletion_probability: number;
    low_probability: number;
    moderate_probability: number;
    high_probability: number;
  }>;
}
