"""
Validation for cases when user
entered wrong name of sheet in input file
"""


class WrongSheetNameProvided(Exception):
    """
    raise when some of important sheets
    in input file weren't founded
    """

    def __init__(self, sheet_name: str):
        self.sheet_name = sheet_name
        super().__init__(f"Sheet '{sheet_name}' " +
                         "was not found in provided input file")
