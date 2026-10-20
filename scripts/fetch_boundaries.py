import urllib.request
import urllib.parse
import json
import time
from pathlib import Path

out_dir = Path("data/processed/boundaries")
out_dir.mkdir(parents=True, exist_ok=True)

user_agent = "GroundwaterDepletionResearchApp/2.0 (contact: hydro@mysore-water.res)"

# 1. Fetch District Boundary
print("Fetching Mysuru District boundary...")
url = "https://nominatim.openstreetmap.org/search?q=" + urllib.parse.quote("Mysuru District Karnataka") + "&format=geojson&polygon_geojson=1"
req = urllib.request.Request(url, headers={"User-Agent": user_agent})
try:
    with urllib.request.urlopen(req) as resp:
        district_data = json.loads(resp.read().decode("utf-8"))
        features = district_data.get("features", [])
        if features:
            district_feature = features[0]
            district_geojson = {
                "type": "FeatureCollection",
                "features": [{
                    "type": "Feature",
                    "properties": {
                        "name": "Mysuru District",
                        "display_name": district_feature.get("properties", {}).get("display_name", "Mysuru District, Karnataka"),
                        "type": "district"
                    },
                    "geometry": district_feature["geometry"]
                }]
            }
            with open(out_dir / "mysore_district.geojson", "w", encoding="utf-8") as f:
                json.dump(district_geojson, f, indent=2)
            print("Successfully saved mysore_district.geojson")
        else:
            print("No features found for Mysuru District")
except Exception as e:
    print(f"Error fetching district: {e}")

time.sleep(1.2)

# 2. Fetch Taluks
taluk_queries = [
    ("MYSORE", "Mysuru taluk Karnataka"),
    ("HUNSUR", "Hunsur taluk Karnataka"),
    ("KRISHNARAJANAGARA", "Krishnarajanagara taluk Karnataka"),
    ("NANJANGUD", "Nanjangud taluk Karnataka"),
    ("PIRIYAPATNA", "Piriyapatna taluk Karnataka"),
    ("TIRUMAKUDAL-NARSIPUR", "Tirumakudal Narsipur taluk Karnataka"),
    ("HEGGADADEVANKOTE", "Heggadadevankote taluk Karnataka"),
    ("SARAGUR", "Saragur taluk Karnataka")
]

taluk_features = []

for block_id, query in taluk_queries:
    print(f"Fetching {block_id} ({query})...")
    url = "https://nominatim.openstreetmap.org/search?q=" + urllib.parse.quote(query) + "&format=geojson&polygon_geojson=1"
    req = urllib.request.Request(url, headers={"User-Agent": user_agent})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            feats = [f for f in data.get("features", []) if f.get("geometry", {}).get("type") in ("Polygon", "MultiPolygon")]
            if feats:
                feat = feats[0]
                taluk_features.append({
                    "type": "Feature",
                    "properties": {
                        "block": block_id,
                        "name": query.split(" taluk")[0],
                        "display_name": feat.get("properties", {}).get("display_name", "")
                    },
                    "geometry": feat["geometry"]
                })
                print(f"  -> Found {feat['geometry']['type']}")
            else:
                print(f"  -> No polygon found for {block_id}")
    except Exception as e:
        print(f"  -> Error: {e}")
    time.sleep(1.2)

if taluk_features:
    taluk_geojson = {
        "type": "FeatureCollection",
        "features": taluk_features
    }
    with open(out_dir / "mysore_taluks.geojson", "w", encoding="utf-8") as f:
        json.dump(taluk_geojson, f, indent=2)
    print(f"Successfully saved mysore_taluks.geojson with {len(taluk_features)} taluks!")
