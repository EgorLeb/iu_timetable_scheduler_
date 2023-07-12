from src.class_hierarchy.teacher import Teacher


class CourseActivity:
    """
    Data Container. To store Lecture/Tutorial
    """
    def __init__(self,
                 course_name: str,
                 course_type: str,
                 study_format: str,
                 study_year: int,
                 teacher: Teacher,
                 activity_type: str):
        """
        course_name: Official name for the course
        course_type: Full/Block1/Block2
        study_format: Online/Offline
        study_year: year of studying
        teacher: class of corresponding teacher
        activity_type: Lecture/Tutorial/Lab
        study_groups: list of all group names to study during this activity
        """
        self._course_name = course_name
        self._course_type = course_type
        self._study_year = study_year
        self._study_format = study_format
        self._teacher = teacher
        self._activity_type = activity_type
        self._study_groups = None

    def get_teacher(self):
        return self._teacher

    def get_format(self):
        return self._study_format

    def get_type(self):
        return self._course_type

    def get_study_year(self):
        return self._study_year

    def __str__(self) -> str:
        return f"{self._course_name}" \
               f"/{self._study_format}" \
               f"/{self._course_type}" \
               f"/{self._study_year}"
