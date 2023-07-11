class NotANumberProvided(Exception):
    def __init__(self, tab_name: str, course_name: str):
        self.tab_name = tab_name
        self.course_name = course_name
        super().__init__(f"You entered not a number!" +
                         f"\nSheet Name: {tab_name}\nCourse Name: {course_name}")
