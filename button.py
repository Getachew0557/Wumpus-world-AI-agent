import pygame as pg

pg.font.init()
btn_txt = pg.font.SysFont('Arial Black', 23)

class Button:
    def __init__(self, xy, text_input, btn_color, hover_color, text_color='white', border_radius=12):
        self.x_pos = xy[0]
        self.y_pos = xy[1]
        self.text_input = text_input
        self.text_color = text_color
        self.btn_color = btn_color
        self.hover_color = hover_color
        self.border_radius = border_radius
        self.text = btn_txt.render(self.text_input, True, self.text_color)
        self.rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def draw_button(self, screen):
        btn_rect = pg.Rect.inflate(self.rect, 40, 25)
        pg.draw.rect(screen, self.btn_color, btn_rect, border_radius=self.border_radius)
        screen.blit(self.text, self.rect)

    def draw_button_transparent(self, screen):
        shape = pg.Surface(self.rect.size, pg.SRCALPHA)
        pg.draw.rect(shape, self.btn_color, shape.get_rect(), border_radius=self.border_radius)
        screen.blit(shape, self.rect)
        screen.blit(self.text, self.rect)

    def click_button(self, pos):
        return self.rect.collidepoint(pos)

    def update_color(self, pos):
        if self.rect.collidepoint(pos):
            self.text = btn_txt.render(self.text_input, True, self.hover_color)
        else:
            self.text = btn_txt.render(self.text_input, True, self.text_color)
