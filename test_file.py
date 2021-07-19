        # distance = 1_000_000
        # future_pos = Vector2(self.vel)
        # future_pos.scale_to_length(100)
        # future_pos += self.pos
        # points = path_object.points
        # for index, point in enumerate(points):
        #     if index == len(points) - 1:
        #         break
        #     new_distance = point.distance_to(future_pos)
        #     if new_distance < distance:
        #         distance = new_distance
        #         closest = index

        # pos_on_line = self.point_on_line(future_pos, points[closest], points[closest+1])
        # # scalar projection

        # future_to_normal = future_pos.distance_to(pos_on_line)

        # pos_on_line_future = pos_on_line - points[closest]
        # pos_on_line_future.scale_to_length(5)
        # pos_on_line_future += points[closest]


        # print(closest)

        # if future_to_normal >= path_object.line_width:
        #     # colour = (255,0,0)
        #     steering = self.seek(pos_on_line)
        # else:
        #     # colour = self.colour
        #     steering = Vector2(0)