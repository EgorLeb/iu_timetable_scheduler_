"""
Validation for cases when
user entered not a number when needed
"""


class NotANumberProvided(Exception):
    """
    raise when in input file expected integer,
    but provided something else
    """

    def __init__(self, tab_name: str, course_name: str):
        self.tab_name = tab_name
        self.course_name = course_name
        super().__init__("You entered not a number!" +
                         f"\nSheet Name: {tab_name}\n" +
                         f"Course Name: {course_name}")
