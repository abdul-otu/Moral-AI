import pygame
from agent import Agent
import random

pygame.init()

window_size = (1050, 700)
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

num_agents_to_win = int(input("Enter the number of agents required to win: "))
font = pygame.font.SysFont(None, 30)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    
    for agent in agents:
        agent.move()

        if len(agent.get_targets_collected()) == 5:
            if agent not in winning_agents.keys():
                text = "Agent " + agent.get_id() + " has collected all targets"
                text_surface = font.render(text, True, (0, 0, 0))
                text_rect = text_surface.get_rect()
                text_rect.right = window_size[0] - 10
                text_rect.top = len(winning_agents) * 30 + 10
                winning_agents[agent] = (text_surface, text_rect)

        if len(winning_agents) == num_agents_to_win:
            running = False
            break
    
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(700, -2, 704, 704), 2)
    pygame.draw.rect(screen, (211, 211, 211), pygame.Rect(702, 0, 700, 700))
    for agent in agents:
        color = (0, 0, 255)
        position = agent.get_position()
        x, y = position[0], position[1]
        pygame.draw.circle(screen, color, (x*cell_size+cell_size//2, y*cell_size+cell_size//2), cell_size//2)
        for target in agent.targets:
            pygame.draw.circle(screen, (255, 0, 0), (target[0]*cell_size+cell_size//2, target[1]*cell_size+cell_size//2), cell_size//4)

    for agent, (text_surface, text_rect) in winning_agents.items():
        screen.blit(text_surface, text_rect)
    
    pygame.display.update()
    pygame.time.wait(100)

pygame.time.wait(1000)
pygame.quit()
