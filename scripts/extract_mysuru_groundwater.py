from pathlib import Path
import re
import pandas as pd
import fitz  # PyMuPDF

PDF = Path("data/raw/groundwater/January_WL_1994-2025.pdf")
OUT = Path("data/interim/groundwater/mysuru_january_groundwater_1994_2025.csv")

OUT.parent.mkdir(parents=True, exist_ok=True)

records = []
doc = fitz.open(PDF)

for page_no in range(doc.page_count):
    lines = [
        line.strip()
        for line in doc.load_page(page_no).get_text("text").splitlines()
        if line.strip()
    ]

    i = 0
    while i <= len(lines) - 8:
        if lines[i] == "Karnataka" and lines[i + 1] == "Mysuru":
            state, district, block, village, lat, lon, date_raw, wl = lines[i:i + 8]
            try:
                float(lat)
                float(lon)
                float(wl)
                valid_date = bool(re.fullmatch(r"\d{2}-\d{2}-\d{2}", date_raw))
            except ValueError:
                valid_date = False

            if valid_date:
                records.append(
                    {
                        "State": state,
                        "District": district,
                        "Block": block,
                        "Village": village,
                        "Latitude": float(lat),
                        "Longitude": float(lon),
                        "Date_raw": date_raw,
                        "WL_mbgl": float(wl),
                        "source_page": page_no + 1,
                    }
                )
                i += 8
                continue
        i += 1

df = pd.DataFrame(records)
df["Date"] = pd.to_datetime(df["Date_raw"], format="%d-%m-%y", errors="raise")
df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")

if df.empty:
    raise RuntimeError("No Mysuru rows were extracted.")

if df.isna().any().any():
    raise RuntimeError("Missing values found in extracted output.")

if df.duplicated(
    subset=["State", "District", "Block", "Village", "Latitude", "Longitude", "Date_raw", "WL_mbgl"]
).any():
    raise RuntimeError("Exact duplicate rows found; inspect before continuing.")

df.to_csv(OUT, index=False)
print(f"Wrote {len(df)} records to {OUT}")
