from random import randint
import pygame
from pygame import Vector2



class Path():
    def __init__(self, screen,  points=None):
        self.points = []
        if points == None:
            old_points = [(0, 469), (100, 493), (200, 507), (300, 441), (400, 587), (500, 435), (600, 525), (700, 464), (800, 403), (900, 511), (1000, 553), (1100, 451), (1200, 447), (1300, 513), (1400, 541), (1500, 469), (1600, 469)]
            for i in old_points:
                self.points.append(Vector2(i))
        else:
            for point in points:
                self.points.append(Vector2(point))

        self.colour = (150,150,150)
        self.screen = screen
        self.screen_width = self.screen.get_width()
        self.line_width = 15
        self.screen_height = self.screen.get_height()

    def append_point(self, point):
        if isinstance(self.points, set):
            self.points.add(point)
        else:
            self.points.append(point)

    def new_path (self,rand_start=False):
        devience = randint(0,100)
        self.points = []
        point_range = 32

        for x in range(point_range + 2):
            if len(self.points) == 0 and rand_start:
                self.points.append(Vector2(0,randint(0,1000)))
            elif len(self.points) == 0 and not rand_start:
                self.points.append(Vector2(0,500))
            else:
                var = self.points[len(self.points) - 1][1]
                point = Vector2((x * (self.screen_width / point_range),randint(var - devience, var + devience)))
                self.points.append(point)
        print(self.points)

    def draw(self):
        for index, pos in enumerate(self.points):
            if isinstance(pos, Vector2):
                pos = (int(pos.x),int(pos.y))
            
            if index == len(self.points)-1:
                pygame.draw.circle(self.screen,self.colour, pos, self.line_width, 1)
                break

            # get vectors for current and next points
            # and construct a vector between 
            current_point = Vector2(self.points[index])
            next_point = Vector2(self.points[index + 1])
            intermedite_line = next_point - current_point
            
            # Left line and a distance of given line width from path line
            l_line_start = intermedite_line.rotate(-90)  # anticlockwise
            l_line_start.scale_to_length(self.line_width)
            l_line_start += current_point 
            l_line_stop = l_line_start + intermedite_line

            # Right line, same as left, but on the right... duh
            r_line_start = intermedite_line.rotate(90)
            r_line_start.scale_to_length(self.line_width)
            r_line_start += current_point
            r_line_stop = r_line_start + intermedite_line

            pygame.draw.circle(self.screen,self.colour, pos, self.line_width, 1)
            pygame.draw.aaline(self.screen, self.colour, l_line_start.xy, l_line_stop.xy)
            pygame.draw.aaline(self.screen, self.colour, r_line_start.xy, r_line_stop.xy)

        pygame.draw.aalines(self.screen, self.colour, False, self.points,)

