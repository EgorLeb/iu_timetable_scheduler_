"""
Exception class for:
     Validation for cases when user entered group which
      doesn't exits in sheet 'Groups Info'
"""


class NoSuchGroupExists(Exception):
    """
    Raise when group name doesn't exist in sheet 'Groups Info'
    """

    def __init__(self, group_name: str, course_name: str):
        self.group_name = group_name
        self.course_name = course_name
        super().__init__("You have entered a group that doesn't" +
                         " exits in sheet 'Groups Info'" +
                         "Check that their names are " +
                         "completely the same!" +
                         f"\nCourse name: {course_name}" +
                         f"\nGroup Name provided: {group_name}")
