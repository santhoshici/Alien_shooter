import pygame

import random

import mysql.connector
from pygame import mixer
#SQL CONNECTIONS


my_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sandy050406",
    database="Ghost_py"
)

mycs = my_db.cursor()

user_name = ""
password = ""
High_score = 0
ID = 0
mode = "HOME"


def login():
    while True:
        user = input("Enter the user name: ")
        pass_ = input("Enter the password: ")
        mycs.execute("SELECT * FROM Space WHERE user = %s AND pass = %s", (user, pass_))
        try:
            myrs = mycs.fetchone()
            global user_name, password, High_score, ID
            ID, user_name, password, High_score = myrs
            break
        except TypeError:
            print("There is no user with this tag!!! \nPress C to create a new user:", end=" ")
            inp = input().upper()
            print()
            if inp == "C":
                while True:
                    new_user = input("Enter the new user name: ")
                    new_pass_ = input("Enter the new password: ")
                    mycs.execute("Insert into Space(user, pass) values(%s, %s)", (new_user, new_pass_))
                    my_db.commit()
                    if mycs.rowcount == 1:
                        print("Your record has been added!!,\nPLEASE DON'T FORGET YOUR USERNAME IS %s AND PASSWORD IS %s"
                              % (new_user, new_pass_))
                        break
    print()


login()
while True:
    print("""**TASKS**
    'start'           ---> To Start
    'leaderboard'     ---> To See Leaderboard
    'score'           ---> To see your score""")
    choice = input("Enter what you want to perform: ")
    print()
    if choice.lower() in "start":
        break
    elif choice.lower() in "leaderboard":
        mycs.execute("SELECT user, highscore FROM space ORDER BY highscore DESC")
        leaderboard = mycs.fetchmany(5)

        print("TOP\tUSER\t\t\tHIGHSCORE")
        for num in range(5):
            try:
                record = leaderboard[num]
                user_, high_S = record
                space = len(user_)
                print(num, "\t", user_," "*(25-space), high_S)
            except IndexError:
                pass
        print()
    elif choice.lower() in "score":
        print("----- YOUR PRESENT HIGH SCORE IS ------")
        print(f"                  {High_score}                    ")
        print()


print(""""
        ENJOY
              THE
                  GAME
                        !!!!!""")

#PYGAME PART
"""HOME SCREEN"""


"""GAME SCREEN"""
"""DISPLAYS"""
pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption(user_name.title() + "'s Space Adventure")

Icon = pygame.image.load('icon.png')
pygame.display.set_icon(Icon)

background = pygame.image.load('background.jpg')
mixer.music.load('background.wav')
mixer.music.play(-1)

"""CHARACTERS"""
#player
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 500
playerChangeX = 0

#score
score = 0
scoreType = {"small": 1, "mid": 2, "big": 3}
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10
show = True

#gameover
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

#high score
highScore = pygame.font.Font('freesansbold.ttf', 32)


#alien
alienType = []
alienHp = []
alienImg = []
alienX = []
alienY = []
alienChangeX = []
alienChangeY = []
alienState = []
totalNoOfAliens = 6
alienToBeShown = 1
for i in range(totalNoOfAliens):
    limits = random.randint(1, 30)
    if limits < 20:
        alienImg.append(pygame.image.load('alien1.png'))
        alienType.append("small")
        alienHp.append(1)
    elif limits < 28:
        alienImg.append(pygame.image.load('alien2.png'))
        alienType.append("mid")
        alienHp.append(2)
    elif limits <= 30:
        alienImg.append(pygame.image.load('alien3.png'))
        alienType.append("big")
        alienHp.append(3)

    alienX.append(random.randint(0, 720))
    alienY.append(random.randint(10, 50))
    alienChangeX.append(1)
    alienChangeY.append(30)
    alienState.append("alive")

#laser
laserImg = pygame.image.load('laser.png')
laserX = playerX
laserY = 480
laserChangeY = 3
laserState = "ready"

"""Functions"""


def game_over():
    global show, score, High_score
    if score >= High_score:
        High_score = score
    over_text = game_over_font.render("GAME OVER", True, (230, 0, 115))
    screen.blit(over_text, (200, 250))
    high_score_text = highScore.render("ALL TIME HIGH SCORE : " + str(High_score), True, (230, 0, 115))
    screen.blit(high_score_text, (230, 350))
    show = False


def show_score(x, y):
    global score, show
    out_score = font.render("SCORE: " + str(score), show, (255, 255, 255))    # (R, G, B) <-- colour
    screen.blit(out_score, (x, y))


def shortest_distance(x1, y1, x2, y2):
    if laserState == "fire":
        distance = (((x2-x1)**2) + ((y2-y1)**2))**0.5
        if distance <= 25:
            return True
        else:
            return False


def alien(img, x, y):
    screen.blit(img, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def fire_laser(x, y):
    screen.blit(laserImg, (x, y + 10))
    global laserState
    laserState = "fire"
    global laserX
    laserX = x
    mixer.music.load('laser.wav')
    mixer.music.play()


"""Mainloop"""
Repeat = True
while Repeat:
    screen.blit(background, (0, 0))

    if mode == "HOME":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Repeat = False
        hoverText = pygame.font.Font('freesansbold.ttf', 32)
        Hover_text1 = hoverText.render("HOVER OVER THE GREEN AREA", True, (230, 0, 115))
        Hover_text2 = hoverText.render("TO PLAY THE GAME", True, (230, 0, 115))
        screen.blit(Hover_text1, (150, 20))
        screen.blit(Hover_text2, (200, 50))
        mouse = pygame.mouse.get_pos()
        pygame.draw.rect(screen, (0, 230, 0), (350, 275, 100, 50))
        if 450 >= mouse[0] >= 350 and 325 >= mouse[1] >= 275:
            pygame.draw.rect(screen, (0, 255, 0), (350, 275, 100, 50))
            mode = "GAME"

    elif mode == "GAME":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Repeat = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerChangeX = -0.7
                if event.key == pygame.K_RIGHT:
                    playerChangeX = 0.7
                if event.key == pygame.K_SPACE and laserState == "ready":
                    fire_laser(playerX, laserY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerChangeX = 0

        #bullet change
        if laserState == "fire":
            fire_laser(laserX, laserY)
            laserY -= laserChangeY

        for i in range(alienToBeShown):
            if shortest_distance(alienX[i], alienY[i], laserX, laserY):
                if alienHp[i] == 1:
                    mixer.music.load('explosion.wav')
                    mixer.music.play()
                    alienState[i] = "dead"
                    score += scoreType[alienType[i]]
                    alienX[i] = random.randint(0, 720)
                    alienY[i] = random.randint(10, 50)
                    limits = random.randint(1, 30)
                    if limits < 20:
                        alienImg[i] = pygame.image.load('alien1.png')
                        alienType[i] = "small"
                        alienHp[i] = 1
                    elif limits < 28:
                        alienImg[i] = pygame.image.load('alien2.png')
                        alienType[i] = "mid"
                        alienHp[i] = 2
                    elif limits <= 30:
                        alienImg[i] = pygame.image.load('alien3.png')
                        alienType[i] = "big"
                        alienHp[i] = 3
                    alienChangeX[i] = 1
                    alien(alienImg[i], alienX[i], alienY[i])
                    laserY = 10
                else:
                    laserY = 10
                    alienHp[i] -= 1
        if laserY <= 10:
            laserState = "ready"
            laserY = 480

        #alien change

        for i in range(alienToBeShown):
            if alienX[i] >= 730:
                alienX[i] = 730
                alienChangeX[i] = -0.8
                alienY[i] += alienChangeY[i]

            if alienX[i] <= 0:
                alienX[i] = 0
                alienChangeX[i] = 0.8
                alienY[i] += alienChangeY[i]

        #boundaries
        if playerX >= 730:
            playerX = 730
        if playerX <= 0:
            playerX = 0

        """Movements"""
        playerX += playerChangeX
        player(playerX, playerY)
        show_score(textX, textY)

        for i in range(alienToBeShown):
            if alienY[i] > 460:
                for j in range(alienToBeShown):
                    alienY[j] = 2000  # to move it out of screen
                game_over()
                break

        for i in range(alienToBeShown):
            alienX[i] += alienChangeX[i]
            alien(alienImg[i], alienX[i], alienY[i])
        if score <= 10:
            alienToBeShown = 1
        elif score <= 20:
            alienToBeShown = 2
        elif score <= 30:
            alienToBeShown = 3
            for i in range(alienToBeShown):
                if alienChangeX[i] == -0.8:
                    alienChangeX[i] = -1.1
                elif alienChangeX[i] == 0.8:
                    alienChangeX[i] = 1.1
        elif score <= 40:
            alienToBeShown = 4
        elif score <= 50:
            alienToBeShown = 5
            for i in range(alienToBeShown):
                if alienChangeX[i] == -1.1:
                    alienChangeX[i] = -1.3
                elif alienChangeX[i] == 1.1:
                    alienChangeX[i] = 1.3
        elif score >= 60:
            alienToBeShown = 6
            for i in range(alienToBeShown):
                if alienChangeX[i] == -1.3:
                    alienChangeX[i] = -1.5
                elif alienChangeX[i] == 1.3:
                    alienChangeX[i] = 1.5

    pygame.display.update()

#final updation of sql
mycs.execute("UPDATE SPACE SET highscore = %s WHERE id = %s" %(High_score, ID))
my_db.commit()
my_db.close()
