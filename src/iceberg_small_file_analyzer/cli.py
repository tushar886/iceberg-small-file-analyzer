# Author: Tushar Srivastava
import argparse
from .analyzer import analyze_files
from .catalog import read_current_snapshot_files
from .report import to_json

def main():
    parser = argparse.ArgumentParser(description="Profile Iceberg data-file layout.")
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--table", required=True)
    parser.add_argument("--small-file-mb", type=int, default=128)
    parser.add_argument("--target-file-mb", type=int, default=512)
    args = parser.parse_args()
    files = read_current_snapshot_files(args.catalog, args.table)
    result = analyze_files(args.table, files,
        small_file_threshold_bytes=args.small_file_mb * 1024 * 1024,
        target_file_size_bytes=args.target_file_mb * 1024 * 1024)
    print(to_json(result))

if __name__ == "__main__":
    main()
