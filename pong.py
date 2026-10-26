import asyncio
import pygame
import js
import math
import random

def collision(circle_pos, circle_radius, rect):
    """Detects collision between a circle and a pygame.Rect without sprites.

    circle_pos: A tuple or pygame.Vector2 (x, y) representing the circle's
    center.
    circle_radius: The radius of the circle (int or float).
    rect: A pygame.Rect object.
    """
    # 1. Clamp the circle's center coordinates to the rectangle's boundaries
    # This finds the closest point on or inside the rectangle
    closest_x = max(rect.left, min(circle_pos[0], rect.right))
    closest_y = max(rect.top, min(circle_pos[1], rect.bottom))

    # 2. Calculate the distance from the circle's center to this closest point
    distance_x = circle_pos[0] - closest_x
    distance_y = circle_pos[1] - closest_y

    # 3. Use the Pythagorean theorem (squared) to avoid a slow square root function
    distance_squared = (distance_x**2) + (distance_y**2)

    # 4. If the distance is less than the radius squared, they are colliding
    return distance_squared <= (circle_radius**2)

pygame.init()
screenWidth = 1280
screenHeight = 720
window = pygame.Window(size=(screenWidth, screenHeight))
window.title = "Pong - Game"
screen = window.get_surface()
gameStarted = False
running = True
playerWidth = 20
playerHeight = 200
playerX = 75
playerY = (screenHeight - playerHeight) // 2
ballX = screenWidth // 2
ballY = screenHeight // 2
ballRadius = 20
ballXDir = random.choice(["left", "right"])
ballYDir = random.choice(["up", "down"])
ballSpeedX = 5
ballSpeedY = 5
font = pygame.font.SysFont("System", 30)
text = 
def setupGame():
    global playerY, ballX, ballY, ballXDir, ballYDir, ballSpeedX, ballSpeedY
    playerY = (screenHeight - playerHeight) // 2
    ballX = screenWidth // 2
    ballY = screenHeight // 2
    ballXDir = "right"
    ballXDir = random.choice(["left", "right"])
    ballYDir = "down"
    ballYDir = random.choice(["up", "down"])
    ballSpeedX = 5
    ballSpeedY = 5
while running:
    screen.fill((0, 0, 0))
    if gameStarted:
        keys = pygame.key.get_pressed()
        movement = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        playerY += movement * 5
        playerY = max(0, min(screenHeight - playerHeight, playerY))
        player = pygame.Rect(playerX, playerY, playerWidth, playerHeight)
        pygame.draw.rect(screen, (255, 255, 255), player)
        pygame.draw.circle(screen, (255,255,255), (ballX, ballY), ballRadius)
        # ballX += 5
        # ballY += 5
        ballX = max(ballRadius, min(screenWidth - ballRadius, ballX))
        ballY = max(ballRadius, min(screenHeight - ballRadius, ballY))
        if ballX == screenWidth - ballRadius:
            ballXDir = "left"
            # js.window.alert(ballXDir)
        elif ballX == ballRadius:
            setupGame()
            gameStarted = False
        if ballY >= screenHeight - ballRadius:
            ballYDir = "up"
        elif ballY - ballRadius == 0:
            ballYDir = "down"
        if ballYDir == "up":
            ballY -= ballSpeedY
        elif ballYDir == "down":
            ballY += ballSpeedY
        if ballXDir == "left":
            ballX -= ballSpeedX
        if collision((ballX, ballY), ballRadius, pygame.Rect(playerX, playerY, playerWidth, playerHeight)):
            if ballXDir == "left":
                ballXDir = "right"
                ballSpeedX += random.randint(1, 3)
                ballSpeedX = max(-5, min(ballSpeedX, 5))
                ballSpeedY += random.randint(1, 3)
                ballSpeedY = max(-5, min(ballSpeedY, 5))
        if ballXDir == "right":
            ballX += ballSpeedX
        
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not gameStarted:
                    gameStarted = True
        




    window.flip()
    await asyncio.sleep(1 / 120)