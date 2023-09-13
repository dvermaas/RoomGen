import itertools


class Level:
    def __init__(self, x, y):
        self.grid = [["[]" for i in range((2 * x + 1))] for j in range((2 * y + 1))]
        self.grid[y][x] = Room([True] * 4)

    def __str__(self):
        result = ""
        for row in self.grid:
            room_row = ""
            path_row = ""
            for location in row:
                if isinstance(location, Room):
                    if location.doors[1]:
                        room_row += "[x]-"
                    else:
                        room_row += "[x] "
                    if location.doors[2]:
                        path_row += " |  "
                    else:
                        path_row += "    "
                else:
                    room_row += "[ ] "
                    path_row += "    "
            result += room_row + "\n" + path_row + "\n"
        return result


class Room:
    def __init__(self, doors):
        self.doors = doors


level = Level(3, 3)
print(level)


# print('permutations:', list(itertools.product([False, True], repeat=4)))
