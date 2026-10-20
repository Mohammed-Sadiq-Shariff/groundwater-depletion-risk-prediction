import json
import pandas as pd
from pathlib import Path

preds_path = Path("reports/all_station_predictions.csv")
gw_path = Path("data/processed/mysore_groundwater_1991_2025.csv")
feats_path = Path("reports/feature_importance.csv")

preds_df = pd.read_csv(preds_path)
gw_df = pd.read_csv(gw_path)
feats_df = pd.read_csv(feats_path) if feats_path.exists() else None

# Clean and prepare stations
stations = []
for _, row in preds_df.iterrows():
    st_name = str(row["Station"])
    # Get last 8 readings from gw_df if available
    st_gw = gw_df[gw_df["Station"] == st_name].dropna(subset=["Groundwater Level Quarterly Manual (meter)"])
    history = []
    if not st_gw.empty:
        tail_df = st_gw.tail(8)
        for _, hrow in tail_df.iterrows():
            date_val = str(hrow.get("Data Acquisition Time") or "")[:10]
            level_val = float(hrow["Groundwater Level Quarterly Manual (meter)"])
            history.append({"date": date_val, "level": round(level_val, 2)})
            
    stations.append({
        "name": st_name,
        "district": str(row.get("District", "Mysore")),
        "tehsil": str(row.get("Tehsil", "")),
        "block": str(row.get("Block", "")),
        "village": str(row.get("Village", "")),
        "latitude": round(float(row["Latitude"]), 6),
        "longitude": round(float(row["Longitude"]), 6),
        "monitoringDate": str(row.get("Monitoring Date", "")),
        "current": round(float(row["Current Groundwater Level (m)"]), 2),
        "predicted": round(float(row["Predicted Next Groundwater Level (m)"]), 2),
        "change": round(float(row["Predicted Groundwater Change (m)"]), 2),
        "risk": str(row["Predicted Depletion Risk"]),
        "probabilities": {
            "no": round(float(row.get("No Depletion Probability", 0)), 1),
            "low": round(float(row.get("Low Probability", 0)), 1),
            "moderate": round(float(row.get("Moderate Probability", 0)), 1),
            "high": round(float(row.get("High Probability", 0)), 1)
        },
        "history": history
    })

# Feature importances
features = []
if feats_df is not None:
    for _, row in feats_df.head(10).iterrows():
        features.append({
            "name": str(row.get("feature", "")),
            "score": round(float(row.get("importance_mean", 0)), 4)
        })

out_ts = Path("frontend/src/data/realStations.ts")
out_content = f"""// Real Station Data & Historical Records from Mysore Groundwater Dataset
export interface StationRecord {{
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
  risk: "No Depletion" | "Low" | "Moderate" | "High";
  probabilities: {{
    no: number;
    low: number;
    moderate: number;
    high: number;
  }};
  history: Array<{{ date: string; level: number }}>;
}}

export const REAL_STATIONS: StationRecord[] = {json.dumps(stations, indent=2)};

export const REAL_FEATURES = {json.dumps(features, indent=2)};
"""

out_ts.write_text(out_content, encoding="utf-8")
print(f"Exported {len(stations)} real stations and {len(features)} features to {out_ts}")
