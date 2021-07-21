from pygame import draw
from pygame import Vector2


class Obstacles:
    def __init__(self, x, y, radius):
        self.pos = Vector2(x, y)
        self.pos_int = (int(self.pos.x), int(self.pos.y))
        self.radius = radius
        self.colour = (200, 200, 200)

    def draw(self, screen):
        draw.circle(screen, self.colour, self.pos_int, self.radius, 1)
