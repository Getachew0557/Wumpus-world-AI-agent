import pygame as pg

space = 90
mg_x = 70
mg_y = 150
WORLD_SIZE = 4

# New custom colors
AQUA = (0, 204, 204)
WHITE = (255, 255, 255)
DARK_GREEN = (34, 139, 34)
LIGHT_GREEN = (169, 209, 142)
DARK_BLUE = (30, 60, 90)

pg.font.init()

class Draw:
    def __init__(self, screen):
        self.screen = screen

        # Update these to custom paths/icons if needed
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

        self.font = pg.font.SysFont('Arial Black', 20)

    def board(self):
        board_rect = pg.Rect(mg_x, mg_y, 360, 360)
        pg.draw.rect(self.screen, DARK_GREEN, board_rect, 7)

        for i in range(1, 4):
            pg.draw.line(self.screen, DARK_GREEN, (mg_x, mg_y + i * space), (mg_x + 355, mg_y + i * space), 3)
            pg.draw.line(self.screen, DARK_GREEN, (mg_x + i * space, mg_y), (mg_x + i * space, mg_y + 355), 3)

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

        if cell_type == '' or cell_type == 'A':
            pg.draw.rect(self.screen, DARK_BLUE, pg.Rect(x, y, space, space))
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

    def status(self, text, color):
        bg = pg.Surface((240, 90))
        bg.fill(DARK_BLUE)
        rect = bg.get_rect(center=(610, 350))
        pg.draw.rect(self.screen, AQUA, rect.inflate(4, 4), 2)

        lines = [text[:16], text[16:]] if len(text) > 16 else [text]
        for i, line in enumerate(lines):
            output = self.font.render(line, True, color)
            line_rect = output.get_rect(center=(rect.centerx, rect.centery + (i * 30 - 15)))
            self.screen.blit(bg, rect)
            self.screen.blit(output, line_rect)

    def score(self, text, color):
        bg = pg.Surface((115, 60))
        bg.fill(LIGHT_GREEN)
        rect = bg.get_rect(center=(680, 180))

        label = self.font.render("Score", True, color)
        value = self.font.render(text, True, color)

        self.screen.blit(bg, rect)
        self.screen.blit(label, label.get_rect(center=(rect.centerx, rect.centery - 10)))
        self.screen.blit(value, value.get_rect(center=(rect.centerx, rect.centery + 10)))
