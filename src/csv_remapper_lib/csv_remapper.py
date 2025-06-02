class CSVFile:
    def openFile(self, path: str):
        open(file=path, mode="w")