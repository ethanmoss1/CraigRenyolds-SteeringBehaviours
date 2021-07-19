#!/usr/bin/env python3

from obstacles import Obstacles
from sys import path
import pygame
import random
from random import randint
from Vehicle import Vehicle
from target import Target
from path import Path as PathFollow

WIDTH = 1600
HEIGHT = 1000
FPS = 60
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Steering Behaviours of Autonomous Vehicles")
clock = pygame.time.Clock()
running = True


def events(draw_bool):
    clock.tick(FPS)
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, draw_bool
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False, draw_bool
            if event.key == pygame.K_SPACE:
                follow.new_path()
            if event.key == pygame.K_v:
                if draw_bool:
                    draw_bool = False
                else:
                    draw_bool = True
            if event.key == pygame.K_i:
                for i in range(100):
                    boid = Vehicle(screen, randint(0, WIDTH), randint(0, HEIGHT), WIDTH, HEIGHT)
                    boid.colour = (randint(50,255),randint(50,255),randint(50,255))
                    # boid.max_force = randint(1,10) / 10
                    # boid.max_spd = randint(1,20)
                    boids.append(boid)
        if event.type == pygame.MOUSEBUTTONDOWN:
            boid = Vehicle(screen, randint(0, WIDTH), randint(0, HEIGHT), WIDTH, HEIGHT)
            boid.colour = (randint(50,255),randint(50,255),randint(50,255))
            # boid.max_force = randint(1,10) / 10
            # boid.max_spd = randint(1,20)
            boids.append(boid)
    return True, draw_bool

boids = []
boid = Vehicle(screen, randint(0, WIDTH), randint(0, HEIGHT), WIDTH, HEIGHT)
boid.colour = (0, 255, 0)
# follow = PathFollow(screen, points=[(0, 500), (50, 500), (100, 500), (150, 500), (200, 500), (250, 500), (300, 500), (350, 500), (400, 500), (450, 500), (500, 500), (550, 500), (600, 500), (650, 500), (700, 500), (750, 500), (
#     800, 500), (850, 500), (900, 500), (950, 500), (1000, 500), (1050, 500), (1100, 500), (1150, 500), (1200, 500), (1250, 500), (1300, 500), (1350, 500), (1400, 500), (1450, 500), (1500, 500), (1550, 500), (1600, 500), (1650, 500)])
follow = PathFollow(screen, points=[pygame.Vector2(200, 200), pygame.Vector2(200, 800), pygame.Vector2(1400, 800),pygame.Vector2(1400, 200),pygame.Vector2(200, 200)])
# follow = PathFollow(screen, points=[pygame.Vector2(0, HEIGHT), pygame.Vector2(500, 500)])

boids.append(boid)
draw_bool = False
# follow.new_path()

while running:
    ###########################################################################
    running, draw_bool = events(draw_bool)
    
    if draw_bool:
        follow.draw()
    
    for boid in boids:   
        steering = boid.follow_path(follow)
        boid.update(steering, )

    ###########################################################################
    pygame.display.flip()
pygame.quit()
