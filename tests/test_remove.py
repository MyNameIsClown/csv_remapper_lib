from csv_remapper_lib import CSVFile
import pytest

def test_remove_key():
    key = "Quantity"
    original_file_path = "tests/data/remove_test/sample.csv"
    new_file_path = "tests/data/remove_test/sample_remove_key.csv"

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
    key = "Unknown"
    original_file_path = "tests/data/remove_test/sample.csv"

    # Creating CSVFile, replacing key and save it
    csv = CSVFile(path=original_file_path)

    with pytest.raises(Exception) as exc_info:
        csv.remove_key(key)
    
    assert "Key not found" in str(exc_info.value)

def test_remove_multiple_keys():
    keys = ["Quantity", "Category", "Total Price"]
    original_file_path = "tests/data/remove_test/sample.csv"
    new_file_path = "tests/data/remove_test/sample_remove_multiple_keys.csv"

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
    keys = ["Unknown key", "Category", "Total Price"]
    original_file_path = "tests/data/remove_test/sample.csv"

    # Creating CSVFile, replacing key and save it
    csv = CSVFile(path=original_file_path)

    with pytest.raises(Exception) as exc_info:
        csv.remove_keys(keys)
    
    assert "One or more keys not found" in str(exc_info.value)

def test_remove_keys_error_lenght():
    keys = ["Total Price"]
    original_file_path = "tests/data/remove_test/sample_remove_key_no_enought_elements.csv"

    # Creating CSVFile, replacing key and save it
    csv = CSVFile(path=original_file_path)

    with pytest.raises(Exception) as exc_info:
        csv.remove_keys(keys)
    
    assert "have not enought elemnts: Index out of range" in str(exc_info.value)