import pygame
import math
import random
from pygame import mixer

# Initialising the pygame
pygame.init()

# Create window
screen = pygame.display.set_mode((800, 600))
# Create background
background = pygame.image.load("backg.png")
mixer.music.load('background.wav')
mixer.music.play(-1)

# Icon and Caption
pygame.display.set_caption("SPACE INVADERS")
icon = pygame.image.load("project.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("space-invaders.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 6

for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)

# Bullet
# Ready - You can't see bullet on screen
# Start - Bullet is currently moving
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"

#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 25)
textX = 10
textY = 10

#Game Over
font_over = pygame.font.Font('font.ttf', 100)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over():
    gameover = font_over.render("GAME OVER", True, (255, 0, 0))
    screen.blit(gameover, (85, 220))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def firebullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 35:
        return True
    else:
        return False


# Game loop
running = True
while running:
    # Red Green Blue
    screen.fill((29, 17, 53))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed check whether is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                # Get the current x cordinate of spaceship
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    firebullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    playerX = playerX + playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(no_of_enemies):
        #Game over
        if enemyY[i] > 400:
            for j in range(no_of_enemies):
                enemyY[j] = 2000
            game_over()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
           explosion_sound = mixer.Sound('explosion.wav')
           explosion_sound.play()
           bulletY = 480
           bullet_state = "ready"
           score_value += 1
           enemyX[i] = random.randint(0, 735)
           enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)


    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        firebullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
