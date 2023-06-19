class WrongCourseActivityTypeException(Exception):
    def __init__(self, activity_type: str):
        self.activity_type = activity_type
        super().__init__(f"Provided wrong activity type: {self.activity_type}")
