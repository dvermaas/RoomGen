import random


class Level:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.grid = [None for i in range(x * y)]
        self.room_coords = [-x, +1, x, -1]
        centre = int(self.x//2 + self.x * (self.y//2))
        self.room_expansion_set = set()
        self.grid[centre] = Room(self, centre, [True, True, True, True], icon="X")
        print("centre", centre)
        self.add_room()

    def add_room(self):
        new_room_index = random.sample(list(self.room_expansion_set), 1)[0]
        self.room_expansion_set.remove(new_room_index)
        x = self.x
        doors = [False] * 4
        # If direction has room with open door True otherwise randomize door
        for i, room in enumerate(doors):
            if isinstance(self.grid[self.room_coords[i]], Room):
                if self.grid[self.room_coords[(i + 2) % 4]]:
                    doors[i] = True
                else:
                    doors[i] = bool(random.getrandbits(1))

        self.grid[new_room_index] = Room(self,new_room_index, doors, icon="Z")
        print("z", self.grid[new_room_index].doors)

    def __str__(self):
        # result = ""
        # for i, room in enumerate(self.grid):
        #     if not i % self.x and i:
        #         result += "\n\n"
        #     icon = str(room) if room else "_"
        #     result += f"[{icon}] "
        # return result

        result = ""
        c1, c2, c3 = "", "", ""
        for i, room in enumerate(self.grid):
            if not i % self.x and i:
                result += f"{c1}\n{c2}\n{c3}\n"
                c1, c2, c3 = "", "", ""
            icon = str(room) if room else "_"
            c1 += f"  {'|' if room and room.doors[0] else ' '}  "
            c2 += f"{'-' if room and room.doors[3] else ' '}[{icon}]{'-' if room and room.doors[1] else ' '}"
            c3 += f"  {'|' if room and room.doors[2] else ' '}  "
        return result + f"{c1}\n{c2}\n{c3}"


class Room:
    def __init__(self, level, index, doors, icon=" "):
        self.level = level
        self.index = index
        self.doors = doors
        self.icon = icon
        x = self.level.x
        for door, di in zip(doors, self.level.room_coords):
            if door:
                self.level.room_expansion_set.add(index + di)
        print('room_expansion:', self.level.room_expansion_set)
        print('room_expansion:', self.get_required_doors)

    def get_required_doors(self):
        required_doors = [None] * 4
        for i, offset in enumerate(self.level.room_coords):
            print('tts', i, offset)
            if self.level.grid[self.index+offset]:
                neighbor_door = self.level.grid[self.index+offset].doors[i]
                print("neighbor_door:", neighbor_door)
                required_doors[(i+2) % 4] = neighbor_door
        return required_doors

    def __str__(self):
        return self.icon
        # return f"  |  \n [{self.icon}] \n   |  "


level = Level(5, 5)
print(level)
print(level.room_expansion_set)

# print('permutations:', list(itertools.product([False, True], repeat=4)))
