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
    assert merge_keys not in csv.content[0]

def test_merge_keys_text_key_not_found():
    original_file_path = "tests/data/merge_test/sample.csv"
    new_file_path = "tests/data/merge_test/sample_merge_keys_text.csv"
    merge_keys = ["Surname", "Unknown key"]
    csv = CSVFile(original_file_path)
    connector = ConnectorType(MergeType.TEXT)
    csv.save(new_file_path)

def test_merge_keys_number():
    original_file_path = "tests/data/merge_test/sample.csv"
    new_file_path = "tests/data/merge_test/sample_merge_keys_number.csv"
    merge_keys = ["AnnualSalary", "BonusSalary"]
    csv = CSVFile(original_file_path)
    connector = ConnectorType(MergeType.NUMBER)
    csv.merge_keys(merge_keys, connector, "Salary", delete_old_keys=True)
    csv.save(new_file_path)

def test_merge_keys_time():
    original_file_path = "tests/data/merge_test/sample.csv"
    new_file_path = "tests/data/merge_test/sample_merge_keys_time.csv"
    merge_keys = ["RetirementDate", "HiringDate"]
    csv = CSVFile(original_file_path)
    connector = ConnectorType(MergeType.TIME, time_format="y", operator="-")
    csv.merge_keys(merge_keys, connector, "Contact days", delete_old_keys=True)
    csv.save(new_file_path)