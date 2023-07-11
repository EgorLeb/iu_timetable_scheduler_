class WrongFormatForSportReservation(Exception):
    def __init__(self, exception_string: str):
        self.exception_string = exception_string
        super().__init__(f"You have entered not a 'Yes' or 'No'\n" +
                         f"Your string: {exception_string}")
