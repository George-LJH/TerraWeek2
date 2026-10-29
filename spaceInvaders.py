import pygame
import sys
import json
import js
import asyncio
import random
import time
# restart game
def resetGame():
    # variables to reset
    global gameStarted, playerX, screenWidth, screenHeight, playerScore, coins, enemyList, enemySpacingX, enemySpacingY, enemySpacingLeft, enemySpacingTop, currentTime, lives, extraLivesGranted, gameOver
    gameStarted = False
    playerX = screenWidth // 2
    enemyList = [
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    enemySpacingX = 70
    enemySpacingY = 75
    enemySpacingTop = 120
    enemySpacingLeft = 30
    currentTime = pygame.time.Clock()
    lives = 3
    extraLivesGranted = False
    gameOver = False
def checkGameOver():
    global enemySpacingTop, gameStarted, enemyList, fps, gameOver
    if (enemySpacingTop >= 597 and any(item != 4 for item in enemyList[4])) or \
       (enemySpacingTop >= 671 and any(item != 4 for item in enemyList[3])) or \
       (enemySpacingTop >= 745 and any(item != 4 for item in enemyList[2])) or \
       (enemySpacingTop >= 819 and any(item != 4 for item in enemyList[1])) or \
       (enemySpacingTop >= 893 and any(item != 4 for item in enemyList[0])):
        gameStarted = False
        bulletActive = False
        enemyBulletActive = False
        gameOver = True
    elif all(item == 4 for row in enemyList for item in row):
        enemyList = [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
        enemySpacingX = 70
        enemySpacingY = 75
        enemySpacingTop = 120
        enemySpacingLeft = 30

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

def isCollide(bulletPosition, enemyIndexRow, enemyIndexCol):
    global enemyList, enemySpacingX, enemySpacingY, enemySpacingLeft, enemySpacingTop, Point10Rect, playerScore
    enemyType = enemyList[enemyIndexRow][enemyIndexCol]
    if enemyType == 4:
        return False
    enemyX = enemyIndexCol * enemySpacingX + enemySpacingLeft
    enemyY = enemyIndexRow * enemySpacingY + enemySpacingTop
    if (bulletPosition[0] >= enemyX and bulletPosition[0] <= enemyX + Point10Rect.width and
        bulletPosition[1] >= enemyY and bulletPosition[1] <= enemyY + Point10Rect.height):
        if enemyType == 0:
            playerScore += 10
        elif enemyType == 1:
            playerScore += 20
        elif enemyType == 2:
            playerScore += 30
        elif enemyType == 3:
            playerScore += 50
        return True
    return False
    
def getCoordsFromIndex(enemyIndexRow, enemyIndexCol):
    global enemySpacingX, enemySpacingY, enemySpacingLeft, enemySpacingTop
    enemyX = enemyIndexCol * enemySpacingX + enemySpacingLeft
    enemyY = enemyIndexRow * enemySpacingY + enemySpacingTop
    return (enemyX, enemyY)
def getFrontMostEnemies(enemyList):
    frontMostEnemies = []
    for col in range(len(enemyList[0])):
        for row in reversed(range(len(enemyList))):
            if enemyList[row][col] != 4:
                frontMostEnemies.append((row, col))
                break
    return frontMostEnemies
def enemyGone():
    global enemyList
    for row in enemyList:
        if any(enemy != 4 for enemy in row):
            return False
    return True
def displayLives():
    global screen, player, lives
    for i in range(lives):
        x = 10 + i * (player.get_width() + 10)
        y = screen.get_height() - player.get_height() - 10
        screen.blit(player, (x, y))


def renderSplitText(text, font, top_color, bottom_color):
    """
    Renders a text surface split horizontally into two colors.
    """
    # 1. Render both versions of the text fully
    top_surf = font.render(text, True, top_color)
    bottom_surf = font.render(text, True, bottom_color)
    
    # 2. Get the dimensions of the text
    width, height = top_surf.get_size()
    half_height = height // 2
    
    # 3. Create a clean transparent destination surface
    final_surf = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # 4. Slice and paste the halves together
    # Top half: Draw from (0,0) to (width, half_height)
    final_surf.blit(top_surf, (0, 0), (0, 0, width, half_height))
    
    # Bottom half: Draw from (0, half_height) to the end
    final_surf.blit(bottom_surf, (0, half_height), (0, half_height, width, height - half_height))
    
    return final_surf


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
playerSpeed = 5
playerX = screenWidth // 2
playerY = screenHeight // 2 + 420
bulletActive = False
bulletSpeed = 12

enemySpacingX = 70
enemySpacingY = 75
enemySpacingTop = 120
enemySpacingLeft = 31
enemyScale = 0.2
enemyMoveDirectionX = "left"
enemySpeed = 1
# Enemies assets
Point10 = pygame.image.load('10Points.png').convert()
Point10 = pygame.transform.smoothscale_by(Point10, enemyScale)
Point10.set_colorkey((0, 0, 0))
Point10Rect = Point10.get_rect()

Point20 = pygame.image.load('20Points.png').convert()
Point20 = pygame.transform.smoothscale_by(Point20, enemyScale)
Point20.set_colorkey((0, 0, 0))
Point20Rect = Point20.get_rect()

Point30 = pygame.image.load('30Points.png').convert()
Point30 = pygame.transform.smoothscale_by(Point30, enemyScale)
Point30.set_colorkey((0, 0, 0))
Point30Rect = Point30.get_rect()

ufo = pygame.image.load('ufo.png').convert()
ufo = pygame.transform.smoothscale_by(ufo, enemyScale)
ufo.set_colorkey((0, 0, 0))
ufoRect = ufo.get_rect()



Point10Rect.center = (screenWidth // 2 - 200, screenHeight // 2 + 300)
Point20Rect.center = (screenWidth // 2 - 200, screenHeight // 2 + 200)
Point30Rect.center = (screenWidth // 2 - 200, screenHeight // 2 + 100)
ufoRect.center = (screenWidth // 2 - 200, screenHeight // 2)

tintHeight = 300
tintSurface = pygame.Surface((screenWidth, tintHeight), pygame.SRCALPHA)
tintSurface.fill((0, 255, 0, 100))

player = pygame.image.load('player.png').convert()
player = pygame.transform.smoothscale_by(player, 0.4)
player.set_colorkey((0, 0, 0))
playerRect = player.get_rect()
playerRect.center = (playerX, playerY)

# 0 = 10 points, 1 = 20 points, 2 = 30 points, 3 = ufo, 4 = none
enemyList = [
[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
front = getFrontMostEnemies(enemyList)
js.alert(random.choice(front))
# for i in getFrontMostEnemies(enemyList):
#     js.alert(getCoordsFromIndex(i[0], i[1]))

bullet = pygame.image.load('laser.png').convert()
bullet = pygame.transform.smoothscale_by(bullet, 0.4)
bullet.set_colorkey((0, 0, 0))
bulletRect = bullet.get_rect()
bulletRect.center = (playerX, playerY)
currentTime = pygame.time.Clock()
enemyTimer = 0
enemyBullet = pygame.image.load('laser.png').convert_alpha()
enemyBullet = pygame.transform.smoothscale_by(enemyBullet, 0.4)
enemyBulletRect = enemyBullet.get_rect()
enemyBulletRect.center = (screenWidth // 2, screenHeight // 2)
enemyBulletActive = False
lives = 3
invincibility = False
extraLivesGranted = False
enemySpeed = 1
baseEnemySpeed = 1
gameOver = False
# Game Loop
running = True

while running:
    dt = currentTime.tick(fps)
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                coins += 1
            if event.key == pygame.K_RETURN:
                if not gameStarted and coins >= 1:
                    gameStarted = True
                    coins -= 1
                    playerScore = 0
                    currentTime = pygame.time.Clock()
                    js.alert(currentTime)
            if gameStarted and event.key == pygame.K_SPACE:
                if not bulletActive:
                    bulletRect.center = (playerX, playerY)
                    bulletActive = True
            if event.key == pygame.K_0:
                js.alert(f"{enemySpacingTop}, {enemySpacingLeft}")
                js.alert(currentTime)
            if event.key == pygame.K_r:
                resetGame()
            if event.key == pygame.K_9:
                invincibility = not invincibility
    if gameStarted:
        enemyTimer += dt
        keys = pygame.key.get_pressed()
        moveX = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * playerSpeed
        playerX += moveX
        playerX = max(0 + playerRect.width // 2, min(screenWidth - playerRect.width // 2, playerX))
        if bulletActive:
            bulletRect.y -= bulletSpeed
            for i in range(len(enemyList)):
                for j in range(len(enemyList[i])):
                    if isCollide(bulletRect.center, i, j):
                        enemyList[i][j] = 4
                        bulletActive = False
            # Reset bullet when it flies off the top of the screen
            if bulletRect.bottom < 90:
                bulletActive = False
        else:
            bulletRect.center = (playerX, playerY)
        playerRect.center = (playerX, playerY)
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
    else:
        scoreText = scoreFont.render("SCORE<1>", True, (255, 255, 255))

        hiScoreText = scoreFont.render("HI-SCORE", True, (255, 255, 255))
        hiScoreRect = hiScoreText.get_rect()
        hiScoreRect.topright = (935, 10)

        currentScoreText = scoreFont.render(str(playerScore), True, (255, 255, 255))

        hiScore = load("hiScore")
        currentHiScoreText = scoreFont.render(str(hiScore), True, (255, 255, 255))
        currentHiScoreRect = currentHiScoreText.get_rect()
        currentHiScoreRect.topright = (935, 60)

        for i in range(5):
            for j in range(11):
                enemyType = enemyList[i][j]
                if enemyType == 0:
                    screen.blit(Point10, (j * enemySpacingX + enemySpacingLeft, i * enemySpacingY + enemySpacingTop))
                elif enemyType == 1:
                    screen.blit(Point20, (j * enemySpacingX + enemySpacingLeft, i * enemySpacingY + enemySpacingTop))
                elif enemyType == 2:
                    screen.blit(Point30, (j * enemySpacingX + enemySpacingLeft, i * enemySpacingY + enemySpacingTop))
                elif enemyType == 3:
                    screen.blit(ufo, (j * enemySpacingX + enemySpacingLeft, i * enemySpacingY + enemySpacingTop))

        if load("hiScore") < playerScore:
            save("hiScore", playerScore)
            hiScore = playerScore
            currentHiScoreText = scoreFont.render(str(hiScore), True, (255, 255, 255))
            currentHiScoreRect = currentHiScoreText.get_rect()
            currentHiScoreRect.topright = (935, 60)
        screen.blit(player, playerRect)
        screen.blit(scoreText, (10, 10))
        screen.blit(hiScoreText, hiScoreRect)
        screen.blit(currentScoreText, (10, 60))
        screen.blit(currentHiScoreText, currentHiScoreRect)
        enemySpeed = baseEnemySpeed + (sum(row.count(4) for row in enemyList) * 0.1)
        enemySpacingLeft += enemySpeed if enemyMoveDirectionX == "right" else -enemySpeed
        if enemySpacingLeft <= 30:
            enemyMoveDirectionX = "right"   
            enemySpacingTop += enemySpacingY // 2
        elif enemySpacingLeft >= 160:
            enemyMoveDirectionX = "left"
            enemySpacingTop += enemySpacingY // 2
        checkGameOver()
        if bulletActive:
            screen.blit(bullet, bulletRect)
        if enemyBulletActive and not invincibility:
            enemyBulletRect.y += bulletSpeed
            screen.blit(enemyBullet, enemyBulletRect)
            if enemyBulletRect.top > screenHeight:
                enemyBulletActive = False
            if enemyBulletRect.colliderect(playerRect):
                enemyBulletRect.y = -1000
                lives -= 1

                if lives <= 0:
                    wordX = screenWidth // 2
                    wordY = screenHeight // 2 - 300
                    gameOverString = ["G","A","M","E"," ","O","V","E","R", ""]
                    gameOverDisplayText = ""
                    gameOverText = renderSplitText("", font(40), (255,0,0), (255,255,255))
                    for i in range(0,9):
                        screen.fill((0, 0, 0))
                        gameOverDisplayText += gameOverString[i]
                        gameOverText = renderSplitText(gameOverDisplayText, font(40), (255,0,0), (255,255,255))
                        gameOverTextRect = gameOverText.get_rect(center=(wordX, wordY))
                        screen.blit(gameOverText, gameOverTextRect)
                        time.sleep(0.05)
                        window.flip()
                        await asyncio.sleep(1 / fps)
                    time.sleep(1)
                    enemyBulletActive = False
                    bulletActive = False
                    gameStarted = False
                    resetGame()
        if gameOver:
            wordX = screenWidth // 2
            wordY = screenHeight // 2 - 300
            gameOverString = ["G","A","M","E"," ","O","V","E","R", ""]
            gameOverDisplayText = ""
            gameOverText = renderSplitText("", font(40), (255,0,0), (255,255,255))
            for i in range(0,9):
                screen.fill((0, 0, 0))
                gameOverDisplayText += gameOverString[i]
                gameOverText = renderSplitText(gameOverDisplayText, font(40), (255,0,0), (255,255,255))
                gameOverTextRect = gameOverText.get_rect(center=(wordX, wordY))
                screen.blit(gameOverText, gameOverTextRect)
                time.sleep(0.05)
                window.flip()
                await asyncio.sleep(1 / fps)
            time.sleep(1)
            resetGame()
        
        if enemyTimer >= 2000 :
            # enemy shooting logic
            front = getFrontMostEnemies(enemyList)
            # js.alert(random.choice(front))
            enemyBulletActive = True
            enemyIndexRow, enemyIndexCol = random.choice(front)
            enemyBulletRect.center = getCoordsFromIndex(enemyIndexRow, enemyIndexCol)
            enemyTimer = 0
        displayLives()
        
        if enemyGone():
            resetGame()
        if playerScore >= 1500 and not extraLivesGranted:
            lives += 1
            extraLivesGranted = True
    screen.blit(tintSurface, (0, screenHeight - tintHeight), special_flags=pygame.BLEND_RGB_MULT)
    window.flip()
    await asyncio.sleep(1 / fps)

# Clean Up & Exit
pygame.quit()
sys.exit()
