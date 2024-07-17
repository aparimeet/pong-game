import pygame
import random
import sys

class Block(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(light_grey)
        self.rect = self.image.get_rect(topleft=(x_pos, y_pos))

class Player(Block):
    def __init__(self, x_pos, y_pos, width, height, speed):
        super().__init__(x_pos, y_pos, width, height)
        self.speed = speed
        self.movement = 0

    def screen_constraint(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def update(self, ball_group):
        self.rect.y += self.movement
        self.screen_constraint()

class Opponent(Block):
    def __init__(self, x_pos, y_pos, width, height, speed):
        super().__init__(x_pos, y_pos, width, height)
        self.speed = speed

    def screen_constraint(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def update(self, ball_group):
        if self.rect.centery < ball_group.sprite.rect.top:
            self.rect.y += self.speed
        if self.rect.centery > ball_group.sprite.rect.bottom:
            self.rect.y -= self.speed
        self.screen_constraint()


class Ball(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, radius, speed_x, speed_y, paddles):
        super().__init__()
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, light_grey, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.speed_x = speed_x * random.choice((1, -1))
        self.speed_y = speed_y * random.choice((1, -1))
        self.paddles = paddles
        self.is_game_active = False
        self.score_time = 0

    def gradual_speed_increase(self):
        # Increase speed_x and speed_y by 0.1
        self.speed_x = (self.speed_x / abs(self.speed_x))*0.1 + self.speed_x
        self.speed_y = (self.speed_y / abs(self.speed_y))*0.1 + self.speed_y

    def update(self):
        if self.is_game_active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.collisions()
        else:
            self.restart_counter()
    
    def collisions(self):
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y *= -1

        if pygame.sprite.spritecollide(self, self.paddles, False):
            collision_paddle = pygame.sprite.spritecollide(self, self.paddles, False)[0].rect
            if abs(self.rect.right - collision_paddle.left) < 10 and self.speed_x > 0:
                self.speed_x *= -1
            if abs(self.rect.left - collision_paddle.right) < 10 and self.speed_x < 0:
                self.speed_x *= -1
            if abs(self.rect.top - collision_paddle.bottom) < 10 and self.speed_y < 0:
                self.rect.top = collision_paddle.bottom
                self.speed_y *= -1
            if abs(self.rect.bottom - collision_paddle.top) < 10 and self.speed_y > 0:
                self.rect.bottom = collision_paddle.top
                self.speed_y *= -1
            # Every time the collision is made with a paddle, increase speed by 0.1
            self.gradual_speed_increase()

    def reset_ball(self):
        self.is_game_active = False
        self.speed_x *= random.choice((1, -1))
        self.speed_y *= random.choice((1, -1))
        self.score_time = pygame.time.get_ticks()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def restart_counter(self):
        current_time = pygame.time.get_ticks()
        countdown_number = 3

        if current_time - self.score_time < 1000:
            countdown_number = 3
        elif 1000 <= current_time - self.score_time < 2000:
            countdown_number = 2
        elif 2000 <= current_time - self.score_time < 3000:
            countdown_number = 1
        elif current_time - self.score_time >= 3000:
            self.is_game_active = True

        time_counter = GAME_FONT.render(str(countdown_number), True, light_grey)
        screen.blit(time_counter, ((SCREEN_WIDTH / 2) - 30, SCREEN_HEIGHT / 2 + 20))
        screen.blit(time_counter, ((SCREEN_WIDTH / 2) + 15, SCREEN_HEIGHT / 2 + 20))

class GameManager:
    def __init__(self, ball_group, paddle_group):
        self.ball_group = ball_group
        self.paddle_group = paddle_group
        self.player_score = 0
        self.opponent_score = 0

    def run_game(self):
        self.paddle_group.draw(screen)
        self.ball_group.draw(screen)

        self.paddle_group.update(self.ball_group)
        self.ball_group.update()

        self.reset_ball()
        self.draw_score()
    
    def reset_ball(self):
        if self.ball_group.sprite.rect.right >= SCREEN_WIDTH:
            self.player_score += 1
            self.ball_group.sprite.reset_ball()
        if self.ball_group.sprite.rect.left <= 0:
            self.opponent_score += 1
            self.ball_group.sprite.reset_ball()
        
    def draw_score(self):
        # Render scored on middle-top of screen
        player_text = GAME_FONT.render(f"{self.player_score}", True, light_grey)
        screen.blit(player_text, ((SCREEN_WIDTH / 2) - 30, 0))
        opponent_text = GAME_FONT.render(f"{self.opponent_score}", True, light_grey)
        screen.blit(opponent_text, ((SCREEN_WIDTH / 2) + 15, 0))

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960

# Setup
pygame.init()
clock = pygame.time.Clock()

# Main window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong')

bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)
GAME_FONT = pygame.font.Font("freesansbold.ttf", 32)
middle_separator = pygame.Rect(SCREEN_WIDTH/2, 0, 4, SCREEN_HEIGHT)

player = Player(20, SCREEN_HEIGHT / 2, 10, 140, 6)
opponent = Opponent(SCREEN_WIDTH - 20, SCREEN_HEIGHT / 2, 10, 140, 6)
paddle_group = pygame.sprite.Group()
paddle_group.add(player)
paddle_group.add(opponent)

ball = Ball(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 20, 4, 4, paddle_group)
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)

game_manager = GameManager(ball_group=ball_sprite, paddle_group=paddle_group)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_DOWN, pygame.K_s]:
                player.movement += player.speed
            if event.key in [pygame.K_UP, pygame.K_w]:
                player.movement -= player.speed
        if event.type == pygame.KEYUP:
            if event.key  in [pygame.K_DOWN, pygame.K_s]:
                player.movement -= player.speed
            if event.key in [pygame.K_UP, pygame.K_w]:
                player.movement += player.speed

    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, middle_separator)

    game_manager.run_game()

    pygame.display.flip()
    clock.tick(60)
