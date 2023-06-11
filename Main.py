import pygame
import random
import math
from pygame import mixer

# Initiaize the pygame
pygame.init()

# Create a screen
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Space Assailant")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('space.jpg')

# Player
PlayerImg = pygame.image.load('spaceship-2.png')
PlayerX = 370
PlayerY = 480
PlayerX_change = 0

# Enemy
EnemyImg = []
EnemyX = []
EnemyY = []
EnemyX_change = []
EnemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    EnemyImg.append(pygame.image.load('aircraft.png'))
    EnemyX.append(random.randint(0, 735))
    EnemyY.append(random.randint(50, 150))
    EnemyX_change.append(3)
    EnemyY_change.append(40)

# Ready = You can't see the bullet on screen
# Fire = The bullet is currently moving
# Bullet
BulletImg = pygame.image.load('bullet.png')
BulletX = 0
BulletY = 480
BulletX_change = 0
BulletY_change = 10
Bullet_state = "Ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over Text
game_font = pygame.font.Font('freesansbold.ttf', 64)

# Background
mixer.music.load('background.wav')
mixer.music.play(-1)

# Game Loop
running = True


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = game_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(PlayerImg, (x, y))


def enemy(x, y, i):
    screen.blit(EnemyImg[i], (x, y))


def fire_bullet(x, y):
    global Bullet_state
    Bullet_state = "fire"
    screen.blit(BulletImg, (x + 16, y + 10))


def isCollision(EnemyX, EnemyY, BulletX, BulletY):
    distance = math.sqrt((math.pow(EnemyX - BulletX, 2)) + (math.pow(EnemyY - BulletY, 2)))
    if distance < 32:
        return True
    else:
        return False


while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                PlayerX_change = -3
            if event.key == pygame.K_RIGHT:
                PlayerX_change = 3
            if event.key == pygame.K_SPACE:
                # Get the current x - coordinate of the system
                if Bullet_state is "Ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    BulletX = PlayerX
                    fire_bullet(BulletX, BulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                PlayerX_change = 0

    # Checking for boundaries of spaceship  as it doesn't go out of bounds
    PlayerX += PlayerX_change
    if PlayerX <= 0:
        PlayerX = 0
    elif PlayerX >= 736:
        PlayerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if EnemyY[i] > 440:
            for j in range(num_of_enemies):
                EnemyY[j] = 2000
            game_over_text()
            break

        EnemyX[i] += EnemyX_change[i]
        if EnemyX[i] <= 0:
            EnemyX_change[i] = 3
            EnemyY[i] += EnemyY_change[i]
        elif EnemyX[i] >= 736:
            EnemyX_change[i] = -3
            EnemyY[i] += EnemyY_change[i]

        # Collision
        collision = isCollision(EnemyX[i], EnemyY[i], BulletX, BulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            BulletY = 480
            Bullet_state = "Ready"
            score_value += 1
            EnemyX[i] = random.randint(0, 735)
            EnemyY[i] = random.randint(50, 150)

        enemy(EnemyX[i], EnemyY[i], i)

    # Bullet Movement
    if BulletY <= 0:
        BulletY = 480
        Bullet_state = "Ready"
    if Bullet_state is "fire":
        fire_bullet(BulletX, BulletY)
        BulletY -= BulletY_change

    player(PlayerX, PlayerY)
    show_score(textX, textY)
    pygame.display.update()
