# Author: Tushar Srivastava
from pyiceberg.catalog import load_catalog
from .models import DataFile

def read_current_snapshot_files(catalog_name: str, table_identifier: str,
                                catalog_properties: dict[str, str] | None = None) -> tuple[DataFile, ...]:
    catalog = load_catalog(catalog_name, **(catalog_properties or {}))
    table = catalog.load_table(table_identifier)
    if table.current_snapshot() is None:
        return ()
    files = []
    for task in table.scan().plan_files():
        data_file = task.file
        partition = str(getattr(data_file, "partition", "unpartitioned"))
        files.append(DataFile(str(data_file.file_path), partition,
                              int(data_file.file_size_in_bytes),
                              int(data_file.record_count)))
    return tuple(files)
