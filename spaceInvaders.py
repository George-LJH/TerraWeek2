# Libraries Import
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
    global gameStarted, playerX, screenWidth, screenHeight, playerScore, coins, enemyList, enemySpacingX, enemySpacingY, enemySpacingLeft, enemySpacingTop, currentTime, lives, extraLivesGranted, gameOver, bunkers, enemyTimer, ufoActive, ufoX, ufoDirection, shotCount
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
    bunkers = makeBunkers()
    enemyTimer = 0
    ufoActive = False
    ufoX = -ufoRect.width
    ufoDirection = 1
    shotCount = 0
def checkGameOver():
    global enemySpacingX, enemySpacingY, enemySpacingLeft, enemySpacingTop
    global gameStarted, enemyList, fps, gameOver, bulletActive, enemyBulletActive
    enemyPlayerLine = 605
    frontRow = -1

    # Start at the bottom row and find the first row with a living enemy.
    for rowIndex in range(len(enemyList) - 1, -1, -1):
        for enemy in enemyList[rowIndex]:
            if enemy != 4:
                frontRow = rowIndex
                break
        if frontRow != -1:
            break

    if frontRow != -1:
        # The bottom row normally sets the limit at 605.
        # If bottom rows are gone, give the formation one row spacing per row.
        rowsGone = len(enemyList) - 1 - frontRow
        gameOverTop = enemyPlayerLine + rowsGone * enemySpacingY
    else:
        gameOverTop = 0

    if enemySpacingTop >= gameOverTop and frontRow != -1:
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

def isCollide(enemyIndexRow, enemyIndexCol):
    global enemyList, enemySpacingX, enemySpacingY, enemySpacingLeft, enemySpacingTop, Point10Rect, playerScore
    enemyType = enemyList[enemyIndexRow][enemyIndexCol]
    if enemyType == 4:
        return False
    if enemyType == 0:
        hitWidth, hitHeight = Point10Rect.width, Point10Rect.height
    elif enemyType == 1:
        hitWidth, hitHeight = Point20Rect.width, Point20Rect.height
    elif enemyType == 2:
        hitWidth, hitHeight = Point30Rect.width, Point30Rect.height
    elif enemyType == 3:
        hitWidth, hitHeight = ufoRect.width, ufoRect.height

    enemyX = enemyIndexCol * enemySpacingX + enemySpacingLeft
    enemyY = enemyIndexRow * enemySpacingY + enemySpacingTop
    enemyRect = pygame.Rect(enemyX, enemyY, hitWidth, hitHeight)
    if (bulletRect.colliderect(enemyRect)):
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

def bunkerCellRect(bunker, row, col):
    return pygame.Rect(
        bunker[0] + col * bunkerCell,
        bunker[1] + row * bunkerCell,
        bunkerCell,
        bunkerCell,
    )


def drawBunkers():
    for bunker in bunkers:
        for row in range(bunkerRows):
            for col in range(bunkerCols):
                if bunker[2][row][col] == 1:
                    pygame.draw.rect(screen, (0, 255, 0), bunkerCellRect(bunker, row, col))


def collideBunkers(bulletRect):
    hit = False
    for bunker in bunkers:
        for row in range(bunkerRows):
            for col in range(bunkerCols):
                if bunker[2][row][col] == 1:
                    if bulletRect.colliderect(bunkerCellRect(bunker, row, col)):
                        bunker[2][row][col] = 0
                        hit = True
    return hit


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
debugMode = True
playerScore = 0
coins = 0
playerSpeed = 5
playerX = screenWidth // 2
playerY = screenHeight // 2 + 420
bulletActive = False
bulletSpeed = 8

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


# Bunkers
# 1 = there, 0 = gone
bunkerTemplate = [
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
]
bunkerCell = 10
bunkerRows = len(bunkerTemplate)
bunkerCols = len(bunkerTemplate[0])
bunkerWidth = bunkerCols * bunkerCell
bunkerY = 800
bunkerCount = 4
ufoActive = False
ufoX = -ufoRect.width
ufoY = 90
ufoSpeed = 4
ufoDirection = 1
shotCount = 0
ufoPointTable = [100, 50, 50, 150, 100, 50, 100, 300, 100, 50, 150, 100, 50, 100, 300]
def makeBunkers():
    # Evenly space the barriers across the screen, with the same gap on both sides
    gap = (screenWidth - bunkerCount * bunkerWidth) // (bunkerCount + 1)
    newBunkers = []
    for i in range(bunkerCount):
        grid = []
        for row in bunkerTemplate:
            grid.append(row[:])
        newBunkers.append([gap + i * (bunkerWidth + gap), bunkerY, grid])
    return newBunkers

bunkers = makeBunkers()

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
            if event.key == pygame.K_RETURN or event.key == pygame.K_x:
                if not gameStarted and coins >= 1:
                    gameStarted = True
                    coins -= 1
                    playerScore = 0
                    currentTime = pygame.time.Clock()
            if gameStarted and event.key == pygame.K_SPACE:
                if not bulletActive:
                    bulletRect.center = (playerX, playerY)
                    bulletActive = True
                    shotCount += 1
            if debugMode and event.key == pygame.K_0:
                js.alert(f"{enemySpacingTop}, {enemySpacingLeft}")
                js.alert(currentTime)
            if debugMode and event.key == pygame.K_r:
                resetGame()
            if debugMode and event.key == pygame.K_9:
                invincibility = not invincibility
            if debugMode and event.key == pygame.K_8:
                command = js.prompt("Enter command:")
                exec(command)
    if gameStarted:
        enemyTimer += dt
        keys = pygame.key.get_pressed()
        moveX = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * playerSpeed
        playerX += moveX
        playerX = max(0 + playerRect.width // 2, min(screenWidth - playerRect.width // 2, playerX))
        if bulletActive:
            previousRect = bulletRect.copy()
            bulletRect.y -= bulletSpeed
            if collideBunkers(previousRect.union(bulletRect)):
                bulletActive = False
            else:
                for i in range(len(enemyList)):
                    for j in range(len(enemyList[i])):
                        if isCollide(i, j):
                            enemyList[i][j] = 4
                            bulletActive = False
                if bulletRect.bottom < 90:
                    bulletActive = False
        else:
            bulletRect.center = (playerX, playerY)
        playerRect.center = (playerX, playerY)
    # 3. Drawing / Rendering
    screen.fill((0, 0, 0))  # Clear screen with black background
    
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
        drawBunkers()
        screen.blit(player, playerRect)
        screen.blit(scoreText, (10, 10))
        screen.blit(hiScoreText, hiScoreRect)
        screen.blit(currentScoreText, (10, 60))
        screen.blit(currentHiScoreText, currentHiScoreRect)
        screen.blit(coinText, coinTextRect)
        enemySpeed = baseEnemySpeed + (sum(row.count(4) for row in enemyList) * 0.03)
        enemySpacingLeft += enemySpeed if enemyMoveDirectionX == "right" else -enemySpeed
        if enemySpacingLeft <= 30:
            enemyMoveDirectionX = "right"   
            enemySpacingTop += 15
        elif enemySpacingLeft >= 160:
            enemyMoveDirectionX = "left"
            enemySpacingTop += 15
        checkGameOver()
        if bulletActive:
            screen.blit(bullet, bulletRect)
        if enemyBulletActive and not invincibility:
            previousRect = enemyBulletRect.copy()
            enemyBulletRect.y += bulletSpeed
            screen.blit(enemyBullet, enemyBulletRect)
            if enemyBulletRect.top > screenHeight:
                enemyBulletActive = False
            elif collideBunkers(previousRect.union(enemyBulletRect)):
                enemyBulletRect.y = -1000
                enemyBulletActive = False
            elif enemyBulletRect.colliderect(playerRect):
                enemyBulletRect.y = -1000
                enemyBulletActive = False
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
        if not ufoActive and random.randint(1, 600) == 1:
            ufoActive = True
            ufoDirection = random.choice([-1, 1])
            ufoX = -ufoRect.width if ufoDirection == 1 else screenWidth

        if ufoActive:
            ufoX += ufoSpeed * ufoDirection
            ufoPosition = pygame.Rect(ufoX, ufoY, ufoRect.width, ufoRect.height)

            if bulletActive and bulletRect.colliderect(ufoPosition):
                ufoPoints = ufoPointTable[(shotCount - 1) % len(ufoPointTable)]
                playerScore += ufoPoints
                bulletActive = False
                ufoActive = False

            if ufoX > screenWidth or ufoX + ufoRect.width < 0:
                ufoActive = False
        if ufoActive:
            screen.blit(ufo, (ufoX, ufoY))
    screen.blit(coinText, coinTextRect)
    screen.blit(tintSurface, (0, screenHeight - tintHeight), special_flags=pygame.BLEND_RGB_MULT)
    window.flip()
    await asyncio.sleep(1 / fps)

# Clean Up & Exit
pygame.quit()
sys.exit()
