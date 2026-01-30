"""
Ping-Pong Game
A two-player Pong game with paddles, ball physics, and score keeping.
"""

import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 500
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 80
BALL_SIZE = 15
PADDLE_SPEED = 6
BALL_SPEED_INITIAL = 5
WINNING_SCORE = 5

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping-Pong")
clock = pygame.time.Clock()


class Paddle:
    """Represents a player's paddle."""

    def __init__(self, x: int, y: int):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = PADDLE_SPEED

    def move(self, dy: int):
        """Move paddle by dy, clamped to screen bounds."""
        self.rect.y += dy
        self.rect.y = max(0, min(self.rect.y, HEIGHT - PADDLE_HEIGHT))

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, WHITE, self.rect)


class Ball:
    """The game ball with position and velocity."""

    def __init__(self):
        self.reset()

    def reset(self):
        """Place ball at center and give it a random initial direction."""
        self.rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
        self.dx = BALL_SPEED_INITIAL * (1 if pygame.time.get_ticks() % 2 == 0 else -1)
        self.dy = BALL_SPEED_INITIAL * (0.5 if pygame.time.get_ticks() % 3 == 0 else -0.5)

    def update(self):
        """Move the ball by its velocity."""
        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, WHITE, self.rect)


def check_ball_paddle_collision(ball: Ball, left_paddle: Paddle, right_paddle: Paddle) -> bool:
    """Handle ball-paddle collisions. Returns True if ball hit a paddle."""
    if ball.rect.colliderect(left_paddle.rect):
        ball.dx = abs(ball.dx)
        # Slight angle change based on where ball hit the paddle
        hit_pos = (ball.rect.centery - left_paddle.rect.centery) / (PADDLE_HEIGHT / 2)
        ball.dy = hit_pos * BALL_SPEED_INITIAL * 0.8
        ball.rect.left = left_paddle.rect.right
        return True
    if ball.rect.colliderect(right_paddle.rect):
        ball.dx = -abs(ball.dx)
        hit_pos = (ball.rect.centery - right_paddle.rect.centery) / (PADDLE_HEIGHT / 2)
        ball.dy = hit_pos * BALL_SPEED_INITIAL * 0.8
        ball.rect.right = right_paddle.rect.left
        return True
    return False


def check_ball_walls(ball: Ball) -> int:
    """
    Handle ball-wall collisions (top/bottom bounce, left/right = score).
    Returns: -1 if left side (right player scores), 1 if right side (left player scores), 0 otherwise.
    """
    if ball.rect.top <= 0:
        ball.rect.top = 0
        ball.dy = abs(ball.dy)
    if ball.rect.bottom >= HEIGHT:
        ball.rect.bottom = HEIGHT
        ball.dy = -abs(ball.dy)
    if ball.rect.left <= 0:
        return 1  # Right player scores
    if ball.rect.right >= WIDTH:
        return -1  # Left player scores
    return 0


def draw_score(surface: pygame.Surface, score_left: int, score_right: int):
    """Draw the score for both players."""
    font = pygame.font.Font(None, 72)
    text_left = font.render(str(score_left), True, WHITE)
    text_right = font.render(str(score_right), True, WHITE)
    surface.blit(text_left, (WIDTH // 4 - text_left.get_width() // 2, 20))
    surface.blit(text_right, (3 * WIDTH // 4 - text_right.get_width() // 2, 20))


def draw_center_line(surface: pygame.Surface):
    """Draw dashed center line."""
    dash_length = 15
    gap = 10
    y = 0
    while y < HEIGHT:
        pygame.draw.rect(surface, GRAY, (WIDTH // 2 - 2, y, 4, dash_length))
        y += dash_length + gap


def main():
    # Game objects
    left_paddle = Paddle(30, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    right_paddle = Paddle(WIDTH - 30 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    ball = Ball()

    score_left = 0
    score_right = 0
    ball_served = False

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # Player input: Left paddle (W/S), Right paddle (Up/Down)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            left_paddle.move(-PADDLE_SPEED)
        if keys[pygame.K_s]:
            left_paddle.move(PADDLE_SPEED)
        if keys[pygame.K_UP]:
            right_paddle.move(-PADDLE_SPEED)
        if keys[pygame.K_DOWN]:
            right_paddle.move(PADDLE_SPEED)

        # Serve ball on space
        if not ball_served and keys[pygame.K_SPACE]:
            ball_served = True

        if ball_served:
            ball.update()
            check_ball_paddle_collision(ball, left_paddle, right_paddle)
            side = check_ball_walls(ball)
            if side != 0:
                if side == 1:
                    score_right += 1
                else:
                    score_left += 1
                ball.reset()
                ball_served = False

        # Draw
        screen.fill(BLACK)
        draw_center_line(screen)
        draw_score(screen, score_left, score_right)
        left_paddle.draw(screen)
        right_paddle.draw(screen)
        ball.draw(screen)

        if not ball_served:
            font = pygame.font.Font(None, 36)
            msg = font.render("Press SPACE to serve", True, GRAY)
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT - 40))

        # Win condition
        if score_left >= WINNING_SCORE or score_right >= WINNING_SCORE:
            winner = "Left" if score_left >= WINNING_SCORE else "Right"
            font = pygame.font.Font(None, 48)
            msg = font.render(f"{winner} player wins! Press ESC to quit.", True, WHITE)
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 24))
            ball_served = False
            pygame.display.flip()
            clock.tick(60)
            continue

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
