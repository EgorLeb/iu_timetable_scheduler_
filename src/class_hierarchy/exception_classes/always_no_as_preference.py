"""
Exception class for:
    Validation for cases when user entered all 'no' in teacher preferences sheet
"""


class AlwaysNoAsTeacherPreference(Exception):
    """
    To raise when all teacher preferences are "no"
    """

    def __init__(self, teacher_name: str):
        self.teacher_name = teacher_name
        super().__init__("You entered only 'no' as teacher preference in sheet 'Teacher Preferences'" +
                         f"\nTeacher Name: {teacher_name}")
