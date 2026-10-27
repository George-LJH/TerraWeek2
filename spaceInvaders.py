import pygame
import sys
import json
import js
import asyncio

def save(key: str, data_list: list):
  json_string = json.dumps(data_list)
  js.localStorage.setItem(key, json_string)


def load(key: str) -> list:
  item = js.localStorage.getItem(key)
  if item and item != "null":
    try:
      parsed = json.loads(item)
      if isinstance(parsed, list):
        return parsed
    except (json.JSONDecodeError, TypeError):
      pass
  return []

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
font = pygame.font.Font("spaceInvadersFont.ttf", 36)

text_surface = font.render(
    "Hello! Testing Font 12345", True, (255, 255, 255)
)
text_rect = text_surface.get_rect(center=(screenWidth // 2, screenHeight // 2))
#Setup variables
gameStarted = False

# Game Loop
running = True
leaderboard = load("leaderboard")
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
        pass
    else:
        # Draw game objects
        pass
    screen.blit(text_surface, text_rect)
    window.flip()
    await asyncio.sleep(1 / fps)

# Clean Up & Exit
pygame.quit()
sys.exit()
