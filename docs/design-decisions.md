# Design Decisions

## Partition-local analysis

Compaction is generally constrained by partition and table semantics. Candidate groups therefore remain within a partition rather than aggregating small files across the table.

## Explicit thresholds

The 128 MiB small-file threshold and 512 MiB target-size input are configurable defaults. Neither is treated as universally correct.

## Read-only operation

The analyzer does not mutate Iceberg metadata or data. Planning and execution are intentionally separate responsibilities.

## Catalog adapter boundary

PyIceberg access is isolated in `catalog.py`. This keeps the statistical core deterministic and makes unit tests independent of cloud credentials.
