from csv_remapper_lib import CSVFile
import json, csv as csvv
import pytest

def test_convert_to_json():
    content = [
        {
            "Item": "Milk",
            "Category": "Dairy",
            "Quantity": 2,
            "Unit Price": 1.50,
            "Total Price": 3.00
        },
        {
            "Item": "Bread",
            "Category": "Bakery",
            "Quantity": 1,
            "Unit Price": 2.00,
            "Total Price": 2.00
        }
    ]

    file_path = "tests/data/conversor_test/sample.csv"
    json_file_path = "tests/data/conversor_test/sample.json"
    csv = CSVFile(file_path)
    json_content = csv.to_json()
    with open(mode="w", file=json_file_path) as json_file:
        json.dump(json_content, json_file)
    assert json_content == content
    csvv.excel

def test_convert_to_json_fail():
    file_path = "tests/data/conversor_test/sample.csv"
    json_file_path = "tests/data/conversor_test/sample.json"
    csv = CSVFile(file_path)
    csv.content = None
    with pytest.raises(ValueError) as e:
        json_content = csv.to_json()
    assert "There is no CSV data" == str(e.value)
    csvv.excel