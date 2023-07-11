class WrongSheetNameProvided(Exception):
    def __init__(self, sheet_name: str):
        self.sheet_name = sheet_name
        super().__init__(f"Sheet '{sheet_name}' was not found in provided input file")
