#!/usr/bin/env python3

# Import files and libs
from obstacles import Obstacles
import pygame
from random import randint
from vehicle import Vehicle
from target import Target
from path import Path as PathFollow

# Initalise Pygame and Variables
pygame.init()
WIDTH = 1600
HEIGHT = 1000
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Steering Behaviours of Autonomous Vehicles")
clock = pygame.time.Clock()
running = True


def events():
    """
    Runs through pygame events and allows quiting of program
    """
    clock.tick(FPS)
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
    return True


# initalise classes
attacker = Vehicle(screen, WIDTH / 2, HEIGHT / 2)
target = Vehicle(screen, WIDTH / 4, HEIGHT / 4)


# attacker.get_vector(test)

while running:
    running = events()
    ###########################################################################
    # YOUR CODE HERE:

    steering = attacker.pursue_sine_law(target)
    attacker.update(steering)

    steering = target.wander(True)
    target.update(steering)

    if attacker.pos.distance_to(target.pos) < target.radius:
        target.reset()

    ###########################################################################
    pygame.display.flip()

# be friendly, always quit!
pygame.quit()
