import pygame
import math
import random
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((1024, 768))

background = pygame.image.load('forest.jpg')
gameIcon = pygame.image.load('chung.png')
pygame.display.set_icon(gameIcon)

mixer.music.load('benny_hill.wav')
mixer.music.play(-1)
pygame.mixer.music.set_volume(.6)
sup = mixer.Sound('whatsup.wav')
sup.set_volume(.5)
sup.play()

global bullet_Sound
bullet_Sound = mixer.Sound('poo.wav')
bullet_Sound.set_volume(.4)

pygame.display.set_caption("CHUNGUNOMICS")

playerImg = pygame.image.load('chung.png')
playerX = 512
playerY = 620
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 35

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('pngbarn.png'))
    enemyX.append(random.randint(0, 960))
    enemyY.append(random.randint(20, 200))
    enemyX_change.append(random.randint(8, 15))
    enemyY_change.append(30)

bulletImg = pygame.image.load('imageedit_3_4617970527.png')
bulletX = 0
bulletY = 600
bulletX_change = 0
bulletY_change = 50
bullet_state = "ready"

score_value = 0

font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

over_font = pygame.font.Font('freesansbold.ttf', 13)


def show_score(x, y):
    score = font.render("Fudd Death = " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text(x, y):
    over_text = over_font.render("YOU HAVE FAILED THE CLASS OF CHUNGUNOMICS. SPACEBAR THROWS A CARROT", True, (255, 255, 255))
    screen.blit(over_text, (300, 384))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 25, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + math.pow(enemyY - bulletY, 2))
    if distance < 30:
        return True
    else:
        return False


running = True

while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -8
            if event.key == pygame.K_RIGHT:
                playerX_change = 8
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound.play()

                    bulletX = playerX
                fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 920
    elif playerX >= 920:
        playerX = 0

    for i in range(num_of_enemies):

        if enemyY[i] > 560:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
                playerImg = pygame.image.load('imageedit_2_7490140388.png')
                game_over_text(400, 384)

                fudd_Sound = mixer.Sound('elmer07.wav')
                fudd_Sound.set_volume(.2)
                fudd_Sound.play(1)

                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()

            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = random.randint(6, 12)
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 960:
            enemyX_change[i] = random.randint(6, 12) * -1
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 600
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 960)
            enemyY[i] = random.randint(0, 50)
            fudd2_Sound = mixer.Sound('Pling-KevanGC-1485374730.wav')
            fudd2_Sound.set_volume(.8)
            fudd2_Sound.play()

        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 600
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
