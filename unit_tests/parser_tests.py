import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).parents[1].resolve()))

from src.input_parsing.parser_algorithm import InputParser


class TestInputParser(unittest.TestCase):

    def test_parse_lectures(self):
        path = Path('../').resolve() / 'input_data/Time_Table_Input.xlsx'
        ip = InputParser(path_to_input=path)
        lectures = ip.get_lectures()
        tutorials = ip.get_tutorials()

        # checks that lectures and tutorials are not empty
        self.assertTrue(lectures)

        for class_obj in list(lectures.values()) + list(tutorials.values()):
            # checks that each parsed lecture and tutorial has teacher
            self.assertIsNotNone(class_obj.get_teacher())
            # checks that each parsed lecture either online either offline
            self.assertIn(class_obj.get_format(), ["Online", "Offline"])

    def test_parse_groups(self):
        path = Path('../').resolve() / 'input_data/Time_Table_Input.xlsx'
        ip = InputParser(path_to_input=path)

        groups = ip.get_groups()

        # checks that dict of all groups is not empty
        self.assertTrue(groups)

        # checks that key = name of group equals its value's field of parsed name
        for group_name, group in groups.items():
            self.assertEqual(group_name, group.get_name())

    def test_parse_rooms(self):
        path = Path('../').resolve() / 'input_data/Time_Table_Input.xlsx'
        ip = InputParser(path_to_input=path)

        rooms = ip.get_rooms()

        # checks that auditoriums are not empty
        self.assertTrue(rooms)

        # checks that key = number of room equals its value's field of parsed number
        for room_number, room in rooms.items():
            self.assertEqual(room_number, room.room_number)

    def test_parse_sport_days(self):
        path = Path('../').resolve() / 'input_data/Time_Table_Input.xlsx'
        ip = InputParser(path_to_input=path)

        sport_days = ip.get_sport_days()

        # Check that the list of days for physical education is not empty
        self.assertTrue(sport_days)

        # Check that chosen days are exists
        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for day in sport_days:
            self.assertIn(day, weekdays)

    def test_parse_teacher_preferences(self):
        path = Path('../').resolve() / 'input_data/Time_Table_Input.xlsx'
        ip = InputParser(path_to_input=path)

        teachers = ip.get_teachers()
        lectures = ip.get_lectures()

        # Check that the list of teachers is not empty
        self.assertTrue(teachers)

        # Check that all lecture instructors have these preferences
        for lec in lectures.values():
            teacher = lec.get_teacher()
            preferences = teacher.get_preferences()
            self.assertTrue(preferences)
            self.assertTrue(all(isinstance(day, str) for day in preferences))


if __name__ == '__main__':
    unittest.main()
