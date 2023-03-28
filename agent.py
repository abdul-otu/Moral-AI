import math
import random

grid_size = 100

class Agent:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.targets = []
        self.targets_collected = []
        self.need_to_visit = []
        self.append_coordinates(grid_size, 5)
        self.num_targets_to_win = 0

    def append_coordinates(self, grid_size, detect_range):
        for x in range(detect_range, grid_size, detect_range):
            for y in range(detect_range, grid_size, detect_range):
                self.need_to_visit.append((x, y))
        random.shuffle(self.need_to_visit)

    def get_id(self):
        return self.id
    
    def get_position(self):
        return (self.x, self.y)
    
    def get_targets_collected(self):
        return self.targets_collected

    def add_target_collected(self, target):
        self.targets_collected.append(target)

    def move(self):
        self.closest_target = None
        self.closest_distance = float('inf')
        self.closest_coord = None
        self.closest_dist = float('inf')
        self.is_near_target = False

        # check if there are any targets left
        if self.targets:
            # find the closest target
            for target in self.targets:
                distance = self.distance_to(target)
                if distance < self.closest_distance and distance <= 10:
                    self.closest_target = target
                    self.closest_distance = distance

            if self.closest_target:
                dx = self.closest_target[0] - self.x
                dy = self.closest_target[1] - self.y
                distance = self.closest_distance
                if distance == 1:
                    # move directly towards the target
                    self.x, self.y = self.closest_target
                    self.add_target_collected(self.closest_target)
                    self.targets.remove(self.closest_target)

                    # remove the target from the need_to_visit list if it is in there
                    if self.closest_target in self.need_to_visit:
                        self.need_to_visit.remove(self.closest_target)
                else:
                    # move towards the closest target
                    if abs(dx) > abs(dy):
                        # move horizontally towards the target
                        self.x += int(dx / abs(dx))
                    else:
                        # move vertically towards the target
                        self.y += int(dy / abs(dy))
            else:
                # check if the agent is near a target
                for target in self.targets:
                    if self.distance_to(target) <= 10:
                        self.is_near_target = True
                        break

                if self.is_near_target:
                    # move towards the closest target
                    for target in self.targets:
                        distance = self.distance_to(target)
                        if distance < self.closest_distance and distance <= 10:
                            self.closest_target = target
                            self.closest_distance = distance

                    dx = self.closest_target[0] - self.x
                    dy = self.closest_target[1] - self.y
                    distance = self.closest_distance
                    if abs(dx) > abs(dy):
                        # move horizontally towards the target
                        self.x += int(dx / abs(dx))
                    else:
                        # move vertically towards the target
                        self.y += int(dy / abs(dy))

                    if distance == 1:
                        # if the agent is at the target, add the target to the list of targets collected
                        self.add_target_collected(self.closest_target)
                        self.targets.remove(self.closest_target)

                        if self.closest_target in self.need_to_visit:
                            self.need_to_visit.remove(self.closest_target)
                else:
                    # find the closest coordinate in need_to_visit
                    for coordinate in self.need_to_visit:
                        dist = self.distance_to(coordinate)
                        if dist < self.closest_dist:
                            self.closest_coord = coordinate
                            self.closest_dist = dist

                    # move towards the closest coordinate
                    dx = self.closest_coord[0] - self.x
                    dy = self.closest_coord[1] - self.y
                    dist = self.closest_dist
                    if abs(dx) > abs(dy):
                        # move horizontally towards the closest coordinate
                        if dx > 0:
                            self.x += 1
                        elif dx < 0:
                            self.x -= 1
                    else:
                        # move vertically towards the closest coordinate
                        if dy > 0:
                            self.y += 1
                        elif dy < 0:
                            self.y -= 1

                    if dist == 1:
                        self.need_to_visit.remove(self.closest_coord)
        else:
            # find the closest coordinate in need_to_visit
                for coordinate in self.need_to_visit:
                    dist = self.distance_to(coordinate)
                    if dist < self.closest_dist:
                        self.closest_coord = coordinate
                        self.closest_dist = dist

                # move towards the closest coordinate
                dx = self.closest_coord[0] - self.x
                dy = self.closest_coord[1] - self.y

                # check if the movement is vertical or horizontal only
                if abs(dx) > abs(dy):
                    # move horizontally towards the closest coordinate
                    if dx > 0:
                        self.x += 1
                    elif dx < 0:
                        self.x -= 1
                else:
                    # move vertically towards the closest coordinate
                    if dy > 0:
                        self.y += 1
                    elif dy < 0:
                        self.y -= 1

                if (self.x, self.y) == self.closest_coord:
                    self.need_to_visit.remove(self.closest_coord)

                return (self.x, self.y)


                

    def distance_to(self, target):
        return ((self.x - target[0]) ** 2 + (self.y - target[1]) ** 2) ** 0.5
    
    
    def __str__(self):
        return f"Agent {self.id} at ({self.x}, {self.y})"
    
    def __repr__(self):
        return self.__str__()