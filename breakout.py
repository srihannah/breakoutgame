import pygame
import random

# Initialize Pygame
pygame.init()
FPS = 60
WIDTH = 700
HEIGHT = 700

COLS = 10
ROWS = 6

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (60, 160, 200)
GREEN = (80, 175, 90)
RED = (250, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Break Out Game!')
clock = pygame.time.Clock()

# Load sound effects
bounce_sound = pygame.mixer.Sound("bounce.wav")
hit_sound = pygame.mixer.Sound("hit.wav")

class Bricks:
    def __init__(self):
        self.width = int(WIDTH / COLS)
        self.height = 30
        self.create_bricks()

    def create_bricks(self):
        self.bricks = []
        self.active_bricks = []
        for row in range(ROWS):
            brick_row = []
            for col in range(COLS):
                brick_x = col * self.width
                brick_y = row * self.height
                br = pygame.Rect(brick_x, brick_y, self.width, self.height)
                brick_row.append(br)
                self.active_bricks.append(True)
            self.bricks.append(brick_row)

    def draw_bricks(self):
        for row, brick_row in enumerate(self.bricks):
            for col, br in enumerate(brick_row):
                if self.active_bricks[row * COLS + col]:  # Draw only active bricks
                    pygame.draw.rect(screen, GREEN, br)
                    pygame.draw.rect(screen, BLACK, br, 2)

    def deactivate_brick(self, row, col):
        self.active_bricks[row * COLS + col] = False

class Paddle:
    def __init__(self):
        self.width = int(WIDTH / COLS)
        self.height = 20
        self.x = int(WIDTH / 2) - int(self.width / 2)
        self.y = HEIGHT - 40
        self.speed = 10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw_paddle(self):
        pygame.draw.rect(screen, WHITE, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

class Ball:
    def __init__(self, x, y):
        self.radius = 10
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)
        self.dx = 3
        self.dy = -3
        self.game_status = 0

    def draw_ball(self):
        pygame.draw.circle(screen, BLUE, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)

    def move_ball(self):
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.dx *= -1
        if self.rect.top < 0:
            self.dy *= -1
        if self.rect.bottom > HEIGHT:
            self.game_status = -1

        if self.rect.colliderect(paddle.rect) and self.dy > 0:
            self.dy *= -1
            bounce_sound.play()

        all_don = True
        for row in range(ROWS):
            for col in range(COLS):
                br = bricks_wall.bricks[row][col]
                if bricks_wall.active_bricks[row * COLS + col] and self.rect.colliderect(br):
                    hit_sound.play()
                    if abs(self.rect.bottom - br.top) < 5 and self.dy > 0:
                        self.dy *= -1
                    if abs(self.rect.top - br.bottom) < 5 and self.dy < 0:
                        self.dy *= -1
                    if abs(self.rect.right - br.left) < 5 and self.dx > 0:
                        self.dx *= -1
                    if abs(self.rect.left - br.right) < 5 and self.dx < 0:
                        self.dx *= -1
                    bricks_wall.deactivate_brick(row, col)
                if bricks_wall.active_bricks[row * COLS + col]:
                    all_don = False

        if all_don:
            self.game_status = 1

        self.rect.x += self.dx
        self.rect.y += self.dy
        return self.game_status

def reset_game():
    global ball, paddle, bricks_wall
    paddle = Paddle()
    ball = Ball(paddle.x + int(paddle.width / 2), paddle.y - 10)
    bricks_wall = Bricks()

reset_game()

# Main game loop
running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)
    bricks_wall.draw_bricks()

    paddle.draw_paddle()
    paddle.move()

    ball.draw_ball()
    game_status = ball.move_ball()

    if game_status == -1:
        screen.fill(BLACK)
        font = pygame.font.SysFont(None, 50)
        text = font.render('GAME OVER!', True, BLUE)
        txtcenter = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(text, txtcenter)
        pygame.display.update()
        pygame.time.wait(2000)
        reset_game()

    if game_status == 1:
        screen.fill(BLACK)
        font = pygame.font.SysFont(None, 50)
        text = font.render('YOU WIN!!', True, BLUE)
        txtcenter = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(text, txtcenter)
        pygame.display.update()
        pygame.time.wait(2000)
        reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

# Clean up
pygame.quit()
