import asyncio
import pygame
import js

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
        ballX += 5
        ballY += 5
        ballX = max(ballRadius, min(screenWidth - ballRadius, ballX))
        ballY = max(ballRadius, min(screenHeight - ballRadius, ballY))
        if ballX == screenWidth - ballRadius:
            ballXDir = "left"
            js.window.alert(ballXDir)
        elif ballX == ballRadius:
            ballXDir = "right"
            js.window.alert(ballXDir)
        
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not gameStarted:
                    gameStarted = True




    window.flip()
    await asyncio.sleep(1 / 120)