class Group:

    def __init__(self, group_name: str, people_number: int):
        self._group_name = group_name
        self._courses = []
        self._people_number = people_number

    def get_courses(self):
        return self._courses

    def get_name(self):
        return self._group_name

    def get_people_number(self):
        return self._people_number
