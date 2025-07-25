import re
import operator
from enum import Enum, auto
from dateutil import parser
from datetime import datetime
from copy import deepcopy

class MergeType(Enum):
    NUMBER = auto()
    TEXT = auto()
    TIME = auto()
    PERCENTAGE = auto()

class ConnectorType:
    def __init__(self, type: MergeType, operator : str = "+", delimiter: str = " ", time_format = "") -> None:
        self.type = type
        self.operator = operator
        self.delimiter = delimiter
        self.time_format = time_format

class CSVFile:
    def __init__(self, path: str = ""):
        # Declare class variables
        self.path : str = path
        self.file = None
        self.content : list[list] = []
        self.delimiter : str = "," # Base delimiter
        self.open_file()
        
    def open_file(self):
        if not self.path:
            raise ValueError("Path to the CSV file is not provided.")
        with open(self.path, 'r', encoding='utf-8') as file:
            self.file = file
            str_content = file.read()
            # First replace float with comma, typically used on spanish alphabet, to english float numbers
            counter = 0
            spanish_float_numbers : list[str] = re.findall('"[0-9]+,[0-9]+"', str_content)
            for spanish_number in spanish_float_numbers:
                # Delete " simbol, then divide the numbers by comma. Replace the original number by new one using dot instead comma
                new_number_divided = spanish_number.replace('"', "").split(",")
                new_number = '%s.%s' % (new_number_divided[0], new_number_divided[1])
                str_content = str_content.replace(spanish_number, new_number)

            # Decompressing String info to list of lists
            for line in str_content.split("\n"):
                # To look for the delimiter of the csv file we are comparing the number of times
                # that one of each posibilities apears at keys row. It has to be 1 time less than the number of keys.
                if counter == 0:
                    posible_delimiters = {
                        ",": line.count(","),
                        ";": line.count(";"),
                        "\t": line.count("\t"),
                        "|": line.count("|"),
                        ":": line.count(":")
                    }
                    for delimiter_key in posible_delimiters.keys():
                        if posible_delimiters.get(delimiter_key) == len(line.split(delimiter_key)) - 1:
                            self.delimiter = delimiter_key
                            break
                # Adding lists of items to content splitted by calculated delimiter 
                self.content.append(line.split(self.delimiter))
                counter += 1
        return self.file
    
    def close_file(self):
        if self.file:
            self.file.close()
            self.file = None
    
    def merge_keys(self, ordered_key_list: list[str], connector: ConnectorType, new_key_name: str, delete_old_keys: bool = True) -> None:
        """
        Merges multiple columns (keys) in the CSV content into a new column using a specified connector.
        Args:
            ordered_key_list (list[str]): List of column names to merge, in the order they should be combined.
            connector (ConnectorType): The value or function used to join the column values (e.g., a string separator).
            new_key_name (str): The name of the new column that will contain the merged values.
            delete_old_keys (bool, optional): If True, the original columns will be removed after merging. Defaults to True.
        Raises:
            FileNotFoundError: If the CSV content is not loaded and cannot be opened.
            KeyError: If any of the specified keys are not found in the CSV header.
        Notes:
            - The method modifies the CSV content in place.
            - The new column is appended to the end of the header and each row.
            - If delete_old_keys is True, the original columns are removed after merging.
        """
        tmp_content = deepcopy(self.content)
        key_indexes = []

        # Add new key at the end of list
        tmp_content[0].append(new_key_name)

        # Look for index of given keys and add it to key_indexes list
        for key in ordered_key_list:
            key_index = self._found_key(key)
            if key_index != None:
                key_indexes.append(key_index)

        # Read content row by row
        for idx, row in enumerate(tmp_content):
            if idx > 0:
                new_value = ""
                for index in key_indexes:
                    # In TEXT case it concatenates all text values from keys by connector delimiter
                    # The default delimiter is space character
                    if connector.type == MergeType.TEXT:
                        if new_value == "":
                            new_value = row[index]
                        else:
                            new_value += connector.delimiter + row[index]
                    elif connector.type == MergeType.NUMBER:
                        if not isinstance(new_value, (int, float)):
                            new_value = float(row[index])
                        else:
                            ops = {
                                "+": operator.add,
                                "-": operator.sub,
                                "x": operator.mul,
                                "*": operator.mul,
                                "/": operator.truediv,
                                "//": operator.floordiv,
                                }
                            
                            fn = ops.get(connector.operator)
                            if fn is None:
                                raise ValueError(f"Operador desconocido: {connector.operator!r}")
                            new_value = fn(new_value, float(row[index]))
                    elif connector.type == MergeType.PERCENTAGE:
                        # Calculates percentage in order, starting from first key value to last one.
                        if not isinstance(new_value, (int, float)):
                            new_value = float(row[index])
                        else:
                            pass
                    elif connector.type == MergeType.TIME:
                        if not isinstance(new_value, (int, float)):
                            new_value = parser.parse(row[index]).timestamp()
                        else:
                            ops = {
                                "+": operator.add,
                                "-": operator.sub,
                                "x": operator.mul,
                                "*": operator.mul,
                                "/": operator.truediv,
                                "//": operator.floordiv,
                                }
                            
                            fn = ops.get(connector.operator)
                            if fn is None:
                                raise ValueError(f"Operador desconocido: {connector.operator!r}")
                            # Timestamp calculated date
                            new_value = fn(new_value, parser.parse(row[index]).timestamp())
                    else:
                        raise Exception("Connector type is not valid")

                # If the new value contains the CSV delimiter or a newline character,
                # it could break the CSV format. To prevent this, the new value is wrapped in double quotes.
                if connector.type == MergeType.TEXT and isinstance(new_value, str) and (self.delimiter in new_value or "\n" in new_value):
                    new_value = '"'+ new_value +'"'
                # Conversor time to selected time_format
                if connector.type == MergeType.TIME and isinstance(new_value, (int, float)):
                    if connector.time_format == "d" or connector.time_format == "D":
                        new_value = round(new_value/60/60/24, 2)
                    elif connector.time_format == "m" or connector.time_format == "M":
                        new_value = round(new_value/60/60/24/30, 2)
                    elif connector.time_format == "y" or connector.time_format == "Y":
                        new_value = round(new_value/60/60/24/30/12, 2)
                    else:
                        new_value = datetime.fromtimestamp(new_value)
                new_value = str(new_value)
                row.append(new_value)

        # Replace original content to new one
        self.content = tmp_content

        # Delete old keys
        if delete_old_keys:
            self.remove_keys(ordered_key_list)

    
    def rename_key(self, old_key: str, new_key: str):
        key_index = None

        # Found Index for matching key
        key_index = self._found_key(old_key)

        if key_index != None:
            self.content[0][key_index] = new_key
        else:
            raise Exception("Old key not found")
    
    def rename_keys(self, key_dict: dict[str, str]):
        tmp_content = deepcopy(self.content)
        for old_key in key_dict.keys():
            # Found Index for matching key
            key_index = self._found_key(old_key)
            if key_index == None:
                raise Exception("One or more key in dict not found")
                
            tmp_content[0][key_index] = key_dict.get(old_key)
        
        self.content = tmp_content

    def remove_key(self, key: str):
        
        key_index = None

        # Found Index for matching key
        key_index = self._found_key(key)

        if key_index != None:
            for row in self.content:
                row.pop(key_index)
        else:
            raise Exception("Key not found")
    
    def remove_keys(self, keys: list[str]):
        
        key_indexes = []
        for key in keys:
            key_indexes.append(self._found_key(key))
        
        if None not in key_indexes:
            # IMPORTANT: Order indexes desc to delete last items first
            key_indexes.sort(reverse=True)

            for row in self.content:
                for key in key_indexes:
                    row.pop(key)
        else:
            raise Exception("One or more keys not found")
        
    def to_positive_number(self, key: str) -> int | list[int]:
        """
        This method transforms all values of given key to positive number.
        If it were posible to transform any value then returns 0, if not then return -1 and 
        if there was errors at some values then return a list of row index, the 0 index indicates the row of the keys
        """
        key_index = self._found_key(key)
        if key_index is None:
            raise Exception("Key not found")
        error_row_indexes = []
        
        for idx, row in enumerate(self.content):
            if idx > 0:
                try:
                    value = float(row[key_index])
                    if value < 0:
                        value = value * -1
                    row[key_index] = str(value)

                except Exception as e:
                    error_row_indexes.append(idx)
        # Case no errors
        if len(error_row_indexes) == 0:
            return 0
        # Case all values error
        elif len(error_row_indexes) == len(self.content) - 1:
            return -1
        # Case some errores
        else:
            return error_row_indexes
    
    def to_negative_number(self, key: str) -> int | list[int]:
        """
        This method transforms all values of given key to negative number.
        If it were posible to transform any value then returns 0, if not then return -1 and 
        if there was errors at some values then return a list of row index, the 0 index indicates the row of the keys
        """
        key_index = self._found_key(key)
        if key_index is None:
            raise Exception("Key not found")
        error_row_indexes = []
        
        for idx, row in enumerate(self.content):
            if idx > 0:
                try:
                    value = float(row[key_index])
                    if value > 0:
                        value = value * -1
                    row[key_index] = str(value)

                except Exception as e:
                    error_row_indexes.append(idx)
        # Case no errors
        if len(error_row_indexes) == 0:
            return 0
        # Case all values error
        elif len(error_row_indexes) == len(self.content) - 1:
            return -1
        # Case some errores
        else:
            return error_row_indexes

    def to_date(self, key: str) -> int | list[int]:
        """
        This method transforms all values of given key to date.
        If it were posible to transform any value then returns 0, if not then return -1 and 
        if there was errors at some values then return a list of row index, the 0 index indicates the row of the keys
        """
        key_index = self._found_key(key)
        if key_index is None:
            raise Exception("Key not found")
        error_row_indexes = []
        
        for idx, row in enumerate(self.content):
            if idx > 0:
                try:
                    value_to_change = row[key_index]
                    new_value = str(parser.parse(value_to_change).date())
                    row[key_index] = new_value
                except parser.ParserError as e:
                    error_row_indexes.append(idx)
        # Case no errors
        if len(error_row_indexes) == 0:
            return 0
        # Case all values error
        elif len(error_row_indexes) == len(self.content) - 1:
            return -1
        # Case some errores
        else:
            return error_row_indexes

    def save(self, new_path: str = ""):
        save_path = new_path or self.path
        if not self.content:
            raise ValueError("There is no csv data")
        # In this context, save does not perform any action as changes are saved immediately
        # after writing to the file in replace_key method.
        with open(save_path, 'w', encoding='utf-8') as file:
            # Compression algorithim
            str_content = ""
            for row in self.content:
                for idx, item in enumerate(row):
                    if idx == 0:
                        str_content += item
                    else:
                        str_content += self.delimiter + item
                str_content += "\n"

            file.write(str_content)
    
    def _found_key(self, key: str = ""):
        """Found key on keys row"""
        for idx, csv_key in enumerate(self.content[0]):
            if key == csv_key:
                return idx
        return None    