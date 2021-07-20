import pygame
from random import randint
from random import random
from pygame import Vector2
import math


class Vehicle():
    def __init__(self, screen, x, y):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        self.mass = 1
        self.max_spd = 5
        self.max_force = 0.1
        self.radius = 15

        self.pos = Vector2(x, y)
        self.pos_xy = (int(self.pos.x), int(self.pos.y))
        self.vel = Vector2(1)
        self.acc = Vector2(1)
        self.steering_force = Vector2(1)

        self.colour = (255, 255, 255)
        self.displacement = None
        self.slowing_distance = ((0.1/self.max_force)*130) * \
            (self.mass) * ((self.max_spd / 5) ** 2)

    def draw(self, circle=False, velocity=False, acceleration=False,
             slowing_field=False, arrow=True):
        """
        Draws vehicle and information used in some steering behaviors
        """
        # Circle from Pos
        if circle:
            pygame.draw.circle(self.screen, self.colour,
                               self.pos_xy, self.radius, 1)

        # Current Velocity line (heading) scaled for visablity
        if velocity:
            vel_line = (self.pos_xy[0] + self.vel.x * 10,
                        self.pos_xy[1] + self.vel.y * 10)
            pygame.draw.aaline(self.screen, self.colour, self.pos_xy, vel_line)

        # Acceleration line (steering force) scaled for visability
        if acceleration:
            acc_line = (self.pos_xy[0] + self.acc.x * 150,
                        self.pos_xy[1] + self.acc.y * 150)
            pygame.draw.aaline(self.screen, (0, 255, 0), self.pos_xy, acc_line)

        # slowing field for arrival
        if slowing_field:
            pygame.draw.circle(self.screen, self.colour,
                               self.pos_xy, int(self.slowing_distance), 1)

        # Arrow poly to show direction aestically
        if arrow:
            point_head = Vector2(self.vel)
            point_head.scale_to_length(self.radius)
            point_right = point_head.rotate(135)
            point_left = point_head.rotate(225)
            pygame.draw.aalines(self.screen, self.colour, True,
                                [point_head + self.pos, point_left + self.pos, self.pos, point_right + self.pos])

    def wrap_around(self):
        """
        Wraps vehicle around the edges
        """
        if self.pos.x < 0:
            self.pos.x = self.screen_width
        elif self.pos.x > self.screen_width:
            self.pos.x = 0
        elif self.pos.y < 0:
            self.pos.y = self.screen_height
        elif self.pos.y > self.screen_height:
            self.pos.y = 0

    def update(self, steering,  wrap_around=True):
        """
        Complete update method of vehicle.

        asseses forces on vehicle and applys them
        """
        self.steering_force += steering
        if self.steering_force.magnitude() > self.max_force:
            self.steering_force.scale_to_length(self.max_force)
        
        self.acc = self.steering_force / self.mass

        self.vel += self.acc
        if self.vel.magnitude() > self.max_spd:
            self.vel.scale_to_length(self.max_spd)

        self.pos += self.vel
        self.pos_xy = (int(self.pos.x), int(self.pos.y))

        if wrap_around:
            self.wrap_around()

        self.draw()  # velocity=True, acceleration=True)

    def seek(self, target):
        """
        seeks given target
        """
        desired_vel = target - self.pos
        desired_vel.scale_to_length(self.max_spd)
        steering = desired_vel - self.vel
        return steering

    def flee(self, target):
        undesired_vel = target - self.pos
        undesired_vel.scale_to_length(self.max_spd)
        steering = -undesired_vel - self.vel
        return steering

    def pursue(self, target, draw=False):
        future_amt = self.pos.distance_to(target.pos)
        speed_ratio = target.vel.magnitude() / self.max_spd
        future_amt = future_amt * speed_ratio
        target_future_pos = Vector2(target.vel)
        target_future_pos.scale_to_length(future_amt)
        target_future_pos += target.pos
        if draw:
            pygame.draw.circle(self.screen, (255, 255, 0), (int(
                target_future_pos.x), int(target_future_pos.y)), 5, 1)
        return self.seek(target_future_pos)

    def pursue_sine_law(self, target, draw=False):
        speed_ratio = target.vel.magnitude() / self.max_spd
        desired = self.pos - target.pos
        target_angle = math.radians(target.vel.angle_to(desired))
        my_angle = math.asin(math.sin(target_angle) * speed_ratio)
        dist = self.pos.distance_to(target.pos)

        sinb = math.sin(math.pi - my_angle - target_angle)
        if sinb == 0:
            prediction = dist
        else:
            prediction = dist * (math.sin(my_angle) /
                                 math.sin(math.pi - my_angle - target_angle))
        new_target = Vector2(target.vel)
        new_target.scale_to_length(prediction)
        if new_target.magnitude() > 1000:
            new_target.scale_to_length(1000)
        new_target += target.pos
        draw_target = (int(new_target.x), int(new_target.y))

        points = [
            [int(target.pos.x), int(target.pos.y)],
            list(draw_target),
            [int(desired.x), int(desired.y)],
        ]
        pygame.draw.aalines(self.screen, self.colour, True, points)

        pygame.draw.circle(self.screen, (0, 255, 0), draw_target, 5, 1)
        return self.seek(new_target)

    def arrive(self, target):
        target_offset = target - self.pos
        distance = target_offset.magnitude()
        ramped_speed = self.max_spd * (distance / self.slowing_distance)
        clipped_speed = min(ramped_speed, self.max_spd)
        desired_vel = (clipped_speed / distance) * target_offset
        steering = desired_vel - self.vel
        return steering

    def wander(self, draw=False):
        wander_strength = 40
        random_displacement = 10
        offset = self.radius * 2 + 20
        wander_centre = Vector2(self.vel)
        wander_centre.scale_to_length(offset + wander_strength)
        wander_centre += self.pos

        if self.displacement == None:
            self.displacement = Vector2((random()*2) - 1, (random()*2) - 1)
            self.displacement.scale_to_length(wander_strength)

        wander_displacement = wander_centre + self.displacement
        random_wander = Vector2((random()*2) - 1, (random()*2) - 1)
        random_wander.scale_to_length(random_displacement)

        self.displacement += random_wander
        self.displacement.scale_to_length(wander_strength)
        target = self.pos + self.displacement

        # wander circle
        if draw:
            pygame.draw.circle(self.screen, self.colour,
                               (int(wander_centre.x), int(wander_centre.y)),
                               wander_strength, 1)

            # wander displacement
            pygame.draw.aaline(self.screen, self.colour, self.pos.xy,
                               (int(wander_displacement.x + random_wander.x),
                                int(wander_displacement.y + random_wander.y)))

            # random radius
            pygame.draw.circle(self.screen, self.colour,
                               (int(wander_displacement.x),
                                int(wander_displacement.y)),
                               random_displacement, 1)

        return self.seek(target)

    def follow_path(self, path_object):
        """
        Needs redoing as its a bit iffy
        """

        distance = 1_000_000
        future_pos = Vector2(self.vel)
        future_pos.scale_to_length(200)
        future_pos += self.pos
        points = path_object.points

        for index in range(len(points) - 1):
            start = points[index]
            end = points[index+1]

            normal_point = self.point_on_line(future_pos, start, end)

            if normal_point.x < start.x or normal_point.x > end.x:
                normal_point = end
            elif normal_point.y < start.y or normal_point.y > end.y:
                normal_point = end

            new_distance = future_pos.distance_to(normal_point)

            if new_distance < distance:
                distance = new_distance
                closest = index

        # for index, point in enumerate(points):
        #     if index == len(points) - 1:
        #         break
        #     new_distance = point.distance_to(future_pos)
        #     if new_distance < distance:
        #         distance = new_distance
        #         closest = index

        # scalar projection
        pos_on_line = self.point_on_line(
            future_pos, points[closest], points[closest+1])

        future_to_normal = future_pos.distance_to(pos_on_line)

        pos_on_line_future = pos_on_line - points[closest]
        pos_on_line_future.scale_to_length(5)
        pos_on_line_future += points[closest]

        if future_to_normal >= path_object.line_width:
            colour = (255, 0, 0)
            steering = self.seek(pos_on_line)
        else:
            colour = self.colour
            steering = Vector2(0)

        draw_normal_pos = (int(pos_on_line.x), int(pos_on_line.y))
        draw_normal_future_pos = (
            int(pos_on_line_future.x), int(pos_on_line_future.y))
        draw_future_pos = (int(future_pos.x), int(future_pos.y))
        pygame.draw.aaline(self.screen, colour,
                           draw_future_pos, draw_normal_pos)
        pygame.draw.circle(self.screen, colour, draw_future_pos, 7, 1)
        pygame.draw.circle(self.screen, colour, draw_normal_pos, 7, 1)
        pygame.draw.circle(self.screen, colour, draw_normal_future_pos, 7, 1)

        return steering

    def point_on_line(self, future_point, start, end):
        ap = future_point - start
        ab = end - start

        ab = ab.normalize()
        dot_product = ap.dot(ab)
        ab *= dot_product

        # start_end_line_dist = start.distance_to(end)

        # if ab.distance_to(end) > start_end_line_dist:
        #     ab.scale_to_length(start_end_line_dist)

        return start + ab

    def obstacle_avoidence(self, obstacles):
        return NotImplementedError()

    def follow_field(self, flowfield):
        return NotImplementedError()

    def unaligned_collision_avoidence(self, targets):
        return NotImplementedError()

    def neighbours(self, targets):
        return NotImplementedError()

    def seperation(self):
        return NotImplementedError()

    def cohesion(self):
        return NotImplementedError()

    def alignment(self):
        return NotImplementedError()

    def leader_follow(self):
        return NotImplementedError()

    def reset(self,):
        self.pos = Vector2(randint(0, self.screen_width),
                           randint(0, self.screen_height))
        # self.vel.rotate_ip(randint(0, 359))
        self.vel = pygame.Vector2((random() * 2) - 1, (random() * 2) - 1)
