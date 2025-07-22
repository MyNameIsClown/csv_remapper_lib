from csv_remapper_lib import CSVFile

def test_load_csv():
    # Test loading a CSV file
    csv = CSVFile(path="tests/data/sample.csv")
    assert csv.file is not None
    csv.close_file()
    assert not csv.file
