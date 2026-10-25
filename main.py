import asyncio
import pygame

pygame.init()
screenWidth = 1280
screenHeight = 720
window = pygame.Window(size=(screenWidth, screenHeight))
window.title = "Pong - Game"
screen = window.get_surface()
gameStarted = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and not gameStarted:
                gameStarted = True
    keys = pygame.key.get_pressed()
    y_axis = keys[pygame.K_DOWN] - keys[pygame.K_UP]