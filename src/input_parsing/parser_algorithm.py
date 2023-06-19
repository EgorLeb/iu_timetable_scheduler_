from src.class_hierarchy.Lab import *
from src.class_hierarchy.Group import *
from src.class_hierarchy.exception_classes.JointLabsFormat import *
from src.class_hierarchy.Room import *

import pandas as pd
from pathlib import Path


class InputParser:
    def __init__(self):
        # initialize absolute path to the input file (/input_data/Time_Table_Input.xlsx)
        path_to_input = Path('../..').resolve() / 'input_data/Time_Table_Input.xlsx'

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
        !!!! TO GET ACCESS FOR GROUP'S LAB IN DICTIONARY:
        dict of all labs
        key = course name + GROUP_NAME (labs[course_name + group.get_name()])
        value = Lab object inherited from CourseActivity class (/src/class_hierarchy/Lab.py)
        """
        self._labs = {}
        """
        dict of all rooms in IU
        key = room number
        value = Room object (/src/class_hierarchy/Room.py)
        """
        self._rooms = {}
        """
        list of all week days where Elective courses on Physical Education are reserved
        example: ["Mon", "Tue"]
        """
        self._sport_classes_days = []

        # execute parsing algorithm to read and initialize data
        self._parse()

    def get_lectures(self):
        return self._lectures

    def get_tutorials(self):
        return self._tutorials

    def get_labs(self):
        return self._labs

    def get_groups(self):
        return self._groups

    def get_teachers(self):
        return self._teachers

    def get_rooms(self):
        return self._rooms

    def get_sport_days(self):
        return self._sport_classes_days

    def _parse(self):
        classes = [self._lectures, self._tutorials, self._labs]
        for row in self._input_file['Courses'].values:
            course_name = row[0].strip()
            course_formats = row[1].split("/")
            course_type, study_year, prim_instructor, tut_instructor = row[2].strip(), \
                int(row[3]), \
                row[4].strip(), \
                row[5].strip()

            index = 0
            for teacher_name, activity_type in \
                    zip([prim_instructor, tut_instructor], ["Lecture", "Tutorial"]):
                if teacher_name != '-':
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

        for row in self._input_file['Group-TA'].values:
            group = self._groups[row[0].strip()]
            course_name, teacher_name, course_format = row[1].strip(), row[2].strip(), row[3].strip()
            is_joint = row[4]
            if is_joint == "No":
                is_joint = False
            elif is_joint == "Yes":
                is_joint = True
            else:
                raise JointLabsFormatException(is_joint)

            self._teachers[teacher_name] = Teacher(teacher_name)

            self._labs[course_name + group.get_name()] = Lab(
                course_name,
                self._lectures[course_name].get_type(),
                course_format,
                self._lectures[course_name].get_study_year(),
                self._teachers[teacher_name],
                "Lab",
                is_joint
            )

            group.get_courses().append(course_name)

        for row in self._input_file['Rooms Info'].values:
            room_number, capacity = row[0], row[1]
            self._rooms[room_number] = Room(room_number, capacity)

        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        for row in self._input_file['Sport Electives Reservations'].values:
            for index, day in enumerate(row):
                if day == "Yes":
                    self._sport_classes_days.append(weekdays[index - 1])

        for row in self._input_file['Teacher Preferences'].values:
            teacher = self._teachers[row[0].strip()]
            for index, day in enumerate(row):
                if day == "yes":
                    teacher.get_preferences().append(weekdays[index - 1])


pd = InputParser()
print(pd.get_labs()["Theoretical Computer Science / Теоретические основы компьютерных наук" + "B22-DSAI-01"].get_teacher())