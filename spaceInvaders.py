import pygame
import sys

# Initialize Pygame
pygame.init()

# Game Constants
screenWidth = 800
screenHeight = 600
# Setup window
window = pygame.Window(size=(screenWidth, screenHeight))
window.title = "Space Invaders - Game"
screen = window.get_surface()
fps = 60

#Setup variables
gameStarted = False

# Game Loop
running = True

# restart game
def resetGame:
    # variables to rest
    gameStarted = False
    pass
while running:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Game Logic Updates
    # (Update positions, check collisions, etc.)

    # 3. Drawing / Rendering
    screen.fill((0, 0, 0))  # Clear screen with black background
    
    # (Draw your objects here)
    if not gameStarted:
        # Draw start screen
        pass
    else:
        # Draw game objects
        pass
    window.flip()
    await asyncio.sleep(1 / fps)

# Clean Up & Exit
pygame.quit()
sys.exit()
