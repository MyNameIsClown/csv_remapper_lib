from csv_remapper_lib import *
import pytest
import os

def test_load_csv():
    # Test loading a CSV file
    csv = CSVFile(path="tests/test_data/sample.csv")
    csv.open_file()
    assert csv.file is not None
    csv.close_file()
    assert not csv.file

def test_replace_key():
    old_key = "Total price"
    new_key = "Total"
    # Test replacing a key in the CSV file
    csv = CSVFile(path="tests/test_data/sample.csv")
    csv.open_file()
    original_content = csv.content
    if csv.file is not None:
        csv.file.seek(0)  # Reset file pointer to the beginning
    csv.replace_key(old_key, new_key)
    if csv.file is not None:
        csv.file.seek(0)
    modified_content = csv.content
    assert new_key in modified_content
    assert old_key not in modified_content
    csv.close_file()
