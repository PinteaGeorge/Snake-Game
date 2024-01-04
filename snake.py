import pygame
import sys
import ctypes
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 800, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Set up colors
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
lime = (0, 255, 0)
pink = (255, 182, 193)
dark_blue = (0, 0, 128)
dark_green = (0, 128, 0)
orange = (255, 165, 0)
purple = (128, 0, 128)
gray = (128,128,128)

# Fonts
font = pygame.font.SysFont(None, 30)

# Set up buttons
play_button = pygame.Rect(width // 2 - 50, height // 2 - 50, 100, 40)
how_to_play_button = pygame.Rect(width // 2 - 100, height // 2 + 20, 200, 40)
about_button = pygame.Rect(width // 2 - 50, height // 2 + 90, 100, 40)
settings_button = pygame.Rect(width // 2 - 50, height // 2 + 160, 100, 40)
quit_button = pygame.Rect(width // 2 - 50, height // 2 + 230, 100, 40)

# Set up end screen buttons
play_again_button = pygame.Rect(width // 2 - 75, height // 2 - 50, 150, 40)
back_to_main_button = pygame.Rect(width // 2 - 75, height // 2 + 20, 150, 40)

# Set up about page button
back_to_main_about_button = pygame.Rect(width // 2 - 75, height - 50, 150, 40)

# Set up how to play page button
back_to_main_how_to_play_button = pygame.Rect(width // 2 - 75, height - 50, 150, 40)

# Set up settings page button
back_to_main_settings_button = pygame.Rect(width // 2 - 75, height - 50, 150, 40)

# Set up resolution dropdown
resolution_options = [(800, 600), (1024, 720), (1366, 768)]  # Add more resolutions as needed
selected_resolution = resolution_options[0]
resolution_dropdown_button = pygame.Rect(width // 2 - 125, height // 4 + 120, 250, 40)
resolution_dropdown_expanded = False

snake_color_options = [white, blue, red, yellow, green, lime, pink, dark_blue, dark_green, orange, purple]
selected_snake_color = white

# Set up snake
snake_score = 0
snake_block = 10
snake_speed = 10

# Set up food properties
food = [{"color": red, "effect": "+1 Point", "spawn_rate": 0.4},
        {"color": yellow, "effect": "Double Points", "spawn_rate": 0.20},
        {"color": blue, "effect": "Triple Points", "spawn_rate": 0.13},
        {"color": orange, "effect": "Fast", "spawn_rate": 0.15},
        {"color": purple, "effect": "Slow", "spawn_rate": 0.12},]

# Game state
in_menu = True
in_game = False
in_about = False
in_how_to_play = False
in_end_screen = False
in_settings = False

# Function to spawn food with random properties
def spawn_food():
    x = random.randrange(0, width - snake_block, snake_block)
    y = random.randrange(0, height - snake_block, snake_block)
    
    # Randomly choose food color, spawn rate, and effect
    food_properties = random.choices(food, weights=[item["spawn_rate"] for item in food])[0]
    color = food_properties["color"]
    effect = food_properties["effect"]

    return (x, y), color, effect

food_position, food_color, food_effect = spawn_food()

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            mouse_pos = event.pos
            if in_menu:
                if play_button.collidepoint(mouse_pos):
                    in_menu = False
                    in_game = True
                    in_end_screen = False  # Reset end screen state
                    snake_score = 0
                    snake = [(width // 2, height // 2)]  # Reset snake position
                    snake_direction = "RIGHT"  # Reset snake direction
                    food_position = (width // 4, height // 4)
                    in_how_to_play = False
                    in_settings = False
                elif how_to_play_button.collidepoint(mouse_pos):
                    in_menu = False
                    in_game = False
                    in_end_screen = False  # Reset end screen state
                    in_how_to_play = True
                    in_settings = False
                elif about_button.collidepoint(mouse_pos):
                    in_menu = False
                    in_about = True
                    in_end_screen = False  # Reset end screen state
                    in_how_to_play = False
                    in_settings = False
                elif settings_button.collidepoint(mouse_pos):
                    in_menu = False
                    in_about = False
                    in_end_screen = False  # Reset end screen state
                    in_how_to_play = False 
                    in_settings = True
                elif quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
            elif in_end_screen:
                if play_again_button.collidepoint(mouse_pos):
                    in_end_screen = False
                    in_game = True
                    snake_score = 0
                    snake = [(width // 2, height // 2)]  # Reset snake position
                    snake_direction = "RIGHT"  # Reset snake direction
                    food_position = (width // 4, height // 4)
                elif back_to_main_button.collidepoint(mouse_pos):
                    in_end_screen = False
                    in_menu = True
                    in_how_to_play = False
                    in_game = False
            elif in_about:
                if back_to_main_about_button.collidepoint(mouse_pos):
                    in_about = False
                    in_menu = True
            elif in_how_to_play:
                if back_to_main_how_to_play_button.collidepoint(mouse_pos):
                    in_how_to_play = False
                    in_menu = True
            elif in_settings:
                # Check color selection in settings page
                for i, color_rect in enumerate(snake_color_rects):
                    if color_rect.collidepoint(mouse_pos):
                        selected_snake_color = snake_color_options[i]
                        break
                if back_to_main_settings_button.collidepoint(mouse_pos):
                    in_about = False
                    in_menu = True
                    in_how_to_play = False
                    in_settings = False
    
    if in_menu:
        # Draw menu
        win.fill(black)
        pygame.draw.rect(win, white, play_button)
        pygame.draw.rect(win, white, how_to_play_button)
        pygame.draw.rect(win, white, about_button)
        pygame.draw.rect(win, white, settings_button)
        pygame.draw.rect(win, white, quit_button)

        # Draw text on buttons
        play_text = font.render("Play", True, black)
        how_to_play_text = font.render("How to play", True, black)
        about_text = font.render("About", True, black)
        settings_text = font.render("Settings", True, black)
        quit_text = font.render("Quit", True, black)

        # Calculate text positions for centering on buttons
        play_text_pos = (play_button.centerx - play_text.get_width() // 2, play_button.centery - play_text.get_height() // 2)
        how_to_play_text_pos = (how_to_play_button.centerx - how_to_play_text.get_width() // 2, how_to_play_button.centery - how_to_play_text.get_height() // 2)
        about_text_pos = (about_button.centerx - about_text.get_width() // 2, about_button.centery - about_text.get_height() // 2)
        settings_text_pos = (settings_button.centerx - settings_text.get_width() // 2, settings_button.centery - settings_text.get_height() // 2)
        quit_text_pos = (quit_button.centerx - quit_text.get_width() // 2, quit_button.centery - quit_text.get_height() // 2)

        win.blit(play_text, play_text_pos)
        win.blit(how_to_play_text, how_to_play_text_pos)
        win.blit(about_text, about_text_pos)
        win.blit(settings_text, settings_text_pos)
        win.blit(quit_text, quit_text_pos)

    elif in_game:
        # Draw everything
        win.fill(black)  # Clear the screen with a black background

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and snake_direction != "DOWN":
            snake_direction = "UP"
        elif keys[pygame.K_s] and snake_direction != "UP":
            snake_direction = "DOWN"
        elif keys[pygame.K_a] and snake_direction != "RIGHT":
            snake_direction = "LEFT"
        elif keys[pygame.K_d] and snake_direction != "LEFT":
            snake_direction = "RIGHT"

        # Update snake position based on the direction
        x, y = snake[0]
        if snake_direction == "UP":
            y -= snake_block
        elif snake_direction == "DOWN":
            y += snake_block
        elif snake_direction == "LEFT":
            x -= snake_block
        elif snake_direction == "RIGHT":
            x += snake_block

        # Check if the snake collides with the boundaries
        if x < 0 or x >= width or y < 0 or y >= height:
            pygame.time.delay(250)
            in_game = False
            in_end_screen = True

        # Check if the snake collides with itself
        if (x, y) in snake[1:]:
            pygame.time.delay(250)
            in_game = False
            in_end_screen = True

        # Check if the snake eats the food
        if (x, y) == food_position:
            if food_color == (255, 0, 0): #red
                snake_score += 1
            elif food_color == (255, 255, 0): #yellow
                if snake_score == 0:
                    snake_score = 2
                else:
                    snake_score *= 2
            elif food_color == (0, 0, 255): #blue
                if snake_score == 0:
                    snake_score = 3
                else:
                    snake_score *= 3
            elif food_color == (255, 165, 0): #orange
                snake_speed += 5
            elif food_color == (128, 0, 128): #purple
                snake_speed -= 5
            # Spawn new food with random properties
            food_position, food_color, food_effect = spawn_food()
        else:
            snake.pop()

        # Update snake position
        snake.insert(0, (x, y))

        # Draw everything
        pygame.draw.rect(win, food_color, (*food_position, snake_block, snake_block))

        for segment in snake:
            pygame.draw.rect(win, selected_snake_color, (*segment, snake_block, snake_block))

        # Display the food effect
        effect_text = font.render(f"Effect: {food_effect}", True, white)
        win.blit(effect_text, (10, 30))

        # Display the score
        score_text = font.render(f"Score: {snake_score}", True, white)
        win.blit(score_text, (10, 10))
    
    elif in_how_to_play:
        # Draw "How to Play" page
        text = "How To Play fsdjf sj sdj sldj fsdlj flsdk jsd jfslkaf jsldf jsdlf jsd fsjlf jsdkl fsdf seioewroweroweu rosd usdof sdof usdf"

        # Wrap text to fit within the window width
        lines = []
        words = text.split()
        current_line = words[0]
        for word in words[1:]:
            if font.size(current_line + ' ' + word)[0] < width - 50:  # 50 is the margin
                current_line += ' ' + word
            else:
                lines.append(current_line)
                current_line = word

        # Append the last line
        lines.append(current_line)

        # Calculate total height of the text block
        total_height = len(lines) * font.get_height()

        # Draw "About" page
        win.fill(black)
        y = (height - total_height) // 2
        for line in lines:
            text = font.render(line, True, white)
            win.blit(text, (width // 2 - text.get_width() // 2, y))
            y += font.get_height()

        # Draw back to main page button
        pygame.draw.rect(win, white, back_to_main_how_to_play_button)
        back_to_main_how_to_play_text = font.render("Back", True, black)
        back_to_main_how_to_play_text_pos = (back_to_main_how_to_play_button.centerx - back_to_main_how_to_play_text.get_width() // 2, back_to_main_how_to_play_button.centery - back_to_main_how_to_play_text.get_height() // 2)
        win.blit(back_to_main_how_to_play_text, back_to_main_how_to_play_text_pos)
    
    elif in_about:
        # Draw "About" page
        about_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean feugiat pretium ante, vel fringilla tellus ornare eget. Suspendisse tincidunt magna ac mi ornare, sed elementum elit auctor. Phasellus nec molestie orci, sit amet condimentum urna. Curabitur aliquet enim a urna rutrum vehicula. Morbi vitae luctus leo, id congue odio. In sollicitudin nibh ac elit posuere imperdiet nec eu magna. Sed facilisis nisl vitae erat convallis rutrum. Phasellus semper lacus ac dapibus volutpat."

        # Wrap text to fit within the window width
        lines = []
        words = about_text.split()
        current_line = words[0]
        for word in words[1:]:
            if font.size(current_line + ' ' + word)[0] < width - 50:  # 50 is the margin
                current_line += ' ' + word
            else:
                lines.append(current_line)
                current_line = word

        # Append the last line
        lines.append(current_line)

        # Calculate total height of the text block
        total_height = len(lines) * font.get_height()

        # Draw "About" page
        win.fill(black)
        y = (height - total_height) // 2
        for line in lines:
            about_text = font.render(line, True, white)
            win.blit(about_text, (width // 2 - about_text.get_width() // 2, y))
            y += font.get_height()

        # Draw back to main page button
        pygame.draw.rect(win, white, back_to_main_about_button)
        back_to_main_about_text = font.render("Back", True, black)
        back_to_main_about_text_pos = (back_to_main_about_button.centerx - back_to_main_about_text.get_width() // 2, back_to_main_about_button.centery - back_to_main_about_text.get_height() // 2)
        win.blit(back_to_main_about_text, back_to_main_about_text_pos)

    elif in_end_screen:
        # Draw end screen
        win.fill(black)
        pygame.draw.rect(win, white, play_again_button)
        pygame.draw.rect(win, white, back_to_main_button)

        # Draw text on buttons
        play_again_text = font.render("Play Again", True, black)
        back_to_main_text = font.render("Back", True, black)

        # Calculate text positions for centering on buttons
        play_again_text_pos = (play_again_button.centerx - play_again_text.get_width() // 2, play_again_button.centery - play_again_text.get_height() // 2)
        back_to_main_text_pos = (back_to_main_button.centerx - back_to_main_text.get_width() // 2, back_to_main_button.centery - back_to_main_text.get_height() // 2)

        win.blit(play_again_text, play_again_text_pos)
        win.blit(back_to_main_text, back_to_main_text_pos)
        
        end_screen_text = font.render(f"Score: {snake_score}", True, white)
        win.blit(end_screen_text, (width // 2 - end_screen_text.get_width() // 2, height // 4))

    elif in_settings:
        # Draw settings page
        win.fill(black)

        # Draw snake color options
        snake_color_rects = []
        snake_color_text = font.render("Snake Color", True, white)
        win.blit(snake_color_text, (width // 8 - snake_color_text.get_width() // 2, height // 8))
        for i, color in enumerate(snake_color_options):
            rect = pygame.Rect((i * 60) + 20, height // 4 + 30, 50, 50)
            pygame.draw.rect(win, color, rect)
            pygame.draw.rect(win, gray if color == selected_snake_color else white, rect, 2)
            snake_color_rects.append(rect)
        
        # Draw resolution dropdown
        pygame.draw.rect(win, white, resolution_dropdown_button)
        resolution_text = font.render(f"Resolution: {selected_resolution[0]} x {selected_resolution[1]}", True, black)
        resolution_text_pos = (resolution_dropdown_button.centerx - resolution_text.get_width() // 2, resolution_dropdown_button.centery - resolution_text.get_height() // 2)
        win.blit(resolution_text, resolution_text_pos)

        if resolution_dropdown_expanded:
            # Draw dropdown options
            dropdown_options_rects = []
            for i, resolution_option in enumerate(resolution_options):
                rect = pygame.Rect(resolution_dropdown_button.left, resolution_dropdown_button.bottom + i * 40, resolution_dropdown_button.width, 40)
                pygame.draw.rect(win, white, rect)
                pygame.draw.rect(win, gray if resolution_option == selected_resolution else white, rect, 2)
                dropdown_options_rects.append(rect)

                # Draw resolution options text
                option_text = font.render(f"{resolution_option[0]} x {resolution_option[1]}", True, black)
                option_text_pos = (rect.centerx - option_text.get_width() // 2, rect.centery - option_text.get_height() // 2)
                win.blit(option_text, option_text_pos)

            # Check for dropdown option selection
            for i, option_rect in enumerate(dropdown_options_rects):
                if option_rect.collidepoint(mouse_pos):
                    selected_resolution = resolution_options[i]
                    resolution_dropdown_expanded = False
                   
                    # Update window size
                    width, height = selected_resolution
                    win = pygame.display.set_mode((width, height))

                    # Center the window on the screen (Windows only)
                    user32 = ctypes.windll.user32
                    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
                    x = screensize[0] // 2 - width // 2
                    y = screensize[1] // 2 - height // 2
                    hwnd = pygame.display.get_wm_info()["window"]
                    user32.SetWindowPos(hwnd, 0, x, y, 0, 0, 0x0001)
            
        # Check if the dropdown button is clicked to toggle dropdown expansion
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and resolution_dropdown_button.collidepoint(mouse_pos):
            resolution_dropdown_expanded = not resolution_dropdown_expanded

        # Draw back to main menu button
        pygame.draw.rect(win, white, back_to_main_settings_button)
        back_to_menu_text = font.render("Back", True, black)
        back_to_menu_text_pos = (back_to_main_settings_button.centerx - back_to_menu_text.get_width() // 2, back_to_main_settings_button.centery - back_to_menu_text.get_height() // 2)
        win.blit(back_to_menu_text, back_to_menu_text_pos)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    pygame.time.Clock().tick(snake_speed)