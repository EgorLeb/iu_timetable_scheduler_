from src.class_hierarchy.CourseActivity import *


class Lab(CourseActivity):
    def __init__(self,
                 course_name: str,
                 course_type: str,
                 study_format: str,
                 study_year: int,
                 teacher: Teacher,
                 activity_type: str,
                 is_joint: bool):
        super().__init__(course_name, course_type, study_format, study_year, teacher, activity_type)
        self._is_joint = is_joint

    def is_joint(self):
        return self._is_joint
