import pygame
import math
from random import randint
from random import random
from pygame import Vector2
from obstacles import Obstacles
from path import Path as PathFollow


class Vehicle():
    """Class for an autonomous vehicle defined by rules created by;
    Craig W. Reynolds 

    based on the paper;
    Steering Behaviors For Autonomous Characters 
    http://www.red3d.com/cwr/steer/gdc99/
    """

    def __init__(self, screen, x, y):
        """Initalises the class Vehicle"""
        # Screen
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        # Vehicle parameters that effect how forces work on
        # this given vehicle
        self.mass = 1
        self.max_spd = 5
        self.max_force = 0.1
        self.radius = 15

        # Set up vectors and inital forces
        self.pos = Vector2(x, y)
        self.pos_xy = (int(self.pos.x), int(self.pos.y))
        self.vel = Vector2(1)
        self.acc = Vector2(1)
        self.steering_force = Vector2(1)
        self.slowing_distance = ((0.1/self.max_force)*130) * \
            (self.mass) * ((self.max_spd / 5) ** 2)

        # Other
        self.colour = (255, 255, 255)
        self.displacement = None

    def draw(self, circle=False, velocity=False, acceleration=False,
             slowing_field=False, arrow=True):
        """Draws vehicle and information used in some steering behaviors"""
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
        """Wraps vehicle around the edges"""
        if self.pos.x < 0:
            self.pos.x = self.screen_width
        elif self.pos.x > self.screen_width:
            self.pos.x = 0
        elif self.pos.y < 0:
            self.pos.y = self.screen_height
        elif self.pos.y > self.screen_height:
            self.pos.y = 0

    def update(self, steering,  wrap_around=True):
        """Update the vehicle with Steering force and draws Vehicle to Screen."""
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
        self.draw(acceleration=True)  # velocity=True, acceleration=True)

    def get_vector_pos(self, obj):
        """Return a Vector if given Vector or Vehicle Position"""
        if isinstance(obj, Vehicle):
            return obj.pos
        elif isinstance(obj, Vector2):
            return obj
        else:
            raise TypeError(
                f"Invalid Type, Use vehicle or pygame Vector2, got {type(obj)}")

    def check_type_vehicle(self, obj):
        """Raise TypeError if not a Vehicle"""
        if not isinstance(obj, Vehicle):
            raise TypeError(
                f"Incorrect target type: Need Vehicle, got {type(obj)}")

    def seek(self, target):
        """Seeks given target ( Vector2 or Vehicle )"""
        target = self.get_vector_pos(target)
        desired_vel = target - self.pos
        desired_vel.scale_to_length(self.max_spd)
        steering = desired_vel - self.vel
        return steering

    def flee(self, target):
        """Return a steering force that flees from given target
        ( Vector2 or Vehicle )"""
        target = self.get_vector_pos(target)
        undesired_vel = target - self.pos
        undesired_vel.scale_to_length(self.max_spd)
        steering = -undesired_vel - self.vel
        return steering

    def pursue(self, target, draw=False):
        """Returns a steering force pursuing a target"""
        self.check_type_vehicle(target)
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
        """Returns a steering force pursuing a target, uses Sine Law"""
        self.check_type_vehicle(target)
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

        if draw:
            points = [
                [int(target.pos.x), int(target.pos.y)],
                list(draw_target),
                [int(desired.x), int(desired.y)],
            ]
            pygame.draw.aalines(self.screen, self.colour, True, points)
            pygame.draw.circle(self.screen, (0, 255, 0), draw_target, 5, 1)

        return self.seek(new_target)

    def arrive(self, target):
        """Return steering force that allows vehicle to precisly arrive at given target"""
        target = self.get_vector_pos(target)
        target_offset = target - self.pos
        distance = target_offset.magnitude()
        ramped_speed = self.max_spd * (distance / self.slowing_distance)
        clipped_speed = min(ramped_speed, self.max_spd)
        desired_vel = (clipped_speed / distance) * target_offset
        steering = desired_vel - self.vel
        return steering

    def wander(self, draw=False):
        """Wander smoothly in a random direction"""
        wander_strength = 40
        random_displacement = 10
        offset = self.radius * 2 + 20

        # find point in front of vehicle
        wander_centre = Vector2(self.vel)
        wander_centre.scale_to_length(offset + wander_strength)
        wander_centre += self.pos

        # if no displacement yet, make a random one.
        if self.displacement == None:
            self.displacement = Vector2((random()*2) - 1, (random()*2) - 1)
            self.displacement.scale_to_length(wander_strength)

        wander_displacement = wander_centre + self.displacement
        random_wander = Vector2((random()*2) - 1, (random()*2) - 1)
        random_wander.scale_to_length(random_displacement)

        # add new displacment to old displacement create seek target
        self.displacement += random_wander
        self.displacement.scale_to_length(wander_strength)
        target = self.pos + self.displacement

        # wander circle - for visual aid in how it works, and debug
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

    def follow_path(self, path_object, draw=False):
        """NOT FULLY IMPLEMENTED - Needs redoing as its a bit iffy"""
        if not isinstance(path_object, PathFollow):
            raise TypeError(f"Expected a Path object, got {type(path_object)}")
        distance = 1_000_000
        future_pos = Vector2(self.vel)
        future_pos.scale_to_length(200)
        future_pos += self.pos
        points = path_object.points

        # run through points and find closest normal scalar point.
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

        if draw:
            draw_normal_pos = (int(pos_on_line.x), int(pos_on_line.y))
            draw_normal_future_pos = (
                int(pos_on_line_future.x), int(pos_on_line_future.y))
            draw_future_pos = (int(future_pos.x), int(future_pos.y))
            pygame.draw.aaline(self.screen, colour,
                               draw_future_pos, draw_normal_pos)
            pygame.draw.circle(self.screen, colour, draw_future_pos, 7, 1)
            pygame.draw.circle(self.screen, colour, draw_normal_pos, 7, 1)
            pygame.draw.circle(self.screen, colour,
                               draw_normal_future_pos, 7, 1)

        return steering

    def point_on_line(self, future_point, start, end):
        """return a vector of a scalar projection from a point on a line."""
        ap = future_point - start
        ab = end - start
        ab = ab.normalize()
        dot_product = ap.dot(ab)
        ab *= dot_product
        return start + ab

    def obstacle_avoidence(self, obstacles, draw=False):
        if not isinstance(obstacles, Obstacles) and not isinstance(obstacles, list):
            raise TypeError("Expected Obstacal Object or list of Obstacles")
        elif isinstance(obstacles, Obstacles):
            obstacles = [obstacles]

        max_point = Vector2(self.vel)
        max_point.scale_to_length(self.slowing_distance + self.radius * 2)
        max_point += self.pos

        closest = self.slowing_distance
        obj_index = None

        for index, obstacle in enumerate(obstacles):
            obstacle_in_way = self.point_on_line(
                obstacle.pos, self.pos, max_point)
            scal_proj_dist_to_obs = self.pos.distance_to(obstacle_in_way)
            scal_proj_dist_to_obs -= obstacle.radius
            in_radius = obstacle_in_way.distance_to(
                obstacle.pos) < self.radius + obstacle.radius
            angle = -90 < self.vel.angle_to(obstacle.pos - self.pos) < 90
            if scal_proj_dist_to_obs < closest and in_radius and angle:
                closest = scal_proj_dist_to_obs
                obj_index = index

        if draw:
            if obj_index == None:
                colour = self.colour
            else:
                colour = (255, 0, 0)

            point_r1 = Vector2(self.vel)
            point_r1.rotate_ip(90)
            point_r1.scale_to_length(self.radius)
            point_r1 += self.pos
            point_r1 = (int(point_r1.x), int(point_r1.y))

            point_l1 = Vector2(self.vel)
            point_l1.rotate_ip(270)
            point_l1.scale_to_length(self.radius)
            point_l1 += self.pos
            point_l1 = (int(point_l1.x), int(point_l1.y))

            point_r2 = Vector2(self.vel)
            point_r2.scale_to_length(self.radius)
            point_r2.rotate_ip(90)
            point_r2 += max_point
            point_r2 = (int(point_r2.x), int(point_r2.y))

            point_l2 = Vector2(self.vel)
            point_l2.rotate_ip(270)
            point_l2.scale_to_length(self.radius)
            point_l2 += max_point
            point_l2 = (int(point_l2.x), int(point_l2.y))

            points = [point_l1, point_r1, point_r2, point_l2]
            pygame.draw.aalines(self.screen, colour, True, points)

        forward = Vector2(self.vel)
        forward.scale_to_length(self.max_spd)
        if obj_index == None:
            return forward
        # else:
        #     return self.flee(obstacles[obj_index].pos)
        
        else:
            obstacles[obj_index].colour = (255, 0, 0)
            obstacle = obstacles[obj_index].pos
            angle = self.vel.angle_to(obstacle - self.pos)
            print(angle)
            desired = Vector2(self.vel)
            desired.scale_to_length(self.max_spd)
            desired.rotate_ip(360 - angle)

            # pygame.draw.aaline(self.screen, self.)
            return desired - self.vel

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

    def reset(self):
        """Resets target to random location with random Velocity"""
        self.pos = Vector2(randint(0, self.screen_width),
                           randint(0, self.screen_height))
        self.vel = pygame.Vector2((random() * 2) - 1, (random() * 2) - 1)
