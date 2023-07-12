class AlwaysNoAsTeacherPreference(Exception):
    def __init__(self, teacher_name: str):
        self.teacher_name = teacher_name
        super().__init__(f"You entered only 'no' as teacher preference in sheet 'Teacher Preferences'" +
                         f"\nTeacher Name: {teacher_name}")
