WORLD_SIZE = 4

class Helper:
    def is_valid(self, x, y):
        return 0 <= x < WORLD_SIZE and 0 <= y < WORLD_SIZE

    def check_row_column(self, agent_pos, wumpus_pos, row_col):
        agent_x, agent_y = agent_pos
        for i in range(WORLD_SIZE):
            if row_col == 'C' and i == wumpus_pos[1] and agent_y == wumpus_pos[1]:
                print("Wumpus killed in COLUMN:", i)
                return True
            elif row_col == 'R' and i == wumpus_pos[0] and agent_x == wumpus_pos[0]:
                print("Wumpus killed in ROW:", i)
                return True
        return False

    def get_adjacent(self, x, y):
        return [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]

    def is_boundary_cell(self, x, y):
        return x in [0, WORLD_SIZE - 1] or y in [0, WORLD_SIZE - 1]

    def assign_char(self, x, y, character, grid):
        if self.is_valid(x, y):
            current_chars = set(grid[x][y])
            current_chars.add(character)
            grid[x][y] = ''.join(sorted(current_chars))
        return grid

    def remove_char(self, x, y, character, grid):
        if self.is_valid(x, y):
            current_chars = set(grid[x][y])
            if character in current_chars:
                current_chars.remove(character)
                grid[x][y] = ''.join(sorted(current_chars))
        return grid

    def check_char(self, cell, letter):
        return any(letter in string for string in cell)

    def generate_patterns(self):
        patterns_list = []
        for i in range(-1, WORLD_SIZE):
            for j in range(-1, WORLD_SIZE):
                # Horizontal patterns
                triangle = [(i, j), (i + 1, j + 1), (i, j + 2)]
                patterns_list.append({"pattern": triangle, "location": (i, j + 1)})

                triangle = [(i + 1, j), (i, j + 1), (i + 1, j + 2)]
                patterns_list.append({"pattern": triangle, "location": (i + 1, j + 1)})

                # Vertical patterns
                triangle = [(i, j), (i + 1, j + 1), (i + 2, j)]
                patterns_list.append({"pattern": triangle, "location": (i + 1, j)})

                triangle = [(i, j + 1), (i + 1, j), (i + 2, j + 1)]
                patterns_list.append({"pattern": triangle, "location": (i + 1, j + 1)})

        # Filter patterns that have more than one valid cell
        patterns_list = [pattern for pattern in patterns_list
                         if sum(1 for coord in pattern["pattern"] if self.is_valid(coord[0], coord[1])) > 1]

        # Remove out-of-bounds cells from pattern
        for pattern in patterns_list:
            pattern["pattern"] = [coord for coord in pattern["pattern"] if self.is_valid(coord[0], coord[1])]

        return patterns_list

    def print_world(self, world):
        print("+" + "-" * 23 + "+")
        for i in range(WORLD_SIZE):
            print("|  ", end="")
            for j in range(WORLD_SIZE):
                print(world[i][j], end="  |  ")
            print("\n+" + "-" * 23 + "+")
