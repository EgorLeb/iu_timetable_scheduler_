"""
Validation when user enters not
'Full' or not 'Block 1' or not 'Block 2'
when entering course type
"""


class WrongCourseActivityTypeException(Exception):
    """
    raise when wrong course type provided
    """

    def __init__(self, exception_string: str, course_name: str):
        self.exception_string = exception_string
        super().__init__("You have entered not a 'Full' or 'Block 2' or 'Block 1'\n" +
                         f"Your string: {exception_string}\n" +
                         f"Course name: {course_name}")
