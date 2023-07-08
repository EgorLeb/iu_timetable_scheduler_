from src.class_hierarchy.exception_classes.WrongCourseActivityType import WrongCourseActivityTypeException
from src.class_hierarchy.Teacher import Teacher


class CourseActivity:
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

        if activity_type != "Lecture" and activity_type != "Tutorial" and activity_type != "Lab":
            raise WrongCourseActivityTypeException(activity_type)
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
        return f"{self._course_name}/{self._study_format}/{self._course_type}/{self._study_year}"

