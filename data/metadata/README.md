# Metadata directory

This directory records discovery and provenance information for project data. It does **not** contain inferred data values or substitute for source files.

- `source_register.csv` is the controlled register of candidate and acquired sources. Unknown facts are labelled `UNKNOWN`, `NOT_VERIFIED`, or `TO_BE_CONFIRMED`.
- `source_notes/` may hold source-specific notes, licences, retrieval records, and schema observations in later phases.

## Provenance rules

Every acquired file must have a source-register entry and a corresponding record of its exact URL, organisation, title/version, publication date where applicable, retrieval date/time, licence or terms, original filename, format, and checksum. Raw data must be stored unmodified and must never be overwritten; derived files belong in `data/interim/` or `data/processed/` with a documented transformation history.

Do not mark a web page or report as an observational dataset until its actual file and schema have been inspected.
