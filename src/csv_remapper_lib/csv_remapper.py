class CSVFile:
    def __init__(self, path: str = ""):
        # Declare class variables
        self.path : str = path
        self.file = None
        self.content : list = []
        self.delimiter : str = "," # Base delimiter
        self.open_file()
        
    def open_file(self):
        if not self.path:
            raise ValueError("Path to the CSV file is not provided.")
        with open(self.path, 'r', encoding='utf-8') as file:
            self.file = file
            str_content = file.read()
            # Decompressing String info to list of lists
            counter = 0
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
    
    def replace_key(self, old_key: str, new_key: str):
        if not self.content:
            self.open_file()

        key_index = None

        # Found Index for matching key
        for idx, key in enumerate(self.content[0]):
            if key == old_key:
                key_index = idx
                break

        if key_index != None:
            self.content[0][key_index] = new_key
        else:
            raise Exception("Old key not found")


    
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
        