from pathlib import Path
import pandas as pd

from src.class_hierarchy.course_activity import *
from src.class_hierarchy.group import *
from src.class_hierarchy.room import *
from src.class_hierarchy.exception_classes.no_teacher_preference import *
from src.class_hierarchy.exception_classes.not_a_number_provided import *
from src.class_hierarchy.exception_classes.no_such_group_exists import *
from src.class_hierarchy.exception_classes.always_no_as_preference import *
from src.class_hierarchy.exception_classes.wrong_sheet_name import *
from src.class_hierarchy.exception_classes.wrong_format_for_sport_reservation import *
from src.class_hierarchy.exception_classes.wrong_course_activity_format import *
from src.class_hierarchy.exception_classes.wrong_course_activity_type import *


class InputParser:
    """
    InputParser is class, that performs deserialization from input file.
    You only have to create new instance and then use data from input
    using getters
    """

    def __init__(self,
                 path_to_input=Path('../..').resolve() / 'input_data/Time_Table_Input.xlsx'):
        # initialize absolute path to the input file (/input_data/Time_Table_Input.xlsx)

        # initialize input file field using pandas library
        self._input_file = pd.read_excel(path_to_input, sheet_name=None)

        # declare fields that will be obtained after parsing

        self._teachers = {}
        self._groups = {}
        self._lectures = {}
        self._tutorials = {}
        self._rooms = {}
        self._sport_classes_days = []
        self._course_groups_dict = {}
        self._ta_courses_capacity = {}

        # execute parsing algorithm to read and initialize data
        self._parse()

    def get_lectures(self) -> dict:
        """
        :return:
            dict of all lectures
            key = course name
            value = CourseActivity object (/src/class_hierarchy/CourseActivity.py)
        """
        return self._lectures

    def get_tutorials(self) -> dict:
        """
        :return:
            dict of all tutorials
            key = course name
            value = CourseActivity object (/src/class_hierarchy/CourseActivity.py)
        """
        return self._tutorials

    def get_groups(self) -> dict:
        """
        :return:
            dict of all groups
            key = group name
            value = Group object (/src/class_hierarchy/Group.py)
        """
        return self._groups

    def get_teachers(self) -> dict:
        """
        :return:
            dict of all teachers
            key = teacher full name
            value = Teacher object (/src/class_hierarchy/Teacher.py)
        """
        return self._teachers

    def get_rooms(self) -> dict:
        """
        :return:
            dict of all rooms in IU
            key = room number
            value = Room object (/src/class_hierarchy/Room.py)
        """
        return self._rooms

    def get_sport_days(self) -> list:
        """
        :return:
            list of all week days when
            Elective courses on Physical
            Education are reserved
            example: ["Mon", "Tue"]
        """
        return self._sport_classes_days

    def get_ta_courses_capacity(self) -> dict:
        """
        :return:
            key = class of Teacher = TA
            value = nested dict with following:
                key = course name
                value = capacity
        """
        return self._ta_courses_capacity

    def get_course_groups_dict(self) -> dict:
        """
        :return:
            dict to store info about course and its groups to teach
            key = string name of the course
            value = list of names of groups that
                    are going to be taught during
                    this course
        """
        return self._course_groups_dict

    def _parse(self):
        """
        Doing parse of input
        :return: nothing
        """
        classes = [self._lectures, self._tutorials]
        tab_name = 'Courses'
        if tab_name not in self._input_file.keys():
            raise WrongSheetNameProvided(tab_name)
        for row in self._input_file[tab_name].values:
            course_name = row[0].strip()
            course_formats = row[1].strip().split("/")
            for c_format in course_formats:
                if c_format not in ["Offline", "Online", "-"]:
                    raise WrongCourseActivityFormat(c_format, course_name)

            course_type, study_year, prim_instructor, tut_instructor = row[2].strip(), \
                row[3], \
                row[4].strip(), \
                row[5].strip()

            if course_type not in ["Full", "Block 1", "Block 2"]:
                raise WrongCourseActivityTypeException(course_type, course_name)

            if not str(study_year).isdigit():
                raise NotANumberProvided(tab_name, course_name)
            study_year = int(study_year)

            index = 0
            for teacher_name, activity_type in \
                    zip([prim_instructor, tut_instructor], ["Lecture", "Tutorial"]):
                if teacher_name != '-':
                    if teacher_name not in self._teachers.keys():
                        self._teachers[teacher_name] = Teacher(teacher_name)

                    classes[index][course_name] = CourseActivity(course_name,
                                                                 course_type,
                                                                 course_formats[index],
                                                                 study_year,
                                                                 self._teachers[teacher_name],
                                                                 activity_type)
                index += 1

        tab_name = 'Groups Info'
        if tab_name not in self._input_file.keys():
            raise WrongSheetNameProvided(tab_name)
        for row in self._input_file[tab_name].values:
            group_name, people_num = row[0].strip(), row[1]
            if not str(people_num).isdigit():
                raise NotANumberProvided(tab_name,
                                         f"Not a course, but group: {group_name}")
            people_num = int(people_num)
            self._groups[group_name] = Group(group_name, people_num)

        tab_name = 'Course-Groups'
        if tab_name not in self._input_file.keys():
            raise WrongSheetNameProvided(tab_name)
        for row in self._input_file[tab_name].values:
            course_name = row[0].strip()
            groups = row[1].strip().split(", ")

            for group in groups:
                if group not in self._groups.keys():
                    raise NoSuchGroupExists(group, course_name)

            self._course_groups_dict[course_name] = groups

        tab_name = 'TA-Course-Groups'
        if tab_name not in self._input_file.keys():
            raise WrongSheetNameProvided(tab_name)
        for row in self._input_file[tab_name].values:

            teacher_name = row[0].strip()
            if teacher_name not in self._teachers.keys():
                self._teachers[teacher_name] = Teacher(teacher_name)

            if self._teachers[teacher_name] not in self._ta_courses_capacity:
                self._ta_courses_capacity[self._teachers[teacher_name]] = {}

            course_name = row[1].strip()
            capacity = row[2]
            if not str(capacity).isdigit():
                raise NotANumberProvided(tab_name, course_name)

            self._ta_courses_capacity[self._teachers[teacher_name]][course_name] = capacity

        tab_name = 'Rooms Info'
        if tab_name not in self._input_file.keys():
            raise WrongSheetNameProvided(tab_name)
        for index, row in enumerate(self._input_file[tab_name].values):
            room_number, capacity = row[0], row[1]
            if not str(room_number).isdigit() or not str(capacity).isdigit():
                raise NotANumberProvided(tab_name,
                                         f"Not a course, but line: {index + 2}")

            self._rooms[room_number] = Room(room_number, capacity)

        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        tab_name = 'Sport Electives Reservations'
        if tab_name not in self._input_file.keys():
            raise WrongSheetNameProvided(tab_name)
        for row in self._input_file[tab_name].values:
            for index, day in enumerate(row[1:]):
                if day == "Yes":
                    self._sport_classes_days.append(weekdays[index - 1])
                elif day != "No":
                    raise WrongFormatForSportReservation(day)

        tab_name = 'Teacher Preferences'
        if tab_name not in self._input_file.keys():
            raise WrongSheetNameProvided(tab_name)
        for row in self._input_file[tab_name].values:
            teacher_name = row[0].strip()
            teacher = self._teachers[teacher_name]
            counter = 0
            for index, day in enumerate(row):
                if day == "yes":
                    teacher.get_preferences().append(weekdays[index - 1])
                elif day == "no":
                    counter += 1

            if counter == 7:
                raise AlwaysNoAsTeacherPreference(teacher_name)

        for lec in self._lectures.values():
            teacher = lec.get_teacher()
            if not teacher.get_preferences():
                raise NoTeacherPreferenceException(teacher)


if __name__ == '__main__':
    ip = InputParser()
    print(ip.get_course_groups_dict()["Mathematical Analysis II"])
    print(ip.get_ta_courses_capacity()[ip.get_teachers()["Zlata Shchedrikova"]].keys())
