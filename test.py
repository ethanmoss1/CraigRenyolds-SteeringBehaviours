from random import random
import pygame
import math
from pygame import Vector2

WIDTH = 1600
HEIGHT = 1000
FPS = 60
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True


def events():
    clock.tick(FPS)
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False

            if event.key == pygame.K_i:
                pursue.max_spd += 0.5
                print(pursue.max_spd)

            if event.key == pygame.K_k:
                pursue.max_spd -= 0.5
                print(pursue.max_spd)

            if event.key == pygame.K_o:
                target.max_spd += 0.5
                target.vel.scale_to_length(target.max_spd)
                print(target.max_spd)

            if event.key == pygame.K_l:
                target.max_spd -= 0.5
                target.vel.scale_to_length(target.max_spd)
                print(target.max_spd)

            if event.key == pygame.K_SPACE:
                target.vel = Vector2(
                    ((random() * 2) - 1,
                     (random() * 2) - 1))
                target.vel.scale_to_length(target.max_spd)
                target.pos = Vector2(
                    (int(random()*WIDTH), int(random() * HEIGHT)))

                pursue.vel = Vector2(
                    ((random() * 2) - 1,
                     (random() * 2) - 1))
                pursue.vel.scale_to_length(pursue.max_spd)
                pursue.pos = Vector2(
                    (int(random()*WIDTH), int(random() * HEIGHT)))

    return True


def draw_line(start, end, offset, colour=(255, 255, 255)):
    if isinstance(start, Vector2):
        newstart = (int(start.x) + offset, int(start.y)+offset)
    else:
        newstart = (int(start[0]+offset), int(start[1]+offset))

    if isinstance(end, Vector2):
        newend = (int(end.x)+offset, int(end.y)+offset)
    else:
        newend = (int(end[0])+offset, int(end[1])+offset)

    pygame.draw.aaline(screen, colour, newstart, newend)


class Veh:
    def __init__(pursue, pos, vel):
        pursue.pos = pos
        pursue.vel = vel
        pursue.radius = 15
        pursue.colour = (255, 255, 255)

        pursue.max_spd = 5
        pursue.max_force = 0.1

    def draw(pursue, screen):
        point1 = Vector2(pursue.vel)
        point1.scale_to_length(pursue.radius)
        point2 = point1.rotate(135)
        point3 = point1.rotate(225)
        pygame.draw.aalines(screen, pursue.colour, True,
                            [point1 + pursue.pos, point2 + pursue.pos, pursue.pos, point3 + pursue.pos])


pursue = Veh(Vector2(1009.67, 753.269), Vector2(4.87249, -0.838534))
pursue.colour = (255, 0, 0)
pursue.max_spd = 50
target = Veh(Vector2(1277.28, 412.55), Vector2(0.810552, 4.62975))
target.colour = (0, 0, 255)


colour = (255, 255, 255)
while running:
    running = events()
    ###########################################################################

    pursue.draw(screen)
    target.draw(screen)

    # GREEN - my pursue implementation
    green = False
    if green:
        future_amt = pursue.pos.distance_to(target.pos)
        speed_ratio = target.vel.magnitude() / pursue.max_spd
        future_amt = future_amt * speed_ratio
        target_future_pos = Vector2(target.vel)
        target_future_pos.scale_to_length(future_amt)
        target_future_pos += target.pos
        pygame.draw.circle(screen, (0, 255, 0), (int(
            target_future_pos.x), int(target_future_pos.y)), 5, 1)

    # YELLOW - sine law implementation
    yellow = True
    if yellow:
        speed_ratio = target.vel.magnitude() / pursue.max_spd
        desired = pursue.pos - target.pos
        pygame.draw.circle(screen, (255, 255, 255), (int(desired.x),int(desired.y   )), 5, 1)

        target_angle = math.radians(target.vel.angle_to(desired))
        my_angle = math.asin(math.sin(target_angle) * speed_ratio)
        dist = pursue.pos.distance_to(target.pos)
        prediction = dist * (math.sin(my_angle) /
                             math.sin(math.pi - my_angle - target_angle))
        new_target = Vector2(target.vel)
        new_target.scale_to_length(prediction)
        new_target += target.pos
        draw_target = (int(new_target.x), int(new_target.y))


        points = [
            [int(target.pos.x),int(target.pos.y)],
            list(draw_target),
            [int(desired.x),int(desired.y)],
        ]
        pygame.draw.aalines(screen,colour, True, points)
        pygame.draw.circle(screen, (255, 255, 0), draw_target, 5, 1)

    ###########################################################################
    pygame.display.flip()
pygame.quit()
