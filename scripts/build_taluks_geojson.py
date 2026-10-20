import urllib.request
import urllib.parse
import json
from pathlib import Path
from shapely.geometry import LineString, MultiLineString, mapping, Polygon, MultiPolygon
from shapely.ops import polygonize, linemerge

query = """
[out:json][timeout:60];
area['name'='Mysuru District']->.a;
(
  relation['boundary'='administrative'](area.a);
);
out body;
>;
out skel qt;
"""

print("Querying Overpass for Mysuru District and Taluk geometries...")
url = "https://overpass-api.de/api/interpreter?data=" + urllib.parse.quote(query)
req = urllib.request.Request(url, headers={"User-Agent": "GroundwaterDepletionBoundaryBuilder/2.0"})

with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode("utf-8"))

nodes = {}
ways = {}
relations = []

for el in data.get("elements", []):
    el_type = el.get("type")
    if el_type == "node":
        nodes[el["id"]] = (el["lon"], el["lat"])
    elif el_type == "way":
        ways[el["id"]] = [nodes[nid] for nid in el.get("nodes", []) if nid in nodes]
    elif el_type == "relation":
        relations.append(el)

print(f"Loaded {len(nodes)} nodes, {len(ways)} ways, {len(relations)} relations.")

# Mapping from OSM name to project Block key
block_map = {
    "Mysuru District": ("DISTRICT", "Mysuru District"),
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
district_features = []

for rel in relations:
    tags = rel.get("tags", {})
    name = tags.get("name:en") or tags.get("name", "")
    
    if name not in block_map:
        # Check partial matching
        matched_key = None
        for k in block_map:
            if k.lower() in name.lower() or name.lower() in k.lower():
                matched_key = k
                break
        if matched_key:
            block_code, block_label = block_map[matched_key]
        else:
            continue
    else:
        block_code, block_label = block_map[name]

    # Collect outer ways
    outer_lines = []
    for member in rel.get("members", []):
        if member.get("type") == "way" and member.get("role") in ("outer", ""):
            wid = member.get("ref")
            if wid in ways and len(ways[wid]) >= 2:
                outer_lines.append(LineString(ways[wid]))

    if not outer_lines:
        print(f"No outer lines for {name}")
        continue

    merged = linemerge(outer_lines)
    polys = list(polygonize(merged))
    
    geom = None
    if len(polys) == 1:
        geom = polys[0]
    elif len(polys) > 1:
        geom = MultiPolygon(polys)
    else:
        print(f"Polygonize failed for {name}, trying buffer...")
        # fallback
        continue

    feature = {
        "type": "Feature",
        "properties": {
            "block": block_code,
            "name": block_label,
            "osm_name": name,
            "admin_level": tags.get("admin_level"),
            "center": [geom.centroid.y, geom.centroid.x]
        },
        "geometry": mapping(geom)
    }

    if block_code == "DISTRICT":
        district_features.append(feature)
        print(f"Processed District: {name}")
    else:
        features.append(feature)
        print(f"Processed Taluk: {name} -> {block_code}")

out_dir = Path("data/processed/boundaries")
out_dir.mkdir(parents=True, exist_ok=True)

if features:
    taluk_geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    with open(out_dir / "mysore_taluks.geojson", "w", encoding="utf-8") as f:
        json.dump(taluk_geojson, f, indent=2)
    print(f"Saved {len(features)} taluk boundaries to mysore_taluks.geojson")

if district_features:
    dist_geojson = {
        "type": "FeatureCollection",
        "features": district_features
    }
    with open(out_dir / "mysore_district.geojson", "w", encoding="utf-8") as f:
        json.dump(dist_geojson, f, indent=2)
    print(f"Saved district boundary to mysore_district.geojson")
