import pygame
from agent import Agent
import random

pygame.init()

window_size = (1080, 700)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Multi-Agent System Simulation")

grid_size = 100
cell_size = 7
num_agents = 5


# append an ID to each target
agents = []
for i in range(num_agents):
    x, y = random.randint(0, grid_size-1), random.randint(0, grid_size-1)
    agent = Agent(chr(65+i), x, y)
    targets = []
    for j in range(5):
        target_x, target_y = random.randint(0, grid_size-1), random.randint(0, grid_size-1)
        targets.append((target_x, target_y))
    agent.targets = targets
    agents.append(agent)


winning_agents = {}
running = True

# set the other agents' targets for each agent
for agent in agents:
    agent.set_other_agents_targets(agents)


#num_agents_to_win = int(input("Enter the number of agents required to win: "))
num_agents_to_win =5
font = pygame.font.SysFont(None, 30)

messages = []
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((193, 225, 193))
    
    for agent in agents:
        agent.move()
        this_message = agent.get_messages()
        if this_message != "":
            messages.append((this_message, (0, 0, 0)))

        if len(agent.get_targets_collected()) == 5:
            if agent not in winning_agents.keys():
                text = "Agent " + agent.get_id() + " has collected all targets"
                messages.append((text, (168, 49, 49)))
                winning_agents[agent] = True

        if len(winning_agents) == num_agents_to_win:
            running = False
            break

    # Vertical line
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(700, -2, 704, 704), 2)

    # Message box
    pygame.draw.rect(screen, (42, 170, 138), pygame.Rect(702, 0, 700, 700))

    # Render the messages
    message_y = 15
    for message, color in messages[-26:]:
        message_surface = font.render(message, True, color)
        message_rect = message_surface.get_rect()
        message_rect.left = 705
        message_rect.top = message_y
        screen.blit(message_surface, message_rect)
        message_y += message_rect.height + 5

    for agent in agents:
        color = (0, 0, 0)
        position = agent.get_position()
        x, y = position[0], position[1]
        pygame.draw.circle(screen, color, (x*cell_size+cell_size//2, y*cell_size+cell_size//2), cell_size//2)
        for target in agent.targets:
            pygame.draw.circle(screen, (255, 0, 0), (target[0]*cell_size+cell_size//2, target[1]*cell_size+cell_size//2), cell_size//4)

    pygame.display.update()
    pygame.time.wait(60)

pygame.time.wait(100)
pygame.quit()