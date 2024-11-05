import random
from typing import List, Optional
import logging

OPPOSITES = {'N': "S", 'E': "W", 'S': "N", 'W': "E"}

logger = logging.getLogger(__name__)


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

        while self.queue:
            self.generate()

    def generate(self):
        choice = random.choice(self.queue)
        self.add_room(choice)

    def add_room(self, i):
        assert self.grid[i] is None
        logger.debug(f'Adding room {i}')

        doors = {direction: bool(random.getrandbits(1)) for direction in self.offsets}
        for direction, offset in self.offsets.items():
            neighbor_index = i + offset
            print(f"adding neighbor {neighbor_index} {len(self.grid) - 1}")
            if neighbor_index < 0 or neighbor_index > len(self.grid) - 1:
                logger.debug(f'Neighbor {i}out of range, skipping')
                doors[direction] = False
                continue
            neighbour = self.grid[neighbor_index]

            # Doors to neighbours that have doors are mandatory
            if neighbour is not None and neighbour.doors[OPPOSITES[direction]]:
                doors[direction] = True
            # Remove illegal doors
            if direction == 'N' and i // self.size == 0:  # Top row
                doors[direction] = False
            elif direction == 'S' and i // self.size == self.size - 1:  # Bottom row
                doors[direction] = False
            elif direction == 'E' and (i % self.size) == self.size - 1:  # Right edge
                doors[direction] = False
            elif direction == 'W' and (i % self.size) == 0:  # Left edge
                doors[direction] = False
            # Doors to nonexistent rooms should be added to the queue
            if neighbour is None and doors[direction]:
                self.queue.append(neighbor_index)

        self.grid[i] = Room(doors)
        self.queue = list(set(self.queue))
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


if __name__ == "__main__":
    level = Level(5)
    print(level)
    print(f"{level.queue=}")
    while level.queue:
        level.generate()
        print(level)
        print(f"{level.queue=}")
