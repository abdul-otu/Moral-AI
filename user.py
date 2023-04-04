import pygame, subprocess

pygame.init()

# Set up the Pygame window
screen = pygame.display.set_mode((500, 400))
pygame.display.set_caption("Scenario Input")

# Set up the font for the input prompt
font = pygame.font.SysFont(None, 35)

# Set up the scenario and number of agents prompts
scenario_prompt = font.render("Enter the scenario:", True, (72,72,72))
num_agents_prompt = font.render("Enter the number of agents:", True, (72,72,72))

num_collaborative_prompt = font.render("Enter the number of collaborative agents", True, (72,72,72))
num_collaborative_prompt2 = font.render("(R for random selection):", True, (72,72,72))

# Initialize the scenario, number of agents, and number of collaborative agents strings
scenario_text = ""
num_agents_text = ""
num_collaborative_text = ""

# Initialize the current prompt
current_prompt = "scenario"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if current_prompt == "scenario":
                    current_prompt = "num_agents"
                elif current_prompt == "num_agents":
                    current_prompt = "num_collaborative"
                elif current_prompt == "num_collaborative":
                    # If user presses enter, call environment.py with the scenario, number of agents, and number of collaborative agents
                    subprocess.call(["python", "environment.py", scenario_text, num_agents_text, num_collaborative_text])
                    pygame.quit()
                    quit()
            elif event.key == pygame.K_BACKSPACE:
                # If user presses backspace, remove last character from current text
                if current_prompt == "scenario":
                    scenario_text = scenario_text[:-1]
                elif current_prompt == "num_agents":
                    num_agents_text = num_agents_text[:-1]
                elif current_prompt == "num_collaborative":
                    num_collaborative_text = num_collaborative_text[:-1]
            elif event.unicode.isalnum() and current_prompt != "scenario":
                # Only allow digits and letters for the number of agents and number of collaborative agents
                if current_prompt == "num_agents":
                    num_agents_text += event.unicode
                elif current_prompt == "num_collaborative":
                    num_collaborative_text += event.unicode
            else:
                # Otherwise, add the pressed key to the current text
                if current_prompt == "scenario":
                    scenario_text += event.unicode

    # Clear the screen and draw the current input prompt and text onto the screen
    screen.fill((183, 201, 226))  # set background color to light blue
    if current_prompt == "scenario":
        prompt_surface = scenario_prompt
        text_surface = font.render(scenario_text, True, (66, 78, 186))
        screen.blit(prompt_surface, (screen.get_width() // 2 - prompt_surface.get_width() // 2,
                                     screen.get_height() // 2 - prompt_surface.get_height() // 2 -60))
        screen.blit(text_surface, (screen.get_width() // 2 - text_surface.get_width() // 2,
                                   screen.get_height() // 2 - text_surface.get_height() // 2))
    elif current_prompt == "num_agents":
        prompt_surface = num_agents_prompt
        text_surface = font.render(num_agents_text, True, (66, 78, 186))
        screen.blit(prompt_surface, (screen.get_width() // 2 - prompt_surface.get_width() // 2,
                                     screen.get_height() // 2 - prompt_surface.get_height() // 2 -60))
        screen.blit(text_surface, (screen.get_width() // 2 - text_surface.get_width() // 2,
                                   screen.get_height() // 2 - text_surface.get_height() // 2))
    elif current_prompt == "num_collaborative":
        prompt_surface = num_collaborative_prompt
        prompt_surface2 = num_collaborative_prompt2
        text_surface = font.render(num_collaborative_text, True, (66, 78, 186))
        screen.blit(prompt_surface, (screen.get_width() // 2 - prompt_surface.get_width() // 2,
                                     screen.get_height() // 2 - prompt_surface.get_height() - 30))
        screen.blit(prompt_surface2, (screen.get_width() // 2 - prompt_surface2.get_width() // 2,
                                     screen.get_height() // 2 - prompt_surface2.get_height() + 10))
        screen.blit(text_surface, (screen.get_width() // 2 - text_surface.get_width() // 2,
                                   screen.get_height() // 2 + text_surface.get_height()))
    pygame.display.update()