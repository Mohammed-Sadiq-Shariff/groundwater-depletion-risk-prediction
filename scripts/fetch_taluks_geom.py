import urllib.request
import urllib.parse
import json
from pathlib import Path
from shapely.geometry import LineString, Polygon, MultiPolygon, mapping
from shapely.ops import linemerge, polygonize

# We query the 9 relations by name or admin_level with out geom (much lighter, no >;)
query = """
[out:json][timeout:35];
area['name'='Mysuru District']->.a;
(
  relation['boundary'='administrative']['admin_level'='6'](area.a);
);
out geom;
"""

print("Fetching geometries with 'out geom;'...")
url = "https://overpass-api.de/api/interpreter?data=" + urllib.parse.quote(query)
req = urllib.request.Request(url, headers={"User-Agent": "MysoreGeoBuild/1.0"})

try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
except Exception as e:
    print(f"Error connecting: {e}")
    # Try alternative overpass mirror
    url = "https://overpass.kumi.systems/api/interpreter?data=" + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={"User-Agent": "MysoreGeoBuild/1.0"})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))

elements = data.get("elements", [])
print(f"Retrieved {len(elements)} relation elements with geometry.")

block_map = {
    "Heggadadevanakote taluk": ("HEGGADADEVANKOTE", "Heggadadevankote"),
    "Hunasuru taluk": ("HUNSUR", "Hunsur"),
    "Krishnarajanagara taluk": ("KRISHNARAJANAGARA", "Krishnarajanagara"),
    "Mysuru taluk": ("MYSORE", "Mysuru"),
    "Nanjanagudu taluk": ("NANJANGUD", "Nanjangud"),
    "Piriyapattana taluk": ("PIRIYAPATNA", "Piriyapatna"),
    "Tirumakudalu Narasipura taluk": ("TIRUMAKUDAL-NARSIPUR", "Tirumakudal Narsipur"),
    "Saraguru taluk": ("SARAGUR", "Saragur"),
    "Saligrama taluku": ("SALIGRAMA", "Saligrama"),
}

features = []

for el in elements:
    tags = el.get("tags", {})
    name = tags.get("name:en") or tags.get("name", "")
    
    # Match block
    matched = None
    for k, v in block_map.items():
        if k.lower() in name.lower() or name.lower() in k.lower():
            matched = v
            break
            
    if not matched:
        print(f"Skipping {name}")
        continue
        
    block_code, block_label = matched
    
    lines = []
    for m in el.get("members", []):
        if m.get("role") in ("outer", "") and "geometry" in m:
            coords = [(pt["lon"], pt["lat"]) for pt in m["geometry"]]
            if len(coords) >= 2:
                lines.append(LineString(coords))
                
    if not lines:
        print(f"No geometry lines for {name}")
        continue
        
    merged = linemerge(lines)
    polys = list(polygonize(merged))
    
    if not polys:
        print(f"Could not form closed polygon for {name}")
        continue
        
    geom = polys[0] if len(polys) == 1 else MultiPolygon(polys)
    
    features.append({
        "type": "Feature",
        "properties": {
            "block": block_code,
            "name": block_label,
            "osm_name": name,
            "center": [round(geom.centroid.y, 5), round(geom.centroid.x, 5)]
        },
        "geometry": mapping(geom)
    })
    print(f"Successfully processed {block_label} ({block_code})")

out_dir = Path("data/processed/boundaries")
out_dir.mkdir(parents=True, exist_ok=True)

if features:
    taluk_geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    with open(out_dir / "mysore_taluks.geojson", "w", encoding="utf-8") as f:
        json.dump(taluk_geojson, f, indent=2)
    print(f"Saved {len(features)} taluk boundaries to data/processed/boundaries/mysore_taluks.geojson")
