import pygame
import os
from button import button
# from pygame.locals import *
pygame.font.init()
pygame.mixer.init()


WIDTH, HEIGHT = 900, 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
RED_L = (150, 0, 0)
GREEN = (0, 255, 0)
GREEN_L = (0, 150, 0)
YELLOW = (255, 255, 0)
OPAC = (100, 100, 100)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Battle Game")
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
BORDER = pygame.Rect((WIDTH-10)//2, 0, 10, HEIGHT)
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('arial', 100)
YELLOW_SPACESHIP = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YS = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP, (55, 40)), 90)
RED_SPACESHIP = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RS = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP, (55, 40)), 270)
SPACE = pygame.image.load(os.path.join('Assets', 'space.png'))
SPACE = pygame.transform.scale(SPACE, (WIDTH, HEIGHT))
BULLET_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
COLLIDE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
VICTORY_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'victory.mp3'))
BTN = button(WHITE, 0, 0, 0, 0)
BTN2 = button(WHITE, 0, 0, 0, 0)


def draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health, text, green_col, red_col):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    red_health_text = HEALTH_FONT.render("Health: "+str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Health: "+str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width()-10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(YS, (yellow.x, yellow.y))
    WIN.blit(RS, (red.x, red.y))
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    if text != "":
        # per-pixel alpha
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 150))
        WIN.blit(s, (0, 0))
        winner_text = WINNER_FONT.render(text, 1, WHITE)
        WIN.blit(winner_text, ((WIDTH-winner_text.get_width()) //
                               2, (HEIGHT - winner_text.get_height())//2))
        BTN = button(
            green_col, (WIDTH-100)//2, (HEIGHT + winner_text.get_height())//2, 100, 50)
        BTN.draw(WIN)
        BTN.add_text("Restart", WHITE, 30)
        BTN2 = button(
            red_col, (WIDTH-100)//2, (HEIGHT + winner_text.get_height())//2 + 100, 100, 50)
        BTN2.draw(WIN)
        BTN2.add_text("Quit", WHITE, 30)
    pygame.display.update()


def move_yellow(key_pressed, yellow):
    if key_pressed[pygame.K_a] and yellow.x-VEL > 0:  # left
        yellow.x -= VEL
    if key_pressed[pygame.K_d] and yellow.x+VEL+yellow.width < BORDER.x:  # right
        yellow.x += VEL
    if key_pressed[pygame.K_w] and yellow.y-VEL > 0:  # up
        yellow.y -= VEL
    if key_pressed[pygame.K_s] and yellow.y+VEL+yellow.height < HEIGHT-20:  # down
        yellow.y += VEL


def move_red(key_pressed, red):
    if key_pressed[pygame.K_LEFT] and red.x-VEL > BORDER.x+BORDER.width:  # left
        red.x -= VEL
    if key_pressed[pygame.K_RIGHT] and red.x+VEL+red.width < WIDTH:  # right
        red.x += VEL
    if key_pressed[pygame.K_UP] and red.y-VEL > 0:  # up
        red.y -= VEL
    if key_pressed[pygame.K_DOWN] and red.y+red.height+VEL < HEIGHT-20:  # down
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def main():

    yellow = pygame.Rect(100, 200, 55, 40)
    red = pygame.Rect(700, 200, 55, 40)
    red_bullets = []
    yellow_bullets = []
    red_health = 3
    yellow_health = 3
    winner_text = ""
    clock = pygame.time.Clock()
    run = True
    green_col = GREEN_L
    red_col = RED_L
    flag = False

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS and winner_text == "":
                    bullet = pygame.Rect(
                        yellow.x+yellow.width, yellow.y+yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS and winner_text == "":
                    bullet = pygame.Rect(red.x, red.y+red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_SOUND.play()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BTN.isOver(pos):
                    main()
                if BTN2.isOver(pos):
                    pygame.quit()
            if event.type == pygame.MOUSEMOTION:
                if BTN.isOver(pos):
                    green_col = GREEN
                else:
                    green_col = GREEN_L
                if BTN2.isOver(pos):
                    red_col = RED
                else:
                    red_col = RED_L
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                COLLIDE_SOUND.play()
            if event.type == RED_HIT:
                red_health -= 1
                COLLIDE_SOUND.play()
        if yellow_health <= 0:
            winner_text = "Red Wins!!"
        if red_health <= 0:
            winner_text = "Yellow Wins!!"

        key_pressed = pygame.key.get_pressed()
        move_yellow(key_pressed, yellow)
        move_red(key_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(yellow, red, yellow_bullets,
                    red_bullets, yellow_health, red_health, winner_text, green_col, red_col)
        if winner_text != "":
            if not flag:
                VICTORY_SOUND.play()
                flag = True
            yellow_bullets = []
            red_bullets = []

    main()


if __name__ == "__main__":
    main()
