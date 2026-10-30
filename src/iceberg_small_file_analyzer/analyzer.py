# Author: Tushar Srivastava
from collections import defaultdict
from collections.abc import Iterable
from math import ceil
from statistics import median
from .models import DataFile, PartitionProfile, TableProfile

def _nearest_rank(values: list[int], percentile: float) -> int:
    if not values:
        return 0
    ordered = sorted(values)
    return ordered[max(0, ceil(percentile * len(ordered)) - 1)]

def analyze_files(table: str, files: Iterable[DataFile], *,
                  small_file_threshold_bytes: int = 128 * 1024 * 1024,
                  target_file_size_bytes: int = 512 * 1024 * 1024,
                  min_files_per_candidate: int = 2) -> TableProfile:
    if small_file_threshold_bytes <= 0 or target_file_size_bytes <= 0:
        raise ValueError("file-size thresholds must be positive")
    if min_files_per_candidate < 2:
        raise ValueError("min_files_per_candidate must be at least 2")

    materialized = tuple(files)
    sizes = [f.size_bytes for f in materialized]
    small = tuple(f for f in materialized if f.size_bytes < small_file_threshold_bytes)
    by_partition = defaultdict(list)
    for f in small:
        by_partition[f.partition].append(f)

    partition_profiles = []
    candidates = []
    for partition, partition_files in sorted(by_partition.items()):
        total = sum(f.size_bytes for f in partition_files)
        # Only recommend a partition-local group; never combine files across partitions.
        estimated_outputs = (total + target_file_size_bytes - 1) // target_file_size_bytes
        files_avoided = max(0, len(partition_files) - estimated_outputs)
        if len(partition_files) >= min_files_per_candidate and files_avoided > 0:
            candidates.extend(partition_files)
        all_partition = [f for f in materialized if f.partition == partition]
        partition_profiles.append(PartitionProfile(
            partition=partition,
            file_count=len(all_partition),
            total_bytes=sum(f.size_bytes for f in all_partition),
            small_file_count=len(partition_files),
            small_file_bytes=total,
            average_file_bytes=(sum(f.size_bytes for f in all_partition) / len(all_partition)),
            candidate_bytes=total if files_avoided > 0 else 0,
            estimated_output_files=estimated_outputs,
            estimated_files_avoided=files_avoided,
        ))

    total_bytes = sum(sizes)
    return TableProfile(
        table=table, file_count=len(materialized), total_bytes=total_bytes,
        small_file_count=len(small), small_file_bytes=sum(f.size_bytes for f in small),
        small_file_ratio=(len(small) / len(materialized)) if materialized else 0.0,
        average_file_bytes=(total_bytes / len(sizes)) if sizes else 0.0,
        p50_file_bytes=int(median(sizes)) if sizes else 0,
        p95_file_bytes=_nearest_rank(sizes, .95),
        partition_profiles=tuple(partition_profiles),
        candidate_files=tuple(candidates),
    )
