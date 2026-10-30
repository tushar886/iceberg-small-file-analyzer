# Iceberg Small File Analyzer

**Author:** Tushar Srivastava  
**Python:** 3.10+ · **Catalog access:** PyIceberg

This utility profiles the current snapshot's data-file layout and groups small files by partition. The output is intended to help an operator decide which partitions deserve a closer look before scheduling compaction.

## What it measures

- Data-file count and total bytes
- Small-file count, bytes, and ratio against a configurable threshold
- Average, p50, and p95 file size
- Per-partition file counts and size totals
- Delete-file signal exposed by the scanned data-file metadata
- Candidate file groups, kept within partition boundaries

Defaults are 128 MiB for the small-file threshold and 512 MiB for the target-size planning input. These are starting points, not universal Iceberg recommendations. Tune them for the query engine, write distribution, partition size, object store, and table properties.

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -e ".[dev]"
iceberg-small-file-analyzer --catalog prod_glue --table analytics.events
```

Configure the PyIceberg catalog and credentials using the mechanism supported by your deployment.

## How to interpret candidates

The analyzer does not combine files across partitions. It reports groups, not a Spark rewrite plan. A production compaction planner would additionally inspect delete-file applicability, sort order, partition evolution, concurrent writers, target output file count, data locality, and engine-specific rewrite semantics.

## Safety boundary

Read-only. It does not rewrite data files or manifests, change table properties, schedule Spark jobs, or delete files. It reads the current snapshot only; historical snapshot comparison is a separate concern.

## Development

```bash
ruff check .
pytest
```
