# Author: Tushar Srivastava
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class DataFile:
    path: str
    partition: str
    size_bytes: int
    record_count: int

    def __post_init__(self):
        if self.size_bytes < 0 or self.record_count < 0:
            raise ValueError("file metrics cannot be negative")

@dataclass(frozen=True, slots=True)
class PartitionProfile:
    partition: str
    file_count: int
    total_bytes: int
    small_file_count: int
    small_file_bytes: int
    average_file_bytes: float
    candidate_bytes: int
    estimated_output_files: int
    estimated_files_avoided: int

@dataclass(frozen=True, slots=True)
class TableProfile:
    table: str
    file_count: int
    total_bytes: int
    small_file_count: int
    small_file_bytes: int
    small_file_ratio: float
    average_file_bytes: float
    p50_file_bytes: int
    p95_file_bytes: int
    partition_profiles: tuple[PartitionProfile, ...]
    candidate_files: tuple[DataFile, ...]
