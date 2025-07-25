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
