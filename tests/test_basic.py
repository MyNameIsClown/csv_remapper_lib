from csv_remapper_lib import *
import pytest
import os

def test_load_csv():
    # Test loading a CSV file
    csv = CSVFile(path="tests/test_data/sample.csv")
    assert csv.file is not None
    csv.close_file()
    assert not csv.file

def test_replace_key():
    old_key = "Total Price"
    new_key = "Total"
    original_file_path = "tests/test_data/sample_2.csv"
    new_file_path = "tests/test_data/sample_new.csv"

    # Creating CSVFile, replacing key and save it
    csv = CSVFile(path=original_file_path)
    
    with open(original_file_path, "r") as f:
        original_content = f.read()

    csv.rename_key(old_key, new_key)
    csv.save(new_file_path)

    # Open new file and compare contents
    with open(new_file_path, "r") as f:
        modified_content = f.read()
    
    assert original_content is not None and old_key in original_content
    assert modified_content is not None and new_key in modified_content
    assert original_content != modified_content
    csv.close_file()

def test_replace_key_error():
    old_key = "Total Pricing"
    new_key = "Total"
    original_file_path = "tests/test_data/sample_2.csv"

    # Creating CSVFile, replacing key and save it
    csv = CSVFile(path=original_file_path)
    
    with open(original_file_path, "r") as f:
        original_content = f.read()

    with pytest.raises(Exception) as exc_info:
        csv.rename_key(old_key, new_key)
    
    assert "Old key not found" in str(exc_info.value)

def test_remove_key():
    key = "Quantity"
    original_file_path = "tests/test_data/sample_2.csv"
    new_file_path = "tests/test_data/sample_new.csv"

    # Creating CSVFile, replacing key and save it
    csv = CSVFile(path=original_file_path)
    
    with open(original_file_path, "r") as f:
        original_content = f.read()

    csv.remove_key(key)
    csv.save(new_file_path)

    # Open new file and compare contents
    with open(new_file_path, "r") as f:
        modified_content = f.read()
    
    assert original_content is not None and key in original_content
    assert modified_content is not None and key not in modified_content
    assert original_content != modified_content
    csv.close_file()


def test_remove_key_error():
    key = "Biscuit"
    original_file_path = "tests/test_data/sample_2.csv"

    # Creating CSVFile, replacing key and save it
    csv = CSVFile(path=original_file_path)

    with pytest.raises(Exception) as exc_info:
        csv.remove_key(key)
    
    assert "Key not found" in str(exc_info.value)

def test_remove_multiple_keys():
    keys = ["Quantity", "Category", "Total Price"]
    original_file_path = "tests/test_data/sample_2.csv"
    new_file_path = "tests/test_data/sample_new.csv"

    # Creating CSVFile, replacing key and save it
    csv = CSVFile(path=original_file_path)
    
    with open(original_file_path, "r") as f:
        original_content = f.read()

    csv.remove_keys(keys)
    csv.save(new_file_path)

    # Open new file and compare contents
    with open(new_file_path, "r") as f:
        modified_content = f.read()
    
    assert original_content is not None 
    for key in keys:
        assert key in original_content
    assert modified_content is not None
    for key in keys:
        assert key not in modified_content
    assert original_content != modified_content
    csv.close_file()

def test_remove_keys_error():
    keys = ["Wall", "Category", "Total Price"]
    original_file_path = "tests/test_data/sample_2.csv"

    # Creating CSVFile, replacing key and save it
    csv = CSVFile(path=original_file_path)

    with pytest.raises(Exception) as exc_info:
        csv.remove_keys(keys)
    
    assert "One or more keys not found" in str(exc_info.value)