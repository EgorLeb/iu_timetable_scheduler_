class Teacher:
    """
    Data container.
    Represents teacher (Lecturer, Prim. Inst. or TA)
    """
    def __init__(self, name: str):
        self._preferences = []
        self._name = name

    def get_preferences(self):
        """
        :return: list of days, where teacher can teach
        """
        return self._preferences

    def __str__(self) -> str:
        return f"Teacher object: {self._name}"
