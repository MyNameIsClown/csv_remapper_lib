from csv_remapper_lib import CSVFile
import pytest

def test_rename_key():
    old_key = "Total Price"
    new_key = "Total"
    original_file_path = "tests/data/rename_test/sample.csv"
    new_file_path = "tests/data/rename_test/sample_test_rename_key.csv"

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

def test_rename_key_error():
    old_key = "Unknown Key"
    new_key = "Total"
    original_file_path = "tests/data/rename_test/sample.csv"

    # Creating CSVFile, replacing key and save it
    csv = CSVFile(path=original_file_path)
    
    with pytest.raises(Exception) as exc_info:
        csv.rename_key(old_key, new_key)
    
    assert "Old key not found" in str(exc_info.value)

def test_rename_keys():
    keys = {
        "Total Price": "Total",
        "Item": "Product Name",
        "Quantity": "Quantities"
    }
    original_file_path = "tests/data/rename_test/sample.csv"
    new_file_path = "tests/data/rename_test/sample_rename_keys.csv"

    # Creating CSVFile, replacing key and save it
    csv = CSVFile(path=original_file_path)
    
    with open(original_file_path, "r") as f:
        original_content = f.read()

    csv.rename_keys(keys)
    csv.save(new_file_path)

    # Open new file and compare contents
    with open(new_file_path, "r") as f:
        modified_content = f.read()
    
    assert original_content is not None
    assert modified_content is not None

    for old_key in keys.keys():
        assert old_key in original_content
        assert old_key not in modified_content
        assert keys.get(old_key) in modified_content # type: ignore

    assert original_content != modified_content
    csv.close_file()

def test_rename_keys_error():
    keys = {
        "Unknown Key": "Total",
        "Item": "Product Name",
        "Quantity": "Quantities"
    }
    original_file_path = "tests/data/rename_test/sample.csv"

    # Creating CSVFile, replacing key and save it
    csv = CSVFile(path=original_file_path)
    
    with open(original_file_path, "r") as f:
        original_content = f.read()

    with pytest.raises(Exception) as exc_info:
        csv.rename_keys(keys)
    
    assert "One or more key in dict not found" in str(exc_info.value)