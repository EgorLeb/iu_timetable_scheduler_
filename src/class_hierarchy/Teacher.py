class Teacher:
    def __init__(self, name: str):
        self._preferences = []
        self._name = name

    def get_preferences(self):
        return self._preferences

    def __str__(self) -> str:
        return f"Teacher object: {self._name}"
