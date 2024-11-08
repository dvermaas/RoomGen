#include <vector>
#include <array>
#include <iostream>
#include <random>
#include <algorithm>
#include <unordered_set>

using namespace std;

class Room {
public:
    array<bool, 4> doors; // [N, E, S, W]
    explicit Room(const array<bool, 4> &doors) : doors(doors) {
    }
};

class Level {
private:
    int size;
    vector<Room *> grid;
    vector<int> queue;
    array<int, 4> offset;
    random_device rd;
    mt19937 rng;

public:
    explicit Level(const int size) : size(size), grid(size * size, nullptr), offset{-size, 1, size, -1}, rng(rd()) {
        const int middle = (size / 2) * size + (size / 2);
        constexpr array<bool, 4> doors = {true, true, true, true};
        grid[middle] = new Room(doors);

        for (int i = 0; i < 4; ++i) {
            if (doors[i]) {
                queue.push_back(middle + offset[i]);
            }
        }


        while (!queue.empty()) {
            generate();
            print();
            printQueue();
        }
    }

    void generate() {
        int choice = queue[rand() % queue.size()];
        addRoom(choice);
    }

    static void removeDuplicates(std::vector<int> &vec) {
        sort(vec.begin(), vec.end()); // Sort the vector
        vec.erase(unique(vec.begin(), vec.end()), vec.end()); // Remove duplicates
    }

    void addRoom(const int o) {
        cout << "Adding room :" << o << endl;
        // stop when illegal position
        if (grid[o] != nullptr) {
            raise(*"Incorrect room added");
            return;
        }

        // randomize doors
        array<bool, 4> doors{};
        for (int i = 0; i < 4; ++i) {
            doors[i] = rand() % 2;
        }

        for (int i = 0; i < 4; ++i) {
            const int neighbor_index = o + offset[i];
            // check if in bounds
            if (neighbor_index < 0 || neighbor_index >= grid.size()) {
                doors[i] = false;
                continue;
            };

            const Room *neighbour = grid[neighbor_index];
            // create door if neighbour has door
            if (neighbour != nullptr && neighbour->doors[(i + 2) % 4]) {
                doors[i] = true;
            }
            // remove illegal doors
            if (i == 0 and i / size == 0) {
                doors[i] = false;
            };
            if (i == 1 and i % size == size - 1) {
                doors[i] = false;
            };
            if (i == 2 and i / size == size - 1) {
                doors[i] = false;
            };
            if (i == 3 and i % size == 0) {
                doors[i] = false;
            };
            // doors to the void should be put in the queue
            if (neighbour == nullptr and doors[i]) {
                cout << "adding to queue: " << neighbor_index << endl;
                queue.push_back(neighbor_index);
            }
        };

        grid[o] = new Room(doors);
        removeDuplicates(queue);
        queue.erase(ranges::remove(queue, o).begin(), queue.end());
    }

    void printQueue() const {
        std::cout << "Queue:";
        for (int value: queue) {
            std::cout << value << " ";
        }
        std::cout << std::endl;
    }

    void print() const {
        vector<vector<char> > display_grid(2 * size - 1, vector<char>(2 * size - 1, ' '));

        for (int i = 0; i < grid.size(); ++i) {
            if (const Room *room = grid[i]; room != nullptr) {
                int x = (i % size) * 2;
                int y = (i / size) * 2;
                display_grid[y][x] = 'X';
                if (room->doors[0]) display_grid[y - 1][x] = '|';
                if (room->doors[1]) display_grid[y][x + 1] = '-';
                if (room->doors[2]) display_grid[y + 1][x] = '|';
                if (room->doors[3]) display_grid[y][x - 1] = '-';
            }
        }

        for (const auto &row: display_grid) {
            for (const char cell: row) {
                cout << cell;
            }
            cout << endl;
        }
    }
};


int main() {
    Level level(5);
    // level.print();
    return 0;
};
