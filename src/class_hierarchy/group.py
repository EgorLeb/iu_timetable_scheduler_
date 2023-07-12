class Group:
    """
    Data Container. Represents Group with students.
    """

    def __init__(self, group_name: str, people_number: int):
        self._group_name = group_name
        self._courses = []
        self._people_number = people_number

    def get_courses(self):
        """
        return list of courses
        """
        return self._courses

    def get_name(self):
        """
        :return: str name of group
        """
        return self._group_name

    def get_people_number(self):
        """
        :return: int # of people in group
        """
        return self._people_number
