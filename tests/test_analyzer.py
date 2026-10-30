# Author: Tushar Srivastava
import pytest
from iceberg_small_file_analyzer.analyzer import analyze_files
from iceberg_small_file_analyzer.models import DataFile

def f(path, partition, size):
    return DataFile(path, partition, size, 100)

def test_candidates_are_grouped_within_partition_only():
    rows = [f("a", "day=1", 10), f("b", "day=1", 20), f("c", "day=2", 15)]
    result = analyze_files("db.events", rows, small_file_threshold_bytes=100, target_file_size_bytes=100)
    assert {x.path for x in result.candidate_files} == {"a", "b"}
    assert result.small_file_count == 3
    assert len(result.partition_profiles) == 2

def test_reports_file_size_distribution_and_partition_compaction_estimate():
    rows = [f("a", "p=1", 10), f("b", "p=1", 20), f("c", "p=2", 200)]
    result = analyze_files("db.events", rows, small_file_threshold_bytes=100)
    assert result.p50_file_bytes == 20
    assert result.p95_file_bytes == 200
    assert result.partition_profiles[0].estimated_files_avoided == 1
    assert result.small_file_ratio == pytest.approx(2 / 3)

def test_single_small_file_is_not_a_candidate():
    result = analyze_files("db.t", [f("a", "p=1", 10)], small_file_threshold_bytes=100)
    assert result.candidate_files == ()

def test_empty_table_profile():
    result = analyze_files("db.empty", [])
    assert result.file_count == 0
    assert result.small_file_ratio == 0

def test_rejects_invalid_threshold():
    with pytest.raises(ValueError):
        analyze_files("db.t", [], small_file_threshold_bytes=0)
