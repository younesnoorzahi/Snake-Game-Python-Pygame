import pygame
import sys
import random

# Initialize pygame
pygame.init()

# --- Game settings ---
WIDTH, HEIGHT = 640, 480
CELL_SIZE = 20
FPS = 12

# Colors
BLACK = (10, 10, 10)
GREEN = (0, 255, 80)
DARK_GREEN = (0, 180, 50)
RED = (255, 70, 70)
GOLD = (255, 215, 0)
LIGHT_BLUE = (0, 180, 255)
WHITE = (255, 255, 255)

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 Snake Game (Glow Edition)")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arialrounded", 28, bold=True)

# --- Helper functions ---
def draw_text(text, color, x, y, size=28, center=False):
    f = pygame.font.SysFont("arialrounded", size, bold=True)
    label = f.render(text, True, color)
    if center:
        rect = label.get_rect(center=(x, y))
        screen.blit(label, rect)
    else:
        screen.blit(label, (x, y))

def random_food():
    return (
        random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
        random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    )

def draw_background():
    # subtle grid pattern
    screen.fill((15, 15, 15))
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, (25, 25, 25), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, (25, 25, 25), (0, y), (WIDTH, y))

def draw_food(food_pos):
    pygame.draw.circle(screen, RED, (food_pos[0] + CELL_SIZE // 2, food_pos[1] + CELL_SIZE // 2), CELL_SIZE // 2)
    pygame.draw.circle(screen, WHITE, (food_pos[0] + CELL_SIZE // 2 - 2, food_pos[1] + CELL_SIZE // 2 - 2), CELL_SIZE // 5)

def draw_snake(snake):
    for i, (x, y) in enumerate(snake):
        glow_color = (0, 255 - min(i * 10, 150), 100)
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, glow_color, rect, border_radius=4)
        if i == 0:
            pygame.draw.circle(screen, LIGHT_BLUE, rect.center, CELL_SIZE // 3)

def game_loop():
    snake = [(100, 100), (80, 100), (60, 100)]
    direction = "RIGHT"
    food = random_food()
    score = 0

    while True:
        # --- Input ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

        # --- Move Snake ---
        x, y = snake[0]
        if direction == "UP":
            y -= CELL_SIZE
        elif direction == "DOWN":
            y += CELL_SIZE
        elif direction == "LEFT":
            x -= CELL_SIZE
        elif direction == "RIGHT":
            x += CELL_SIZE
        new_head = (x, y)
        snake.insert(0, new_head)

        # --- Collision ---
        if (
            x < 0 or x >= WIDTH or
            y < 0 or y >= HEIGHT or
            new_head in snake[1:]
        ):
            game_over(score)
            return

        # --- Eat food ---
        if new_head == food:
            score += 10
            food = random_food()
        else:
            snake.pop()

        # --- Draw ---
        draw_background()
        draw_food(food)
        draw_snake(snake)
        draw_text(f"Score: {score}", GOLD, 10, 10)
        pygame.display.flip()
        clock.tick(FPS)

def start_screen():
    while True:
        draw_background()
        draw_text("🐍 SNAKE GAME", GREEN, WIDTH // 2, HEIGHT // 2 - 60, 42, True)
        draw_text("Press SPACE to Start", WHITE, WIDTH // 2, HEIGHT // 2 + 10, 26, True)
        draw_text("Use Arrow Keys to Move", (180, 180, 180), WIDTH // 2, HEIGHT // 2 + 50, 22, True)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()
                    return

def game_over(score):
    while True:
        draw_background()
        draw_text("💀 GAME OVER 💀", RED, WIDTH // 2, HEIGHT // 2 - 60, 42, True)
        draw_text(f"Final Score: {score}", GOLD, WIDTH // 2, HEIGHT // 2, 28, True)
        draw_text("Press SPACE to Restart or ESC to Quit", WHITE, WIDTH // 2, HEIGHT // 2 + 60, 22, True)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# --- Run game ---
if __name__ == "__main__":
    start_screen()
