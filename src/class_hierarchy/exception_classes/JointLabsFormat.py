class JointLabsFormatException(Exception):

    def __init__(self, provided: str):
        self.provided = provided
        super().__init__(f"Provided wrong joint classes type: {self.provided}")
