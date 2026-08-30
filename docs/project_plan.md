# Project plan

This plan describes intended work. Completion of each phase depends on real data availability, inspection, and documented decisions.

1. **Phase 1 — Project setup:** establish repository structure, documentation, configuration, logging, and test skeletons.
2. **Phase 2 — Data acquisition:** obtain authorised rainfall, groundwater-level, and geographic data; record provenance, coverage, and licenses.
3. **Phase 3 — Data validation and cleaning:** inspect schemas, units, missingness, duplicates, temporal/spatial alignment, and cleaning decisions.
4. **Phase 4 — Exploratory analysis:** describe distributions, trends, relationships, and data limitations without causal overclaiming.
5. **Phase 5 — Feature engineering:** define features from confirmed data fields and prevent temporal or target leakage.
6. **Phase 6 — Baseline modeling:** implement transparent baseline(s) after the target and evaluation protocol are confirmed.
7. **Phase 7 — Model comparison:** compare suitable candidate models using a documented validation strategy.
8. **Phase 8 — Risk classification:** define Low/Medium/High classes using approved, data-supported thresholds or policy.
9. **Phase 9 — GIS visualization:** prepare geographic outputs only at the spatial resolution supported by source data.
10. **Phase 10 — Application/interface:** build a user-facing interface with explicit input limits and uncertainty communication.
11. **Phase 11 — Testing and validation:** run code, data, model, and interface checks; document limitations and failures.
12. **Phase 12 — Final documentation:** complete provenance, methodology, model card, results, and reproducibility guidance.

No phase should be represented as complete merely because its code skeleton exists.

