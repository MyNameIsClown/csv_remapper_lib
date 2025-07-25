from csv_remapper_lib import CSVFile
import pytest

def test_to_positive_value():
    key = "Unit Price"

    original_file_path = "tests/data/transform_test/sample.csv"
    modified_file_path = "tests/data/transform_test/sample_positive_number.csv"

    csv = CSVFile(original_file_path)
    result = csv.to_positive_number(key)
    csv.save(modified_file_path)

    assert result == 0

def test_to_positive_value_key_not_found():
    key = "Unknown key"
    original_file_path = "tests/data/transform_test/sample.csv"
    csv = CSVFile(original_file_path)
    with pytest.raises(Exception) as exc_info:
        csv.to_positive_number(key)
    assert "Key not found" in str(exc_info.value)

def test_to_positive_value_half_error():
    test_csv_path = "tests/data/transform_test/sample_errors.csv"
    csv = CSVFile(test_csv_path)
    # Should process rows with missing/invalid values, but not raise if at least one is valid
    result = csv.to_positive_number("Unit Price")
    assert type(result) is list
    assert len(result) == 1

def test_to_positive_value_full_name():
    test_csv_path = "tests/data/transform_test/sample_errors.csv"
    csv = CSVFile(test_csv_path)
    # Should process rows with missing/invalid values, but not raise if at least one is valid
    result = csv.to_positive_number("Product Name")
    assert result == -1

def test_to_negative_value():
    key = "Unit Price"

    original_file_path = "tests/data/transform_test/sample.csv"
    modified_file_path = "tests/data/transform_test/sample_negative_number.csv"

    csv = CSVFile(original_file_path)
    result = csv.to_negative_number(key)
    csv.save(modified_file_path)

    assert result == 0
    
def test_to_negative_value_key_not_found():
    key = "Unknown key"
    original_file_path = "tests/data/transform_test/sample.csv"
    csv = CSVFile(original_file_path)
    with pytest.raises(Exception) as exc_info:
        csv.to_negative_number(key)
    assert "Key not found" in str(exc_info.value)

def test_to_negative_value_half_error():
    test_csv_path = "tests/data/transform_test/sample_errors.csv"
    csv = CSVFile(test_csv_path)
    # Should process rows with missing/invalid values, but not raise if at least one is valid
    result = csv.to_negative_number("Unit Price")
    assert type(result) is list
    assert len(result) == 1

def test_to_negative_value_full_error():
    test_csv_path = "tests/data/transform_test/sample_errors.csv"
    csv = CSVFile(test_csv_path)
    # Should process rows with missing/invalid values, but not raise if at least one is valid
    result = csv.to_negative_number("Product Name")
    assert result == -1


def test_to_date_value():
    key = "Fecha de compra"

    original_file_path = "tests/data/transform_test/sample_date.csv"
    modified_file_path = "tests/data/transform_test/new_sample_date.csv"

    csv = CSVFile(original_file_path)
    result = csv.to_date(key)
    csv.save(modified_file_path)

    assert result == 0
    
def test_to_date_value_key_not_found():
    key = "Unknown key"
    original_file_path = "tests/data/transform_test/sample_date.csv"
    csv = CSVFile(original_file_path)
    with pytest.raises(Exception) as exc_info:
        csv.to_date(key)
    assert "Key not found" in str(exc_info.value)

def test_to_date_value_half_error():
    key = "Fecha de compra"
    test_csv_path = "tests/data/transform_test/sample_date_errors.csv"
    csv = CSVFile(test_csv_path)
    # Should process rows with missing/invalid values, but not raise if at least one is valid
    result = csv.to_date(key)
    assert type(result) is list
    assert len(result) == 3

def test_to_date_value_full_error():
    key = "Nombre del producto"
    test_csv_path = "tests/data/transform_test/sample_date_errors.csv"
    csv = CSVFile(test_csv_path)
    # Should process rows with missing/invalid values, but not raise if at least one is valid
    result = csv.to_date(key)
    assert result == -1