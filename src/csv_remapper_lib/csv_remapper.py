class CSVFile:
    def __init__(self, path: str = ""):
        self.path = path
        self.file = None
        self.content = None

    def open_file(self):
        if not self.path:
            raise ValueError("Path to the CSV file is not provided.")
        with open(self.path, 'r', encoding='utf-8') as file:
            self.file = file
            self.content = file.read()
        return self.file
    
    def close_file(self):
        if self.file:
            self.file.close()
            self.file = None
    
    def replace_key(self, old_key: str, new_key: str):
        if not self.content:
            self.open_file()
        else:
            self_content = self.content.replace(old_key, new_key)
    
    
    def save(self):
        if not self.content:
            raise ValueError("File is not open.")
        # In this context, save does not perform any action as changes are saved immediately
        # after writing to the file in replace_key method.
        with open(self.path, 'w', encoding='utf-8') as file:
            file.write(self.content)
        