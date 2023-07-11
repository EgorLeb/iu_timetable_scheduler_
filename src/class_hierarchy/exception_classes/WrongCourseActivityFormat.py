class WrongCourseActivityFormat(Exception):
    def __init__(self, exception_string: str, course_name: str):
        self.exception_string = exception_string
        super().__init__(f"You have entered not a 'Offline' or 'Online' or '-'\n" +
                         f"Your string: {exception_string}\n" +
                         f"Course name: {course_name}")
