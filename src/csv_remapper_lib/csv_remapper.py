import re
from copy import deepcopy

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
    
    def rename_key(self, old_key: str, new_key: str):
        if not self.content:
            self.open_file()

        key_index = None

        # Found Index for matching key
        key_index = self._found_key(old_key)

        if key_index != None:
            self.content[0][key_index] = new_key
        else:
            raise Exception("Old key not found")
    
    def rename_keys(self, key_dict: dict[str, str]):
        if not self.content:
            self.open_file()

        tmp_content = deepcopy(self.content)
        for old_key in key_dict.keys():
            # Found Index for matching key
            key_index = self._found_key(old_key)
            if key_index == None:
                raise Exception("One or more key in dict not found")
                
            tmp_content[0][key_index] = key_dict.get(old_key)
        
        self.content = tmp_content

    def remove_key(self, key: str):
        if not self.content:
            self.open_file()
        
        key_index = None

        # Found Index for matching key
        key_index = self._found_key(key)

        if key_index != None:
            for row in self.content:
                row.pop(key_index)
        else:
            raise Exception("Key not found")
    
    def remove_keys(self, keys: list[str]):
        if not self.content:
            self.open_file()
        
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



    def save(self, new_path: str = ""):
        save_path = new_path or self.path
        if not self.content:
            raise ValueError("File is not open.")
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