import pygame
from pygame import Vector2
from random import randint


class Target():
    def __init__(self, screen, vehicle):
        self.vehicle = vehicle
        self.screen = screen
        self.white = (255, 255, 255)
        self.rect = pygame.draw.circle(screen, self.white, (0, 0), 6)
        self.rect.x = randint(0, self.screen.get_width())
        self.rect.y = randint(0, self.screen.get_height())
        self.pos = Vector2(self.rect.x, self.rect.y)

    def update(self):
        self.draw()
        if type(self.vehicle) == list:
            for boid in self.vehicle:
                if boid.pos.distance_to(self.pos) < 1:

                    self.rect.x = randint(20, self.screen.get_width() - 20)
                    self.rect.y = randint(20, self.screen.get_height() - 20)
                    self.pos = Vector2(self.rect.x, self.rect.y)
                    break
        else:
            if self.vehicle.pos.distance_to(self.pos) < 1:
                self.rect.x = randint(20, self.screen.get_width() - 20)
                self.rect.y = randint(20, self.screen.get_height() - 20)
                self.pos = Vector2(self.rect.x, self.rect.y)

    def draw(self):
        pygame.draw.circle(self.screen, self.white,
                           (self.rect.x, self.rect.y), 10, 1)
