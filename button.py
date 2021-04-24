import pygame


class button():
    def __init__(self, color, x, y, width, height, outline=None, outline_width=0):
        self.color = color
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.outline = outline
        self.outline_width = outline_width
        self.surface = None

    def draw(self, surface):
        self.surface = surface
        if self.outline:
            pygame.draw.rect(surface, self.outline, (self.x - self.outline_width, self.y -
                             self.outline_width, self.height+2*self.outline_width, self.width+2*self.outline_width), 0)
        pygame.draw.rect(surface, self.color,
                         (self.x, self.y, self.width, self.height), 0)

    def add_text(self, txt, text_color, text_size):
        if txt != "":
            font = pygame.font.SysFont('comicsans', text_size)
            text = font.render(txt, 1, text_color)

        self.surface.blit(text, (self.x + (self.width - text.get_width())//2,
                                 self.y + (self.height - text.get_height())//2))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x+self.width:
            if pos[1] > self.y and pos[1] < self.y+self.height:
                return True
        return False
