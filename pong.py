import pygame
import random
import sys
import time

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
BALL_SPEED_X = 9 * random.choice((1, -1))
BALL_SPEED_Y = 9 * random.choice((1, -1))
PLAYER_SPEED = 0
OPPONENT_SPEED = 7
PLAYER_SCORE, OPPONENT_SCORE = 0, 0
SCORE_TIME= True

def reset_ball_location():
    global BALL_SPEED_X, BALL_SPEED_Y, SCORE_TIME

    current_time = pygame.time.get_ticks()
    # Reset ball location to center of screen
    ball.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    # Keep the ball still in the center then the time diff between current time and last score time is 3 seconds or less
    time_diff = current_time - SCORE_TIME

    if current_time - SCORE_TIME <= 1000:
        display_num_3 = GAME_FONT.render("3", True, light_grey)
        screen.blit(display_num_3, ((SCREEN_WIDTH / 2) - 30, SCREEN_HEIGHT / 2 + 20))
        screen.blit(display_num_3, ((SCREEN_WIDTH / 2) + 15, SCREEN_HEIGHT / 2 + 20))
    if 1001 < current_time - SCORE_TIME <= 2000:
        display_num_2 = GAME_FONT.render("2", True, light_grey)
        screen.blit(display_num_2, ((SCREEN_WIDTH / 2) - 30, SCREEN_HEIGHT / 2 + 20))
        screen.blit(display_num_2, ((SCREEN_WIDTH / 2) + 15, SCREEN_HEIGHT / 2 + 20))
    if 2001 < current_time - SCORE_TIME <= 3000:
        display_num_1 = GAME_FONT.render("1",False,light_grey)
        screen.blit(display_num_1, ((SCREEN_WIDTH / 2) - 30, SCREEN_HEIGHT / 2 + 20))
        screen.blit(display_num_1, ((SCREEN_WIDTH / 2) + 15, SCREEN_HEIGHT / 2 + 20))

    if time_diff <= 3000:
        BALL_SPEED_X, BALL_SPEED_Y = 0, 0
    else:
        # Randomize the X and Y vectors of the ball
        BALL_SPEED_X = 7 * random.choice((1, -1))
        BALL_SPEED_Y = 7 * random.choice((1, -1))
        # Reset score time
        SCORE_TIME = None

def ball_animations():
    global BALL_SPEED_X, BALL_SPEED_Y, PLAYER_SCORE, OPPONENT_SCORE, SCORE_TIME
    ball.x += BALL_SPEED_X
    ball.y += BALL_SPEED_Y

    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        BALL_SPEED_Y *= -1

    # If the ball hits the leftmost and rightmost side of the screen, reset the ball location
    if ball.left <= 0:
        OPPONENT_SCORE += 1
        SCORE_TIME = pygame.time.get_ticks()

    if ball.right >= SCREEN_WIDTH:
        PLAYER_SCORE += 1
        SCORE_TIME = pygame.time.get_ticks()

    if ball.colliderect(player) and BALL_SPEED_X < 0:
        if abs(ball.left - player.right) < 5:
            BALL_SPEED_X *= -1
        elif abs(ball.top - player.bottom) < 5 and BALL_SPEED_Y < 0:
            BALL_SPEED_Y *= -1
        elif abs(ball.bottom - player.top) < 5 and BALL_SPEED_Y > 0:
            BALL_SPEED_Y *= -1

    if ball.colliderect(opponent) and BALL_SPEED_X > 0:
        if abs(ball.right - opponent.left) < 5:
            BALL_SPEED_X *= -1
        elif abs(ball.top - opponent.bottom) < 5 and BALL_SPEED_Y < 0:
            BALL_SPEED_Y *= -1
        elif abs(ball.bottom - opponent.top) < 5 and BALL_SPEED_Y > 0:
            BALL_SPEED_Y *= -1

def player_animations():
    player.y += PLAYER_SPEED

    if player.top <= 0:
        player.top = 0
    if player.bottom >= SCREEN_HEIGHT:
        player.bottom = SCREEN_HEIGHT

def opponent_animations():
    # If opponent's top is higher than ball's top, opponent goes down (along y-axis) by speed of 7
    if opponent.top > ball.top:
        opponent.y -= OPPONENT_SPEED
    # If opponent's bottom is lower than ball's bottom, opponent goes up (along y-axis) by speed of 7
    if opponent.bottom < ball.bottom:
        opponent.y += OPPONENT_SPEED

    # Prevent opponent from going off the screen
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= SCREEN_HEIGHT:
        opponent.bottom = SCREEN_HEIGHT

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong')

ball = pygame.Rect(SCREEN_WIDTH/2 - 15, SCREEN_HEIGHT/2 - 15, 30, 30)
player = pygame.Rect(10, SCREEN_HEIGHT/2 - 70, 10, 140)
opponent = pygame.Rect(SCREEN_WIDTH - 20, SCREEN_HEIGHT/2 - 70, 10, 140)


bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)

GAME_FONT = pygame.font.Font("freesansbold.ttf", 32)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_DOWN, pygame.K_s]:
                PLAYER_SPEED += 7
            if event.key in [pygame.K_UP, pygame.K_w]:
                PLAYER_SPEED -= 7
        if event.type == pygame.KEYUP:
            if event.key  in [pygame.K_DOWN, pygame.K_s]:
                PLAYER_SPEED -= 7
            if event.key in [pygame.K_UP, pygame.K_w]:
                PLAYER_SPEED += 7

    ball_animations()
    player_animations()
    opponent_animations()

    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (SCREEN_WIDTH/2, 0), (SCREEN_WIDTH/2, SCREEN_HEIGHT))

    if SCORE_TIME:
        reset_ball_location()

    # Render scored on middle-top of screen
    player_text = GAME_FONT.render(f"{PLAYER_SCORE}", True, light_grey)
    screen.blit(player_text, ((SCREEN_WIDTH / 2) - 30, 0))
    opponent_text = GAME_FONT.render(f"{OPPONENT_SCORE}", True, light_grey)
    screen.blit(opponent_text, ((SCREEN_WIDTH / 2) + 15, 0))

    pygame.display.flip()
    clock.tick_busy_loop(60)
