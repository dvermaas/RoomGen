import random
from typing import List, Optional

OPPOSITES = {'N': "S", 'E': "W", 'S': "N", 'W': "E"}


class Level:
    """
    Object that holds information and methods about a level.
    """
    def __init__(self, size):
        self.size: int = size
        self.grid: List[Optional[Room]] = [None] * (size * size)
        self.offsets: dict[str, int] = {'N': -size, 'E': 1, 'S': size, 'W': -1}
        self.queue: List[int] = []

        # generate starting room
        middle = (size // 2) * size + (size // 2)
        doors = {'N': True, 'E': True, 'S': True, 'W': True}
        self.grid[middle] = Room(doors)
        for direction, is_door in doors.items():
            if is_door:
                self.queue.append(middle + self.offsets[direction])

    def generate(self):
        choice = random.choice(self.queue)
        self.add_room(choice)

    def add_room(self, i):
        assert self.grid[i] is None
        print(f"adding room {i}")

        # neighbour check
        doors = {}
        for direction, offset in self.offsets.items():
            neighbor_index = i + offset
            neighbour = self.grid[neighbor_index]
            if neighbour is not None and neighbour.doors[OPPOSITES[direction]]:
                doors[direction] = True
            else:
                doors[direction] = bool(random.getrandbits(1))
                if doors[direction]:
                    self.queue.append(neighbor_index)
        self.grid[i] = Room(doors)
        self.queue.remove(i)

    def __str__(self):
        display_grid = [[" " for _ in range(2 * self.size - 1)] for _ in range(2 * self.size - 1)]

        for index, room in enumerate(self.grid):
            if room is not None:
                x, y = (index % self.size) * 2, (index // self.size) * 2
                display_grid[y][x] = "X"  # Mark room position with 'R'

                # Connect corridors based on room doors
                if room.doors['N']:
                    display_grid[y - 1][x] = "|"
                if room.doors['E']:
                    display_grid[y][x + 1] = "-"
                if room.doors['S']:
                    display_grid[y + 1][x] = "|"
                if room.doors['W']:
                    display_grid[y][x - 1] = "-"

        # Print the display grid
        return "\n".join(["".join(row) for row in display_grid])


class Room:
    def __init__(self, doors):
        self.doors = doors
        for key in OPPOSITES:
            if key not in self.doors:
                self.doors[key] = bool(random.getrandbits(1))


level = Level(5)
print(level)
print(f"{level.queue=}")
while level.queue:
    level.generate()
    print(level)
    print(f"{level.queue=}")