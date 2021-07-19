import pygame
from pygame import Vector2

class Obstacles:
    def __init__(self, x, y, radius):
        self.posV = Vector2(x,y)
        self.pos = (int(self.posV.x), int(self.posV.y))
        self.radius = radius
        self.colour = (200,200,200)
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, self.pos, self.radius, 1)