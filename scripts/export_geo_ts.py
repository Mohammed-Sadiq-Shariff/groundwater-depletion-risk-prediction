import json
from pathlib import Path

taluk_path = Path("data/processed/boundaries/mysore_taluks.geojson")
dist_path = Path("data/processed/boundaries/mysore_district.geojson")

taluks_data = json.loads(taluk_path.read_text(encoding="utf-8")) if taluk_path.exists() else {"features": []}
dist_data = json.loads(dist_path.read_text(encoding="utf-8")) if dist_path.exists() else {"features": []}

out_ts = Path("frontend/src/data/mysoreGeo.ts")
out_ts.parent.mkdir(parents=True, exist_ok=True)

ts_content = f"""// Generated Mysore District and Taluk Boundaries GeoJSON
export interface TalukFeature {{
  type: "Feature";
  properties: {{
    block: string;
    name: string;
    osm_name: string;
    center: [number, number];
  }};
  geometry: {{
    type: string;
    coordinates: any;
  }};
}}

export interface MysoreGeoData {{
  taluks: {{
    type: "FeatureCollection";
    features: TalukFeature[];
  }};
  district: any;
}}

export const MYSORE_GEOJSON: MysoreGeoData = {{
  taluks: {json.dumps(taluks_data, indent=2)},
  district: {json.dumps(dist_data, indent=2)}
}};
"""

out_ts.write_text(ts_content, encoding="utf-8")
print(f"Successfully wrote {len(taluks_data.get('features', []))} taluks to {out_ts}")
