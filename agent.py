import random

grid_size = 100

class Agent:
    def __init__(self, id, x, y, scenario, is_collaborative):
        self.id = id
        self.x = x
        self.y = y
        self.targets = []
        self.targets_collected = []
        self.need_to_visit = []
        self.append_coordinates(grid_size, 5)
        self.num_targets_to_win = 0
        self.other_targets = {}
        self.target_coordinates = []
        self.messages = []
        self.other_messages = []
        self.message_printer = ""
        self.buffer = ""
        self.is_collaborative = is_collaborative
        self.sent = False
        self.scenario = scenario
        self.fuel = 500

    def append_coordinates(self, grid_size, detect_range):
        for x in range(detect_range, grid_size, detect_range):
            for y in range(detect_range, grid_size, detect_range):
                self.need_to_visit.append((x, y))
        random.shuffle(self.need_to_visit)

    def set_other_agents_targets(self, agents):
        # update the dictionary with other agents' targets
        for agent in agents:
            if agent != self:
                self.other_targets[agent] = agent.targets

    def send_target_location(self, target, sender):
        remove = target
        if self.is_collaborative == False and self.scenario != "collaborative":  # check if the agent is competitive
            if target[0] > 40 and target[0] < 60 and target[1] > 40 and target[1] < 60:
                opposite_x = random.randint(0, 40)  # get the opposite x-coordinate
                opposite_y = random.randint(0, 40) + 60  # get the opposite y-coordinate
            else:
                opposite_x = grid_size - target[0]  # get the opposite x-coordinate
                opposite_y = grid_size - target[1]  # get the opposite y-coordinate
            target_coords = (opposite_x, opposite_y)  # modify the target location
        else:
            target_coords = target
        sender.messages.append(target_coords)  # send the target location to the sender
        for receiver, targets in self.other_targets.items():
            if target in targets:
                self.message_printer = f"[Agent {self.id} to Agent {receiver.id}] Target at {target_coords}"
                self.other_targets[receiver] = [t for t in targets if t != remove]

    
    def get_messages(self):
        self.buffer = self.message_printer
        self.message_printer = ""
        return self.buffer
    
    def send_message(self, message, sender):
        # send message to all other agents
        sender_id = sender.get_id()
        self.message_printer = f"[Agent {self.id}] {message}"
        for receiver in self.other_targets.keys():
            if receiver.get_id() != sender_id:
                receiver.other_messages.append(message)

    def get_id(self):
        return self.id
    
    def get_position(self):
        return (self.x, self.y)
    
    def get_targets_collected(self):
        return self.targets_collected

    def add_target_collected(self, target):
        self.targets_collected.append(target)

    def move(self):
        if self.fuel <= 0:
            return (self.x, self.y)
        
        self.messages = list(set(self.messages))
        self.closest_target = None
        self.closest_distance = float('inf')
        self.closest_coord = None
        self.closest_dist = float('inf')
        self.is_near_target = False

        
        if ((len(self.targets_collected) == 2) and not self.sent and self.is_collaborative == False and self.scenario == "competitive" and self.fuel > 250) or ((len(self.targets_collected) == 3) and not self.sent and self.is_collaborative == False and self.scenario == "competitive"):
            self.send_message("Collected 4 Targets", self)
            self.sent = True
        
        if "Collected 4 Targets" in self.other_messages and self.is_collaborative == False and self.scenario == "competitive":
            self.fuel -= 100
            self.other_messages.remove("Collected 4 Targets")
    
        
        for agent, targets in self.other_targets.items():
            for target in targets:
                dist_other_target = self.distance_to(target)
                if dist_other_target <= 10:
                    if (self.is_collaborative == True and self.scenario != "competitive") or (self.scenario != "competitive" and self.is_collaborative == False and len(self.targets_collected) == 5):
                        self.send_target_location(target, agent)
                    elif self.is_collaborative == False and self.scenario == "competitive":
                        if target[0] > 40 and target[0] < 60 and target[1] > 40 and target[1] < 60:
                            opposite_x = random.randint(0, 40)  # get the opposite x-coordinate
                            opposite_y = random.randint(0, 40) + 60  # get the opposite y-coordinate
                        else:
                            opposite_x = grid_size - target[0]  # get the opposite x-coordinate
                            opposite_y = grid_size - target[1]  # get the opposite y-coordinate
                        target_coords = (opposite_x, opposite_y)  # modify the target location
                        self.message_printer = f"[Agent {self.id}] Target at {target_coords}"
                        self.other_targets[agent] = [t for t in targets if t != target]
                        for other_agent in self.other_targets.keys():
                            other_agent.messages.append(target_coords)
                        
        # check if there are any targets left
        if self.targets or self.scenario == "collaborative":
            if self.scenario != "collaborative":
                self.fuel -= 1
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
                if distance == 0:
                    # move directly towards the target
                    self.x, self.y = self.closest_target
                    self.add_target_collected(self.closest_target)
                    self.targets.remove(self.closest_target)
                    self.fuel += 300

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

                    if distance == 0:
                        # if the agent is at the target, add the target to the list of targets collected
                        self.add_target_collected(self.closest_target)
                        self.targets.remove(self.closest_target)

                        if self.closest_target in self.need_to_visit:
                            self.need_to_visit.remove(self.closest_target)

                elif self.messages and self.is_collaborative == True:
                    for message_coord in self.messages:
                        distance = self.distance_to(message_coord)
                        if distance < self.closest_dist:
                            self.closest_coord = message_coord
                            self.closest_dist = distance

                    dx = self.closest_coord[0] - self.x
                    dy = self.closest_coord[1] - self.y
                    dist = self.closest_dist
                    if abs(dx) > abs(dy):
                        # move horizontally towards the closest message coordinate
                        if dx > 0:
                            self.x += 1
                        elif dx < 0:
                            self.x -= 1
                    else:
                        # move vertically towards the closest message coordinate
                        if dy > 0:
                            self.y += 1
                        elif dy < 0:
                            self.y -= 1

                    # If the agent is at the message coordinate, remove the message
                    if dist == 0:
                        self.messages.remove(self.closest_coord)
                        
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
                return (self.x, self.y)

    def distance_to(self, target):
        return ((self.x - target[0]) ** 2 + (self.y - target[1]) ** 2) ** 0.5
    
    def __str__(self):
        return f"Agent {self.id} at ({self.x}, {self.y})"
    
    def __repr__(self):
        return self.__str__()