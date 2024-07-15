import pygame
import random
import sys
import time

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
BALL_SPEED_X = 8 * random.choice((1, -1))
BALL_SPEED_Y = 8 * random.choice((1, -1))
PLAYER_SPEED = 0
OPPONENT_SPEED = 7

def reset_ball_location():
    global BALL_SPEED_X, BALL_SPEED_Y
    # Reset ball location to center of screen
    ball.center = (SCREEN_HEIGHT/2, SCREEN_WIDTH/2)
    BALL_SPEED_Y *= random.choice((1, -1))
    BALL_SPEED_X *= random.choice((1, -1))

def ball_animations():
    global BALL_SPEED_X, BALL_SPEED_Y
    ball.x += BALL_SPEED_X
    ball.y += BALL_SPEED_Y

    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        BALL_SPEED_Y *= -1

    # If the ball hits the leftmost and rightmost side of the screen, reset the ball location
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        reset_ball_location()

    if ball.colliderect(player) or ball.colliderect(opponent):
        BALL_SPEED_X *= -1

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

    pygame.display.flip()
    clock.tick_busy_loop(60)
