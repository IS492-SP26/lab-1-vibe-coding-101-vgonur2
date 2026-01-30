def main():
    import random
    import sys
    try:
        import pygame
    except Exception:
        print("pygame is required to run this game. Install with: pip install -r requirements.txt")
        sys.exit(1)

    # Game constants
    WIDTH, HEIGHT = 800, 600
    PADDLE_WIDTH, PADDLE_HEIGHT = 12, 100
    PADDLE_SPEED = 6
    BALL_RADIUS = 8
    FPS = 60

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ping-Pong")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 48)

    class Paddle:
        def __init__(self, x, y):
            self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

        def move(self, dy):
            self.rect.y += dy
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT

        def draw(self, surf):
            pygame.draw.rect(surf, (255, 255, 255), self.rect)

    class Ball:
        def __init__(self):
            self.reset(direction=random.choice((-1, 1)))

        def reset(self, direction=1):
            self.x = WIDTH // 2
            self.y = HEIGHT // 2
            self.vx = 5 * direction
            self.vy = random.choice((-3, -2, -1, 1, 2, 3))

        def rect(self):
            return pygame.Rect(int(self.x - BALL_RADIUS), int(self.y - BALL_RADIUS), BALL_RADIUS * 2, BALL_RADIUS * 2)

        def update(self):
            self.x += self.vx
            self.y += self.vy

            # Bounce off top/bottom
            if self.y - BALL_RADIUS <= 0:
                self.y = BALL_RADIUS
                self.vy = -self.vy
            if self.y + BALL_RADIUS >= HEIGHT:
                self.y = HEIGHT - BALL_RADIUS
                self.vy = -self.vy

        def draw(self, surf):
            pygame.draw.circle(surf, (255, 255, 255), (int(self.x), int(self.y)), BALL_RADIUS)

    # Create paddles and ball
    left_paddle = Paddle(20, (HEIGHT - PADDLE_HEIGHT) // 2)
    right_paddle = Paddle(WIDTH - 20 - PADDLE_WIDTH, (HEIGHT - PADDLE_HEIGHT) // 2)
    ball = Ball()

    score_left = 0
    score_right = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            left_paddle.move(-PADDLE_SPEED)
        if keys[pygame.K_s]:
            left_paddle.move(PADDLE_SPEED)
        if keys[pygame.K_UP]:
            right_paddle.move(-PADDLE_SPEED)
        if keys[pygame.K_DOWN]:
            right_paddle.move(PADDLE_SPEED)

        ball.update()

        # Check collisions with paddles
        if ball.rect().colliderect(left_paddle.rect):
            ball.x = left_paddle.rect.right + BALL_RADIUS
            ball.vx = -ball.vx
            # tweak vy based on where it hit the paddle
            offset = (ball.y - left_paddle.rect.centery) / (PADDLE_HEIGHT / 2)
            ball.vy += offset * 3

        if ball.rect().colliderect(right_paddle.rect):
            ball.x = right_paddle.rect.left - BALL_RADIUS
            ball.vx = -ball.vx
            offset = (ball.y - right_paddle.rect.centery) / (PADDLE_HEIGHT / 2)
            ball.vy += offset * 3

        # Score conditions
        if ball.x < 0:
            score_right += 1
            pygame.time.delay(300)
            ball.reset(direction=1)

        if ball.x > WIDTH:
            score_left += 1
            pygame.time.delay(300)
            ball.reset(direction=-1)

        # Draw everything
        screen.fill((0, 0, 0))
        # center line
        for y in range(0, HEIGHT, 20):
            pygame.draw.rect(screen, (50, 50, 50), (WIDTH // 2 - 1, y, 2, 10))

        left_paddle.draw(screen)
        right_paddle.draw(screen)
        ball.draw(screen)

        # Scores
        left_surf = font.render(str(score_left), True, (255, 255, 255))
        right_surf = font.render(str(score_right), True, (255, 255, 255))
        screen.blit(left_surf, (WIDTH // 4 - left_surf.get_width() // 2, 20))
        screen.blit(right_surf, (3 * WIDTH // 4 - right_surf.get_width() // 2, 20))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()