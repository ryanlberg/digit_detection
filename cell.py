import pygame
class cell:

    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.clicked = False
        self.color = (255,255,255)

    def changeColor(self):
        self.color = (0,0,0)

    def draw(self, screen):
        cellrect = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(screen, self.color, cellrect)

    def click(self):
        if not self.clicked:
            self.changeColor()
