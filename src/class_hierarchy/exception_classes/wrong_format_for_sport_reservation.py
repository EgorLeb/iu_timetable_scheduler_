"""
Validation when user enters not 'Yes'
or not 'No' when entering sport
electives reservation
"""


class WrongFormatForSportReservation(Exception):
    """
    raise when something unexpected entered in
    sheet for sport reservation
    """

    def __init__(self, exception_string: str):
        self.exception_string = exception_string
        super().__init__("You have entered not a 'Yes' or 'No'\n" +
                         f"Your string: {exception_string}")
