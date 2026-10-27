import pygame
import sys
import json
import js
import asyncio
def save(key, value):
    js.localStorage.setItem(str(key), str(value))

def load(key):
    val = js.localStorage.getItem(str(key))
    if val is None: 
        return 0
    try:
        return int(val)
    except (ValueError, TypeError):
        return 0

def font(size):
    return pygame.font.Font("spaceInvadersFont.ttf", size)

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
coins = 0

Point10 = pygame.image.load('10Points.png').convert()
Point10 = pygame.transform.smoothscale_by(Point10, 0.4)
Point10.set_colorkey((0, 0, 0))
Point10Rect = Point10.get_rect()

Point20 = pygame.image.load('20Points.png').convert()
Point20 = pygame.transform.smoothscale_by(Point20, 0.4)
Point20.set_colorkey((0, 0, 0))
Point20Rect = Point20.get_rect()

Point30 = pygame.image.load('30Points.png').convert()
Point30 = pygame.transform.smoothscale_by(Point30, 0.4)
Point30.set_colorkey((0, 0, 0))
Point30Rect = Point30.get_rect()

ufo = pygame.image.load('ufo.png').convert()
ufo = pygame.transform.smoothscale_by(ufo, 0.4)
ufo.set_colorkey((0, 0, 0))
ufoRect = ufo.get_rect()



Point10Rect.center = (screenWidth // 2 - 200, screenHeight // 2 + 300)
Point20Rect.center = (screenWidth // 2 - 200, screenHeight // 2 + 200)
Point30Rect.center = (screenWidth // 2 - 200, screenHeight // 2 + 100)
ufoRect.center = (screenWidth // 2 - 200, screenHeight // 2)

tintHeight = 300
tintSurface = pygame.Surface((screenWidth, tintHeight), pygame.SRCALPHA)
tintSurface.fill((0, 255, 0, 100))
# Game Loop
running = True

# restart game
def resetGame():
    # variables to reset
    global gameStarted, playerScore
    gameStarted = False
    playerScore = 0
while running:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                coins += 1

    # 2. Game Logic Updates
    # (Update positions, check collisions, etc.)

    # 3. Drawing / Rendering
    screen.fill((0, 0, 0))  # Clear screen with black background
    
    # (Draw your objects here)
    if not gameStarted:
        # Draw start screen

        scoreText = scoreFont.render("SCORE<1>", True, (255, 255, 255))

        hiScoreText = scoreFont.render("HI-SCORE", True, (255, 255, 255))
        hiScoreRect = hiScoreText.get_rect()
        hiScoreRect.topright = (935, 10)

        currentScoreText = scoreFont.render(str(playerScore), True, (255, 255, 255))

        hiScore = load("hiScore")
        currentHiScoreText = scoreFont.render(str(hiScore), True, (255, 255, 255))
        currentHiScoreRect = currentHiScoreText.get_rect()
        currentHiScoreRect.topright = (935, 60)

        startText = font(20).render("PLAY", True, (255, 255, 255))
        startTextRect = startText.get_rect(center=(screenWidth // 2, screenHeight // 2 - 300))
        gameTitle = font(22).render("SPACE INVADERS", True, (255, 255, 255))
        gameTitleRect = gameTitle.get_rect(center=(screenWidth // 2, screenHeight // 2 - 200))

        scoreTableTitle = font(20).render("*SCORE ADVANCE TABLE*", True, (255, 255, 255))
        scoreTableTitleRect = scoreTableTitle.get_rect(center=(screenWidth // 2, screenHeight // 2 - 100))
        
        Point10Text = font(20).render("= 10 POINTS", True, (255, 255, 255))
        Point10TextRect = Point10Text.get_rect(midleft=(Point10Rect.right + 10, Point10Rect.centery))
        Point20Text = font(20).render("= 20 POINTS", True, (255, 255, 255))
        Point20TextRect = Point20Text.get_rect(midleft=(Point20Rect.right + 10, Point20Rect.centery))
        Point30Text = font(20).render("= 30 POINTS", True, (255, 255, 255))
        Point30TextRect = Point30Text.get_rect(midleft=(Point30Rect.right + 10, Point30Rect.centery))
        ufoText = font(20).render("= ? MYSTERY", True, (255, 255, 255))
        ufoTextRect = ufoText.get_rect(midleft=(ufoRect.right + 10, ufoRect.centery))
        
        coinText = font(20).render(f"CREDIT: {min(99, coins):02d}", True, (255, 255, 255))
        coinTextRect = coinText.get_rect(topright=(screenWidth - 10, screenHeight - 50))
        screen.blit(scoreTableTitle, scoreTableTitleRect)
        screen.blit(startText, startTextRect)
        screen.blit(gameTitle, gameTitleRect)
        screen.blit(scoreText, (10, 10))
        screen.blit(hiScoreText, hiScoreRect)
        screen.blit(currentScoreText, (10, 60))
        screen.blit(currentHiScoreText, currentHiScoreRect)
        screen.blit(Point10, Point10Rect)
        screen.blit(Point20, Point20Rect)
        screen.blit(Point30, Point30Rect)
        screen.blit(ufo, ufoRect)
        screen.blit(Point10Text, Point10TextRect)
        screen.blit(Point20Text, Point20TextRect)
        screen.blit(Point30Text, Point30TextRect)
        screen.blit(ufoText, ufoTextRect)
        screen.blit(coinText, coinTextRect)



        # Tint effect at the bottom of the screen to mimic original game
        screen.blit(tintSurface, (0, screenHeight - tintHeight), special_flags=pygame.BLEND_RGB_MULT)
    else:
        # Draw game objects
        pass

    window.flip()
    await asyncio.sleep(1 / fps)

# Clean Up & Exit
pygame.quit()
sys.exit()
