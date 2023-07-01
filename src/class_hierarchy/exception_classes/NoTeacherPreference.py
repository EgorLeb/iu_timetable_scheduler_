class NoTeacherPreferenceException(Exception):
    def __init__(self, teacher_name: str):
        self.teacher_name = teacher_name
        super().__init__(f"You didn't provide a preferences for {self.teacher_name}")
