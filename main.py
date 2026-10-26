import asyncio
import pygame
import js
# Source - https://stackoverflow.com/a/24728182
# Posted by martineau, modified by community. See post 'Timeline' for change history
# Retrieved 2026-10-26, License - CC BY-SA 3.0

import math

def collision(rleft, rtop, width, height,   # rectangle definition
              center_x, center_y, radius):  # circle definition
    """ Detect collision between a rectangle and circle. """

    # complete boundbox of the rectangle
    rright, rbottom = rleft + width/2, rtop + height/2

    # bounding box of the circle
    cleft, ctop     = center_x-radius, center_y-radius
    cright, cbottom = center_x+radius, center_y+radius

    # trivial reject if bounding boxes do not intersect
    if rright < cleft or rleft > cright or rbottom < ctop or rtop > cbottom:
        return False  # no collision possible

    # check whether any point of rectangle is inside circle's radius
    for x in (rleft, rleft+width):
        for y in (rtop, rtop+height):
            # compare distance between circle's center point and each point of
            # the rectangle with the circle's radius
            if math.hypot(x-center_x, y-center_y) <= radius:
                return True  # collision detected

    # check if center of circle is inside rectangle
    if rleft <= center_x <= rright and rtop <= center_y <= rbottom:
        return True  # overlaid

    return False  # no collision detected


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
ballXDir = "right"
ballYDir = "down"
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
            ballXDir = "right"
        if ballY >= screenHeight - ballRadius:
            ballYDir = "up"
        elif ballY - ballRadius == 0:
            ballYDir = "down"
            # js.window.alert(ballXDir)
        if ballYDir == "up":
            ballY -= 5
        elif ballYDir == "down":
            ballY += 5
        if ballXDir == "left":
            ballX -= 5
        if collision(playerX, playerY, playerWidth, playerHeight, ballX, ballY, ballRadius):
            if ballXDir == "right":
                ballXDir = "left"
            elif ballXDir == "left":
                ballXDir = "right"
        elif ballXDir == "right":
            ballX += 5
        
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not gameStarted:
                    gameStarted = True




    window.flip()
    await asyncio.sleep(1 / 120)