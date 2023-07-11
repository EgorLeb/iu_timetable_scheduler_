class NoSuchGroupExists(Exception):
    def __init__(self, group_name: str, course_name: str):
        self.group_name = group_name
        self.course_name = course_name
        super().__init__(f"You have entered a group that doesn't exits in sheet 'Groups Info'" +
                         f"Check that their names are completely the same!" +
                         f"Course name: {course_name}\nGroup Name provided: {group_name}")
