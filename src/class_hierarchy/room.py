class Room:
    """
    Data Container. All fields are public:
    room_number: int
    room_capacity: int
    """
    def __init__(self, room_number: int, room_capacity: int):
        self.room_number = room_number
        self.room_capacity = room_capacity

    def __str__(self):
        return f"Room {self.room_number}. Capacity: {self.room_capacity}."