from src.class_hierarchy.CourseActivity import *
from src.class_hierarchy.Group import *
from src.class_hierarchy.Room import *
from src.class_hierarchy.exception_classes.NoTeacherPreference import *

import pandas as pd
from pathlib import Path


class InputParser:
    def __init__(self,
                 path_to_input=Path('../..').resolve() / 'input_data/Time_Table_Input.xlsx'):
        # initialize absolute path to the input file (/input_data/Time_Table_Input.xlsx)

        # initialize input file field using pandas library
        self._input_file = pd.read_excel(path_to_input, sheet_name=None)

        # declare fields that will be obtained after parsing
        """
        dict of all teachers
        key = teacher full name
        value = Teacher object (/src/class_hierarchy/Teacher.py)
        """
        self._teachers = {}
        """
        dict of all groups
        key = group name
        value = Group object (/src/class_hierarchy/Group.py)
        """
        self._groups = {}
        """
        dict of all lectures
        key = course name
        value = CourseActivity object (/src/class_hierarchy/CourseActivity.py)
        """
        self._lectures = {}
        """
        dict of all tutorials
        key = course name
        value = CourseActivity object (/src/class_hierarchy/CourseActivity.py)
        """
        self._tutorials = {}

        """
        dict of all rooms in IU
        key = room number
        value = Room object (/src/class_hierarchy/Room.py)
        """
        self._rooms = {}
        """
        list of all block1 days where Elective courses on Physical Education are reserved
        example: ["Mon", "Tue"]
        """
        self._sport_classes_days = []

        """
        NEW CHANGE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        dict to store info about course and its groups to teach
        key = string name of the course
        value = list of names of groups that are going to be taught during this course
        """
        self._course_groups_dict = {}

        """
        NEW CHANGE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        key = class of Teacher = TA
            value = nested dict with following:
                key = course name
                value = capacity
        """
        self._ta_courses_capacity = {}

        # execute parsing algorithm to read and initialize data
        self._parse()

    def get_lectures(self):
        return self._lectures

    def get_tutorials(self):
        return self._tutorials

    def get_groups(self):
        return self._groups

    def get_teachers(self):
        return self._teachers

    def get_rooms(self):
        return self._rooms

    def get_sport_days(self):
        return self._sport_classes_days

    def get_ta_courses_capacity(self) -> dict:
        return self._ta_courses_capacity

    def get_course_groups_dict(self) -> dict:
        return self._course_groups_dict

    def _parse(self):
        classes = [self._lectures, self._tutorials]
        for row in self._input_file['Courses'].values:
            course_name = row[0].strip()
            course_formats = row[1].strip().split("/")
            course_type, study_year, prim_instructor, tut_instructor = row[2].strip(), \
                int(row[3]), \
                row[4].strip(), \
                row[5].strip()

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

        for row in self._input_file['Groups Info'].values:
            group_name, people_num = row[0].strip(), int(row[1])
            self._groups[group_name] = Group(group_name, people_num)

        for row in self._input_file['Course-Groups'].values:
            course_name = row[0].strip()
            groups = row[1].strip().split(", ")
            self._course_groups_dict[course_name] = groups

        for row in self._input_file['TA-Course-Groups'].values:

            teacher_name = row[0].strip()
            if teacher_name not in self._teachers.keys():
                self._teachers[teacher_name] = Teacher(teacher_name)

            if self._teachers[teacher_name] not in self._ta_courses_capacity:
                self._ta_courses_capacity[self._teachers[teacher_name]] = {}

            course_name = row[1].strip()
            capacity = row[2]
            self._ta_courses_capacity[self._teachers[teacher_name]][course_name] = capacity

        for row in self._input_file['Rooms Info'].values:
            room_number, capacity = row[0], row[1]
            self._rooms[room_number] = Room(room_number, capacity)

        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        for row in self._input_file['Sport Electives Reservations'].values:
            for index, day in enumerate(row):
                if day == "Yes":
                    self._sport_classes_days.append(weekdays[index - 1])

        for row in self._input_file['Teacher Preferences'].values:
            teacher_name = row[0].strip()

            teacher = self._teachers[row[0].strip()]
            for index, day in enumerate(row):
                if day == "yes":
                    teacher.get_preferences().append(weekdays[index - 1])

        for lec in self._lectures.values():
            teacher = lec.get_teacher()
            if not teacher.get_preferences():
                raise NoTeacherPreferenceException(teacher)


if __name__ == '__main__':
    ip = InputParser()
    print(ip.get_course_groups_dict()["Mathematical Analysis II"])
    print(ip.get_ta_courses_capacity()[ip.get_teachers()["Zlata Shchedrikova"]].keys())
