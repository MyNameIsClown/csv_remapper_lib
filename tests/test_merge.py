import pytest
import re
from csv_remapper_lib import CSVFile, ConnectorType, MergeType

def test_merge_keys_not_found():
    original_file_path = "tests/data/merge_test/sample.csv"
    merge_keys = ["Surname", "Unknown key"]
    csv = CSVFile(original_file_path)
    connector = ConnectorType(MergeType.TEXT)
    with pytest.raises(ValueError) as e:
        csv.merge_keys(merge_keys, connector, "Full name", delete_old_keys=True)
    assert re.search("Keys: .+, were not found", str(e.value))

def test_merge_keys_no_keys_error():
    original_file_path = "tests/data/merge_test/sample.csv"
    merge_keys = []
    csv = CSVFile(original_file_path)
    connector = ConnectorType(MergeType.TEXT)
    with pytest.raises(ValueError) as e:
        csv.merge_keys(merge_keys, connector, "Full name", delete_old_keys=True)
    assert "Ordered key list is empty" in str(e.value)

def test_merge_keys_connector_not_correct():
    original_file_path = "tests/data/merge_test/sample.csv"
    merge_keys = ["Surname", "Name"]
    csv = CSVFile(original_file_path)
    connector = ConnectorType(type="Unknown connector")
    with pytest.raises(ValueError) as e:
        csv.merge_keys(merge_keys, connector, "Full name", delete_old_keys=True)
    assert re.search("Connector type is not valid", str(e.value))

def test_merge_keys_text():
    original_file_path = "tests/data/merge_test/sample.csv"
    new_file_path = "tests/data/merge_test/sample_merge_keys_text.csv"
    merge_keys = ["Surname", "Name"]
    csv = CSVFile(original_file_path)
    connector = ConnectorType(MergeType.TEXT)
    csv.merge_keys(merge_keys, connector, "Full name", delete_old_keys=True)
    csv.save(new_file_path)
    assert merge_keys not in csv.content[0]

def test_merge_keys_text_break_csv_with_delimiter():
    original_file_path = "tests/data/merge_test/sample.csv"
    new_file_path = "tests/data/merge_test/sample_merge_keys_text.csv"
    merge_keys = ["Surname", "Name"]
    csv = CSVFile(original_file_path)
    connector = ConnectorType(MergeType.TEXT, delimiter=", ")
    csv.merge_keys(merge_keys, connector, "Full name", delete_old_keys=True)
    csv.save(new_file_path)
    assert merge_keys not in csv.content[0]

def test_merge_keys_text_delimiter_error():
    original_file_path = "tests/data/merge_test/sample.csv"
    merge_keys = ["Surname", "Name"]
    csv = CSVFile(original_file_path)
    connector = ConnectorType(MergeType.TEXT)
    connector.delimiter = None
    with pytest.raises(ValueError) as e:
        csv.merge_keys(merge_keys, connector, "Full name", delete_old_keys=True)
    assert "Connector delimiter cannot be None for TEXT type" in str(e.value)

def test_merge_keys_number():
    original_file_path = "tests/data/merge_test/sample.csv"
    new_file_path = "tests/data/merge_test/sample_merge_keys_number.csv"
    merge_keys = ["AnnualSalary", "BonusSalary"]
    csv = CSVFile(original_file_path)
    connector = ConnectorType(MergeType.NUMBER)
    csv.merge_keys(merge_keys, connector, "Salary", delete_old_keys=True)
    csv.save(new_file_path)

def test_merge_keys_number_operator_not_found():
    original_file_path = "tests/data/merge_test/sample.csv"
    merge_keys = ["AnnualSalary", "BonusSalary"]
    csv = CSVFile(original_file_path)
    connector = ConnectorType(MergeType.NUMBER, operator="Unknown operator")
    with pytest.raises(ValueError) as e:
        csv.merge_keys(merge_keys, connector, "Salary", delete_old_keys=True)
    assert re.search("Unknown operator: .+", str(e.value))

def test_merge_keys_number_not_a_number_error():
    original_file_path = "tests/data/merge_test/sample.csv"
    merge_keys = ["AnnualSalary", "Name"]
    csv = CSVFile(original_file_path)
    connector = ConnectorType(MergeType.NUMBER)
    with pytest.raises(ValueError) as e:
        csv.merge_keys(merge_keys, connector, "Salary", delete_old_keys=True)
    assert "One value are not numbers" in str(e.value)
    # First value not a number error
    merge_keys.sort(reverse=True)
    with pytest.raises(ValueError) as e:
        csv.merge_keys(merge_keys, connector, "Salary", delete_old_keys=True)
    assert "One value are not numbers" in str(e.value)

def test_merge_keys_date_year_format():
    original_file_path = "tests/data/merge_test/sample.csv"
    new_file_path = "tests/data/merge_test/sample_merge_keys_date.csv"
    merge_keys = ["RetirementDate", "HiringDate"]
    csv = CSVFile(original_file_path)
    connector = ConnectorType(MergeType.DATE, time_format="y", operator="-")
    csv.merge_keys(merge_keys, connector, "Contact days", delete_old_keys=True)
    csv.save(new_file_path)

def test_merge_keys_date_day_format():
    original_file_path = "tests/data/merge_test/sample.csv"
    new_file_path = "tests/data/merge_test/sample_merge_keys_date.csv"
    merge_keys = ["RetirementDate", "HiringDate"]
    csv = CSVFile(original_file_path)
    connector = ConnectorType(MergeType.DATE, time_format="d", operator="-")
    csv.merge_keys(merge_keys, connector, "Contact days", delete_old_keys=True)
    csv.save(new_file_path)

def test_merge_keys_date_month_format():
    original_file_path = "tests/data/merge_test/sample.csv"
    new_file_path = "tests/data/merge_test/sample_merge_keys_date.csv"
    merge_keys = ["RetirementDate", "HiringDate"]
    csv = CSVFile(original_file_path)
    connector = ConnectorType(MergeType.DATE, time_format="m", operator="-")
    csv.merge_keys(merge_keys, connector, "Contact days", delete_old_keys=True)
    csv.save(new_file_path)

def test_merge_keys_date_regular_date_format():
    original_file_path = "tests/data/merge_test/sample.csv"
    new_file_path = "tests/data/merge_test/sample_merge_keys_date.csv"
    merge_keys = ["RetirementDate", "HiringDate"]
    csv = CSVFile(original_file_path)
    connector = ConnectorType(MergeType.DATE)
    csv.merge_keys(merge_keys, connector, "Contact days", delete_old_keys=True)
    csv.save(new_file_path)

def test_merge_keys_date_operator_not_found():
    original_file_path = "tests/data/merge_test/sample.csv"
    merge_keys = ["RetirementDate", "HiringDate"]
    csv = CSVFile(original_file_path)
    connector = ConnectorType(MergeType.DATE, time_format="y", operator="Unknown operator")
    with pytest.raises(ValueError) as e:
        csv.merge_keys(merge_keys, connector, "Salary", delete_old_keys=True)
    assert re.search("Unknown operator: .+", str(e.value))

def test_merge_keys_date_not_a_date_error():
    original_file_path = "tests/data/merge_test/sample.csv"
    merge_keys = ["RetirementDate", "Name"]
    csv = CSVFile(original_file_path)
    connector = ConnectorType(MergeType.DATE, time_format="d", operator="-")
    with pytest.raises(ValueError) as e:
        csv.merge_keys(merge_keys, connector, "Contact days", delete_old_keys=True)
    assert "One or more values are not a date" in str(e.value)

def test_merge_keys_time():
    original_file_path = "tests/data/merge_test/sample.csv"
    new_file_path = "tests/data/merge_test/sample_merge_keys_time.csv"
    merge_keys = ["WorkStartingHour", "WorkEndingHour"]
    csv = CSVFile(original_file_path)
    connector = ConnectorType(MergeType.TIME)
    csv.merge_keys(merge_keys, connector, "WorkingTime", delete_old_keys=False)
    csv.save(new_file_path)

def test_merge_keys_time_diference():
    original_file_path = "tests/data/merge_test/sample.csv"
    new_file_path = "tests/data/merge_test/sample_merge_keys_time.csv"
    merge_keys = ["WorkEndingHour", "WorkStartingHour"]
    csv = CSVFile(original_file_path)
    connector = ConnectorType(MergeType.TIME, operator="-")
    csv.merge_keys(merge_keys, connector, "WorkingTime", delete_old_keys=False)
    csv.save(new_file_path)

def test_merge_keys_time_operator_not_found():
    original_file_path = "tests/data/merge_test/sample.csv"
    merge_keys = ["WorkEndingHour", "WorkStartingHour"]
    csv = CSVFile(original_file_path)
    connector = ConnectorType(MergeType.TIME, operator="Unknown operator")
    with pytest.raises(ValueError) as e:
        csv.merge_keys(merge_keys, connector, "Salary", delete_old_keys=True)
    assert re.search("Unknown operator: .+", str(e.value))

def test_merge_keys_time_not_a_time_error_first_key():
    original_file_path = "tests/data/merge_test/sample.csv"
    merge_keys = ["WorkStartingHour", "Name"]
    csv = CSVFile(original_file_path)
    connector = ConnectorType(MergeType.TIME, operator="-")
    with pytest.raises(ValueError) as e:
        csv.merge_keys(merge_keys, connector, "Contact days", delete_old_keys=True)
    assert re.search("Invalid time isoformat string: .+", str(e.value))

def test_merge_keys_time_not_a_time_error_second_key():
    original_file_path = "tests/data/merge_test/sample.csv"
    merge_keys = ["Name", "WorkStartingHour"]
    csv = CSVFile(original_file_path)
    connector = ConnectorType(MergeType.TIME, operator="-")
    with pytest.raises(ValueError) as e:
        csv.merge_keys(merge_keys, connector, "Contact days", delete_old_keys=True)
    assert re.search("Invalid time isoformat string: .+", str(e.value))

def test_merge_keys_percentage():
    original_file_path = "tests/data/merge_test/sample.csv"
    new_file_path = "tests/data/merge_test/sample_merge_keys_percentage.csv"
    merge_keys = ["AnnualSalary", "BonusSalary"]
    csv = CSVFile(original_file_path)
    connector = ConnectorType(MergeType.PERCENTAGE)
    csv.merge_keys(merge_keys, connector, "BonusSalary%", delete_old_keys=True)
    csv.save(new_file_path)

def test_merge_keys_percentage_base_value():
    original_file_path = "tests/data/merge_test/sample.csv"
    new_file_path = "tests/data/merge_test/sample_merge_keys_percentage.csv"
    merge_keys = [10000, "BonusSalary"]
    csv = CSVFile(original_file_path)
    connector = ConnectorType(MergeType.PERCENTAGE)
    csv.merge_keys(merge_keys, connector, "BonusSalary%", delete_old_keys=True)
    csv.save(new_file_path)

def test_merge_keys_percentage_base_error_no_enought_keys():
    original_file_path = "tests/data/merge_test/sample.csv"
    merge_keys = ["BonusSalary"]
    csv = CSVFile(original_file_path)
    connector = ConnectorType(MergeType.PERCENTAGE)
    with pytest.raises(ValueError) as e:
        csv.merge_keys(merge_keys, connector, "BonusSalary%", delete_old_keys=True)
    
    assert "There are necesary only 2 keys to calculate the percentage" in str(e.value)

def test_merge_keys_percentage_base_error_at_number_conversion():
    original_file_path = "tests/data/merge_test/sample.csv"
    merge_keys = [10000, "Name"]
    csv = CSVFile(original_file_path)
    connector = ConnectorType(MergeType.PERCENTAGE)
    with pytest.raises(ValueError) as e:
        csv.merge_keys(merge_keys, connector, "BonusSalary%", delete_old_keys=True)
    
    assert re.search("Value: .+ could not be converted to number", str(e.value))