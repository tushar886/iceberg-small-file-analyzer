# Architecture

The code separates catalog I/O from deterministic analysis.

- `catalog.py` loads the table through PyIceberg and materializes data-file descriptors from scan planning.
- `models.py` defines immutable input and output records.
- `analyzer.py` calculates table-wide and partition-level metrics and selects candidate groups.
- `report.py` serializes the profile.
- `cli.py` is a thin command-line adapter.

The analysis function accepts an iterable of `DataFile` records, so it can be tested without a catalog, cloud credentials, or object-store access.

## Candidate grouping

Small files are grouped by their partition identity. A candidate group is never assembled from different partitions. The output is a diagnostic shortlist, not an executable compaction plan.
