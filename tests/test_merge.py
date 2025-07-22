from csv_remapper_lib import CSVFile, ConnectorType, MergeType
import pytest

def test_merge_keys_text():
    original_file_path = "tests/data/merge_test/sample.csv"
    new_file_path = "tests/data/merge_test/sample_merge_keys_text.csv"
    merge_keys = ["Surname", "Name"]
    csv = CSVFile(original_file_path)
    connector = ConnectorType(MergeType.TEXT)
    csv.merge_keys(merge_keys, connector, "Full name", delete_old_keys=True)
    csv.save(new_file_path)