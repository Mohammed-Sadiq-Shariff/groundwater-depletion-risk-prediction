# Expected data dictionary

All fields below are **expected, not confirmed**. Actual schemas, units, definitions, and availability must be verified during data acquisition and inspection.

| Expected field | Expected role | Expected description | Status |
|---|---|---|---|
| `observation_date` | temporal key | Date or timestamp of an observation | Expected; not confirmed |
| `location_id` | spatial key | Monitoring station, well, or geographic-unit identifier | Expected; not confirmed |
| `latitude`, `longitude` | spatial attributes | Coordinate pair, including an as-yet-unconfirmed CRS | Expected; not confirmed |
| `rainfall_mm` | input | Rainfall amount for a stated period | Expected; not confirmed |
| `groundwater_level` | input/target candidate | Groundwater-level measurement with confirmed datum and units | Expected; not confirmed |
| `measurement_unit` | metadata | Unit used for rainfall or groundwater measurements | Expected; not confirmed |
| `source_name` | provenance | Agency, dataset, or provider identifier | Expected; not confirmed |
| `administrative_unit` | map attribute | Relevant local administrative area, if supplied | Expected; not confirmed |

Additional metadata such as collection method, quality flags, missing-value codes, well depth, and coordinate reference system may be necessary, subject to the acquired data.

## Confirmed concepts from official source documentation

The following are documented by official source pages or reports; they are **not a confirmed final input schema** and do not establish that a field is present in every downloadable file.

| Confirmed concept | Source context | Confirmed detail |
|---|---|---|
| Groundwater-level observation date/season | CGWB water-level monitoring | Monitoring is conducted four times yearly: January, April/May, August, and November. |
| Groundwater level | CGWB water-level monitoring | CGWB publishes historical ground-water-level data; exact file column name, datum, and unit remain TO_BE_CONFIRMED after file inspection. |
| Annual groundwater recharge | CGWB Dynamic Ground Water Resources of Karnataka 2024 | The assessment reports annual groundwater recharge at taluk assessment-unit level. |
| Annual extractable groundwater resource | CGWB Dynamic Ground Water Resources of Karnataka 2024 | Reported assessment variable. |
| Current annual groundwater extraction | CGWB Dynamic Ground Water Resources of Karnataka 2024 | Reported assessment variable. |
| Stage of groundwater extraction | CGWB Dynamic Ground Water Resources of Karnataka 2024 | Defined as annual extraction divided by annual extractable resource. |
| Assessment category | CGWB resource assessment | Categories include Safe, Semi-critical, Critical, and Over-exploited. |
| District rainfall | Karnataka OGD annual-rainfall catalogue | Catalogue describes district-wise annual rainfall in Karnataka; exact resource fields and years remain TO_BE_CONFIRMED after download inspection. |

Source discovery details and limitations are recorded in `docs/data_source_strategy.md` and `data/metadata/source_register.csv`.
