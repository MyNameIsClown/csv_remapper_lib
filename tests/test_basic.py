import pytest
from csv_remapper_lib import CSVFile

def test_load_csv():
    # Test loading a CSV file
    csv = CSVFile(path="tests/data/sample.csv")
    assert csv.file is not None
    csv.close_file()
    assert not csv.file

def test_load_csv_error():
    with pytest.raises(Exception) as exc_info:
        CSVFile()
    
    assert "Path to the CSV file is not provided." in str(exc_info.value)

def test_save_error():
    # Test loading a CSV file
    csv = CSVFile(path="tests/data/sample.csv")
    csv.content = None # type: ignore
    with pytest.raises(Exception) as exc_info:
        csv.save()
    assert "There is no csv data" in str(exc_info.value)

def test_check_types():
    keys_types = {
        "Item": str,
        "Category": str,
        "Quantity": int,
        "Unit Price": float,
        "Total Price": float
    }
    csv = CSVFile(path="tests/data/sample.csv")
    item_key_type = csv.type_of("Quantity")
    item_key_dict = csv.all_key_types()
    assert item_key_dict == keys_types
    assert item_key_type == int

def test_check_fail_no_keys():
    csv = CSVFile(path="tests/data/sample.csv")
    with pytest.raises(ValueError) as e:
        item_key_type = csv.type_of(12)
    assert "The key_name is missing or not a string" == str(e.value)
    csv.content_keys = None
    with pytest.raises(ValueError) as e:
        csv.all_key_types()
    assert "The header row is missing or invalid" == str(e.value)

def test_check_fail_no_content():
    csv = CSVFile(path="tests/data/sample.csv")
    csv.content = None
    with pytest.raises(ValueError) as e:
        item_key_type = csv.type_of("Quantity")
    assert "There is no CSV content" == str(e.value)
    with pytest.raises(ValueError) as e:
        item_key_dict = csv.all_key_types()
    assert "There is no CSV content" == str(e.value)