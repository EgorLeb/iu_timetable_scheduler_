"""
Exception class for:
    Validation when user didn't enter preference
    for some lecture teacher
"""


class NoTeacherPreferenceException(Exception):
    """
    raise when lecture teacher
    from sheet 'Courses' don't have
    preferences
    """

    def __init__(self, teacher_name: str):
        self.teacher_name = teacher_name
        super().__init__(f"You didn't provide a preferences for {self.teacher_name}")
