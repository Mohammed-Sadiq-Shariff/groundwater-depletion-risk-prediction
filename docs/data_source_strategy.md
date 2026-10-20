# Phase 2A — data-source strategy

**Project:** AI-Based Groundwater Depletion Risk Prediction for Mysuru District, Karnataka  
**Discovery date:** 2026-08-30  
**Scope:** official-source research and metadata only. No data have been downloaded, inspected, cleaned, or modelled.

## Data requirements

The future workflow needs historical groundwater-level observations, rainfall observations, and administrative boundaries. A useful modelling dataset would require documented measurement dates, locations or administrative units, units/datums, and provenance. These requirements must be tested during acquisition; no spatial or temporal join is assumed here.

## Candidate-source comparison

| ID | Candidate | Classification | Confirmed coverage / frequency | Mysuru relevance | Machine-readable status | Decision |
|---|---|---|---|---|---|---|
| GW-01 | CGWB historical water-level data | A. observational data | National historical compilations: January 1994–2024; April/May 1994–2003, 2004–2013, 2014–2024; August 1994–2023; November 1994–2023. CGWB says four measurements per year. | Need to filter and verify after obtaining the file; NOT_VERIFIED at file level. | File format and direct URL NOT_VERIFIED from the discovered page. | **Preferred groundwater input, subject to manual file retrieval and schema/Mysuru checks.** |
| GW-02 | CGWB Karnataka Ground Water Year Book 2023–24 | B. PDF report | Karnataka; May, August, November 2023 and January 2024 groundwater-level sections. The publication record explicitly lists Mysuru. | Explicitly included in the publication record. | No; PDF report, not a raw-observation dataset. | Supporting validation/context source and backup if raw compilation cannot be obtained. |
| GW-03 | CGWB Dynamic Ground Water Resources of Karnataka 2024 | E. resource-assessment report | Karnataka 2024; taluk is the assessment unit. | Statewide report; Mysuru-specific rows require inspection. | No; PDF report. | Use only for taluk-level resource context/possible labels, not as groundwater-level time series. |
| GW-04 | India-WRIS / NWIC | C. interactive portal | Integrated water-information platform. | NOT_VERIFIED. | Download/API availability NOT_VERIFIED. | Backup discovery route; portal must be queried manually. |
| RF-01 | IMD Data Service Portal (DSP) | A. historical observational-data request service | Historical observations request form supports state, district, station, period, and month selection. | A Mysuru request appears feasible, but station availability must be checked in the portal. | Data format, years, and delivery terms TO_BE_CONFIRMED; login is required. | **Preferred rainfall route** for historical data at the best available station/district granularity. |
| RF-02 | IMD rainfall-information portal / Bengaluru MC reports | C. interactive portal and B. current report | Current daily, weekly, monthly, and cumulative district views; a discovered Bengaluru MC report lists Mysuru. | Explicit in discovered current report. | Not verified as a bulk historical download. | Operational/current reference and backup, not confirmed for historical ML data. |
| RF-03 | Karnataka OGD district-wise annual rainfall | A. machine-readable catalogue candidate / D. annual summary | Karnataka district-wise annual rainfall catalogue; publication/update shown as 2021. | File contents not inspected; Mysuru row NOT_VERIFIED. | Catalogue exposes a Zip Download and Catalog API; resource format, years, and anonymous download behaviour TO_BE_CONFIRMED. | Backup annual district-level series; likely too coarse for seasonal groundwater modelling unless coverage is adequate. |
| GIS-01 | Survey of India Administrative Boundary Database | F. geographic boundary dataset | India or state coverage up to taluk/sub-district with headquarters; Shapefile, 1:1M. | Karnataka state product should contain Mysuru only after file inspection; NOT_VERIFIED at feature level. | Shapefile is confirmed; portal has sign-in. Product is listed at ₹0. | **Preferred GIS source**, subject to portal access and post-download feature/CRS verification. |
| GIS-02 | Mysuru District Administration map page | F. official static map reference | District map and maps for Mysuru, Hunsur, H.D. Kote, Nanjangud, T. Narasipura, Piriyapatna, K.R. Nagara, Saligrama, and Saraguru are shown. | Explicit. | Static images/download links; not GIS vector data. | Boundary-name and visual QA reference only. |
| GIS-03 | NWIC Admin Boundaries on OGD | F. geographic boundary dataset candidate | Described as state, district, and block boundaries for India. | NOT_VERIFIED. | Zip Download and Catalog API are exposed; detailed contents and taluk representation TO_BE_CONFIRMED. | Backup for district-level boundary only; do not assume it meets the taluk requirement. |

## Recommended source combination

1. **Groundwater:** acquire CGWB's historical water-level compilations (GW-01) first. They are the only discovered source explicitly described as multi-decade, four-season groundwater observations. Obtain the exact files manually from the CGWB monitoring page and verify whether Mysuru wells/piezometers and usable location identifiers are present. Use Karnataka Year Books (GW-02) to cross-check reporting seasons and regional context.
2. **Rainfall:** submit/request access through IMD DSP (RF-01), asking for the precise historical period, station list, data format, units, and license/usage terms for Mysuru District. Use the Karnataka OGD annual catalogue (RF-03) only as a documented backup for annual district summaries, after checking its resource content.
3. **Boundaries:** obtain the Survey of India Karnataka state administrative-boundary product up to taluk level (GIS-01). Verify its Mysuru feature names, vintage, CRS, scale appropriateness, and access terms after download. The Mysuru district site (GIS-02) is not a vector substitute.

## Compatibility and joining considerations

No join has been validated. CGWB describes groundwater monitoring as four seasonal measurements per year, while the verified OGD rainfall candidate is annual and the IMD historical service may provide station- or district-level data only after request. The most feasible **candidate** approach is to aggregate rainfall to the same CGWB monitoring season and assign rainfall by a confirmed common spatial key:

- use a common station/location identifier only if both sources provide one; otherwise,
- spatially join confirmed groundwater coordinates to a confirmed rainfall station/grid; otherwise,
- aggregate both sources to a confirmed taluk or district unit.

This is a future acquisition/validation plan, not a modelling decision. It depends on location fields, coordinate reference systems, station density, exact observation dates, rainfall aggregation convention, and missing-data patterns that have not yet been inspected. Annual district rainfall cannot directly support four-season well-level analysis without a justified aggregation choice.

## Confirmed temporal and spatial facts

- CGWB states that it monitors water levels four times a year: March/April/May, August, November, and January. Its historical compilations are explicitly described with the date ranges listed for GW-01 above.
- CGWB Karnataka Year Book 2023–24 contains May, August, and November 2023 plus January 2024 groundwater-level sections, including shallow and deeper aquifer headings.
- The CGWB publication repository lists Karnataka yearbooks from 2013–14 onward and lists Mysuru in the Karnataka 2019–20 and 2024–25 publication records. This verifies report applicability, not individual-well rows.
- IMD's current rainfall pages expose daily, weekly, monthly, and monsoon-season cumulative district displays. The historical coverage necessary for this project has **not** been verified from the public page; DSP request/portal inspection is needed.
- The Survey of India product description confirms nationwide/state administrative boundaries to taluk level in Shapefile at 1:1M. Mysuru feature inclusion and boundary vintage require file inspection.

## Access, provenance, and legal/technical risks

- **CGWB raw data:** the official page confirms historical compilations but the discovered page did not expose a stable, directly verifiable file URL or schema. Manual retrieval and file-level provenance capture are required.
- **PDFs:** yearbooks and resource assessments are reports. Tables/maps may require PDF extraction and manual validation; they must not be silently treated as raw observations.
- **IMD DSP:** historical observations are managed through a login/request portal. Access, delivery format, pricing/terms, and exact available years/stations must be confirmed before use.
- **OGD:** catalogue pages show NDSAP/Government Open Data License information, but the exact resource licence and data content must be preserved with any downloaded file.
- **Survey of India:** the portal exposes sign-in and product terms. Check the applicable terms, dataset vintage, and geographic fitness before redistribution or publication.
- **Naming/vintage:** official pages use both Mysore and Mysuru and show a current set of taluks. Reconcile names and any administrative-boundary changes only after source inspection.

## Phase 2B acquisition checklist

1. Manually retrieve CGWB seasonal historical water-level files; save unmodified originals in the designated raw-data source directory and record exact URLs, retrieval timestamps, checksums, file formats, and file headers.
2. Verify whether the CGWB files contain Mysuru/Mysore wells or piezometers, coordinates, aquifer/depth information, observation dates, water-level units, and quality flags. Stop if not.
3. Register with/request IMD DSP historical rainfall data. Ask for a written description of station/district coverage, period, units, missing codes, data licence, and delivery format.
4. Inspect the OGD rainfall ZIP/API resource only as a small metadata/content check before deciding whether it is usable.
5. Obtain the Survey of India taluk-boundary Shapefile; inspect CRS, fields, Mysuru features, and license/terms. Do not substitute static map images for vector boundaries.
6. Update `data/metadata/source_register.csv` and add one provenance entry per actual acquired file before any cleaning.
