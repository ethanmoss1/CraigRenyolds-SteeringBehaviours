import pygame
from random import randint
from random import random
from pygame import Vector2


class Vehicle(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, width, height):
        super().__init__()
        self.screen = screen
        self.screen_width, self.screen_height = width, height
        self.radius = 15
        self.rect = pygame.draw.circle(
            self.screen, (255, 255, 255), (x, y), self.radius, 2)
        self.pos = Vector2(x, y)
        self.vel = Vector2(random() - 1, random() - 1)
        self.acc = Vector2(0)
        self.max_spd = 10
        self.max_force = 0.1

        self.white = (255, 255, 255)

    def map_linear(self, value, start1, stop1, start2, stop2):
        return ((value - start1) / (stop1 - start1)) * (stop2 - start2) + start2

    def seek(self, target):
        force = target - self.pos
        force.scale_to_length(self.max_spd)
        force -= self.vel
        if force.magnitude() > self.max_force:
            force.scale_to_length(self.max_force)
        return force

    def flee(self, target):
        return self.seek(target).rotate(180)

    def apply_force(self, force):
        force.scale_to_length(self.max_force)
        self.acc += force

    def pursue(self, target):
        if isinstance(target, Vehicle):
            distance = self.pos.distance_to(target.pos) / 2
            intercept_pos = Vector2(target.vel)
            intercept_pos.scale_to_length(distance)
            intercept_pos += target.pos
            pygame.draw.circle(self.screen, (255, 255, 255),
                               (int(intercept_pos.x), int(intercept_pos.y)), 5, 1)
            return self.seek(intercept_pos)
        else:
            return Vector2(0)

    def evade(self, target):
        if isinstance(target, Vehicle):
            return self.pursue(target).rotate(180)
        else:
            return Vector2(0)

    def arrive(self, target):
        """
            Arrival behavior is identical to seek while the character is far
            from its target. But instead of moving through the target at 
            full speed, this behavior causes the character to slow down 
            as it approaches the target, eventually slowing to a stop 
            coincident with the target, as shown in Figure 6.
            The distance at which slowing begins is a parameter of the
            behavior. This implementation is similar to seek:
            a desired velocity is determined pointing from the character
            towards the target. Outside the stopping radius this
            desired velocity is clipped to max_speed, inside the stopping
            radius, desired velocity is ramped down (e.g. linearly) to zero.

            target_offset = target - position
            distance = length (target_offset)
            ramped_speed = max_speed * (distance / slowing_distance)
            clipped_speed = minimum (ramped_speed, max_speed)
            desired_velocity = (clipped_speed / distance) * target_offset
            steering = desired_velocity - velocity        
        """
        slowing_distance = 100
        target_offset = target - self.pos
        distance = target_offset.magnitude()
        ramped_speed = self.max_spd * (distance / slowing_distance)
        clipped_speed = min(ramped_speed, self.max_spd)
        desired_vel = (clipped_speed / distance) * target_offset
        
        # if desired_vel.magnitude() > self.max_spd:
        #     print(desired_vel)
        #     print("scaling desired vel")
        #     desired_vel.scale_to_length(self.max_spd)
        # print(f"{target_offset}\n{distance}\n{ramped_speed}\n{clipped_speed}\n{desired_vel}\n{ desired_vel - self.vel}\n")
        # input("")
        steering = desired_vel - self.vel
        # steering.scale_to_length(self.max_force)
        return steering

        # influence_dist = 100  # fine tune

        # desired_vel = target - self.pos
        # distance = desired_vel.length()
        # if desired_vel.length() >= 0.001:
        #     desired_vel.scale_to_length(self.max_spd)

        # if distance <= 0.1:
        #     return Vector2(0)
        # elif distance <= influence_dist:
        #     max_force = self.map_linear(distance, 0, influence_dist, 0, self.max_spd)
        #     desired_vel.scale_to_length(max_force)
        #     force = desired_vel - self.vel

        #     if force.magnitude() > self.max_force:
        #         force.scale_to_length(self.max_force)
        #     return force
        # else:
        #     return self.seek(target)

    def wrap_around(self, width, height):
        if self.pos.x < 0:
            self.pos.x = width
        elif self.pos.x > width:
            self.pos.x = 0
        elif self.pos.y < 0:
            self.pos.y = height
        elif self.pos.y > height:
            self.pos.y = 0

    def combine_vectors(self):
        self.vel += self.acc
        if self.vel.magnitude() >= self.max_spd:
            self.vel.scale_to_length(self.max_spd)
        self.pos += self.vel
        self.rect.center = [self.pos.x, self.pos.y]

    def update(self):
        self.combine_vectors()
        self.draw()
        self.acc = Vector2(0)

    def draw(self):
        # self rect
        pygame.draw.circle(self.screen, (255, 255, 255),
                           self.rect.center, self.radius, 1)

        # Current Velocity line (heading)
        pygame.draw.aaline(self.screen, (255, 255, 255), self.rect.center,
                           (self.rect.center[0] + self.vel.x * 10, self.rect.center[1] + self.vel.y * 10))

        # Acceleration line (steering force)
        pygame.draw.aaline(self.screen, (255, 0, 255), self.rect.center,
                           (self.rect.center[0] + self.acc.x * 50, self.rect.center[1] + self.acc.y * 50))

    def reset(self, width, height):
        self.pos.x, self.pos.y = randint(0, width), randint(0, height)
        self.vel = Vector2(randint(-1, 1), randint(-1, 1))
