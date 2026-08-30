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

