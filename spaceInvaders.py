import pygame
import sys
import json
import js
import asyncio
def save(key, value):
    """Saves a key-value pair to browser localStorage."""
    js.localStorage.setItem(str(key), str(value))

def load(key):
    """
    Loads a value from browser localStorage by key.
    """
    val = js.localStorage.getItem(str(key))
    if type(val) != int:
        return 0
    return int(val)


# Initialize Pygame
pygame.init()

# Game Constants
screenWidth = 945
screenHeight = 1080
# Setup window
window = pygame.Window(size=(screenWidth, screenHeight))
window.title = "Space Invaders - Game"
screen = window.get_surface()
fps = 60
scoreFont = pygame.font.Font("spaceInvadersFont.ttf", 20)
#Setup variables
gameStarted = False
playerScore = 0
# Game Loop
running = True
# restart game
def resetGame():
    # variables to rest
    gameStarted = False
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
        scoreText = scoreFont.render("Score<1>", True, (255, 255, 255))

        hiScoreText = scoreFont.render("Hi-Score", True, (255, 255, 255))
        hiScoreRect = hiScoreText.get_rect()
        hiScoreRect.topright = (935, 10)

        currentScoreText = scoreFont.render(str(playerScore), True, (255, 255, 255))

        hiScore = load("hiScore")
        currentHiScoreText = scoreFont.render(str(hiScore), True, (255, 255, 255))
        currentHiScoreRect = currentHiScoreText.get_rect()
        currentHiScoreRect.topright = (935, 60)
        screen.blit(scoreText, (10, 10))
        screen.blit(hiScoreText, hiScoreRect)
        screen.blit(currentScoreText, (10, 60))
        screen.blit(currentHiScoreText, currentHiScoreRect)
    else:
        # Draw game objects
        pass
    window.flip()
    await asyncio.sleep(1 / fps)

# Clean Up & Exit
pygame.quit()
sys.exit()
