#!/usr/bin/env python3


# Import files and libs
from obstacles import Obstacles
from sys import path
import pygame
import random
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
boids = []
boid = Vehicle(screen, randint(0, WIDTH), randint(0, HEIGHT), WIDTH, HEIGHT)
boid.colour = (0, 255, 0)
follow = PathFollow(screen, points=[pygame.Vector2(200, 200), pygame.Vector2(
    200, 800), pygame.Vector2(1400, 800), pygame.Vector2(1400, 200), pygame.Vector2(200, 200)])

boids.append(boid)

while running:
    ###########################################################################
    # YOUR CODE HERE:

    for boid in boids:
        steering = boid.follow_path(follow)
        boid.update(steering, )

    ###########################################################################
    running = events()
    pygame.display.flip()
    
# be friendly, always quit!
pygame.quit()