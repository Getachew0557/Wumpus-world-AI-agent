import pygame as pg

pg.font.init()
btn_txt = pg.font.SysFont('Arial Black', 23)

class Button:
    def __init__(self, xy, text_input, btn_color, hover_color, text_color='white',
                 border_radius=12, padding=(40, 25), font=None, border_color=None, border_width=0):
        self.x_pos, self.y_pos = xy
        self.text_input = text_input
        self.text_color = text_color
        self.btn_color = btn_color
        self.hover_color = hover_color
        self.border_radius = border_radius
        self.padding = padding
        self.font = font or btn_txt
        self.border_color = border_color
        self.border_width = border_width

        self.text = self.font.render(self.text_input, True, self.text_color)
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.btn_rect = pg.Rect.inflate(self.text_rect, *self.padding)
        self.current_color = self.btn_color

    def draw_button(self, screen):
        # Draw button background
        pg.draw.rect(screen, self.current_color, self.btn_rect, border_radius=self.border_radius)

        # Optional border
        if self.border_color and self.border_width > 0:
            pg.draw.rect(screen, self.border_color, self.btn_rect, width=self.border_width, border_radius=self.border_radius)

        # Draw text
        screen.blit(self.text, self.text_rect)

    def draw_button_transparent(self, screen):
        shape = pg.Surface(self.btn_rect.size, pg.SRCALPHA)
        pg.draw.rect(shape, self.current_color, shape.get_rect(), border_radius=self.border_radius)
        screen.blit(shape, self.btn_rect.topleft)
        screen.blit(self.text, self.text_rect)

    def click_button(self, pos):
        return self.btn_rect.collidepoint(pos)

    def update_color(self, pos):
        if self.btn_rect.collidepoint(pos):
            self.current_color = self.hover_color
        else:
            self.current_color = self.btn_color
