import pygame as pg

# Constants
space = 90
mg_x = 70
mg_y = 150
WORLD_SIZE = 4

# Custom Colors (no white)
TEAL = (0, 128, 128)
SOFT_GREEN = (100, 200, 150)
DEEP_NAVY = (25, 35, 65)
LIGHT_BLUE = (173, 216, 230)
GOLDENROD = (218, 165, 32)
CHARCOAL = (54, 69, 79)

# Font Initialization
pg.font.init()

class Draw:
    def __init__(self, screen):
        self.screen = screen

        # Load assets
        self.agent_img = pg.image.load("assets/agent.png")
        self.agent_side_img = pg.image.load("assets/agent_side.png")
        self.agent_victory_img = pg.image.load("assets/agent_victory.png")
        self.arrow_img = pg.image.load("assets/arrow.png")
        self.arrow_side_img = pg.image.load("assets/arrow_side.png")
        self.breeze_img = pg.image.load("assets/cell_breeze.png")
        self.breeze_stench_img = pg.image.load("assets/cell_breeze-stench.png")
        self.gold_img = pg.image.load("assets/cell_gold.png")
        self.pit_img = pg.image.load("assets/cell_pit.png")
        self.stench_img = pg.image.load("assets/cell_stench.png")
        self.wumpus_img = pg.image.load("assets/cell_wumpus.png")

        # Modern Font
        self.font = pg.font.SysFont('Segoe UI', 20, bold=True)
        self.large_font = pg.font.SysFont('Segoe UI Semibold', 26, bold=True)

    def board(self):
        board_rect = pg.Rect(mg_x, mg_y, space * WORLD_SIZE, space * WORLD_SIZE)
        pg.draw.rect(self.screen, CHARCOAL, board_rect, 6, border_radius=10)

        for i in range(1, WORLD_SIZE):
            pg.draw.line(self.screen, CHARCOAL, (mg_x, mg_y + i * space), (mg_x + space * WORLD_SIZE, mg_y + i * space), 2)
            pg.draw.line(self.screen, CHARCOAL, (mg_x + i * space, mg_y), (mg_x + i * space, mg_y + space * WORLD_SIZE), 2)

    def agent(self, row, col, direction):
        x = mg_x + col * space + 10
        y = mg_y + row * space + 20

        if direction == 'N':
            y -= 10
            self.screen.blit(self.agent_img, (x, y))
        elif direction == 'S':
            self.screen.blit(self.agent_img, (x, y))
        elif direction == 'W':
            self.screen.blit(self.agent_side_img, (x, y))
        elif direction == 'E':
            flipped = pg.transform.flip(self.agent_side_img, True, False)
            self.screen.blit(flipped, (x, y))
        elif direction == 'V':
            self.screen.blit(self.agent_victory_img, (x - 10, y - 20))

        self.board()

    def environment(self, world):
        for row in range(WORLD_SIZE):
            for col in range(WORLD_SIZE):
                self.fill_env(row, col, world)

    def fill_env(self, row, col, world):
        cell_type = world[row][col]
        x = mg_x + col * space
        y = mg_y + row * space

        cell_rect = pg.Rect(x, y, space, space)
        pg.draw.rect(self.screen, DEEP_NAVY, cell_rect)

        if cell_type == '' or cell_type == 'A':
            pass
        elif cell_type == 'B':
            self.screen.blit(self.breeze_img, (x, y))
        elif cell_type == 'BS':
            self.screen.blit(self.breeze_stench_img, (x, y))
        elif 'G' in cell_type:
            self.screen.blit(self.gold_img, (x, y))
        elif 'P' in cell_type:
            self.screen.blit(self.pit_img, (x, y))
        elif 'S' in cell_type and 'B' not in cell_type:
            self.screen.blit(self.stench_img, (x, y))
        elif 'W' in cell_type:
            self.screen.blit(self.wumpus_img, (x, y))

        if 'A' in cell_type:
            self.screen.blit(self.agent_img, (x + 10, y + 10))

        self.board()

    def arrows(self, direction, pos):
        row, col = pos
        x = mg_x + col * space + 10
        y = mg_y + row * space + 10

        if direction == "N":
            for r in range(row, -1, -1):
                self.screen.blit(self.arrow_img, (x, mg_y + r * space + 10))
        elif direction == "S":
            arrow_down = pg.transform.flip(self.arrow_img, False, True)
            for r in range(row, WORLD_SIZE):
                self.screen.blit(arrow_down, (x, mg_y + r * space + 10))
        elif direction == "W":
            arrow_west = pg.transform.flip(self.arrow_side_img, True, False)
            for c in range(col, -1, -1):
                self.screen.blit(arrow_west, (mg_x + c * space + 10, y))
        elif direction == "E":
            for c in range(col, WORLD_SIZE):
                self.screen.blit(self.arrow_side_img, (mg_x + c * space + 10, y))

    def status(self, text, color=TEAL):
        bg = pg.Surface((250, 90))
        bg.fill(DEEP_NAVY)
        rect = bg.get_rect(center=(620, 350))
        pg.draw.rect(self.screen, GOLDENROD, rect.inflate(6, 6), 3, border_radius=8)

        # Dynamic multi-line support
        words = text.split(' ')
        lines = []
        line = ""
        for word in words:
            if len(line + word) < 20:
                line += word + " "
            else:
                lines.append(line.strip())
                line = word + " "
        lines.append(line.strip())

        for i, line in enumerate(lines[:2]):
            output = self.font.render(line, True, color)
            self.screen.blit(bg, rect)
            line_rect = output.get_rect(center=(rect.centerx, rect.top + 30 + i * 25))
            self.screen.blit(output, line_rect)

    def score(self, text, color=CHARCOAL):
        bg = pg.Surface((130, 70))
        bg.fill(SOFT_GREEN)
        rect = bg.get_rect(center=(680, 180))
        pg.draw.rect(self.screen, TEAL, rect, 2, border_radius=6)

        label = self.font.render("Score", True, color)
        value = self.large_font.render(text, True, color)

        self.screen.blit(bg, rect)
        self.screen.blit(label, label.get_rect(center=(rect.centerx, rect.centery - 15)))
        self.screen.blit(value, value.get_rect(center=(rect.centerx, rect.centery + 15)))
